import fs from 'node:fs';
const ROOT = new URL('..', import.meta.url).pathname;
const files = JSON.parse(fs.readFileSync(ROOT + 'files6.json', 'utf8'));
const ids = ['asset-c668c00d', 'asset-b6319499', 'asset-b3350b64', 'asset-1ba31203', 'asset-c3970b4c', 'asset-9a6b53b4', 'asset-07e0e3d5', 'asset-100fd5be', 'asset-41788c35', 'asset-72000289', 'asset-1db77583', 'asset-8c430752', 'asset-c8c83226', 'asset-99abbc0d', 'asset-e0d1dd16', 'asset-e5b68c03', 'asset-613c5302', 'asset-8f814dfe', 'asset-6b15368d', 'asset-a5d82b5d', 'asset-8a97e6d1', 'asset-3e0b0bc5', 'asset-7fb1eb8e', 'asset-aab65f45', 'asset-57214070', 'asset-8f04b5cb', 'asset-2e529610', 'asset-dfcfe7da', 'asset-2530b0cf', 'asset-ac2bfd53', 'asset-526532f4', 'asset-0fef1903', 'asset-6e4591eb', 'asset-e6f95509', 'asset-fde3c20b', 'asset-56abfd24', 'asset-b10f3ae6', 'asset-f92ed115', 'asset-79a38aa0', 'asset-065d8f5a', 'asset-eac8e054', 'asset-26dfa791', 'asset-29d4785d', 'asset-42a83ee8', 'asset-b12c73d5'];
const AS = {}; files.forEach((f, i) => { AS[f.split('/').pop().replace(/\.\w+$/, '')] = ids[i]; });
const SC = JSON.parse(fs.readFileSync(ROOT + 'scenes.json', 'utf8'));
const V = ['g0', 'g1', 'g2', 'g3', 'g4', 'g5'];
const LEN = [6.33, 3.2, 6.0, 5.2, 3.8, 4.5];
const TAIL = {};
const D = [6.060408, 2.507755, 4.075102, 4.858776, 3.343673, 3.813878];
const VOICE = 'track-0446168e', MUSIC = 'track-8808119b';
const r3 = (n) => Math.round(n * 1000) / 1000, r2 = (n) => Math.round(n * 100) / 100;
const rect = (sc, l) => { const j = JSON.parse(fs.readFileSync(ROOT + 'rects-s' + sc + '.json', 'utf8')); const [, x, y, w, h] = j.find((a) => a[0] === l); return { cx: x + w / 2 - 540, cy: 960 - (y + h / 2) }; };
const tf = (x, y, s = 1, op = 1) => ({ x: r2(x), y: r2(y), scaleX: s, scaleY: s, rotation: 0, rotationX: 0, rotationY: 0, opacity: op });
const pop = (s, d = 0.24) => ({ end: r3(s + d), dur: d, ease: 'backOut', to: { 'transform.scaleX': 1, 'transform.scaleY': 1, 'transform.opacity': 1 } });
export const clips = []; let c = 0;
SC.forEach((s, i) => {
  const len = LEN[i], end = c + len;
  clips.push({ asset: AS[V[i]], start: r3(c + 0.05), end: r3(c + 0.05 + D[i]), anims: [], type: 'audio' });
  if (TAIL[i]) clips.push({ asset: AS[TAIL[i].asset], start: r3(c + TAIL[i].off), end: r3(c + TAIL[i].off + TAIL[i].dur), anims: [], type: 'audio' });
  clips.push({ asset: AS[`s${i}-base`], start: r3(c), end: r3(end), t: tf(0, 0), anims: [], type: 'image' });
  s.layers.forEach((l) => { const r = rect(i, l.id), st = c + l.d; clips.push({ asset: AS[`s${i}-${l.id}`], start: r3(st), end: r3(end), t: tf(r.cx, r.cy, 0.85, 0), anims: [pop(st)], type: 'image' }); });
  c = end;
});
export const TOTAL = r3(c);
const [mode, a, b] = process.argv.slice(2);
if (mode === 'info') console.log(clips.length, TOTAL, AS['music-reaching-out']);
if (mode === 'adds') console.log(JSON.stringify(clips.slice(+a, +b).map((k) => k.type === 'audio' ? { command: 'clip_add', args: { type: 'audio', assetId: k.asset, start: k.start, duration: r3(k.end - k.start), track: VOICE } } : { command: 'clip_add', args: { type: 'image', assetId: k.asset, start: k.start, duration: r3(k.end - k.start), props: { transform: k.t } } })));
if (mode === 'anims') { const cl = JSON.parse(fs.readFileSync(ROOT + 'ids6.json', 'utf8')); const cmds = []; clips.forEach((k, i) => k.anims.forEach((an) => cmds.push({ command: 'animation_add', args: { clip: cl[i], end: an.end, duration: an.dur, easing: an.ease, to: an.to } }))); console.log(JSON.stringify(cmds)); }
