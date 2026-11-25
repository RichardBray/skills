---
name: plugin-roundup-beacon
scope: org:firecrawl
default_scope: org:firecrawl
metadata:
  version: "0.4.0"
description: Make a 1080 x 1920 "Stop using X without these 5 plugins" roundup video in Beacon: Firecrawl look, Fish voice, new Epidemic Sound track each, no sound effects; scripts build layers, checks, voice tightening, one Beacon build script and the motion graphics (3D card intro, private-data padlock). Use for another harness or audience in the series, a tool swap, a test variant, or a hook, voice or music fix. HyperFrames Reel: chatgpt-plugins-reel.
---

# plugin-roundup-beacon

One video is one folder holding a `cfg.ts`. The scripts in `scripts/` turn it into PNG layers, voice-line texts, checked timing, one Beacon build script and two motion-graphic pages; you do the judgment steps and run the MCP calls (Beacon, Fish Audio, Epidemic Sound and Firecrawl are MCP tools, so no script can call them). `example/` is a finished control config (Gemini CLI); `~/fc/videos/plugins-3/chatgpt-marketing` and `chatgpt-jobs` are finished payoff configs, approved by the owner; `chatgpt-business` and `claude-recruiting` are custom-hook configs (burst and desk intros), approved by the owner with no notes.

## What you need

- Bun, ffmpeg, ffprobe and `agent-browser` on the path.
- The Beacon MCP with the project open (`project_open` with the `.beproj` path; do it again after any session resume, or calls fail with "no project open"). Fish Audio, Epidemic Sound and Firecrawl MCPs for voice, music and the Alexandria check.
- A Beacon project with a Voice audio track and a Music audio track; read their ids from `project_describe`.

## Standing rules

- **Firecrawl is in every video**, at position 1 to 5, and the position varies from video to video. On screen it is "The knowledge library for your agent. Private data sources <harness> can't usually reach."; the voice line (`FC_LINE` in `voices.ts`) adds that it gives the harness private data sources it would not usually have access to, then "Live data on people, emails, jobs, and much more. All from one place." Never say or show the word "Alexandria".
- **No tool that is an Alexandria provider** (it overlaps what Firecrawl already offers, and reads badly next to it). `check.ts` enforces it. Vercel was accepted once by the owner; anything else needs a swap.
- **Two spoken sentences per other tool**, a different typed prompt per video, and any made-up app content in a scene's result window labelled "Illustrative". The intro deck carries no label.
- **No dead air.** The voice lines run back to back: each scene ends where its line ends, the hook ends where its speech does, and `voices.ts tighten` trims the pauses inside each line.
- **On "private data sources"** a padlock graphic shows six locked data sources that unlock on "access" (`motion.ts private`), filling the gap before the Firecrawl rows.
- **Number scenes fill the whole 1080 x 1920 page with colour.** No "?" slot row shows during them.
- **No counter pill, tag or top-left header.**
- **Everything sits in the Reels/TikTok safe zone** (x 120-960, y 250-1440): the "?" slot row is at the top, result windows are 840 px wide (so `win` content must fit 840, not 984). `core.ts` holds this layout; check each prompt ends clear of the send button.
- **End card:** the five logo tiles slide in one by one in list order (left column from the left, right column from the right, the last from below).
- **Voice:** Fish Audio Sarah (`933563129e564b19a115bedd57b7406a`), model `drama-3`, tag `[warm, upbeat, like telling a friend]`, `<emphasis>` on the name.
- **Music:** Epidemic Sound, instrumental, a different track from every earlier video, one continuous clip at volume 0.12. **No sound effects at all.**
- **Export at speed 1.2**, 1080 x 1920.

## Workflow

Run scripts as `bun scripts/<name>.ts <video-dir> ...` (paths relative to this skill).

