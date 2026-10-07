#!/usr/bin/env python3
"""Find split-screen sections and solid-colour placeholder regions in a vertical short.

usage: detect_layout.py <video.mp4> [--green]

Prints runs of "split@<y>" (a strong horizontal edge between 30% and 70% of the
height, i.e. screen recording on top / speaker below) and, with --green, runs
where the top rows are a flat green placeholder plate (y range in 1080x1920).
"""
import subprocess, sys

W, H = 270, 480
path = sys.argv[1]
green = "--green" in sys.argv
fmt = "rgb24" if green else "gray"
bpp = 3 if green else 1
raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format={fmt}", "-f", "rawvideo", "-"],
    capture_output=True, check=True).stdout
fps = float(eval(subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", path],
    capture_output=True, text=True, check=True).stdout.strip()))
n = len(raw) // (W * H * bpp)
scale = 1920 / H


def luma_rows(f):
    if bpp == 1:
        return [sum(f[r * W:(r + 1) * W]) / W for r in range(H)]
    return [sum(f[(r * W + x) * 3 + 1] for x in range(W)) / W for r in range(H)]


def is_green(f, x, y):
    i = (y * W + x) * 3
    r, g, b = f[i], f[i + 1], f[i + 2]
    # ratio, not a fixed margin: editors use dark plates (#255908, #1f4a06...) as well as key green
    return g > 40 and g > r * 1.5 and g > b * 1.5


prev = None
for k in range(n):
    f = raw[k * W * H * bpp:(k + 1) * W * H * bpp]
    rows = luma_rows(f)
    lo, hi = int(H * 0.3), int(H * 0.7)
    best = max(range(lo, hi), key=lambda r: abs(rows[r] - rows[r - 1]))
    edge = abs(rows[best] - rows[best - 1])
    lab = f"split@{round(best * scale / 10) * 10}" if edge > 25 else "full"
    if green:
        g = [y for y in range(H) if sum(is_green(f, x, y) for x in range(0, W, 9)) >= 28]
        if g:
            lab += f" green y{round(min(g) * scale)}-{round((max(g) + 1) * scale)}"
    if lab != prev:
        print(f"{k / fps:7.2f}  {lab}")
        prev = lab
