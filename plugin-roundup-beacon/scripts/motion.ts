// usage: bun motion.ts <dir> intro
//          writes <dir>/motion-intro.html, the payoff variant's card deck, from cfg.intro
//        bun motion.ts <dir> private --t0 <s> --private <s> --access <s>
//          writes <dir>/motion-private.html, timed from the transcript's "private" and "access" (timeline seconds),
//          and prints the clip's start and duration: it ends where the Firecrawl use-case rows arrive
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { loadCfg, opt as optIn, r3 } from './lib.ts';

const argv = process.argv.slice(2);
const DIR = resolve(argv[0] || '.'), mode = argv[1];
const opt = (n: string) => Number(optIn(argv, n));
const cfg = await loadCfg(DIR);
const tpl = (f: string) => readFileSync(new URL(`./motion/${f}`, import.meta.url), 'utf8');
const esc = (t: string) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;');

if (mode === 'intro') {
  const it = cfg.intro;
  if (!it) { console.error('cfg.intro is missing'); process.exit(1); }
  const file = resolve(DIR, it.icon);
  if (!existsSync(file)) { console.error(`icon file not found: ${it.icon}`); process.exit(1); }
  const icon = `<img src="data:image/${it.icon.endsWith('.png') ? 'png' : 'svg+xml'};base64,${readFileSync(file).toString('base64')}" alt="">`;
  const cards = it.cards.map(([b, i, chip], n) => `    <div class=card id=c${n} style="top:${116 + n * 144}px"><div><b>${esc(b)}</b><i>${esc(i)}</i></div><span class=chip>${esc(chip)}</span></div>`).join('\n');
  const html = tpl('intro.html').replace('{{ACCENT}}', it.accent).replace('{{SOFT}}', it.soft).replace('{{INK}}', it.ink).replace('{{PILL}}', it.pill ?? '#111')
    .replace('{{ICON}}', icon).replace('{{COUNT}}', String(it.count)).replace('{{LABEL}}', esc(it.label)).replace('{{CARDS}}', cards);
  const v = JSON.parse(readFileSync(resolve(DIR, 'voices.json'), 'utf8')) as { hookEnd?: number };
  const len = r3(Math.min(5.2, v.hookEnd ?? 5.2));
  writeFileSync(resolve(DIR, 'motion-intro.html'), html.replace('{{EXIT}}', String(r3(len - 0.5))));
  console.log(`motion-intro.html: motion_add at T0 for ${len}s, then motion_code with the file's text`);
} else if (mode === 'private') {
  const t0 = opt('t0'), p = opt('private'), a = opt('access');
  if (![t0, p, a].every(Number.isFinite)) { console.error('need --t0, --private and --access'); process.exit(1); }
  process.env.VDIR = DIR; process.env.T0 = String(t0);
  const { marks } = await import('./spec.ts');
  const start = r3(p - 0.05), dur = r3(marks.rowsAt - start);
  if (dur < 3) console.warn(`WARN only ${dur}s between "private" and the rows: the graphic will feel rushed`);
  const html = tpl('private.html').replaceAll('{{UNLOCK}}', String(r3(Math.max(1.2, a - start - 0.05)))).replace('{{EXIT}}', String(r3(dur - 0.45)));
  writeFileSync(resolve(DIR, 'motion-private.html'), html);
  console.log(`motion-private.html: motion_add at ${start} for ${dur}s, then motion_code with the file's text`);
} else { console.error('usage: motion.ts <dir> intro | private --t0 --private --access'); process.exit(1); }