1. **Pick the tools (judgment).** Four real connectors, plugins, extensions or apps for the harness, from different categories, each with a recognisable logo (simple-icons, or an Alexandria provider icon). Choose where Firecrawl goes, and read the positions the other videos used.
2. **Write `cfg.ts`.** Copy a finished config into a new folder next to your other videos and edit: `harness`, `hookLogo`, `noun`, `fcPos`, `fcPrompt`, `NAMES` and `L` (always `[Firecrawl, tool1..tool4]`, in that order, not scene order), `subs` (the two sentences per tool, which are also spoken), and `tools[]` with `chip`, a typed `prompt` and the `win` HTML for the result window. Put each tool's logo file in the folder. Optional `say: { "Clinical Trials.gov": "Clinical Trials dot gov" }` fixes how a name is spoken. For the payoff variant add `variant: 'payoff'` and `intro` (see Variants).
3. **Check the tools against Alexandria.** `bun scripts/check.ts <dir> --print-alexandria-command` prints a `ls /library/*/ | grep -iE ...` command. Run it with `alexandria_library_search`, save its stdout to a file, then `bun scripts/check.ts <dir> --alexandria-list <file> --used <positions of the last few videos>`. Fix every FAIL; read each WARN.
4. **Voice.** `bun scripts/voices.ts <dir> lines` writes `lines.json` and lists the lines that need generating (changed text or missing file). For each, call the Fish `text_to_speech` MCP tool with that `text`, the `voice_id` and `model` from the file, and download the mp3 to `voices/vN.mp3`. v6 ("Follow for more plugin suggestions") never changes: copy it from another video's `voices/v6.raw.mp3` (or `v6.mp3`). Cost is about one Fish credit per byte; check `get_credit_balance` first, and only regenerate what changed. Then `voices.ts <dir> done`, `voices.ts <dir> tighten` (v1-v5 lose their lead-in to 0.05 s, tail to 0.15 s and every pause to 0.3 s, v6 its lead-in and tail; the takes are kept as `vN.raw.mp3`; the hook is never touched because its words are timed to it) and `voices.ts <dir> measure`, which writes `voices.json`: the durations, where the hook's speech ends and the Firecrawl cue.
5. **Render the layers.** `bun scripts/render.ts <dir>` (set `SCENES="s3"` to redo one scene; the hook always re-renders). The hook runs twice so the black bar is sized to the measured "5 noun." text. Look at every page as a whole (all layers shown) for overlapping text, and measure each prompt against its send button. Then `bun scripts/check.ts <dir> --post`.
6. **Music.** `SearchRecordings` (instrumental, upbeat, about the video length) and pick a track no earlier video used, `DownloadRecording` (MP3, FULL) into `<dir>/music/`.
7. **Stage and import.** `bun scripts/stage.ts <dir> <prefix>` copies the layers and voices into `<dir>/stage` and writes `import-1.json`, `import-2.json` (36 files each). Call `media_import` for each list, adding the music file to the last, with a high `at` (3000 and up) so nothing lands on the section, then remove every clip from 2999 on with one `script` (the assets stay). Save the layer and voice asset ids, in import order and without the music's, to `<dir>/ids.json` and run `bun scripts/stage.ts <dir> --map` to write `assets.json`.
8. **Build the section.** Pick `T0` just after the end of the last video on the timeline. `bun scripts/plan.ts <dir> --t0 <T0> --voice-track <id> --music-asset <id> --music-track <id>` writes `build.js`: run its whole text with the Beacon `script` tool (`seconds: 30`). It adds the music first, then every clip and animation, in one undo step. Add `--section <id> --name <name>` (from `project_describe`) and it sets the section too; a custom hook names the export after its first sentence.
9. **Motion graphics.** For the custom variant: save Fish `speech_to_text` (with timestamps) of `voices/v0.mp3` as `<dir>/hook-words.json` (Beacon's transcript times run up to 0.4 s late, so not those), run `bun scripts/motion.ts <dir> hook`, then `motion_add` at `T0` for the printed length and `motion_code` with the text of `motion-hook.html`. For the payoff variant: `bun scripts/motion.ts <dir> intro`, then `motion_add` at `T0` for the printed length and `motion_code` with the text of `motion-intro.html`. For every video: `transcript_get` with `find: "private data sources"` and `find: "have access to"` (format `words`), then `bun scripts/motion.ts <dir> private --t0 <T0> --private <time of "private"> --access <time of "access">`, `motion_add` at the printed start and length, `motion_code` with `motion-private.html`. Each draw is a job: `job_status` with `wait`, then look at frames across it.
10. **Export.** Look at a `frames_sheet` of the whole section, then submit `export.json` to `export_start` (speed 1.2, overwrite true) and wait with `job_status`. Then `bun scripts/verify.ts <video.mp4>`: length, 1080 x 1920, loudness (expect -23 to -20 LUFS) and `<video>-sheet.png`. Open the sheet and look at it.

## Variants

`cfg.variant` picks the opening, for testing what holds viewers. Everything after the hook stays the same.

- `control` (default): the five "?" tiles.
- `payoff`: a 3D deck of three result cards is dealt in from the first frame (spin from depth, shockwave, count-up, chips popping), sways under the hook and whips away as it ends. Use the video's most impressive result, usually Firecrawl's. `cfg.intro` sets it: `icon` (an .svg or .png in the folder: the topic's own icon, such as the Meta logo for ads or a briefcase for jobs, never the Firecrawl logo), `accent`, `soft` and `ink` (count, chip background and chip text colours, in the topic's colours), optional `pill` (the header pill, default `#111`), `count`, `label` ("active Meta ads") and three `cards` of `[title, subtitle, chip]`.
- `custom`: a new spoken hook (`cfg.hookLine`, with `<emphasis>` tags) and a motion intro over a blank hook page, from `cfg.hook` (see `Hook` in `scripts/lib.ts`). The hook runs to where its speech ends plus 0.4 s, and every word lands as it is spoken. Research and log the hook in `references/hooks.md` first. Two styles, both ending on the regular "?" slot row so the cut to number card 1 matches the other variants:
  - `burst` (`chatgpt-business`): words slam in, a highlighter hits `mark`, 30 emoji app tiles explode and shrink to five as the closing `bar` sweeps in. Suits "you don't need all of them, just these".
  - `desk` (`claude-recruiting`): line 1 types out after the logo, line 2 slams in with `mark` in the accent, a stack of `cards` is dealt and the first is stamped (`stamp`), the other lines rise in, five `tiles` drop and the bar sweeps in. Suits "<harness> can now <job>", with cards from the job's world.
  Give each video its own `accent` (the harness or topic colour) and `second`. For a new style, copy a template in `scripts/motion/` and keep its data contract.

## Changing an existing video

- **Swap a tool:** edit `cfg.ts`, re-run `voices.ts lines` (only that line is stale), regenerate it, `done`, `tighten`, `measure`, re-render, restage with a new prefix, remove the old section's clips (motion clips too: a rebuild doesn't keep them), rebuild at a new `T0`, redo the motion graphics, export.
- **Fix only a layer:** copy the new PNG under a new name, `media_replace` the asset with it, and `clip_set` the clip's `transform.x` and `y` from the new `rects-*.json` (centre `cx = x + w/2 - 540`, `cy = 960 - (y + h/2)`). A prompt's cover and cursor also need their `transform.x` animations redone.
- **Edits made by hand in Beacon** (ripple cuts) split the music into pieces that jump: replace them with one continuous music clip before exporting.

