---
name: rough-cut-beacon
description: Rough cut a long-form (16:9) talking-head video in Beacon through the Beacon MCP tools, the way the user does - lay the recordings out in script order, cut retakes, false starts, fillers and chatter, keep the last full take, tighten pauses, and leave the screens in sync for the user's own screen pass. Uses the video's script.md (usually in ~/client-videos/firecrawl/<slug>/) as a guide, not a transcript. Use when the user asks for a rough cut, to remove retakes / filler words / silences, or to "cut it like the script" on a Beacon project that isn't a Short. For vertical Shorts use short-edit-beacon.
---

# Rough cut in Beacon (long videos)

Approved on the HackerTube video (2026-11-13, `hackertube.beproj`; the user:
"this is perfect", after a few small tweaks that are folded in below).
480 s from 35 min of raw recordings.

Order: **open → read → lay out → read every transcript → cut takes → check →
pauses → joins → look → report**. Edits go straight onto the timeline (the
user reviews there and tweaks by hand); label every step `Rough cut: …` so
each is one undo.

## 1. Open and read

- `project_open` (no path: the project open in the app). `memory_list`:
  follow its `sentences`; `transcript_habits` gives the long-form silence
  threshold (0.5 s on 423 decisions) and "keep the last take".
- Read the whole `script.md`, including the **Outro** (it's near the end,
  after the long middle section; don't stop reading at the last `[show]`).
  Bracketed lines (`[show: …]`, `[source: …]`, `[riff]`) are notes, not
  speech. The user goes off script: the script settles which take wins and
  what order things go in, never whether an off-script riff stays.
- `project_get` with `/assets`: the Media Bin names (`intro`, `exp_1`,
  `harness`, `exp_2`… `outro`) live there, not in `project_describe`.

## 2. Lay out the recordings

- Use every recording in the Media Bin unless the user excludes one (on
  HackerTube: everything but `creator_portal`). Ask if one looks unrelated.
- **Order by the script's sections, not by recording time.** The outro is
  often recorded early but goes last. A name like `exp_35` means **3.5**: it
  goes between `exp_3` and `exp_4` (the user moved it there by hand).
  Sections named after a script part (`harness`) go where that part is.
- Screens on their own bottom track: `track_add` name `Screen` at `index: 0`,
  then `asset_place` each recording at the previous one's end with
  `track: <Screen>`. The first clip a recording makes is its screen, so screen
  → Screen, camera → the track above, audio → the one above that. A
  camera-only recording (intro, outro) goes with `track: <camera track>`.
- Place one at a time and take the next `time` from the result's end: lengths
  aren't the media durations (snapped, camera offset).
- The camera covers the screen for now. The user does the screen pass
  themselves: the job is the spoken flow.

## 3. Read every transcript, then decide

`transcript_get` in chunks of ~450 s (text format). Then plan the whole cut
before touching anything:

- **Keep the last full take** of each line. If the last take trails off or
  stumbles, keep the latest *complete* one ("a small demo… a different
  method." over a later take that stops at "a different").
- **Reworded repeats are retakes too**: two neighbouring lines saying one
  thing in different words. Keep the one that leads into what follows. Watch
  for these inside a kept line as well: "and the results we get, and the
  response when we run that code" (the user cut the first half).
- Cut stutters inside a kept line by word index: "Karpathy used hack-
  carpathy used hacking carpathy used hacker news" → keep from the last
  "carpathy"; "So in my case, I so in my case" → keep the second.
- Cut chatter and fillers: "Wait, it's still recording", "Amen", "Ahem",
  "um", "I just thought something", "okay so I'm gonna stop here", "sorry".
  Keep an off-script line the user clearly meant ("Okay, it's more of a
  better YouTube UI…").
- Two takes of a list or example said differently ("list of products to
  buy" / "gear the viewer needs"): one idea, keep the cleanest take.
- CTA: keep a take that **finishes** ("Don't tell anyone I work with.").
  A later take that adds a line but clips the last word loses.
- Leave doubled words that run together with no gap ("and and", 20 ms
  apart): cutting them chops a word.
- Index boundaries inside a line: check with `transcript_get` `format:
  words` over a 2-4 s window (one call per spot, in parallel). Don't count
  words from the text line by hand for anything past a few words.

## 4. Cut

- One `transcript_cut` with every range (indices from the transcript as read;
  it closes gaps on every track, screens included).
- Re-read `transcript_get` (`pause: 1.5`): every sentence once, in order,
  nothing missing.
- `transcript_removePauses` `min: 0.5`, `keep: 0.3` (the user's long-form
  habit). This also cuts long screen-action silences (terminal running, a page
  loading): say which ones in the report so the user can open them back up
  for the screen pass.
- `transcript_joins` `chopped: true` must come back empty:
  - Scraps at the head (bits of the first cut-away takes before the first
    kept word): `timeline_rippleDelete` from 0 to just before that word.
  - A join that chops a short connective ("…new model **but** | this is
    to…"): cut that word with `transcript_cut` (the user did) rather than
    leaving a clipped word.
- `frames_sheet` over the whole timeline (20 frames): camera on screen
  throughout, no black or stray screen frames.

## 5. Report

- Before → after length.
- What was cut, grouped: retakes (name the big ones), reworded repeats,
  chatter. Keep it short.
- Judgement calls the user might reverse: off-script lines kept, which CTA
  take, any word left doubled, any join left near a word, long screen-action
  pauses that were cut, where an oddly named section was placed.

## Gotchas

- `asset_clips` fails with a result-shape error (Beacon MCP bug, 2026-11-13):
  use `asset_place` with `dryRun: true` to see what a recording makes.
- `timeline_rippleDelete` drops any piece left under 0.5 s with the cut, so
  a range ending just before a short clip can take the clip too. Check the
  `changed` list.
- After any edit, word indices shift: re-read before the next
  `transcript_cut`.
- Whisper spells names wrong ("Andrei/Andre", "Firecool", "clawed", "hack and
  use" for Hacker News). That's the transcript, not a bad take.
