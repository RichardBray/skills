#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Build the base video from face footage, one layout per scene, then lay the transparent overlay frames on top.

usage: compose_face.py <short-dir> [--face-x 960]

Needs in <short-dir>: footage.mp4 (16:9), scene_times.json (from render.mjs --template face), overlay/f_*_0.png
(render.mjs --template face --alpha --sub 1 --out overlay), optional sfx.wav. Writes short.mp4.
--face-x is the source-pixel x of the middle of your face; crops are centred on it.
"""
import json, os, subprocess, sys
d = os.path.abspath(sys.argv[1]); fx = 960
if '--face-x' in sys.argv: fx = int(sys.argv[sys.argv.index('--face-x') + 1])
sc = json.load(open(f'{d}/scene_times.json')); foot = f'{d}/footage.mp4'
def probe(k, f=foot):
    return subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', f'stream={k}', '-of', 'csv=p=0', f]).decode().split()[0]
W, H = int(probe('width')), int(probe('height'))
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', foot]))
clamp = lambda x, w: max(0, min(W - w, x))
BG = '0x141414'
parts = []; labels = []
for i, s in enumerate(sc):
    a, b = s['start'], s['end'] if i + 1 < len(sc) else dur
    seg = f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS'
    kind = s['face']
    if kind == 'full':        # full-height vertical crop
        w = round(H * 9 / 16); f = f'{seg},crop={w}:{H}:{clamp(fx - w // 2, w)}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0'
    elif kind in ('bottom', 'top'):   # half-screen panel: 1080x960 from a 9:8 crop
        w = round(H * 1080 / 960); y = 960 if kind == 'bottom' else 0
        f = f'{seg},crop={w}:{H}:{clamp(fx - w // 2, w)}:0,scale=1080:960:flags=lanczos,pad=1080:1920:0:{y}:{BG}'
    elif kind == 'strip':     # whole wide shot across the middle
        f = f'{seg},scale=1080:{round(1080 * H / W / 2) * 2}:flags=lanczos,pad=1080:1920:0:{(1920 - round(1080 * H / W / 2) * 2) // 2}:{BG}'
    elif kind == 'bubble':    # small round face over a full-screen graphic
        sq = H; f = (f'color=c={s.get("bg") or BG}:s=1080x1920:r=30:d={b - a}[c{i}];{seg},crop={sq}:{sq}:{clamp(fx - sq // 2, sq)}:0,scale=360:360:flags=lanczos,format=yuva420p,'
                     f"geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='if(lt(hypot(X-180,Y-180),178),255,0)'[b{i}];[c{i}][b{i}]overlay=x=680:y=90")
    parts.append(f'{f},fps=30,format=yuv420p,setsar=1[v{i}]'); labels.append(f'[v{i}]')
fc = ';'.join(parts) + ';' + ''.join(labels) + f'concat=n={len(sc)}:v=1:a=0[base]'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', foot, '-filter_complex', fc, '-map', '[base]', '-c:v', 'libx264', '-crf', '13', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{d}/base.mp4'], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{d}/base.mp4', '-framerate', '30', '-i', f'{d}/overlay/f_%05d_0.png', '-filter_complex', '[0:v][1:v]overlay=format=auto,format=yuv420p[v]', '-map', '[v]', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-shortest', f'{d}/video_only.mp4'], check=True)
ins = ['-i', f'{d}/video_only.mp4', '-i', foot]; fa = '[1:a]loudnorm=I=-14:TP=-1.5[v]'; mix = '[v]'; n = 2
if os.path.exists(f'{d}/sfx.wav'): ins += ['-i', f'{d}/sfx.wav']; fa += f';[{n}:a]volume=-8dB[s]'; mix += '[s]'; n += 1
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + ins + ['-filter_complex', f'{fa};{mix}amix=inputs={n - 1}:normalize=0:duration=first,alimiter=limit=0.89[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', f'{d}/short.mp4'], check=True)
print(f'{d}/short.mp4  {dur:.1f}s')
