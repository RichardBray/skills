// Render a short's frames with headless Chrome.
// usage: node render.mjs <short-dir> [--template face] [--alpha] [--captions off] [--times 1.5,4] [--fps 30] [--sub 2] [--out frames] [--from s --to s]
// <short-dir> needs words.json (from align.py) and scenes.json. Writes events.json and scene_times.json too.
import { createRequire } from 'module'; import fs from 'fs'; import path from 'path'; import os from 'os'; import { fileURLToPath } from 'url';
const require = createRequire(path.join(os.homedir(), '.cache/short-skill/x.js'));
const puppeteer = require('puppeteer-core');
const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2); const dir = path.resolve(args[0]);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const FPS = +opt('fps', 30), SUB = +opt('sub', 2), SHUTTER = 0.5, out = path.resolve(dir, opt('out', 'frames'));
const aligned = JSON.parse(fs.readFileSync(path.join(dir, 'words.json'))); const spec = JSON.parse(fs.readFileSync(path.join(dir, 'scenes.json')));
const last = aligned.words[aligned.words.length - 1].end;
const alpha = args.includes('--alpha'); const tmpl = opt('template', 'default') === 'face' ? 'template_face.html' : 'template.html';
const data = { captions: opt('captions', 'on') !== 'off', words: aligned.words, scenes: spec.scenes, duration: +(spec.duration || (last + (spec.tail ?? 1.2))), assets: path.join(dir, 'assets') };
const chrome = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium'].find(fs.existsSync);
const b = await puppeteer.launch({ executablePath: chrome, headless: 'new', args: ['--allow-file-access-from-files', '--force-device-scale-factor=1'] });
const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 });
p.on('pageerror', e => { console.error('PAGE ERROR:', e.message); process.exit(1); });
await p.evaluateOnNewDocument(d => { window.DATA = d; }, data);
await p.goto('file://' + path.join(here, tmpl)); await p.evaluate('window.ready');
fs.writeFileSync(path.join(dir, 'events.json'), JSON.stringify(await p.evaluate('window.events()')));
fs.writeFileSync(path.join(dir, 'scene_times.json'), JSON.stringify(await p.evaluate('window.sceneTimes()')));
console.log('duration', data.duration.toFixed(2), 'scenes', JSON.stringify(await p.evaluate('window.sceneTimes()')));
fs.mkdirSync(out, { recursive: true });
const times = opt('times', null);
if (times) { for (const t of times.split(',').map(Number)) { await p.evaluate(t => render(t), t); await p.screenshot({ path: `${out}/test_${t.toFixed(2)}.png`, omitBackground: alpha }); } }
else {
  const n0 = Math.round(+opt('from', 0) * FPS), n1 = Math.round(+opt('to', data.duration) * FPS);
  for (let n = n0; n < n1; n++) {
    for (let k = 0; k < SUB; k++) { const t = (n + (SUB === 1 ? 0 : (k / SUB - 0.5) * SHUTTER)) / FPS; await p.evaluate(t => render(Math.max(0, t)), t); await p.screenshot({ path: `${out}/f_${String(n).padStart(5, '0')}_${k}.png`, omitBackground: alpha }); }
    if (n % 90 === 0) console.log('frame', n, '/', n1);
  }
}
await b.close();
