#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Word-level timings for a voiceover, using the script's own words for the text.

usage: align.py voiceover.wav script.txt words.json

Whisper (OpenAI) supplies timings only; its spelling is discarded, so captions show the script's words
("y combinator", "404") even when Whisper mishears them. Reads OPENAI_API_KEY. Script lines are the
non-empty, non-heading lines of script.txt; each output word carries its line index.
"""
import difflib, json, os, re, subprocess, sys, urllib.request, uuid

def whisper_words(audio):
    wav = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', '16000', '-f', 'wav', '-'], capture_output=True, check=True).stdout
    b = uuid.uuid4().hex
    def field(n, v): return f'--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'
    body = (field('model', 'whisper-1') + field('response_format', 'verbose_json') + field('timestamp_granularities[]', 'word')
            + f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n').encode() + wav + f'\r\n--{b}--\r\n'.encode()
    req = urllib.request.Request('https://api.openai.com/v1/audio/transcriptions', data=body,
                                 headers={'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'], 'Content-Type': 'multipart/form-data; boundary=' + b})
    return json.load(urllib.request.urlopen(req, timeout=180))['words']

norm = lambda t: re.sub(r"[^a-z0-9']", '', t.lower())

def main():
    audio, script, out = sys.argv[1:4]
    lines = [l.strip() for l in open(script) if l.strip() and not l.lstrip().startswith('#')]
    sw = [(w, i) for i, l in enumerate(lines) for w in l.split()]
    ww = whisper_words(audio)
    a = [norm(w) for w, _ in sw]; b = [norm(w['word']) for w in ww]
    t = [None] * len(sw)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): t[i1 + k] = (ww[j1 + k]['start'], ww[j1 + k]['end'])
        elif tag == 'replace' and j2 > j1:            # different word counts: spread the script words over the heard span
            s, e = ww[j1]['start'], ww[j2 - 1]['end']; n = i2 - i1
            for k in range(n): t[i1 + k] = (s + (e - s) * k / n, s + (e - s) * (k + 1) / n)
    matched = sum(1 for x in t if x is not None)
    # fill any gaps by interpolating between known neighbours
    for i in range(len(t)):
        if t[i] is None:
            p = next((j for j in range(i - 1, -1, -1) if t[j]), None); n = next((j for j in range(i + 1, len(t)) if t[j]), None)
            lo = t[p][1] if p is not None else 0.0; hi = t[n][0] if n is not None else lo + 0.3 * (n or 1)
            gap = [j for j in range(i, len(t)) if t[j] is None and (n is None or j < n)]; k = gap.index(i)
            t[i] = (lo + (hi - lo) * k / len(gap), lo + (hi - lo) * (k + 1) / len(gap))
    words = [{'w': w, 'line': li, 'start': round(s, 3), 'end': round(e, 3)} for (w, li), (s, e) in zip(sw, t)]
    json.dump({'lines': lines, 'words': words}, open(out, 'w'), indent=1)
    dur = ww[-1]['end'] if ww else 0
    print(f'{len(words)} script words, {matched} matched to what was heard ({matched/len(words)*100:.0f}%), voiceover speech ends at {dur:.1f}s')
    if matched / len(words) < 0.85: print('WARNING: the recording differs from the script; check for ad-libs or missing lines.', file=sys.stderr)
    extra = len(ww) - sum(b2 - b1 for tag, _, _, b1, b2 in sm.get_opcodes() if tag == 'equal' or tag == 'replace')
main()
