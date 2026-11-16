import path from 'node:path';
import { r3 } from './lib.ts';
import type { Clip } from './spec.ts';

const [dir, mode, a, b, ...ids] = process.argv.slice(2);
if (!dir || !mode) { console.error('usage: T0=<s> bun emit.ts <dir> info|adds <from> <to>|anims <from> <to> <ids...>'); process.exit(1); }
process.env.VDIR = path.resolve(dir);
const { clips, END } = await import('./spec.ts');
const VOICE = process.env.VOICE_TRACK || 'track-c99ce6e2';
const dur = (c: Clip) => r3((c.trimEnd || c.end) - c.start);
const addCmd = (c: Clip) => c.type === 'audio'
  ? { command: 'clip_add', args: { type: 'audio', assetId: c.asset, start: c.start, duration: dur(c), track: VOICE } }
  : { command: 'clip_add', args: { type: 'image', assetId: c.asset, start: c.start, duration: r3(c.end - c.start), props: { transform: c.t } } };
if (mode === 'info') { console.log('clips', clips.length, 'end', END); console.log(clips.map((c, i) => i + ':' + c.key + ' ' + c.start + '-' + c.end).join('\n')); }
if (mode === 'adds') console.log(JSON.stringify(clips.slice(Number(a), Number(b)).map(addCmd)));
if (mode === 'anims') {
  const cmds: Array<{ command: string; args: Record<string, unknown> }> = [];
  clips.slice(Number(a), Number(b)).forEach((c, i) => {
    const id = ids[i];
    if (!id) throw new Error(`missing clip id for ${c.key}`);
    for (const an of c.anims) cmds.push({ command: 'animation_add', args: { clip: id.startsWith('clip-') ? id : 'clip-' + id, end: an.end, duration: an.dur, easing: an.ease, to: an.to } });
  });
  console.log(JSON.stringify(cmds));
}
