---
name: plugin-roundup-beacon
scope: org:firecrawl
default_scope: org:firecrawl
metadata:
  version: "0.1.0"
description: Make a vertical 1080 x 1920 "Stop using X without these 5 plugins" roundup video (about 45 s) in Beacon, in the Firecrawl look - hook, five numbered full-page colour scenes with a typed prompt and an illustrative result, a Firecrawl scene at a varying position, Fish Audio voice, a different Epidemic Sound track per video and no sound effects. A script builds the layers, voice timing, checks and Beacon batch files; the agent submits them through the Beacon MCP. Use when asked for another video in the plugins, connectors, skills, extensions or apps roundup series (Copilot, Codex, Cursor, Hermes, Gemini, OpenClaw and so on), to swap a tool in one, or to fix its hook, voice or music. For the older HyperFrames one-file Reel with sound effects use chatgpt-plugins-reel.
---

# plugin-roundup-beacon

One video is one folder holding a `cfg.mjs`. The scripts in `scripts/` turn it into PNG layers, voice-line texts, checked timing and Beacon transactions; you do the judgment steps and run the MCP calls (Beacon, Fish Audio, Epidemic Sound and Firecrawl are MCP tools, so no script can call them). `example/` is a finished config (Gemini CLI) to copy.

## What you need

- Node 22 or newer, ffmpeg, ffprobe and `agent-browser` on the path.
- The Beacon MCP with the project open (`project_open` with the `.beproj` path; do it again after any session resume, or calls fail with "no project open"). Fish Audio, Epidemic Sound and Firecrawl MCPs for voice, music and the Alexandria check.
- A Beacon project with a Voice audio track and a Music audio track; read their ids from `project_describe`.

## Standing rules

- **Firecrawl is in every video**, at position 1 to 5, and the position varies from video to video. It is always described as "The knowledge library for your agent. Live data on people, emails, jobs and more." Never say or show the word "Alexandria".
- **No tool that is an Alexandria provider** (it overlaps what Firecrawl already offers, and reads badly next to it). `check.mjs` enforces it. Vercel was accepted once by the owner; anything else needs a swap.
- **Two spoken sentences per other tool**, a different typed prompt per video, and any made-up app content in the result window labelled "Illustrative".
- **Number scenes fill the whole 1080 x 1920 page with colour.** No "?" slot row shows during them.
- **No counter pill, tag or top-left header.**
- **Voice:** Fish Audio Sarah (`933563129e564b19a115bedd57b7406a`), model `drama-3`, tag `[warm, upbeat, like telling a friend]`, `<emphasis>` on the name.
- **Music:** Epidemic Sound, instrumental, a different track from every earlier video, clip volume 0.15. **No sound effects at all.**
- **Export at speed 1.2**, 1080 x 1920.

## Workflow

Run scripts as `node scripts/<name>.mjs <video-dir> ...` (paths relative to this skill).

