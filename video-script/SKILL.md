---
name: video-script
description: Write, check and improve a YouTube script for the Firecrawl channel using what the channel's own retention and performance data says works. Drafts client-videos/firecrawl/<slug>/script.md in the user's voice and structure, checks the opener, length and middle against the retention rules, scores title options, offers a fact-check, and after publishing links the video to its script so its retention feeds back into the rules. Use when the user asks to write, draft, rework, check or review a video script, fix an intro, or asks "is this script good".
user-invocable: true
argument-hint: "<topic or existing script folder> e.g. 'anydoc' or 'check harness-tax'"
---

# video-script

The channel's data and scripts live in the firecrawl-data repo; this skill's own files sit next to this SKILL.md:

```bash
REPO=~/fc/firecrawl-data/youtube
SKILL=<absolute path of the directory containing this SKILL.md>
VIDEOS_DIR=~/client-videos/firecrawl
```

Bare paths below (`data/...`, `references/what-performs.md`, `scripts/...`) are relative to `$REPO`. `$SKILL/references/lessons.md` is this skill's own file.

## Before writing

Read these first, every time:
- `$SKILL/references/lessons.md`: what the user has corrected and approved in past scripts (how to propose edits, hooks, structure of build videos, voice, Notes). These override the general guidance below where they conflict.
- `references/what-performs.md`: the pitch signals and the **script rules** (hook in lines 1 and 2, no recap opener, worked demos or a live build in the middle, 4 to 6 minutes).
- `data/script-retention.md`: which real openings held viewers and which lost them, with the numbers.
- The three most recent `script.md` files in `$VIDEOS_DIR` (`ls -t`), for the user's structure and voice.

If the topic hasn't been researched yet, gather primary sources first: the repo, docs or announcement, pricing pages for any money claim, and the numbers you plan to say on camera. Never put a number in a script that you haven't read in a source.

## Writing

Create `$VIDEOS_DIR/<short-slug>/script.md`, or edit the existing one, in this shape:

- **Several `# ` title options at the top.** Pitch through a hook (money, free, a pain, a surprising number), never "Feature X explained".
- **`## Intro`:**
  - The first two spoken lines carry the hook: the viewer's problem, or a specific surprising fact with a real number.
  - If the user wants a particular first line (for example "this is X"), keep it and put the hard number in the very next line.
  - Never open by recapping news ("X was just released", "topping the benchmarks", "people are sharing demos", "the official X is now available").
- **`## Exp`:** the explanation, kept short. Its first line names the product.
- **`## Build your own`** (build videos only): one numbered step per tutorial branch, written from the real code.
- **`## Demo`:** worked demos as numbered `### 1.`, `### 2.` subsections, or one live build. Leave results as placeholders like `[results]`; never invent them.
- **`## Outro`:** includes the 500 extra credits line.
- **`## Notes`:**
  - for anything demoed or built on camera, "Recording the build" and "Recording the demo" blocks: how to run it, which examples are cached, per-demo gotchas and what to re-check on the day;
  - caveats to say on camera;
  - claims to avoid;
  - key numbers with sources;
  - every source URL, Hacker News threads and X posts.

Voice: short spoken lines, mostly lowercase, one idea per line, `[url]` and `[show ...]` cues for what's on screen. Match the recent scripts, not a polished blog tone.

## Checking

Run all of these and report the results plainly:

```bash
python3 "$REPO/scripts/script_check.py" "$VIDEOS_DIR/<slug>/script.md"
```

`script_check.py` is a heuristic fitted to 18 past videos. It is right about most openers but has missed two (Fable 5.1 and the Developer Index), so treat a PASS or WARN on the opener as a prompt to reread the opener against `data/script-retention.md`, not as a verdict. Fix FAILs before recording unless the user decides otherwise.

- Score the title options with the `title-score` skill if it's installed.
- Offer a fact-check with the `delegate` skill: an independent model reads the script against the primary sources and lists anything wrong, misleading or unverifiable. Apply the fixes and add a line to Notes saying what was checked.

## Updating this skill

At the end of every script session, before saying you're done:

1. List what the user changed, rejected or praised in the script (rewritten lines, cut sections, "much better", "doesn't make sense").
2. Turn each into a one-line lesson with its reason, and add it to the right section of `$SKILL/references/lessons.md`, tagged with the video slug. Merge it into an existing lesson if it repeats one; don't add duplicates.
3. If a lesson contradicts a rule in this SKILL.md, fix the rule here as well.
4. Show the user the lessons you added in one short list, then commit in `~/skills` (stage only `video-script/`).

## After the video is published

- Add `"<slug>": "<video_id>"` to `data/script-map.json` (video IDs from `scripts/channel_videos.py`).
- After about two weeks, pull its retention and rerun the comparison:

  ```bash
  python3 "$REPO/scripts/studio_retention.py" <video_id>
  python3 "$REPO/scripts/retention_vs_scripts.py"
  ```

- If it breaks a rule's pattern (a recap opener that held, or a hook that didn't), update `data/script-retention.md` and the rules in `references/what-performs.md`.
- Back up `$REPO` the usual way (it isn't a git repo), and commit any skill changes in `~/skills`.
