---
name: workflow-explainer-beacon
scope: org:firecrawl
default_scope: org:firecrawl
metadata:
  version: "0.1.0"
description: Make a 1080 x 1920 "do X with Claude in 5 steps" video in Beacon that runs one Firecrawl Alexandria workflow skill on real data - paper-and-ink cards, question-mark step tabs, Fish voice, pixel-art guide, SFX, jingle. Use for a new workflow video, a script, voice, SFX or character change, or a re-export. For the five-plugin roundup series use plugin-roundup-beacon.
---

# workflow-explainer-beacon

One video walks a viewer through one Alexandria workflow skill, run for real, in five steps: **Setup, Ask, then three result steps, ending on a payoff.** First one made: "Stop using LinkedIn to find your next job" (freshly funded hiring shortlist). The working files are in `example/` (`gen/` generator, `char/` sprite scripts, `voice/` takes, `beacon/` placement script). The full project lives in `~/fc/videos/jobs-hunt/` (`jobs-hunt-v6.beproj`, exports v1 to v8).

Videos in the series so far, all in `jobs-hunt-v6.beproj` one after another, each exported on its own range:

| Video | Folder | Timeline | Music |
|---|---|---|---|
| Find your next job (LinkedIn) | `jobs-hunt/` | 0 to 30 s | Reaching Out (Dovetail) |
| Find creators (Instagram) | `jobs-hunt/creators/` | 60 to 96.6 s | `creators/music.mp3` |
| Used car (dealer's price) | `jobs-hunt/car/` (`script.md`, `data.md`) | 110 to 146.7 s | Cheetah Print (Cushy, `f031ac3b-1858-424a-9890-a2ba10487daf`) |
| Winning funnel teardown (Comfrt) | `jobs-hunt/funnel/` | 160 to 197.5 s | Keep Your Focus on Me, instrumental (Basixx, `66ac3725-ba78-4559-81e5-4e1db6663eba`) |
| Hook swipe file (pet supplies) | `jobs-hunt/hooks/` | 210 to 249.4 s | Out of Order (The Fly Guy Five, `9ef318f2-2fd7-42db-9785-b8d3b8214f59`) |

| Sports card buy-low (Trevor Lawrence), **Grok** | `jobs-hunt/cards/` | 260 to 294.4 s | Liberty City (DonVayei, `34b72f66-f0d1-4298-9a54-0d717f322d67`) |
| Offer salary benchmark (software engineer, Chicago), **Grok** | `jobs-hunt/salary/` | 300 to 333.7 s | Moving Up (Origo, `72ead9c2-60c5-4e9f-9f5d-bbdb4aeaaca3`) |
| Interview prep pack (Duolingo Senior PM, Growth), **Grok** | `jobs-hunt/interview/` | 345 to 384.2 s | STYLE (Ballpoint, `03e71f7f-ad6f-4845-9fbd-9fce110cfa5e`) |

Salary benchmark notes: ZipRecruiter `salary` 502s for some titles ("software engineer") but works for others ("software developer"); its `search_jobs` failed every time, so take live posted pay from Firecrawl `jobs_search` (Indeed plus employer boards; most rows unverified) and report the median range midpoint of non-senior rows. BLS OEWS series ids can be built by hand (`OEUM` + 7-digit MSA + `000000` + SOC without the dash + datatype 04 mean, 12 25th, 13 median, 14 75th); pick a title with a clean SOC match (software developers 15-1252; "data analyst" has none). Age BLS with CPIAUCSL levels from FRED. Label the offer on screen as an example.

Interview prep notes: Benzinga news needs a paid plan, so use `firecrawl_search` with `sources: ["news"]`. Particle podcast mentions by `company_id` with `role: guest` can return nothing; search by the executive's person slug instead (`entity_id`, e.g. `luis-von-ahn`). Fiscal.ai transcripts come with speaker names and timestamps; flatten them to a text file and grep for the role's metric. Keep breaking leadership news out of the video and in the prep notes.

Reviewer feedback (18 Nov 2026): "good new angles", but the voice and music were distracting. What people would resonate with most is repeated "top 3 Claude connectors / top 3 ChatGPT plugins" videos: swap tools 1 and 3 each time, keep Firecrawl as tool 2 with a bigger middle mention (about 5 s per other tool, 10 s for Firecrawl). That format belongs in `plugin-roundup-beacon` (cut to 3 tools), not this skill; this skill's workflow videos are the "new angles".

Researched but not built (owner said no): fantasy football start or sit, in ChatGPT (`jobs-hunt/fantasy/`, Week 11 data, stale after 22 Nov 2026).

Sports card buy-low notes: PSA's public football price guide stops at 2021 (and only some 2021 sets list rookies), so pick a 2020 or 2021 rookie. Check several players' ESPN seasons first; the cheap cards marked "down" usually belong to declining players. The buy-low case is a player whose stats jumped while his base rookie card has no change marker; a peer whose cards are already marked up makes a good "hold". Every 2021 sealed box at Steel City was sold out. Each call costs 5 credits. On screen say "guide value", not "sells for", and add "Not financial advice".

Ideas: Alexandria has about 250 skills (`ls /library/skills/firecrawl`, descriptions in `/library/skills/INDEX`), mostly for businesses. The consumer and side-hustle ones that fit this format: used car, offer salary benchmark, startup offer runway check, interview prep pack, campsite booking, fantasy football start or sit, sports card buy-low screen, Turo host fleet pick, and for online sellers winning funnel teardown and hook swipe file. There is no dropshipping or consumer coupon skill; the owner wants existing skills only, not new team skills.

Start a new video from the newest folder's `gen/build.mjs` (`example/gen/build-car.mjs` is the latest copy): it has the prompt highlight, the tab cell and the DY offsets the older `example/gen/build.mjs` lacks.

## What you need

- Beacon MCP with the project open (`project_open` with the `.beproj` path; again after any session resume).
- Fish Audio MCP **on a paid plan** (see Voice), Epidemic Sound MCP, Firecrawl CLI/MCP for Alexandria.
- `agent-browser`, `ffmpeg`, `ffprobe`, `node` and Python with Pillow.
- Brand files beside the generator: `SuisseIntl-400.woff2`, `SuisseIntl-500.woff2`, `GeistMono-Variable.woff2` (copy from `~/fc/videos/jobs-hunt/`; not stored in the skill), plus `claude.svg` and `logo-orange.svg` (in `example/`).

## Steps

1. **Pick the workflow.** `firecrawl find-tools` or `alexandria_library_search`, read the skill and provider contracts, then **run it for real** and keep the numbers you show (names, amounts, counts). Anything inferred (for example "0 open jobs" from guessed board names) is an inference; keep the on-screen claim to what the run returned, and say so to the owner. Save each run's raw results and a `data.md` next to the `script.md`.
   - Check prices first (`firecrawl_find_tools` with `includeCosts: true`) and ask the owner before an expensive step. Upspring is cheap (50 a page, 100 an ad or a brand lookup). Similarweb charges per row returned: 550 per channel, 330 per referrer, 110 per metric, so the funnel teardown's traffic half cost about 4,700 credits.
   - Similarweb with `country: "us"` returned 502 on every call (not charged); `ww` worked. Say on screen that the figures are worldwide.
   - Large results land in a file: copy it into the video folder (`raw/`) and read it with `jq`.
   - The assistant varies per video (Claude, ChatGPT or Grok; the owner picks). It changes the hook and setup lines, the setup card and the prompt card; with Claude, reuse the setup take. For Grok the setup says "app" and the prompt card uses a plain ink "G" tile, not the Grok logo (`example/gen/build-cards.mjs`). `example/gen/grok-common.part` holds the shared Grok helpers (hook card, setup scene, ask scene with the skill wipe and 2 to 4 source cards, sticker); build a video as `head.part + grok-common.part + mid.part + tail.part`, and reuse one Grok setup take ("Add the Firecrawl app to Grok.", `cards/voices/t_setup.mp3`). Long stickers (more than about 12 characters) need a left of about 520 px to stay inside the 960 px safe edge.
2. **Script it** (see Script shape). Show the script to the owner before spending voice credits.
3. **Voice.** Record each line as its own take. Check lengths with `silencedetect` to time the reveals.
4. **Build layers.** Copy `example/gen/` to a new folder, edit `build.mjs`, run `render.sh`. It writes `s{i}.html`, `s{i}-base.png`, one transparent PNG per `data-layer` (`s{i}-{id}.png`), `rects-s{i}.json` and `scenes.json`.
5. **Build the Beacon project** (see Beacon). Check frames with `frame_at` (at least the hook, one middle step and the end), then export at 1.0x.
6. **SFX, character, jingle**, then export and `open -R` the file.

## Script shape

Hook (voice names no Alexandria): "Stop using X to <outcome>. Claude finds it <hook>. Five steps."
1. Setup: "Add the Firecrawl plugin to Claude." (say plugin for ChatGPT, apps for Grok, connector for Claude desktop if the owner asks; the owner finds "official connector" too stiff.)
2. Ask: names the skill ("Then tell it: use the <skill name> skill.") and the result cards.
3. to 4. One idea per step with a visible result (counts, people).
5. Payoff (ranked shortlist) plus "Follow for more."

Rules: **mention Firecrawl Alexandria from step 1 on screen, never in the hook.** Name the skill out loud. Voice lines are short and spoken, not official. No step numbers in the voice; the big numerals carry them. No captions. Keep text on screen to one short idea per scene.

## Look

- Paper `#efe9dd` with dot grid, 4 px ink borders, hard offset shadows, orange `#fa5d19`, green and red for results. **Stickers and pills are orange `#fa5d19` with white text**; the owner asked to replace every pink (`#ff6fa8`) with dark text. The pink-to-orange gradient icon tiles have white text and stay. The `.stk` class in `example/gen/*.mjs` is already orange. To recolor a layer already in a project, `example/gen/recolor-pink.sh <folder> <scene> <layer>` re-renders it as `s<scene>-<layer>-orange.png`, then `media_replace` the asset with that new file: every clip keeps its place, timing and animation.
- Tab bar at the top: five cells showing **"?"**; the current cell reveals its label with a pop layer (`tab`), finished cells keep their label. The `tab` layer is `fixed` so the per-scene vertical offset (`DY`) is not applied.
- Safe area (Instagram and TikTok): x 120 to 960, y 250 to 1440; keep key content there. The tab bar sits just above it by design.
- To animate a highlight (marker wipe) split the card into a plain card plus a transparent `hl` layer that has only the highlight, then animate `crop.right` from the layer width to 0 (`clip_set` crop right first, then `animation_add` `to: {"crop.right": 0}`). The `hlmode` class in the generator draws that layer. A highlight that wraps onto two lines needs `box-decoration-break: clone` on the span; the wipe then reveals both lines together, which reads fine. Any card can get one (the car video wipes the skill name in Ask and "0 accidents" in Listing).
- No real photos of the subject (a dealer's listing photo can show the dealer's name, and downloading one counts as fetching media): draw it as an inline SVG in the generator (the car video's orange SUV), and show data providers as text cards (name plus what each one returned), not logos.
- Check the scenes at full size before importing: open each `s{i}.html` with `agent-browser` at 1080 x 1920, screenshot and `hstack` them into one sheet. Long headlines overflow the 840 px card at 84 px (the car hook needed 66 px), and stickers placed high cover the step heading.

## Voice

- **Voice is being re-chosen (Nov 2026).** A reviewer found Friendly Young Female and the music distracting and preferred "the voice we used before". The owner moved the first three videos (jobs, creators, car) to **Explainer** (`3e8a237e7b5d4eaab50bd9e05053d70e`, model `drama-3`, same tag) and sent the reviewer a shortlist page: https://claude.ai/artifact/1DTYYNi8mqbg76pVEGdeC6 (12 voices, all reading the same top-3 line; files in `jobs-hunt/voice-picker/`). Use the voice they pick; until then ask which voice before recording.
- Voice history, so you don't re-suggest a rejected one: Slax (`c5f56a6c…`) was the first try and was called "horrible". Explainer was next. Friendly Young Female (`1b1286fcf2f44d8ba1405e0b71abca22`, tag `[casual, natural, like talking to a friend]`) voiced the next nine videos. Sarah (`933563129e564b19a115bedd57b7406a`) is the plugin-roundup voice. Energetic Crowd and Slax were removed from the shortlist.
- Past sessions are searchable: `grep -rhoE 'voice_id\\?":\s*\\?"[0-9a-f]{32}' ~/.claude-work/projects` counts every Fish voice used, and the session `.jsonl` files hold the exact `text_to_speech` texts (for re-voicing a video word for word).
- To re-voice a finished video: regenerate every line with the same text and tag, trim the tails, check each take fits the gap before the next line (speed up with `atempo` only if it overruns, at most about 8%), import, then remove the old voice clips and add the new ones at the same starts in one `script`.
- **Needs the Plus plan** for commercial use and credits (the free plan's terms say non-commercial, and the MCP only bills package credits; pay-as-you-go API credit is a separate balance the MCP does not spend). 1 credit per UTF-8 byte; a line costs about 80 to 130.
- `output_path` does not save files: download each take from the returned `audio_url` with `curl`. Never re-call a line (it is charged again).
- Trim the tail silence of each take (`-t` with a 0.06 s fade) and use that length as the voice clip.
- Reuse a take when the line is word for word the same: "Add the Firecrawl plugin to Claude." is `creators/voices/t_setup.mp3` (2.5 s).
- Time the reveals from the pauses: `silencedetect=n=-35dB:d=0.1` on the trimmed take finds the gaps between sentences. Inside one sentence, estimate words by position. After placing, `transcript_get` on the range gives word times on the timeline.
- **No gaps between voice lines.** The owner wants each line to follow the last one directly, and every reveal (sticker, card, badge, chime) to land on the words it belongs to, such as "5 STEPS" on "Five steps". Make each scene as long as its line, and put any reveal that would sit in a pause inside the line instead. To tighten a finished video: first `clip_move` every reveal that starts inside a gap onto its words (otherwise the cut deletes it, or leaves a sliver under 0.5 s that gets removed), then one `timeline_rippleDelete` with all the gaps (`exact: true`), then replace the cut-up music with one continuous clip from `mediaStart` 0. Everything later on the timeline moves left by the total cut, sections included.
- Reusing old audio: cut with `ffmpeg -ss/-t` from the pauses `silencedetect` finds; write through wav then mp3 to avoid encoder errors.

## SFX and jingle (Epidemic Sound, volume 0.4 to 0.5, music 0.075)

The reviewer found the music distracting, so the music bed is 0.075 (it was 0.15). Every video in `jobs-hunt-v6.beproj` was halved to 0.075.

- Pop on every card, tab and step reveal: "User Interface, Click, UI Buttons, Bubbly, Select" (`7cce069c-4a3a-4746-b5c8-94a653fab587`).
- Swish on hook cards, stickers and the character: "Swooshes, Swish, Stick, Fast Swipe Through Air 02" (`66d23571-4b85-49e4-a0e0-4966a6d60034`).
- Chime on the key result: "User Interface, Misc, Completions, Melodic, Success" (`aaa20ea0-8cdc-4c8f-991b-c58a94c0d130`).
- Marker for the highlight wipe: "Marker Pen, Scribble On Cardboard Sheet, Short" (`e55a339f-f8dd-4143-b7c5-110aeb7a4cf7`).
- Jingle after "Follow for more": "User Interface, Alert, Game, Points, Jingle 01" (`9906413b-7c6c-4b9a-ae58-be464cc8c14e`, 3.3 s). Extend the last scene about 2 s so it plays out.
- Music bed: "Reaching Out" (Dovetail, recording `1a2fa0a8-c84f-3aa7-8092-6d3f6048e881`); pick a new track for each new video.
- Downloads return a signed `assetUrl` that **expires within minutes**: run `curl` in the very next call (a later fetch gets HTTP 401; ask for a new link). Check the size with `ffprobe` afterwards. Put pops and swishes on a dedicated `SFX` track and the marker, jingle and character swishes on `SFX 2` (clips on a track may not overlap).

## Character

Pixel recruiter (16-bit, 26 x 40 grid, brown bun, red glasses, pink blazer, orange lanyard, clipboard), drawn in code: `example/char/sprite.py` (run from the folder that holds `char/`) writes `char-wave.png` (hook, 7x) and `char-thumb.png` (outro, 6x). `options.py` draws four alternates (professor, whiteboard teacher, study buddy, desk mascot) onto `options.png`. Hook: bottom left (`x -319, y -330`), pop at 0.6 s, two bounces. Outro: bottom right (`x 328, y -355`), thumbs-up, pop with the sticker, two bounces.

## Beacon

- Create the project 1080 x 1920 at 30 fps. Import everything at `at: 1000`, then **remove the staging clips**, add a `Voice` track at index 0, and place the clips.
- **Place everything in one `script` call** (`example/beacon/place-car.js`): it removes the staging clips, then adds voice, base, layers with their pop animations, highlight wipes, the music track, both character clips and the SFX (shared out over `SFX` and `SFX 2` so none overlap), as one undo step that runs in under 30 s. `beacon.run` returns the new clip id, so there are no ids to copy between calls. Generate the JS from `scenes.json`, `rects-s{i}.json` and the import result (asset ids come back in file order). The older way, `transaction` batches of at most 20 that you read ids from, also works but takes about six round trips.
- To add a video to an existing project, start it after the last one with a gap (the car video went at 110 s after the creators video ended at 96.6 s), reuse the existing `Voice`, `Highlight`, `Character`, `SFX` and `SFX 2` tracks and SFX assets, and give the music a new `Music N` track.
- Frame snapping can leave a layer one frame past its scene end, so it shows over the next scene for a frame. After placing, trim every image clip that ends past its scene end with `clip_trim`. `example/beacon/place-body.js` does this at the end of the same script.
- **Several videos at once:** import all their files in one `media_import` (asset ids come back in file order), then place them all in one `script`. `example/beacon/gen-place.py` turns each video's `scenes.json`, rects and timings (voice lengths, wipe ends, marker, chime, character and jingle times) into the data that `place-body.js` reads. Two videos, about 260 commands, ran inside the 30 s limit.
- Don't put `rm` in a compound shell command (a safety check blocks it). Leave the generator's `.part` files where they are.
- In zsh, `set -- $pair` does not split words, so a loop over "name id" pairs silently downloads nothing. Write one `curl` per take.
- Each layer: image clip at scale 0.85, opacity 0, with a `backOut` 0.24 s animation to scale 1 and opacity 1. Centre transform from the layer rect: `x = rx + rw/2 - 540`, `y = 960 - (ry + rh/2)`.
- Music: give it its **own new track**, props `audio {gain 1, volume 0.075, normalize false, muted false}` (all four fields, or the project is rejected). The owner may consolidate music onto one track later; find music clips by track name (`/^Music/`) rather than by id.
- `media_replace` can keep showing the old image the second time you use the same path: copy the new file to a fresh name and replace from that. It is a tool of its own and cannot run inside a `transaction`; call it once per asset (calls can run in parallel).
- In `script`, `beacon.query("project_get")` returns `assets` (and sometimes `sections`) as an object map, so wrap it in `Object.values(...)`. Section times there are in ticks (705,600,000 per second); `project_describe` prints them in seconds.
- Give every video a **section** (`section_add`, named with number, topic, assistant and voice, e.g. "3 Used car · Claude · Explainer"). Sections move with ripple edits, but their starts can drift from the content. Before exporting, read each video's real first and last clip and export that range, not the section's.
- The owner edits between requests (trims ends, moves music, shifts clips). Re-read the range with `timeline_clips` and `transcript_get` before every change, and never reuse earlier ids or times. If Beacon closes the connection, `project_open` the same path again.
- `timeline_insertSpace` splits clips that cross the point: afterwards remove the right-hand halves of image clips and `clip_trim` the left halves forward; fix the music by trimming the left piece's end and moving the right piece back with its `mediaStart` in step.
- The owner edits in the Beacon app and leaves comments (`project_describe` lists them with times). Re-open the project and re-read the timeline before changing anything; their edits shift clips.
- Export `export_start` at 1.0x (the owner did not want 1.2x here), with `from`/`to` set to the video's range when the project holds several, then `open -R <file>` so it shows in Finder. A 37 s export takes about 5 s.
- Before building, confirm Fish (`get_credit_balance` shows `plan: plus`), Epidemic (any `SearchRecordings`) and Beacon (`project_open`). If any is not connected, stop and tell the owner.

## Checks before you say done

- Frame checks of the hook, one middle step and the last step (and any scene you changed).
- Say which scenes you did not look at, that you have not listened to the audio, and what on screen is an inference.
- Check the export with `ffprobe` (size, length, an audio stream) and `volumedetect` (car, funnel and hooks videos: mean about -15.5 dB, peak about -1.0 dB). That proves sound is there, not that the mix is right.
- When the owner says go on several scripts, "done" means exported. Researching and drafting a script is not a built video, so say clearly which stage each one is at.
- An approved `script.md` often comes with wording rules (for example "say an insurer, never name it", "no dealer name", "no full VIN", "never say salvage title"). Check every card against them before importing.
- Voice is on a paid Fish plan (commercial use), and no tool or logo is shown that is not an official Alexandria provider.
