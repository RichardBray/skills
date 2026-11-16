import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const ROOT = path.resolve(process.env.VDIR || process.cwd()) + '/';
const cfg = (await import(pathToFileURL(ROOT + 'cfg.mjs'))).default;
const AS = JSON.parse(fs.readFileSync(ROOT + 'assets.json', 'utf8'));
const rect = (sc, l) => { const j = JSON.parse(fs.readFileSync(ROOT + 'rects-' + sc + '.json', 'utf8')); const [, x, y, w, h] = j.find(a => a[0] === l); return { x, y, w, h, cx: x + w / 2 - 540, cy: 960 - (y + h / 2) }; };
const r2 = n => Math.round(n * 100) / 100, r3 = n => Math.round(n * 1000) / 1000;
const tf = (x, y, sx = 1, sy = 1, op = 1) => ({ x: r2(x), y: r2(y), scaleX: sx, scaleY: sy, rotation: 0, rotationX: 0, rotationY: 0, opacity: op });
const T0 = +process.env.T0, N = 5, W = 978 / N;
const VJ = JSON.parse(fs.readFileSync(ROOT + 'voices.json', 'utf8')); const D = VJ.D; const FCPOS = +(process.env.FCPOS || cfg.fcPos || 1);
if (!(T0 >= 0)) throw new Error('set T0 (timeline start, seconds)');
export const clips = [];
const C = (key, asset, start, end, t, anims = [], type = 'image', extra = {}) => clips.push({ key, asset: AS[asset], start: r3(start), end: r3(end), t, anims, type, ...extra });
const pop = (s, d = .22) => ({ end: r3(s + d), dur: d, ease: 'backOut', to: { 'transform.scaleX': 1, 'transform.scaleY': 1, 'transform.opacity': 1 } });
const fade = (s, d = .15) => ({ end: r3(s + d), dur: d, ease: 'easeOut', to: { 'transform.opacity': 1 } });
const rise = (s, y) => ({ end: r3(s + .3), dur: .3, ease: 'easeOut', to: { 'transform.y': r2(y), 'transform.opacity': 1 } });
const blockAnims = (c, e) => [{ end: r3(c + .15), dur: .15, ease: 'easeOut', to: { 'transform.scaleX': 1, 'transform.scaleY': 1, 'transform.opacity': 1 } }, { end: r3(e), dur: .3, ease: 'easeIn', to: { 'transform.scaleY': 0, 'transform.y': 960 } }];
const blockT = sc => { const r = rect(sc, 'block'); return tf(r.cx, r.cy, 1.06, 1.06, 0); };
const HE = T0 + 5.2;
C('v0', 'v0', T0, Math.min(T0 + D[0], HE - .03), null, [], 'audio');
C('hook-base', 'hook-base', T0, HE, tf(0, 0));
const slotCy = 960 - 1720;
for (let i = 0; i < N; i++) {
  const r = rect('hook', 't' + i), s = T0 + 0.2 + i * 0.12, fall = HE - 1.0;
  const tx = 51 + (i + .5) * W - 540;
  C('hook-t' + i, 'hook-t' + i, T0, HE, tf(r.cx, r.cy, .8, .8, 0), [pop(s), { end: r3(HE - .2), dur: .6, ease: 'easeIn', to: { 'transform.y': -1150, 'transform.scaleX': .8, 'transform.scaleY': .8 } }]);
}
[['stop', .08], ['using', 1.03], ['hlogo', 1.29], ['hname', 1.29], ['without', 2.29], ['these', 2.61]].forEach(([n, s]) => { const r = rect('hook', n); C('hook-' + n, 'hook-' + n, T0 + s, HE, tf(r.cx, r.cy, .8, .8, 0), [pop(T0 + s)]); });
{ const r = rect('hook', 'bar'); C('hook-bar', 'hook-bar', T0 + 3.21, HE, tf(r.x - 540, r.cy, 0, 1, 1), [{ end: r3(T0 + 3.91), dur: .7, ease: 'easeOut', to: { 'transform.x': r2(r.cx), 'transform.scaleX': 1 } }]);
  let q = rect('hook', 'three'); C('hook-three', 'hook-three', T0 + 3.21, HE, tf(q.cx, q.cy, .8, .8, 0), [pop(T0 + 3.21)]);
  q = rect('hook', 'plugins'); C('hook-plugins', 'hook-plugins', T0 + 4.03, HE, tf(q.cx, q.cy, .8, .8, 0), [pop(T0 + 4.03)]); }
