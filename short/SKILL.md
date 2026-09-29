---
name: short
description: Make a vertical 9:16 YouTube Short from a topic or a script - write or take the script, let the user edit it, voice it with their cloned voice or their own recording, then build captions, motion graphics, music and sound effects. Use when the user asks to make, create or produce a short or shorts video.
argument-hint: [topic or path to a script]
allowed-tools: Bash(sh *), Bash(node *), Bash(uv run *), Bash(ffmpeg *), Bash(ffprobe *)
---

# Short

Make one 1080x1920 short in its own folder. The script is a plain file the user can edit, and every visual is timed to the spoken words, so edits and re-recordings just re-time it.

Requirements: `uv`, `ffmpeg`, Google Chrome, node, `OPENAI_API_KEY` (word timings) and `REPLICATE_API_TOKEN` (cloned voice, music). Run `sh scripts/setup.sh` once; it installs puppeteer-core into `~/.cache/short-skill`. Script paths below are relative to this skill's directory, e.g. `~/.claude/skills/short`.

## 1. The script

Make a folder named after the topic in the current directory and work there. If the user gave a script, use it as written. If they gave a topic, write the script following the `shorts-writer` skill's rules and references (read them), then save it as `script.md`. Check every number and claim against a real source or run; say what you could not verify. Aim for 45-55 seconds, about 2.7 words a second.

Stop here. Show the script and say the user can edit `script.md` directly. Ask which voice: their cloned voice (the `say-as-me` skill) or their own recording. Do not continue until they confirm the script.

## 2. The voiceover

Cloned voice: run `say-as-me` on the spoken lines and save the result as `voiceover.wav`. Check words per second and length and report them.

Own recording: tell the user to read `script.md` and save it as `voiceover.wav`, `.mp3` or `.m4a` in the folder, then wait. If they say it is there, carry on.

Either way the pipeline reads `voiceover.*`. Then run `uv run scripts/align.py voiceover.* script.md words.json`. It shows the script's own words in the captions, using Whisper only for timing. If under 85% of words match, the recording differs from the script: tell the user what differs before going on.

## 3. Scenes

Write `scenes.json` from `references/scenes.md`, using `references/example-scenes.json` as a model. Pick visuals that support each line without repeating it, and take numbers and commands only from real runs or data. Put any logos in `assets/png/` and `assets/logos/firecrawl-logo.svg` in the folder (they are not in this repo). Then look at stills before rendering everything:

```sh
node scripts/render.mjs . --times 2,10,20,30,40 --out stills
```

Read the images and fix overlaps, clipped text and dead scenes. The phone screen is small: text must be big.

## 4. Build

```sh
node scripts/render.mjs . --sub 2 --out frames      # frames, events.json, scene_times.json
uv run scripts/sfx.py events.json <seconds> sfx.wav scene_times.json
uv run scripts/music.py music.mp3 "<prompt>"         # calm, sparse, no drops, leaves room for a voice
sh scripts/compose.sh .                              # short.mp4
```

Music costs a few cents and is optional; reuse an existing `music.mp3` when redoing a cut. Do not delete old frames folders without asking.

## 5. Report

Give the path, length and loudness. Say plainly that you cannot hear the audio and the user should listen. Remind them to set YouTube's altered or synthetic content label if the voice is cloned, and that under 60 seconds counts as a Short. Never push or commit anything for the user's channel folder.
