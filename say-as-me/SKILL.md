---
name: say-as-me
description: Speak a script or line of text in the user's cloned voice and save it as a .wav. Use when the user asks to voice, narrate, record or read something in their voice, or wants the audio for a script just written.
argument-hint: [text, or path to a script]
allowed-tools: Bash(uv run *)
---

Turn text into audio in the user's own cloned voice (Qwen3-TTS on Replicate). Only ever use the user's own voice.

## Before running

The voice sample lives outside this repo, in `~/.config/voice-clone/` (override with `VOICE_CLONE_DIR`): `reference.wav`, a clean 20-30 second clip of the user speaking, and `reference.txt`, its exact transcript. The repo is public, so never copy either file into it or commit them. If the folder is missing, stop and point the user to the README for setup; do not look for other audio to use.

`REPLICATE_API_TOKEN` must be set in the shell.

## Run it

```sh
uv run ~/.claude/skills/say-as-me/scripts/say.py "text or @path/to/script.txt" out.wav [--style "..."] [--speed 0.92]
```

Pass only the words to be spoken. Strip headings, frontmatter and stage directions first, and write them to a temp file if the script is long. Lines without end punctuation (as in shorts scripts) are treated as sentences. Save the audio next to the script unless the user says otherwise.

## Check the result

The command prints duration and words per second. The user's natural pace is about 2.7. Qwen reads fast, and short standalone lines run 3.3-3.5. A style instruction nudges this but is not a reliable dial: in testing, `--style "Speak at a relaxed, natural conversational pace, like explaining something to a friend."` cut a take from 3.46 to 3.08, while "speak slowly" changed nothing. `--speed 0.9` slows the finished audio with a pitch-preserving stretch and is dependable, but below about 0.85 it starts to sound processed. If a take is over about 3.2, rerun with the relaxed style plus `--speed 0.92`, and go down towards 0.85 only if it still runs fast. Report the numbers each time. I cannot hear the audio, so say so, and ask the user to listen before it goes into a video or is published. For a short, tell them if the audio runs past 55 seconds.

A call costs a few cents, so don't regenerate speculatively; one retake is fine, more needs a reason. HTTP 402 means the Replicate balance is empty and only the user can top it up. Transient Replicate errors are retried automatically.

## When the audio will be published

Once per session, remind the user that YouTube asks for the altered or synthetic content label on realistic cloned voices.
