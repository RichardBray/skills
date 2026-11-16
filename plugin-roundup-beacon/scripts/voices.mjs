// usage: node voices.mjs <dir> lines      write lines.json: the 7 voice lines, flagging which need (re)generating
//        node voices.mjs <dir> done       record the current line texts as generated (after the Fish calls)
//        node voices.mjs <dir> measure    ffprobe voices/v0..v6.mp3 into voices.json (D) and the Firecrawl cue shift (sh)
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { execFileSync, spawnSync } from 'node:child_process';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [d, mode] = process.argv.slice(2);
if (!d || !mode) { console.error('usage: voices.mjs <dir> lines|done|measure'); process.exit(1); }
const DIR = resolve(d);
const cfg = (await import(pathToFileURL(resolve(DIR, 'cfg.mjs')))).default;
const TAG = '[warm, upbeat, like telling a friend]';
const VOICE = { voice_id: '933563129e564b19a115bedd57b7406a', model: 'drama-3', note: 'Fish Audio Sarah. Pass `text` to the fish-audio text_to_speech MCP tool with these two fields, then download the mp3 URL to `file`.' };
const ORD = ['One', 'Two', 'Three', 'Four', 'Five'], NUM = ['', 'one', 'two', 'three', 'four', 'five'];
const FC_LINE = '<emphasis>Firecrawl</emphasis>. The <emphasis>knowledge library</emphasis> for your agent. Live data on people, emails, jobs, and <emphasis>much more</emphasis>. All from one place.';
const say = n => (cfg.say && cfg.say[n]) || n;

const lines = [{ i: 0, key: 'hook', file: 'voices/v0.mp3', text: `${TAG} <emphasis>Stop</emphasis> using ${cfg.harness} without these <emphasis>${NUM[5]}</emphasis> ${cfg.noun}.` }];
let ti = 0;
for (let p = 1; p <= 5; p++) {
  const isFc = p === cfg.fcPos, name = isFc ? 'Firecrawl' : cfg.NAMES[ti + 1];
  const body = isFc ? FC_LINE : `<emphasis>${say(name)}</emphasis>. ${cfg.subs[ti++]}`;
  lines.push({ i: p, key: name, file: `voices/v${p}.mp3`, text: `${TAG} ${ORD[p - 1]}, ${body}` });
}
lines.push({ i: 6, key: 'cta', file: 'voices/v6.mp3', text: '[warm and friendly] <emphasis>Follow</emphasis> for more plugin suggestions.', reusable: 'The CTA never changes: copy voices/v6.mp3 from another video instead of regenerating.' });
const hash = t => createHash('sha1').update(t).digest('hex').slice(0, 12);
const lockPath = resolve(DIR, 'voices.lock.json');
const lock = existsSync(lockPath) ? JSON.parse(readFileSync(lockPath, 'utf8')) : {};

if (mode === 'lines') {
  for (const l of lines) { l.hash = hash(l.text); l.stale = !existsSync(resolve(DIR, l.file)) || lock[l.i] !== l.hash; }
  writeFileSync(resolve(DIR, 'lines.json'), JSON.stringify({ settings: VOICE, lines }, null, 1));
  console.log(lines.map(l => `${l.stale ? 'GENERATE' : 'ok      '} v${l.i} ${l.text}`).join('\n'));
  console.log(`${lines.filter(l => l.stale).length} of 7 lines need generating (about 1 credit per byte of text).`);
}
if (mode === 'done') {
  const out = {}; for (const l of lines) out[l.i] = hash(l.text);
  writeFileSync(lockPath, JSON.stringify(out)); console.log('voices.lock.json written');
}
if (mode === 'measure') {
  const dur = f => +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString().trim();
  const D = lines.map(l => dur(resolve(DIR, l.file)));
  const out = { D, sh: {} };
  // The scene's use-case rows were authored against a reference Firecrawl line: the third pause of 0.4s or more
  // ends where "Live data on people..." starts, which sat 4.69s into the reference.
  const r = spawnSync('ffmpeg', ['-nostats', '-i', resolve(DIR, `voices/v${cfg.fcPos}.mp3`), '-af', 'silencedetect=noise=-30dB:d=0.12', '-f', 'null', '-'], { encoding: 'utf8' });
  const longEnds = [...r.stderr.matchAll(/silence_end: ([0-9.]+) \| silence_duration: ([0-9.]+)/g)].filter(m => +m[2] >= 0.4).map(m => +m[1]);
  const fcD = D[cfg.fcPos];
  if (longEnds.length >= 3 && longEnds[2] < fcD - 1) out.sh[cfg.fcPos] = Math.round((longEnds[2] - 4.69) * 100) / 100;
  else console.warn(`WARN could not find the "Live data" pause (long pauses: ${longEnds.join(', ')}); spec falls back to D-11.6766, check the rows by eye`);
  writeFileSync(resolve(DIR, 'voices.json'), JSON.stringify(out));
  console.log('voices.json', JSON.stringify(out));
}
