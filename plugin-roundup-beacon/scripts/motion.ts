// usage: bun motion.ts <dir> intro
//          writes <dir>/motion-intro.html, the payoff variant's card deck, from cfg.intro
//        bun motion.ts <dir> hook
//          writes <dir>/motion-hook.html, the custom variant's intro, from cfg.hook and hook-words.json
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
const BURST_TILES = ['📅','📊','✉️','🎨','🧾','📦','💬','📈','🗂️','🛒','🎵','📷','📝','⚙️','🔔','💳','🧠','📌','📣','🏷️','🧮','🔗','📁','🎯','🖊️','📞','🌐','🧩','📍','🗓️'];
const esc = (t: string) =>t.replace(/&/g, '&amp;').replace(/</g, '&lt;');

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
} else if (mode === 'hook') {
  const h = cfg.hook;
  if (cfg.variant !== 'custom' || !h) { console.error("the hook intro needs variant: 'custom' and cfg.hook"); process.exit(1); }
  const wf = resolve(DIR, 'hook-words.json');
  if (!existsSync(wf)) { console.error('hook-words.json is missing: save Fish speech_to_text (with timestamps) of voices/v0.mp3 there'); process.exit(1); }
  const spoken = spokenWords(JSON.parse(readFileSync(wf, 'utf8')));
  const NUM = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'];
  const norm = (s: string) => { const n = s.toLowerCase().replace(/[^a-z0-9]/g, ''); return /^\d+$/.test(n) && NUM[+n] ? NUM[+n] : n; };
  let k = 0;
  const timed = [...h.lines, h.bar].map(line => line.trim().split(/\s+/).map(text => {
    let j = k;
    while (j < spoken.length && j - k <= 2 && norm(spoken[j].text) !== norm(text)) j++;
    if (j >= spoken.length || norm(spoken[j].text) !== norm(text)) {
      console.error(`"${text}" isn't among the next spoken words. Heard: ${spoken.map(w => w.text).join(' ')}`); process.exit(1);
    }
    k = j + 1;
    return { text, t: r3(spoken[j].start) };
  }));
  const lines = timed.slice(0, -1), bar = timed[timed.length - 1];
  const find = (word: string) => { for (const [i, l] of lines.entries()) { const j = l.findIndex(w => norm(w.text) === norm(word)); if (j >= 0) return [i, j]; } return null; };
  const mark = find(h.mark);
  if (!mark) { console.error(`mark "${h.mark}" isn't one of the shown words`); process.exit(1); }
  if (h.style === 'desk' && (lines.length < 2 || mark[0] !== 1)) { console.error('desk needs at least two lines, with the mark on line 2'); process.exit(1); }
  if (h.style === 'ledger' && (lines.length < 4 || mark[0] < 2 || mark[0] > 3 || !h.ledger?.rows.length)) { console.error('ledger needs at least four lines, the mark on line 3 or 4, and cfg.hook.ledger rows'); process.exit(1); }
  const tiles = h.tiles ?? (h.style === 'burst' ? BURST_TILES : undefined);
  const want = h.style === 'burst' ? 30 : 5;
  if (!tiles || tiles.length !== want) { console.error(`${h.style} needs ${want} tiles`); process.exit(1); }
  if (h.style === 'desk' && h.cards && (h.cards.length < 2 || !h.stamp)) { console.error('desk cards need at least two cards and a stamp'); process.exit(1); }
  const logoFile = resolve(DIR, cfg.hookLogo);
  const logo = existsSync(logoFile) ? `data:image/${cfg.hookLogo.endsWith('.png') ? 'png' : 'svg+xml'};base64,${readFileSync(logoFile).toString('base64')}` : null;
  const v = JSON.parse(readFileSync(resolve(DIR, 'voices.json'), 'utf8')) as { hookEnd?: number };
  const len = r3((v.hookEnd ?? 4.6) + 0.4);
  const data = {
    lines, bar, mark, len, accent: h.accent, second: h.second ?? { burst: '#ffe14d', desk: '#14b8a6', ledger: '#16a34a' }[h.style], tiles,
    logo: h.style === 'burst' ? find(cfg.harness) && logo : logo, logoAt: h.style === 'burst' && logo ? find(cfg.harness) : null,
    cards: h.cards ?? [], stamp: h.stamp ?? '', ledger: h.ledger ?? null,
  };
  writeFileSync(resolve(DIR, 'motion-hook.html'), tpl(`hook-${h.style}.html`).replace('{{DATA}}', JSON.stringify(data).replace(/</g, '\\u003c')));
  console.log(`motion-hook.html (${h.style}): motion_add at T0 for ${len}s, then motion_code with the file's text`);
} else { console.error('usage: motion.ts <dir> intro | hook | private --t0 --private --access'); process.exit(1); }

// Fish speech_to_text output varies in shape: take every object with a word and a start time, innermost first.
function spokenWords(j: unknown): Array<{ text: string; start: number }> {
  const out: Array<{ text: string; start: number }> = [];
  const walk = (o: unknown): boolean => {
    if (Array.isArray(o)) return o.map(walk).some(Boolean);
    if (!o || typeof o !== 'object') return false;
    const r = o as Record<string, unknown>;
    const inner = Object.values(r).map(walk).some(Boolean);
    const text = r.text ?? r.word, start = r.start ?? r.start_time;
    if (inner || typeof text !== 'string' || typeof start !== 'number') return inner;
    out.push({ text, start }); return true;
  };
  walk(j);
  return out.sort((a, b) => a.start - b.start);
}
