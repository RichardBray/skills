# short

Make a vertical 9:16 YouTube Short from a topic or a script. It writes (or takes) the script and stops so you can edit it, then voices it with your cloned voice (via [`say-as-me`](../say-as-me/README.md)) or your own recording, and builds word-by-word captions, motion graphics, music and sound effects.

## Installation

```sh
npx skills add https://github.com/RichardBray/skills --skill short
sh ~/.claude/skills/short/scripts/setup.sh
```

Needs `uv`, `ffmpeg`, Google Chrome, node, `OPENAI_API_KEY` and `REPLICATE_API_TOKEN`.

## Usage

```
/short [topic or path to a script]
```

Each short lives in its own folder: `script.md`, `voiceover.wav`, `words.json`, `scenes.json`, then the rendered `short.mp4`. Edit `script.md` any time before the voiceover; to use your own voice, drop a recording named `voiceover.wav` in the folder. Visuals are timed to spoken phrases, so edits and re-recordings re-time themselves.

See [`references/scenes.md`](references/scenes.md) for the scene types.
