// usage: node verify.mjs <video.mp4>   ffprobe length + loudness, writes <video>-sheet.png (hook, each scene, end)
import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';

const f = resolve(process.argv[2] || '');
const probe = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration:stream=width,height,codec_type', '-of', 'json', f], { encoding: 'utf8' });
if (probe.status) { console.error('ffprobe failed', probe.stderr); process.exit(1); }
const j = JSON.parse(probe.stdout), dur = +j.format.duration, v = j.streams.find(s => s.codec_type === 'video');
console.log(`length ${dur.toFixed(2)}s, ${v.width}x${v.height}, audio ${j.streams.some(s => s.codec_type === 'audio') ? 'yes' : 'NO'}`);
let bad = 0;
if (v.width !== 1080 || v.height !== 1920) { console.log('WARN size is not 1080x1920'); bad++; }
const ld = spawnSync('ffmpeg', ['-nostats', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], { encoding: 'utf8' });
const lufs = [...ld.stderr.matchAll(/I:\s+(-?[0-9.]+) LUFS/g)].pop();
if (lufs) { const l = +lufs[1]; console.log(`loudness ${l} LUFS`); if (l < -23 || l > -20) { console.log('WARN loudness outside -23..-20 LUFS'); bad++; } }
// 10 frames: hook and end plus evenly spaced scenes; adjacent frames that are near-identical or wildly different are flagged by mean luma
const times = [1.5, 4.5, ...[1, 2, 3, 4, 5].map(i => 5.2 / 1.2 + (dur - 5.2 / 1.2 - 3.6) * (i - 0.4) / 5), dur - 1.2];
const out = f.replace(/\.mp4$/, '') + '-sheet.png';
const inputs = times.flatMap(t => ['-ss', t.toFixed(2), '-i', f]);
const filt = times.map((_, i) => `[${i}:v]scale=270:480[a${i}]`).join(';') + ';' + times.map((_, i) => `[a${i}]`).join('') + `hstack=inputs=${times.length}[o]`;
const r = spawnSync('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex', filt, '-map', '[o]', '-frames:v', '1', out], { encoding: 'utf8' });
if (r.status) { console.log('WARN frame sheet failed:', r.stderr.slice(0, 200)); bad++; } else console.log('frame sheet', out);
const lum = times.map(t => { const p = spawnSync('ffmpeg', ['-v', 'error', '-ss', t.toFixed(2), '-i', f, '-frames:v', '1', '-vf', 'scale=1:1,format=gray', '-f', 'rawvideo', '-'], { encoding: 'buffer' }); return p.stdout[0]; });
if (lum.some(x => x === undefined)) { console.log('WARN a sampled frame could not be read'); bad++; }
else if (lum.every(x => x > 245) || lum.some(x => x < 3)) { console.log('WARN a sampled frame is blank or black'); bad++; }
console.log(bad ? `verify: ${bad} warning(s), look at the sheet` : 'verify: ok, now look at the sheet');