1. **Pick the tools (judgment).** Four real connectors, plugins, extensions or apps for the harness, from different categories, each with a recognisable logo (simple-icons, or an Alexandria provider icon). Choose where Firecrawl goes, and read the positions the other videos used.
2. **Write `cfg.mjs`.** Copy `example/cfg.mjs` into a new folder next to your other videos and edit: `harness`, `hookLogo`, `noun`, `fcPos`, `fcPrompt`, `NAMES` and `L` (always `[Firecrawl, tool1..tool4]`, in that order, not scene order), `subs` (the two sentences per tool, which are also spoken), and `tools[]` with `chip`, a typed `prompt` and the `win` HTML for the result window. Put each tool's logo file in the folder. Optional `say: { "Clinical Trials.gov": "Clinical Trials dot gov" }` fixes how a name is spoken.
3. **Check the tools against Alexandria.** `node scripts/check.mjs <dir> --print-alexandria-command` prints a `ls /library/*/ | grep -iE ...` command. Run it with `alexandria_library_search`, save its stdout to a file, then `node scripts/check.mjs <dir> --alexandria-list <file> --used <positions of earlier videos>`. Fix every FAIL; read each WARN.
4. **Voice.** `node scripts/voices.mjs <dir> lines` writes `lines.json` and lists the lines that need generating (changed text or missing file). For each, call the Fish `text_to_speech` MCP tool with that `text`, the `voice_id` and `model` from the file, and download the mp3 to `voices/vN.mp3`. v6 ("Follow for more plugin suggestions") never changes: copy it from another video. Then `voices.mjs <dir> done` and `voices.mjs <dir> measure`, which writes `voices.json` (the seven durations and the Firecrawl cue shift). Cost is about one Fish credit per byte; check `get_credit_balance` first. Only regenerate what changed.
5. **Render the layers.** `bash scripts/render.sh <dir>` (set `SCENES="s3"` to redo one scene; the hook always re-renders). The hook runs twice so the black bar is sized to the measured "5 noun." text. Open `hook-base.png` and each `sN-base.png`/result layer and look for overlapping text. Then `node scripts/check.mjs <dir> --post`.
6. **Stage and import.** `node scripts/stage.mjs <dir> <prefix>` copies the layers and voices into `<dir>/stage` and writes `import-1.json`, `import-2.json` (36 files each). Call `media_import` for each list with a high `at` (3000 and up) so nothing lands on the section, then `clip_remove` the staging clips (the assets stay). Save every asset id, in import order, to `<dir>/ids.json` and run `node scripts/stage.mjs <dir> --map` to write `assets.json`.
7. **Build the section.** Pick `T0` just after the end of the last video on the timeline. `node scripts/plan.mjs <dir> --t0 <T0> --voice-track <track-id>` writes `plan-1.json`..: submit each as a `transaction` in order, and append the returned ids (the `result` array, in order) to `ids.txt`. Beacon returns only the first 20 ids per transaction, so keep batches at 20 or fewer. Then `node scripts/plan.mjs <dir> --t0 <T0> --anims --music-asset <id> --music-track <track-id>`, and submit `anims.json` as one transaction.
8. **Music.** `SearchRecordings` (instrumental, upbeat, about the video length) and pick a track no earlier video used, `DownloadRecording` (MP3, FULL), `media_import` it at a high `at`, `clip_remove` the staging clip, pass the asset id as `--music-asset` in step 7 and submit `music.json`. Volume goes in `props.audio.volume` (0.15); a top-level `volume` prop is rejected.
9. **Export.** Submit `export.json` to `export_start` (speed 1.2, overwrite true) and wait with `job_status`. Then `node scripts/verify.mjs <video.mp4>`: length, 1080 x 1920, loudness (expect -23 to -20 LUFS) and `<video>-sheet.png`. Open the sheet and look at it, including the hook bar and the Firecrawl scene.

## Changing an existing video

- **Swap a tool:** edit `cfg.mjs`, re-run `voices.mjs lines` (only that line is stale), regenerate it, `measure`, re-render, restage with a new prefix, remove the old section's clips, rebuild at a new `T0`, re-add the music, export. Voice durations shift everything after the swap, so rebuild the whole section.
- **Fix only a layer:** `media_replace` the asset with the new PNG and `clip_set` the clip's `transform.x` and `y` from the new `rects-*.json` (centre `cx = x + w/2 - 540`, `cy = 960 - (y + h/2)`).

## Gotchas

- The hook bar width comes from the text, not from `cfg.barW` (kept only as a first-pass default). A bar that ends far from the text means `render.sh` was skipped after a `noun` change.
- The Firecrawl cue shift comes from the third pause of 0.4 s or more in the Firecrawl voice line, which is where "Live data on people..." starts (4.69 s into the reference line). `measure` warns if it cannot find it.
- Provider-wall logos on the Firecrawl scene are named in `scripts/core.mjs` (`provIcons`). They show what the library covers and are not tools, so Shopify and the like can appear there.
- `zsh` does not word-split variables, so run `emit.mjs` with `$(cat ids.txt)` through `bash -c`.
- The scene timing constants live in `scripts/spec.mjs`; change them there, never per video.
- Rendered PNGs differ by anti-aliasing noise between runs (PSNR 58+ dB); compare `rects-*.json`, not bytes.

## Files

- `scripts/core.mjs` builds the seven pages from `cfg.mjs`; `render.sh` shoots them; `spec.mjs` is the timeline; `emit.mjs` prints clip commands; `plan.mjs` writes the Beacon batches; `check.mjs`, `voices.mjs`, `stage.mjs`, `verify.mjs` as above. `scripts/assets/` holds the fonts, orange Firecrawl logo and provider icons the pages use; `render.sh` copies them into the video folder.
- `example/` is the Gemini CLI config and its logos. Its first-pass check and render are the quickest test that a machine is ready: `cp -R example scratch && bash scripts/render.sh scratch`.
