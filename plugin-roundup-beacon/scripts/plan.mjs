// usage: node plan.mjs <dir> --t0 <seconds> [--voice-track track-id]
//          writes plan-1.json.. : transactions of at most 20 clip_add commands (Beacon only returns the first 20 ids)
//        node plan.mjs <dir> --t0 <seconds> --anims [--music-asset asset-id --music-track track-id --out file.mp4]
//          reads ids.txt (every clip id from the adds, in order) and writes anims.json, music.json and export.json
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';

const argv = process.argv.slice(2);
const opt = n => { const i = argv.indexOf('--' + n); return i < 0 ? undefined : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const DIR = resolve(argv[0] || '.');
const T0 = +opt('t0');
if (!(T0 >= 0)) { console.error('--t0 <timeline seconds> is required'); process.exit(1); }
process.env.VDIR = DIR; process.env.T0 = String(T0);
const VOICE = opt('voice-track') || 'track-c99ce6e2';
const { clips, END } = await import('./spec.mjs');
const cfg = (await import('file://' + resolve(DIR, 'cfg.mjs'))).default;
const dur = c => Math.round(((c.trimEnd || c.end) - c.start) * 1000) / 1000;
const add = c => c.type === 'audio'
  ? { command: 'clip_add', args: { type: 'audio', assetId: c.asset, start: c.start, duration: dur(c), track: VOICE } }
  : { command: 'clip_add', args: { type: 'image', assetId: c.asset, start: c.start, duration: Math.round((c.end - c.start) * 1000) / 1000, props: { transform: c.t } } };
const w = (f, o) => writeFileSync(resolve(DIR, f), JSON.stringify(o));

if (!opt('anims')) {
  const n = Math.ceil(clips.length / 20);
  for (let i = 0; i < n; i++) w(`plan-${i + 1}.json`, clips.slice(i * 20, i * 20 + 20).map(add));
  console.log(`${clips.length} clips -> plan-1..${n}.json, section ${T0} to ${Math.round(END * 1000) / 1000}.`);
  console.log(`Submit each as a Beacon transaction in order. Append every returned id (the "result" array, in order) to ${DIR}/ids.txt, space separated, ${clips.length} ids in all. Then re-run with --anims.`);
} else {
  if (!existsSync(resolve(DIR, 'ids.txt'))) { console.error('ids.txt missing'); process.exit(1); }
  const ids = readFileSync(resolve(DIR, 'ids.txt'), 'utf8').split(/\s+/).filter(Boolean);
  if (ids.length !== clips.length) { console.error(`ids.txt has ${ids.length} ids, expected ${clips.length}`); process.exit(1); }
  const cmds = [];
  clips.forEach((c, i) => c.anims.forEach(an => cmds.push({ command: 'animation_add', args: { clip: ids[i].startsWith('clip-') ? ids[i] : 'clip-' + ids[i], end: an.end, duration: an.dur, easing: an.ease, to: an.to } })));
  w('anims.json', cmds);
  console.log(`anims.json: ${cmds.length} animation_add commands (one transaction).`);
  if (opt('music-asset')) {
    w('music.json', [{ command: 'clip_add', args: { type: 'audio', assetId: opt('music-asset'), start: T0, duration: Math.round((END - T0) * 1000) / 1000, track: opt('music-track'), props: { audio: { gain: 1, volume: 0.15, normalize: true, muted: false } } } }]);
    console.log('music.json: volume 0.15 via props.audio (a top-level volume prop is rejected).');
  }
  const out = opt('out') || resolve(dirname(DIR), `stop-using-${cfg.harness.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-without-these-5-${cfg.noun}.mp4`);
  w('export.json', { output: out, from: T0, to: Math.round(END * 1000) / 1000, speed: 1.2, overwrite: true });
  console.log('export.json:', JSON.stringify(JSON.parse(readFileSync(resolve(DIR, 'export.json')))));
}
