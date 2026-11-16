// usage: bun check.ts <dir> [--alexandria-list <file>] [--used 1,3,2] [--print-alexandria-command] [--post]
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadCfg, opt as optIn } from './lib.ts';

type Rect = [string, number, number, number, number];

const argv = process.argv.slice(2);
const DIR = resolve(argv[0] || '.');
const opt = (n: string) => optIn(argv, n);
const cfg = await loadCfg(DIR);
const ASSETS = fileURLToPath(new URL('./assets/', import.meta.url));
const norm = (s: unknown) => String(s).toLowerCase().replace(/[^a-z0-9]/g, '');
const fails: string[] = [], warns: string[] = [];
const fail = (m: string) => { fails.push(m); }, warn = (m: string) => { warns.push(m); };

const names = (cfg.NAMES ?? []).slice(1);
if (opt('print-alexandria-command')) {
  const pat = [...new Set(names.flatMap(n => [n.toLowerCase().replace(/[^a-z0-9]+/g, '.*'), n.toLowerCase().replace(/[^a-z0-9]/g, '')]))].join('|');
  console.log(`mcp alexandria_library_search command: ls /library/*/ | grep -iE "${pat}"`);
  console.log('Save its stdout to a file and pass it as --alexandria-list. No output means no overlap.');
  process.exit(0);
}

for (const k of ['harness', 'hookLogo', 'noun', 'fcPrompt'] as const) if (!cfg[k]) fail(`cfg.${k} is missing`);
if (!Array.isArray(cfg.NAMES) || cfg.NAMES.length !== 5) fail('cfg.NAMES must list 5 names: [Firecrawl, tool1..tool4]');
else if (cfg.NAMES[0] !== 'Firecrawl') fail('cfg.NAMES[0] must be "Firecrawl" (core inserts Firecrawl at fcPos; names/logos stay in [Firecrawl, tools...] order)');
if (!Array.isArray(cfg.L) || cfg.L.length !== 5) fail('cfg.L must list 5 logos: [logo-orange.svg, tool1..tool4]');
else if (cfg.L[0] !== 'logo-orange.svg') fail('cfg.L[0] must be logo-orange.svg');
if (!Array.isArray(cfg.tools) || cfg.tools.length !== 4) fail('cfg.tools must have 4 entries');
if (!Array.isArray(cfg.subs) || cfg.subs.length !== 4) fail('cfg.subs must have 4 entries (the two spoken sentences per tool)');
if (!Number.isInteger(cfg.fcPos) || cfg.fcPos < 1 || cfg.fcPos > 5) fail(`cfg.fcPos must be 1..5, got ${cfg.fcPos}`);
const used = String(opt('used') || '').split(',').filter(Boolean).map(Number);
if (used.includes(cfg.fcPos)) fail(`fcPos ${cfg.fcPos} was already used by another video (${used.join(',')}); vary it`);

for (const f of [...(cfg.L ?? []), cfg.hookLogo].filter(Boolean)) if (!existsSync(resolve(DIR, f)) && !existsSync(resolve(ASSETS, f))) fail(`logo file not found: ${f}`);
(cfg.tools ?? []).forEach((t, i) => {
  for (const k of ['chip', 'prompt', 'win'] as const) if (!t[k]) fail(`cfg.tools[${i}].${k} is missing`);
  if (t.win && !/illustrative/i.test(t.win)) fail(`tool "${t.chip}" result window is not labelled Illustrative`);
  if (cfg.NAMES && t.chip && norm(t.chip) !== norm(cfg.NAMES[i + 1])) warn(`chip "${t.chip}" differs from NAMES[${i + 1}] "${cfg.NAMES[i + 1]}"`);
});

const listFile = opt('alexandria-list');
if (!listFile || listFile === true) warn('no --alexandria-list given: tools were NOT checked against Alexandria providers (run with --print-alexandria-command)');
else {
  const slugs = readFileSync(resolve(listFile), 'utf8').split('\n').map(s => s.trim().replace(/\/$/, '')).filter(s => s && !/^README/i.test(s));
  for (const n of names) {
    const a = norm(n);
    const hit = slugs.filter(s => { const b = norm(s); return a.length >= 4 && (b.includes(a) || (b.length >= 4 && a.includes(b))); });
    if (hit.length) fail(`"${n}" is an Alexandria provider (${hit.join(', ')}); pick a tool Firecrawl does not already cover`);
  }
  const stop = new Set(['www', 'com', 'org', 'net', 'gov', 'index', 'developers', 'google', 'maps', 'trends', 'blog', 'docs']);
  const tokens = new Set(slugs.flatMap(s => s.split(/[-.]/)).filter(t => t.length >= 5 && !stop.has(t)));
  const texts = [cfg.fcPrompt, ...(cfg.subs ?? []), ...(cfg.tools ?? []).map(t => t.prompt)].filter(Boolean);
  for (const tok of tokens) for (const t of texts) if (new RegExp('\\b' + tok + '\\b', 'i').test(t)) warn(`text mentions "${tok}", an Alexandria provider name: "${t}"`);
}

const everything = JSON.stringify(cfg);
if (/alexandria/i.test(everything)) fail('the word "Alexandria" appears in cfg text (never say or show it)');

if (opt('post')) {
  const rp = resolve(DIR, 'rects-hook.json');
  if (!existsSync(rp)) fail('rects-hook.json missing (render first)');
  else {
    const r = JSON.parse(readFileSync(rp, 'utf8')) as Rect[], g = (n: string) => r.find(a => a[0] === n);
    const bar = g('bar'), pl = g('plugins');
    if (!bar || !pl) fail('hook rects lack bar or plugins layer');
    else {
      const gap = bar[1] + bar[3] - (pl[1] + pl[3]);
      if (gap < 30 || gap > 55) fail(`hook bar ends ${Math.round(gap)}px past the text (want ~41): re-run render.ts`);
      else console.log(`bar ends ${Math.round(gap)}px past the text`);
    }
  }
  const vp = resolve(DIR, 'voices.json');
  if (!existsSync(vp)) fail('voices.json missing (run voices.ts measure)');
  else {
    const v = JSON.parse(readFileSync(vp, 'utf8')) as { D?: number[] };
    if (!Array.isArray(v.D) || v.D.length !== 7 || v.D.some(x => !(x > 0))) fail('voices.json D must hold 7 positive durations');
  }
  const lp = resolve(DIR, 'lines.json');
  if (existsSync(lp) && /alexandria/i.test(readFileSync(lp, 'utf8'))) fail('"Alexandria" appears in the voice lines');
}

warns.forEach(w => console.log('WARN', w));
fails.forEach(f => console.log('FAIL', f));
console.log(fails.length ? `check: ${fails.length} problem(s)` : 'check: ok');
process.exit(fails.length ? 1 : 0);
