import path from 'node:path';
const [dir, mode, a, b, ...ids] = process.argv.slice(2);
if (!dir || !mode) { console.error('usage: T0=<s> node emit.mjs <dir> info|adds <from> <to>|anims <from> <to> <ids...>'); process.exit(1); }
process.env.VDIR = path.resolve(dir);
const { clips, END } = await import('./spec.mjs');
const VOICE = process.env.VOICE_TRACK || 'track-c99ce6e2';
const dur = c => Math.round(((c.trimEnd || c.end) - c.start) * 1000) / 1000;
const addCmd = c => c.type === 'audio'
  ? { command: 'clip_add', args: { type: 'audio', assetId: c.asset, start: c.start, duration: dur(c), track: VOICE } }
  : { command: 'clip_add', args: { type: 'image', assetId: c.asset, start: c.start, duration: Math.round((c.end - c.start) * 1000) / 1000, props: { transform: c.t } } };
if (mode === 'info') { console.log('clips', clips.length, 'end', END); console.log(clips.map((c, i) => i + ':' + c.key + ' ' + c.start + '-' + c.end).join('\n')); }
if (mode === 'adds') console.log(JSON.stringify(clips.slice(+a, +b).map(addCmd)));
if (mode === 'anims') {
  const cmds = [];
  clips.slice(+a, +b).forEach((c, i) => c.anims.forEach(an => cmds.push({ command: 'animation_add', args: { clip: ids[i].startsWith('clip-') ? ids[i] : 'clip-' + ids[i], end: an.end, duration: an.dur, easing: an.ease, to: an.to } })));
  console.log(JSON.stringify(cmds));
}
