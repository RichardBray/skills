// usage: bun plan.ts <dir> --t0 <seconds> --voice-track <track-id> --music-asset <asset-id> --music-track <track-id> [--out file.mp4]
//   writes build.js, one Beacon `script` that adds the music, every clip and every animation in one undo step,
//   and export.json for export_start
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { loadCfg, opt as optIn, r3 } from './lib.ts';

const argv = process.argv.slice(2);
const opt = (n: string) => optIn(argv, n);
const DIR = resolve(argv[0] || '.');
const T0 = Number(opt('t0'));
const VOICE = opt('voice-track'), MUSIC = opt('music-asset'), MTRACK = opt('music-track');
if (!(T0 >= 0) || typeof VOICE !== 'string' || typeof MUSIC !== 'string' || typeof MTRACK !== 'string') {
  console.error('need --t0, --voice-track, --music-asset and --music-track'); process.exit(1);
}
process.env.VDIR = DIR; process.env.T0 = String(T0);
const { clips, END } = await import('./spec.ts');
const cfg = await loadCfg(DIR);
const data = clips.map(c => [c.type === 'audio' ? 1 : 0, c.asset, c.start, r3((c.trimEnd || c.end) - c.start), c.t ? [c.t.x, c.t.y, c.t.scaleX, c.t.scaleY, c.t.opacity] : 0, c.anims.map(a => [a.end, a.dur, a.ease, a.to])]);
// The music goes on first: clip_add puts images on the lowest free track, which is the music track until it is filled.
const js = `const B = ${JSON.stringify({ T0, END: r3(END), C: data })};
beacon.run("clip_add", { type: "audio", assetId: ${JSON.stringify(MUSIC)}, start: B.T0, duration: Math.round((B.END - B.T0) * 1000) / 1000, track: ${JSON.stringify(MTRACK)}, props: { audio: { gain: 1, volume: 0.12, normalize: true, muted: false } } });
let n = 0;
for (const [audio, asset, start, duration, t, anims] of B.C) {
  const id = audio
    ? beacon.run("clip_add", { type: "audio", assetId: asset, start, duration, track: ${JSON.stringify(VOICE)} })
    : beacon.run("clip_add", { type: "image", assetId: asset, start, duration, props: { transform: { x: t[0], y: t[1], scaleX: t[2], scaleY: t[3], rotation: 0, rotationX: 0, rotationY: 0, opacity: t[4] } } });
  for (const [end, dur, easing, to] of anims) { beacon.run("animation_add", { clip: id, end, duration: dur, easing, to }); n++; }
}
return { clips: B.C.length, anims: n, end: B.END };
`;
writeFileSync(resolve(DIR, 'build.js'), js);
const out = opt('out') || resolve(dirname(DIR), `stop-using-${cfg.harness.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-without-these-5-${cfg.noun.replace(/[^a-z0-9]+/gi, '-').toLowerCase()}.mp4`);
writeFileSync(resolve(DIR, 'export.json'), JSON.stringify({ output: out, from: T0, to: r3(END), speed: 1.2, overwrite: true }));
console.log(`build.js: ${clips.length} clips, section ${T0} to ${r3(END)}. Run its text with the Beacon script tool (seconds: 30).`);
console.log('export.json:', readFileSync(resolve(DIR, 'export.json'), 'utf8'));