## Gotchas

- A long noun ("marketing plugins") is shrunk with the number so the bar ends inside the frame; `render.ts` does it from its first pass.
- `media_replace` with the same path keeps showing the cached image: copy the new file under a new name first.
- `clip_add` without a track puts an image on the lowest free track, the music track included, so the music must be added before the images (`build.js` does).
- Motion graphics: Beacon draws half-transparent pixels light, so soft shadows turn into white halos and tinted fills go pale. Give the part of the page behind the graphic a solid `#f9f9f9` floor. The page loads nothing from outside (no CDN, no external images): Beacon inlines GSAP 3.15 and Three.js when the HTML uses them, and images must be data URIs. Keep 3D spins under 90 degrees: past that the card's text shows mirrored, `backface-visibility` notwithstanding.
- Motion pages: Beacon gives every `.w` and `.in` element its own CSS word-in animation, which overrides GSAP, so name word classes something else (`.wd`). Its renderer draws the page's first frame (t = 0) without GSAP's from-states, so everything shows finished for one frame: hide the scene in `window.__frame = t => ...` while `t < 0.02` (both templates do). Installed fonts work by name (`"Suisse Intl"`), which keeps a page small enough to paste into `motion_code`.
- `check.ts --used` takes the positions of the last few videos only; after ten videos every position has been used.
- The hook bar width comes from the text, not from `cfg.barW` (kept only as a first-pass default). A bar that ends far from the text means `render.ts` was skipped after a `noun` change.
- The Firecrawl cue comes from the `FC_CUE_PAUSE`-th pause of 0.4 s or more in the untrimmed Firecrawl take (4 now), which is where "Live data on people..." starts, carried across `tighten`'s cuts by `vN.map.json`. `measure` prints every long pause; if `FC_LINE` gains or loses a sentence before "Live data", change `FC_CUE_PAUSE`. Keep "All from one place." at the end, or the provider wall is cut after about a second.
- Provider-wall logos on the Firecrawl scene are named in `scripts/core.ts` (`provIcons`). They show what the library covers and are not tools, so Shopify and the like can appear there.
- The scene timing constants live in `scripts/spec.ts`; change them there, never per video.
- Rendered PNGs differ by anti-aliasing noise between runs (PSNR 58+ dB); compare `rects-*.json`, not bytes.

## Files

- `scripts/core.ts` builds the seven pages from `cfg.ts`; `render.ts` shoots them; `spec.ts` is the timeline; `plan.ts` writes `build.js` and `export.json`; `motion.ts` fills `scripts/motion/intro.html` and `private.html`; `check.ts`, `voices.ts`, `stage.ts`, `verify.ts` as above; `emit.ts` prints single clip commands for repairs. `scripts/assets/` holds the fonts, orange Firecrawl logo and provider icons the pages use; `render.ts` copies them into the video folder.
- `example/` is the Gemini CLI config and its logos. Its first-pass check and render are the quickest test that a machine is ready: `cp -R example scratch && bun scripts/render.ts scratch`.
