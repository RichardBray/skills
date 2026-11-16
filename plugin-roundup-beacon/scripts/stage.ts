// usage: bun stage.ts <dir> <prefix>        copy layers + voices into <dir>/stage, write import-N.json (36 files each)
//        bun stage.ts <dir> --map ids.json  write assets.json from the asset ids media_import returned, in import order
import { copyFileSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const [d, arg] = process.argv.slice(2);
if (!d || !arg) { console.error('usage: stage.ts <dir> <prefix> | stage.ts <dir> --map ids.json'); process.exit(1); }
const DIR = resolve(d), ST = resolve(DIR, 'stage');
const SCENES = ['hook', 's1', 's2', 's3', 's4', 's5', 'end'];

if (arg === '--map') {
  const names = JSON.parse(readFileSync(resolve(DIR, 'stage-names.json'), 'utf8')) as string[], prefix = JSON.parse(readFileSync(resolve(DIR, 'stage-prefix.json'), 'utf8')) as string;
  const raw = JSON.parse(readFileSync(resolve(DIR, process.argv[4] || 'ids.json'), 'utf8')) as Array<string | string[]>;
  const ids = raw.flat();
  if (ids.length !== names.length) { console.error(`expected ${names.length} asset ids, got ${ids.length}`); process.exit(1); }
  const map: Record<string, string> = {};
  names.forEach((n, i) => { map[n.slice(prefix.length).replace(/\.(png|mp3)$/, '')] = ids[i]!; });
  writeFileSync(resolve(DIR, 'assets.json'), JSON.stringify(map));
  console.log('assets.json:', Object.keys(map).length, 'entries');
  process.exit(0);
}

const prefix = arg;
rmSync(ST, { recursive: true, force: true }); mkdirSync(ST);
const files: Array<[string, string]> = [];
for (const sc of SCENES) {
  const rects = JSON.parse(readFileSync(resolve(DIR, `rects-${sc}.json`), 'utf8')) as Array<[string, ...number[]]>;
  for (const f of [`${sc}-base.png`, ...rects.map(l => `${sc}-${l[0]}.png`)]) files.push([resolve(DIR, f), prefix + f]);
}
for (let i = 0; i < 7; i++) files.push([resolve(DIR, `voices/v${i}.mp3`), `${prefix}v${i}.mp3`]);
for (const [src, name] of files) { if (!existsSync(src)) { console.error('missing', src); process.exit(1); } copyFileSync(src, resolve(ST, name)); }
const names = files.map(f => f[1]);
writeFileSync(resolve(DIR, 'stage-names.json'), JSON.stringify(names));
writeFileSync(resolve(DIR, 'stage-prefix.json'), JSON.stringify(prefix));
for (let i = 0; i * 36 < names.length; i++) {
  const list = names.slice(i * 36, i * 36 + 36).map(n => resolve(ST, n));
  writeFileSync(resolve(DIR, `import-${i + 1}.json`), JSON.stringify(list));
  console.log(`import-${i + 1}.json (${list.length} files):`); console.log(JSON.stringify(list));
}
console.log(`staged ${names.length} files. Import each list with media_import at a high \`at\` (e.g. 3000), clip_remove the staging clips, save the asset ids in import order to ids.json, then: bun stage.ts ${d} --map`);
