#!/usr/bin/env python3
"""Generate realistic stock-style footage for a green plate with Seedance 1 Pro on Replicate,
then trim/crop it to the plate.

usage: gen_footage.py <slug> <plate_w> <plate_h> <plate_dur> "<scene prompt>" [seed]
writes assets/clips/<slug>-raw.mp4 (1440x1440, 5s) and assets/clips/<slug>.mp4 (plate size, 30fps, no audio)
"""
import json, os, subprocess, sys, time, urllib.request

slug, W, H, dur, scene = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 71
token = os.environ.get("REPLICATE_API_TOKEN") or subprocess.run(
    ["fish", "-c", "echo $REPLICATE_API_TOKEN"], capture_output=True, text=True).stdout.strip()
# Replicate rejects Python's default user agent
hdr = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": "curl/8.7.1"}
# Seedance paints gibberish lettering on any sign it draws unless told hard not to
NEG = " Absolutely no text, no letters, no signs, no posters, no logos, no captions, no watermark anywhere in the frame."
body = {"input": {"prompt": "Photorealistic handheld documentary footage. " + scene + NEG,
                  "duration": 5 if dur <= 5 else 10, "resolution": "1080p", "aspect_ratio": "1:1", "fps": 24, "seed": seed}}
r = json.load(urllib.request.urlopen(urllib.request.Request(
    "https://api.replicate.com/v1/models/bytedance/seedance-1-pro/predictions", json.dumps(body).encode(), hdr)))
while r["status"] not in ("succeeded", "failed", "canceled"):
    time.sleep(5)
    r = json.load(urllib.request.urlopen(urllib.request.Request(r["urls"]["get"], headers=hdr)))
if r["status"] != "succeeded":
    sys.exit(f"seedance {r['status']}: {r.get('error')}")
out = r["output"] if isinstance(r["output"], str) else r["output"][0]
raw = f"assets/clips/{slug}-raw.mp4"
urllib.request.urlretrieve(out, raw)
# cover-crop the square to the plate aspect, trimming the top (usually sky) rather than the bottom
ch = min(1440, round(1440 * H / W))
cw = min(1440, round(1440 * W / H))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-t", str(dur),
                "-vf", f"crop={cw}:{ch}:{(1440 - cw) // 2}:{1440 - ch},scale={W}:{H},fps=30",
                "-an", "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
                f"assets/clips/{slug}.mp4"], check=True)
print(f"assets/clips/{slug}.mp4")
