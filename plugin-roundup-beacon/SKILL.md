---
name: plugin-roundup-beacon
scope: org:firecrawl
default_scope: org:firecrawl
metadata:
  version: "0.1.0"
description: Make a 1080 x 1920 "Stop using X without these 5 plugins" roundup video in Beacon: Firecrawl look, Fish voice, new Epidemic Sound track each, no sound effects; scripts build layers, checks, Beacon batches. Use for another harness in the series, a tool swap, or a hook, voice or music fix. HyperFrames Reel: chatgpt-plugins-reel.
---

# plugin-roundup-beacon

One video is one folder holding a `cfg.ts`. The scripts in `scripts/` turn it into PNG layers, voice-line texts, checked timing and Beacon transactions; you do the judgment steps and run the MCP calls (Beacon, Fish Audio, Epidemic Sound and Firecrawl are MCP tools, so no script can call them). `example/` is a finished config (Gemini CLI) to copy.

## What you need

- Bun, ffmpeg, ffprobe and `agent-browser` on the path.
- The Beacon MCP with the project open (`project_open` with the `.beproj` path; do it again after any session resume, or calls fail with "no project open"). Fish Audio, Epidemic Sound and Firecrawl MCPs for voice, music and the Alexandria check.
- A Beacon project with a Voice audio track and a Music audio track; read their ids from `project_describe`.

## Standing rules

- **Firecrawl is in every video**, at position 1 to 5, and the position varies from video to video. On screen it is "The knowledge library for your agent. Private data sources <harness> can't usually reach."; the voice line (`FC_LINE` in `voices.ts`) adds that it gives the harness private data sources it would not usually have access to, then "Live data on people, emails, jobs, and much more. All from one place." Never say or show the word "Alexandria".
- **No tool that is an Alexandria provider** (it overlaps what Firecrawl already offers, and reads badly next to it). `check.ts` enforces it. Vercel was accepted once by the owner; anything else needs a swap.
- **Two spoken sentences per other tool**, a different typed prompt per video, and any made-up app content in the result window labelled "Illustrative".
- **Number scenes fill the whole 1080 x 1920 page with colour.** No "?" slot row shows during them.
- **No counter pill, tag or top-left header.**
- **Everything sits in the Reels/TikTok safe zone** (x 120-960, y 250-1440): the "?" slot row is at the top, result windows are 840 px wide (so `win` content must fit 840, not 984). `core.ts` holds this layout; check each prompt ends clear of the send button.
- **Voice:** Fish Audio Sarah (`933563129e564b19a115bedd57b7406a`), model `drama-3`, tag `[warm, upbeat, like telling a friend]`, `<emphasis>` on the name.
- **Music:** Epidemic Sound, instrumental, a different track from every earlier video, clip volume 0.15. **No sound effects at all.**
- **Export at speed 1.2**, 1080 x 1920.

## Workflow

Run scripts as `bun scripts/<name>.ts <video-dir> ...` (paths relative to this skill).

