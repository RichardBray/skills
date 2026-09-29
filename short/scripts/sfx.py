#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Synthesize sound effects from events.json (written by render.mjs) so each sound lands on its visual.

usage: sfx.py events.json duration_seconds out.wav
Event types: pop, key, tick, count, chime, whoosh, impact.
"""
import json, sys, wave
import numpy as np, scipy.signal as sg
sr = 44100; rng = np.random.default_rng(3)
events = json.load(open(sys.argv[1])); T = float(sys.argv[2]); out = sys.argv[3]; N = int(sr * (T + 2))
bus = np.zeros((2, N))
tt = lambda d: np.arange(int(d * sr)) / sr
ex = lambda n, tau: np.exp(-np.arange(n) / sr / tau)
def hp(x, fc): return sg.sosfilt(sg.butter(2, fc, 'hp', fs=sr, output='sos'), x)
def lp(x, fc): return sg.sosfilt(sg.butter(2, min(fc, sr * .45), 'lp', fs=sr, output='sos'), x)
def place(sig, t, gain=1.0, pan=0.0):
    i = int(t * sr)
    if i < 0 or i >= N: return
    if sig.ndim == 1:
        a = (pan + 1) * np.pi / 4; sig = np.stack([sig * np.cos(a), sig * np.sin(a)])
    n = min(sig.shape[1], N - i); bus[:, i:i + n] += sig[:, :n] * gain
def pop(f, d=.28):
    t = tt(d); ph = 2 * np.pi * np.cumsum(f * (1 + .9 * np.exp(-t / .025))) / sr
    return np.sin(ph) * ex(len(t), .07) * (1 - np.exp(-t / .002))
def click(f):
    n = int(.03 * sr); t = tt(.03)
    return hp(rng.standard_normal(n), 1800) * ex(n, .004) * .5 + np.sin(2 * np.pi * f * t) * ex(n, .007) * .35
def tick(f):
    t = tt(.05); return np.sin(2 * np.pi * f * t) * ex(len(t), .012) * .5 + hp(rng.standard_normal(len(t)), 4000) * ex(len(t), .004) * .2
def chime(f, d=1.4):
    t = tt(d); y = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / tau) for r, a, tau in ((1, 1, 1.0), (2.76, .45, .55), (5.4, .25, .3)))
    return y * (1 - np.exp(-t / .002)) * .5
def whoosh(d=.6, up=True):
    n = int(d * sr); x = np.linspace(0, 1, n); f0, f1 = (350, 6000) if up else (6000, 350)
    curve = f0 * (f1 / f0) ** x; env = np.sin(np.pi * x) ** 1.6; y = np.zeros((2, n))
    for c in range(2):
        noise = rng.standard_normal(n); o = np.zeros(n); zi = None
        for s in range(0, n, 512):
            fc = curve[s]; sos = sg.butter(2, [max(30, fc / 1.7), min(sr * .45, fc * 1.7)], 'bp', fs=sr, output='sos')
            if zi is None: zi = np.zeros((sos.shape[0], 2))
            seg, zi = sg.sosfilt(sos, noise[s:s + 512], zi=zi); o[s:s + 512] = seg
        y[c] = o * env
    return y / (np.abs(y).max() + 1e-9)
def impact(d=1.8):
    t = tt(d); ph = 2 * np.pi * np.cumsum(42 + 90 * np.exp(-t / .09)) / sr
    y = np.sin(ph) * np.exp(-t / .7) + lp(rng.standard_normal(len(t)), 500) * np.exp(-t / .18) * .8
    return y / (np.abs(y).max() + 1e-9)
n_by = {}
for e in sorted(events, key=lambda e: e['t']):
    k = e['type']; g = e.get('gain', 1.0); n_by[k] = n_by.get(k, 0) + 1; i = n_by[k]; t = e['t']
    pan = rng.uniform(-.3, .3)
    if k == 'pop': place(pop(520 + 60 * (i % 6)), t, .3 * g, pan)
    elif k == 'key': place(click(2400 + rng.uniform(-500, 600)), t, .34 * g, pan)
    elif k == 'tick': place(tick(1800), t, .3 * g, pan)
    elif k == 'count': place(tick(1300 + 60 * (i % 14)), t, .14 * g, pan)
    elif k == 'chime': place(chime(1318.5 if i % 2 else 1568), t, .3 * g, pan)
    elif k == 'whoosh': place(whoosh(.7, True), t - .1, .3 * g)
    elif k == 'impact': place(impact(), t, .6 * g)
# a soft whoosh on every scene change, if the caller passed scene times
if len(sys.argv) > 4:
    for _, s, _ in json.load(open(sys.argv[4]))[1:]: place(whoosh(.55, True), s - .18, .22)
bus /= (np.abs(bus).max() + 1e-9) / .6
d = (np.clip(bus, -1, 1).T * 32767).astype('<i2')
with wave.open(out, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(d.tobytes())
print(f'{len(events)} events -> {out}')
