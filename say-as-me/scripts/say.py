#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Speak text in a cloned voice (Qwen3-TTS on Replicate).

usage: say.py "text or @file.txt" out.wav [--style "..."] [--speed 0.92] [--max-chars 220]

Reads REPLICATE_API_TOKEN. The voice lives in $VOICE_CLONE_DIR (default: ~/.config/voice-clone) as
reference.wav plus reference.txt, its exact transcript. Keep that folder out of git.
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.request, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get('VOICE_CLONE_DIR', os.path.expanduser('~/.config/voice-clone'))
K = os.environ['REPLICATE_API_TOKEN']
UA = 'curl/8.7.1'  # Cloudflare 1010 blocks Python's default User-Agent

def call(method, url, body=None):
    for attempt in range(12):
        req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method,
                                     headers={'Authorization': 'Bearer ' + K, 'Content-Type': 'application/json', 'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(8 + attempt); continue
            if e.code == 402: sys.exit('Replicate: insufficient credit (HTTP 402). Top up at replicate.com/account/billing')
            raise
    raise RuntimeError('rate limited')

def upload(path):
    b = uuid.uuid4().hex
    body = (f'--{b}\r\nContent-Disposition: form-data; name="content"; filename="reference.wav"\r\nContent-Type: audio/wav\r\n\r\n').encode() + open(path, 'rb').read() + f'\r\n--{b}--\r\n'.encode()
    req = urllib.request.Request('https://api.replicate.com/v1/files', data=body, headers={'Authorization': 'Bearer ' + K, 'Content-Type': 'multipart/form-data; boundary=' + b, 'User-Agent': UA})
    return json.load(urllib.request.urlopen(req, timeout=180))['urls']['get']

def chunks(text, n):
    # one sentence per unit; a line without end punctuation (shorts scripts) gets a period so the voice pauses
    units = []
    for line in text.splitlines():
        line = line.strip()
        if not line: continue
        if line[-1] not in '.!?': line += '.'
        units += re.split(r'(?<=[.!?])\s+', line)
    out, cur = [], ''
    for s in units:
        if cur and len(cur) + len(s) + 1 > n: out.append(cur); cur = s
        else: cur = (cur + ' ' + s).strip()
    if cur: out.append(cur)
    return out

def main():
    a = sys.argv[1:]; style = None; mx = 220; speed = 1.0
    if '--speed' in a: i = a.index('--speed'); speed = float(a[i + 1]); del a[i:i + 2]
    if '--style' in a: i = a.index('--style'); style = a[i + 1]; del a[i:i + 2]
    if '--max-chars' in a: i = a.index('--max-chars'); mx = int(a[i + 1]); del a[i:i + 2]
    if len(a) < 2: sys.exit(__doc__)
    text, out = a[0], a[1]
    if text.startswith('@'): text = open(text[1:]).read()
    if not (os.path.exists(f'{VOICE}/reference.wav') and os.path.exists(f'{VOICE}/reference.txt')):
        sys.exit(f'No voice found. Put reference.wav and reference.txt (its exact transcript) in {VOICE}, or set VOICE_CLONE_DIR.')
    ref_text = open(f'{VOICE}/reference.txt').read().strip()
    ref_url = upload(f'{VOICE}/reference.wav')
    ver = call('GET', 'https://api.replicate.com/v1/models/qwen/qwen3-tts')['latest_version']['id']
    tmp = tempfile.mkdtemp(); parts = []
    for i, c in enumerate(chunks(text, mx)):
        inp = {'mode': 'voice_clone', 'text': c, 'reference_audio': ref_url, 'reference_text': ref_text, 'language': 'English'}
        if style: inp['style_instruction'] = style
        for attempt in range(3):
            p = call('POST', 'https://api.replicate.com/v1/predictions', {'version': ver, 'input': inp})
            while p['status'] in ('starting', 'processing'): time.sleep(3); p = call('GET', p['urls']['get'])
            if p['status'] == 'succeeded': break
            print(f'chunk {i+1} retry: {p.get("error")}', file=sys.stderr)
        else: sys.exit(f'chunk {i+1} failed')
        o = p['output']; o = o[0] if isinstance(o, list) else o
        f = f'{tmp}/{i:03d}.wav'
        urllib.request.urlretrieve(o, f); parts.append(f)
        print(f'chunk {i+1} ok: {c[:60]}', file=sys.stderr)
    gap = f'{tmp}/gap.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '0.25', gap], check=True)
    lst = f'{tmp}/list.txt'
    open(lst, 'w').write(''.join(f"file '{p}'\nfile '{gap}'\n" for p in parts[:-1]) + f"file '{parts[-1]}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-ac', '1', '-ar', '44100'] + (['-af', f'atempo={speed}'] if speed != 1.0 else []) + [out], check=True)
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]))
    print(f'{out}  {d:.1f}s  {len(text.split())/d:.2f} words/sec')

main()