1. **Pick the tools (judgment).** Four real connectors, plugins, extensions or apps for the harness, from different categories, each with a recognisable logo (simple-icons, or an Alexandria provider icon). Choose where Firecrawl goes, and read the positions the other videos used.
2. **Write `cfg.ts`.** Copy `example/cfg.ts` into a new folder next to your other videos and edit: `harness`, `hookLogo`, `noun`, `fcPos`, `fcPrompt`, `NAMES` and `L` (always `[Firecrawl, tool1..tool4]`, in that order, not scene order), `subs` (the two sentences per tool, which are also spoken), and `tools[]` with `chip`, a typed `prompt` and the `win` HTML for the result window. Put each tool's logo file in the folder. Optional `say: { "Clinical Trials.gov": "Clinical Trials dot gov" }` fixes how a name is spoken.
3. **Check the tools against Alexandria.** `bun scripts/check.ts <dir> --print-alexandria-command` prints a `ls /library/*/ | grep -iE ...` command. Run it with `alexandria_library_search`, save its stdout to a file, then `bun scripts/check.ts <dir> --alexandria-list <file> --used <positions of earlier videos>`. Fix every FAIL; read each WARN.
4. **Voice.** `bun scripts/voices.ts <dir> lines` writes `lines.json` and lists the lines that need generating (changed text or missing file). For each, call the Fish `text_to_speech` MCP tool with that `text`, the `voice_id` and `model` from the file, and download the mp3 to `voices/vN.mp3`. v6 ("Follow for more plugin suggestions") never changes: copy it from another video. Then `voices.ts <dir> done` and `voices.ts <dir> measure`, which writes `voices.json` (the seven durations and the Firecrawl cue shift). Cost is about one Fish credit per byte; check `get_credit_balance` first. Only regenerate what changed.
5. **Render the layers.** `bun scripts/render.ts <dir>` (set `SCENES="s3"` to redo one scene; the hook always re-renders). The hook runs twice so the black bar is sized to the measured "5 noun." text. Open `hook-base.png` and each `sN-base.png`/result layer and look for overlapping text. Then `bun scripts/check.ts <dir> --post`.
6. **Stage and import.** `bun scripts/stage.ts <dir> <prefix>` copies the layers and voices into `<dir>/stage` and writes `import-1.json`, `import-2.json` (36 files each). Call `media_import` for each list with a high `at` (3000 and up) so nothing lands on the section, then `clip_remove` the staging clips (the assets stay). Save every asset id, in import order, to `<dir>/ids.json` and run `bun scripts/stage.ts <dir> --map` to write `assets.json`.
7. **Build the section.** Pick `T0` just after the end of the last video on the timeline. `bun scripts/plan.ts <dir> --t0 <T0> --voice-track <track-id>` writes `plan-1.json`..: submit each as a `transaction` in order, and append the returned ids (the `result` array, in order) to `ids.txt`. Beacon returns only the first 20 ids per transaction, so keep batches at 20 or fewer. Then `bun scripts/plan.ts <dir> --t0 <T0> --anims --music-asset <id> --music-track <track-id>`, and submit `anims.json` as one transaction.
8. **Music.** `SearchRecordings` (instrumental, upbeat, about the video length) and pick a track no earlier video used, `DownloadRecording` (MP3, FULL), `media_import` it at a high `at`, `clip_remove` the staging clip, pass the asset id as `--music-asset` in step 7 and submit `music.json`. Volume goes in `props.audio.volume` (0.15); a top-level `volume` prop is rejected.
9. **Export.** Submit `export.json` to `export_start` (speed 1.2, overwrite true) and wait with `job_status`. Then `bun scripts/verify.ts <video.mp4>`: length, 1080 x 1920, loudness (expect -23 to -20 LUFS) and `<video>-sheet.png`. Open the sheet and look at it, including the hook bar and the Firecrawl scene.

## Changing an existing video

- **Swap a tool:** edit `cfg.ts`, re-run `voices.ts lines` (only that line is stale), regenerate it, `measure`, re-render, restage with a new prefix, remove the old section's clips, rebuild at a new `T0`, re-add the music, export. Voice durations shift everything after the swap, so rebuild the whole section.
- **Fix only a layer:** `media_replace` the asset with the new PNG and `clip_set` the clip's `transform.x` and `y` from the new `rects-*.json` (centre `cx = x + w/2 - 540`, `cy = 960 - (y + h/2)`).

## Gotchas

- A long noun ("marketing plugins") is shrunk with the number so the bar ends inside the frame; `render.ts` does it from its first pass.
- `media_replace` with the same path keeps showing the cached image: copy the new PNG under a new name first.
- `check.ts --used` takes the positions of the last few videos only; after ten videos every position has been used.
- The hook bar width comes from the text, not from `cfg.barW` (kept only as a first-pass default). A bar that ends far from the text means `render.ts` was skipped after a `noun` change.
- The Firecrawl cue shift comes from the `FC_CUE_PAUSE`-th pause of 0.4 s or more in the Firecrawl voice line (4 now), which is where "Live data on people..." starts (4.69 s into the reference line). `measure` prints every long pause; if `FC_LINE` gains or loses a sentence before "Live data", change `FC_CUE_PAUSE`. Keep "All from one place." at the end, or the provider wall is cut after about a second.
- Provider-wall logos on the Firecrawl scene are named in `scripts/core.ts` (`provIcons`). They show what the library covers and are not tools, so Shopify and the like can appear there.
- `zsh` does not word-split variables, so pass ids to `emit.ts` through `bash -c` with `$(cat ids.txt)`.
- The scene timing constants live in `scripts/spec.ts`; change them there, never per video.
- Rendered PNGs differ by anti-aliasing noise between runs (PSNR 58+ dB); compare `rects-*.json`, not bytes.

## Files

- `scripts/core.ts` builds the seven pages from `cfg.ts`; `render.ts` shoots them; `spec.ts` is the timeline; `emit.ts` prints clip commands; `plan.ts` writes the Beacon batches; `check.ts`, `voices.ts`, `stage.ts`, `verify.ts` as above. `scripts/assets/` holds the fonts, orange Firecrawl logo and provider icons the pages use; `render.ts` copies them into the video folder.
- `example/` is the Gemini CLI config and its logos. Its first-pass check and render are the quickest test that a machine is ready: `cp -R example scratch && bun scripts/render.ts scratch`.