const sc = []; let c = HE;
for (let n = 1; n <= 5; n++) {
  const d = D[n]; const s = n === FCPOS ? { n, c, e: c + 2.3, ps: c + 2.5, t0: c + 3.0, d: 2.6, ce: c + D[n] - .27, vend: D[n] - .37, sh: (VJ.sh && VJ.sh[n] !== undefined) ? VJ.sh[n] : D[n] - 11.6766 } : { n, c, e: c + 1.8, ps: c + 2.0, t0: c + 2.3, d: 2.2, r: c + Math.max(4.4, d * .55), ce: c + d + .3 };
  sc.push(s); C('v' + n, 'v' + n, c, c + d, null, [], 'audio', s.vend ? { trimEnd: c + s.vend } : {}); c = s.ce;
}
sc.forEach(s => { const K = 's' + s.n, R = l => rect(K, l); const nx = s.ce;
  C(K + '-base', K + '-base', s.c, s.ce, tf(0, 0));
  let r = R('slot'); C(K + '-slot', K + '-slot', s.e, s.ce, tf(r.cx, r.cy, .7, .7, 0), [pop(s.e, .25)]);
  r = R('head'); const hs = s.e + .05; C(K + '-head', K + '-head', hs, s.ce, tf(r.cx, r.cy - 30, 1, 1, 0), [rise(hs, r.cy)]);
  r = R('prompt'); C(K + '-prompt', K + '-prompt', s.ps, s.ce, tf(r.cx, r.cy, 1, 1, 0), [fade(s.ps)]);
  const cv = R('cover'), we = s.t0 + s.d;
  C(K + '-cover', K + '-cover', s.ps, we + .1, tf(cv.cx, cv.cy, 1, 1, 0), [fade(s.ps), { end: r3(we), dur: s.d, ease: 'linear', to: { 'transform.x': r2(cv.x + cv.w - 540), 'transform.scaleX': 0 } }]);
  C(K + '-cursor', K + '-cursor', s.t0, we, tf(cv.x + 2.5 - 540, cv.cy, 1, 1, 0), [{ end: r3(s.t0 + .05), dur: .05, ease: 'linear', to: { 'transform.opacity': 1 } }, { end: r3(we - .05), dur: r3(s.d - .05), ease: 'linear', to: { 'transform.x': r2(cv.x + cv.w - 540 + 2.5) } }]);
  if (s.n === FCPOS) {
    [['uc0', 5.97], ['uc1', 6.53], ['uc2', 7.43]].forEach(([n, o]) => { o += s.sh; const q = R(n); C(K + '-' + n, K + '-' + n, s.c + o, s.c + 8.6 + s.sh, tf(q.cx, q.cy, .8, .8, 0), [pop(s.c + o, .26)]); });
    [['wall0', 8.6], ['wall1', 8.77], ['wall2', 8.9]].forEach(([n, o]) => { o += s.sh; const q = R(n); C(K + '-' + n, K + '-' + n, s.c + o, s.ce, tf(q.cx, q.cy, .6, .6, 0), [pop(s.c + o, .25)]); });
  } else { r = R('result'); C(K + '-result', K + '-result', s.r, s.ce, tf(r.cx, r.cy - 30, 1, 1, 0), [rise(s.r, r.cy)]); }
  C(K + '-block', K + '-block', s.c, s.e, blockT(K), blockAnims(s.c, s.e));
});
{ const E = c, f1 = rect('end', 'f1'), f2 = rect('end', 'f2'), tl = rect('end', 'tiles');
  C('v6', 'v6', E + .05, E + .05 + D[6], null, [], 'audio');
  C('end-base', 'end-base', E, E + 3.63, tf(0, 0));
  C('end-f1', 'end-f1', E + .08, E + 3.63, tf(f1.cx, f1.cy - 30, 1, 1, 0), [rise(E + .08, f1.cy)]);
  C('end-f2', 'end-f2', E + 1.35, E + 3.63, tf(f2.cx, f2.cy - 30, 1, 1, 0), [rise(E + 1.35, f2.cy)]);
  C('end-tiles', 'end-tiles', E + 2.27, E + 3.63, tf(tl.cx, tl.cy, .7, .7, 0), [pop(E + 2.27, .25)]);
  clips.END = E + 3.63; }
export const END = clips.END; delete clips.END;
