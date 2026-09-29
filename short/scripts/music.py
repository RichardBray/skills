#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Generate a music bed with MiniMax Music on Replicate (instrumental).

usage: music.py out.mp3 "prompt describing the bed"
Reads REPLICATE_API_TOKEN. Output length is set by the model (often 1-2 minutes); compose.sh trims it.
"""
import json, os, sys, time, urllib.error, urllib.request
K = os.environ['REPLICATE_API_TOKEN']
def call(method, url, body=None):
    for a in range(12):
        req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method,
                                     headers={'Authorization': 'Bearer ' + K, 'Content-Type': 'application/json', 'User-Agent': 'curl/8.7.1'})
        try:
            with urllib.request.urlopen(req, timeout=120) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(8 + a); continue
            if e.code == 402: sys.exit('Replicate: insufficient credit (HTTP 402). Top up at replicate.com/account/billing')
            raise
out, prompt = sys.argv[1], sys.argv[2]
p = call('POST', 'https://api.replicate.com/v1/models/minimax/music-2.6/predictions',
         {'input': {'prompt': prompt, 'is_instrumental': True, 'audio_format': 'mp3', 'sample_rate': 44100, 'bitrate': 256000}})
while p['status'] in ('starting', 'processing'): time.sleep(5); p = call('GET', p['urls']['get'])
if p['status'] != 'succeeded': sys.exit(f"music failed: {p.get('error')}")
o = p['output']; o = o[0] if isinstance(o, list) else o
urllib.request.urlretrieve(o, out); print('saved', out)
