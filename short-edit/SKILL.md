---
name: short-edit
description: The full edit for a vertical talking-head Short / Reel / TikTok — speed it up 1.2x, cover any green placeholder plate with a paper-cutout animation, add Reels-style phrase captions (2-4 words, white bold on a flat black box, no bounce, no logo tiles), render, then research Shorts titles (real view counts, ranked with title-score) and write titles + descriptions for YouTube, Instagram and TikTok. Use when the user says "do the usual", hands over a new short (.mov/.mp4 in Downloads), asks to caption / subtitle a short, or asks for titles and descriptions for one.
---

# Short edit

If the short is a Beacon project (`.beproj`), use `short-edit-beacon` instead; come back here only for §6 (titles and descriptions).

Pipeline: **speed up → transcribe → detect layout → green panel → config → generate → lint → render → verify frames → titles & descriptions**.
"The usual" = all of it. Approved on `fake-reviews`, `harness-tax-2`, `firecrawl-trends`
and `firecrawl-jobs` (configs in `configs/<slug>-captions.json`, panels in
`compositions/<slug>-panel.html`). Copy the closest one.

Work from the HyperFrames project `~/fc/firecrawl-transition` (`cd` there first):
`assets/`, `configs/`, `compositions/`, `thumbnails/` and `final/` are relative to it.

Scripts live in `~/skills/short-edit/scripts/` (run them from the project root):
- `detect_layout.py <video> [--green]` prints layout runs (`full`, `split@<y>`, `green y0-y1`).
- `gen_captions.py <config.json>` writes the composition and prints every caption (start, duration, position, text).
- `shorts_titles.py "query" ...` real Shorts titles with view counts, highest first (step 6).

## 1. Speed up (new file, never overwrite the original)

```bash
ffmpeg -y -v error -i ~/Downloads/<name>.mp4 -filter_complex "[0:v]setpts=PTS/1.2[v];[0:a]atempo=1.2[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset medium -r 30 -c:a aac -b:a 192k ~/Downloads/<name>_1.2x.mp4
cp ~/Downloads/<name>_1.2x.mp4 assets/clips/<slug>-fast.mp4
ffmpeg -y -v error -i assets/clips/<slug>-fast.mp4 -vn -q:a 2 assets/clips/<slug>-fast.mp3
```

Transcribe the **sped-up** audio so timestamps match the video. The key is in the fish shell:

```bash
fish -c 'curl -s https://api.openai.com/v1/audio/transcriptions -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@assets/clips/<slug>-fast.mp3 -F model=whisper-1 -F response_format=verbose_json \
  -F "timestamp_granularities[]=word"' > assets/clips/<slug>-fast.json
```

Fallback when OpenAI fails: Replicate `vaibhavs10/incredibly-fast-whisper` (see CLAUDE.md).

## 2. Find the layout

1. Contact sheet first (eyeball the structure, 0.5s steps):
   `ffmpeg -i clip.mp4 -vf "fps=2,scale=108:192,drawtext=text='%{pts\:hms}':x=2:y=2:fontsize=12:fontcolor=yellow:box=1:boxcolor=black" g%03d.png`
   then `tile=23x2`.
2. `detect_layout.py clip.mp4 --green`. Real splits are long runs at one y
   (≈850 or ≈960 so far; read it per video and set `split_y`). Short flickery `split@1200`-style runs are edges
   inside full-screen screen recordings: ignore them. A split can also cut to a
   full-screen zoom of the recording with no clean edge (detector keeps saying
   `split@<other y>`): the contact sheet is the judge of where a split ends.
3. Whisper mishears product names. Check the screen recording for the real
   spelling (it heard "Py" for the Pi harness) and fix it via `display`.

## 3. Config (`configs/<slug>-captions.json`)

```json
{
  "id": "<slug>-captions",
  "video": "assets/clips/<slug>-fast.mp4",
  "transcript": "assets/clips/<slug>-fast.json",
  "duration": 45.5,
  "out": "compositions/<slug>-captions.html",
  "split_y": 850,
  "splits": [[6.73, 10.30], [17.63, 28.60]],
  "phrases": "Everyone thinks | changing a model | ...",
  "display": {"Py": "Pi", "1 33": "$1.33", "27 000": "27,000", "5 star": "5-star"},
  "subcomps": [{"id": "x-panel", "src": "compositions/x-panel.html", "start": 17.63, "duration": 10.97, "top": 0, "height": 852}],
  "logos": []
}
```

- **phrases**: hand-written groups separated by `|`, written in the transcript's
  own tokens (Whisper splits "$1.33" into `1 33` and "27,000" into `27 000`).
  The script fails loudly on any mismatch. 2-4 words per group, broken at
  natural phrase boundaries, never mid-name ("New / Jersey" is wrong). Greedy
  auto-grouping was tried and rejected for exactly that.
- **display**: replacements applied to the shown text after punctuation is stripped.
- **caption_bg**: `"box"` (default: flat black rounded box, 90% opacity, no
  gradient, no shadow), `"none"` (shadow only, the original fake-reviews look),
  or `"gradient"` (soft black band across the frame behind the caption).
- **caption_anim**: omit for the default hard cut (each phrase just appears, no
  bounce). `"pop"` restores the old scale/back.out pop-in.
- **Re-exports of the same edit**: copy the old config, re-transcribe, diff the
  word lists, and re-run `detect_layout.py`. Cuts usually shift by a frame or
  two (move `splits` and subcomp `start`), and trimmed endings mean dropping
  trailing phrases.
- **logos**: always `[]`. The user dropped the pop-in logo tiles that
  appeared with captions; only add them back if asked (older configs such as
  `fake-reviews-captions.json` show the `pos`/`style`/`stagger` fields).

## Locked style (user-approved)

- Captions: Poppins 800, 76px, white, no quotes, no highlighted words, on a
  flat black rounded box (`rgba(0,0,0,.9)`, radius 24px). No gradient on the box.
- No caption animation: each phrase hard-cuts in and out with its clip. The
  bounce pop-in was dropped at the user's request.
- Position: centred at y 900-1140 (just under the chin) on full-frame shots and
  full-screen recordings; in split sections the caption's bottom sits 20px above
  the split line.
- Position follows majority overlap with the split windows, and a caption is
  cut short at a layout boundary so it never sits in the wrong place after a cut.
- No logo tiles over the captions (user request). Brand logos inside panels
  are still fine: real logos only (`assets/icons/`, `assets/leadgen/logos/`, simple-icons
  via `cdn.jsdelivr.net/npm/simple-icons@latest/icons/<name>.svg`, Wikimedia
  Commons API for anything else, e.g. `File:Benzinga Wordmark.png`). Never hand-draw a brand.
- **No SFX.**

## Green placeholder sections → paper-cutout panel

If part of the frame is a flat green plate (the editor left room for a
graphic), cover exactly that rect and time window with a sub-composition in the
`/paper-cutout` style (load that skill first). Proven pattern:
`compositions/harness-tax-panel.html`:

- `<template>` sub-comp at `1080 x <green height>`, all ids/classes prefixed
  (`hp-`), selectors scoped through a `q()` helper. The linter then reports
  `__unresolved__` overlapping-tween warnings: those are false positives.
- Keep the bottom ~200px of the panel empty: split captions sit there.
- **Full-frame plate** (`green y0-1920`, e.g. `firecrawl-jobs-panel.html`): the
  caption sits centred at y 900-1140 over it, so put the scene above (cards at
  y ~360-700) and chips below (y ~1270+), camera VY 960.
- Plates can be short (1.6-3.3s so far): 2-4 beats keyed to the key words,
  one camera move at most. Read the narration under the plate and visualise
  that idea (paywall → a wall + padlock slams between ChatGPT and the data;
  "products, news, brands" → a torn tree of three cards).
- Timeline is local (0 = panel start); key every beat to word times minus the start.
- Camera `cam()` with motion blur centred on the panel (VX 540, VY ≈ 360).
- Mount via `subcomps` in the config; the plate is opaque, so no keying is needed.
- **Several plates in one video** (top-3 had five): write them from one Python
  generator so they share the material block, as in
  `scripts/panels_example_top3.py`: a `write()` helper (defs + base CSS +
  cam/card/pop/punch JS), a reusable **rank card** ("Number N is X": torn fire
  number + logo card + chip) and two story panels. Copy it and edit the world/
  css/js per plate. Ink chips vanish on the dark ground: use fire or cream for
  the payoff chip.
- **Read the plate's label first.** The editor often types a note on the green
  ("Motion busy people near subway", "Typing in claude desktop input"): build
  what it says. Unlabelled plates get a paper-cutout panel from the narration.
  Exception: when the line under an unlabelled plate describes a person in a
  real-life moment ("makes better trades while you sleep"), the user preferred
  realistic footage of it (someone asleep while a rising chart glows on the
  nightstand) over a cutout. Use the REALISTIC flow below for those.
- **Mockup plates** ("typing in claude desktop input"): recreate that app's UI
  as a plain sub-comp instead of paper-cutout, and type the spoken prompt into it
  char by char inside each word's Whisper window (`scripts/panel_coffee_claude.py`,
  Claude.ai dark home screen, 1080x1920).
- **Plate cover check:** a sub-comp can start one frame late and leak a green
  frame. Start each panel ~0.02s before the plate, and after rendering scan the
  final for green frames (any frame >3% `#2x7x2x`-ish green must be fixed).

### REALISTIC plates → generated footage

If the plate's label contains **REALISTIC** (any case, e.g. "REALISTIC crowd
near a subway", or "realistic footage of ..."), don't build a cutout. Generate
real-looking footage with Seedance 1 Pro on Replicate and mount it as a muted
`<video>` in a tiny sub-comp (`compositions/coffee-subway-video-panel.html`):

```bash
python3 ~/skills/short-edit/scripts/gen_footage.py <slug>-<scene> 1080 960 3.9 \
  "Morning rush hour in Williamsburg: commuters with coffee cups stream along a sidewalk toward a subway staircase with green railings, seen from behind and slightly above, soft early sunlight." 71
```

- Write the scene from the label plus the narration under it. No on-screen
  text: the script appends a hard no-text clause, but Seedance still paints
  gibberish on signs it draws, so frame the scene away from signage (a
  wide street view, not a station entrance close-up) and check a contact sheet.
- Generate 2 takes (different framing or seed) and pick the cleanest; keep the
  others in `assets/clips/` for the user.
- The script cover-crops the 1440x1440 square to the plate (trimming sky) and
  trims to the plate duration.

## 4. Lint, render, verify

```bash
python3 ~/skills/short-edit/scripts/gen_captions.py configs/<slug>-captions.json
npx --yes hyperframes@0.6.88 lint 2>&1 | grep -A1 "\[compositions/<slug>"     # no ✗ allowed
npx --yes hyperframes@0.6.88 render -c compositions/<slug>-captions.html -o final/videos/<slug>-captions.mp4 -q high
```

Project-wide lint is noisy from older files, so filter to yours. Expected
warnings: `timeline_track_too_dense`, `google_fonts_import`.
Render takes ~6 min for 45s, so run it in the background.

Verify by frames: one per layout section, plus every panel beat, tiled with
`hstack`. Check caption legibility on light frames and the panel beats.

Whisper squashes fast words, so re-check the printed caption list: merge any
caption under ~0.4s into a neighbour (5 words is fine for a merge).

## 5. Deliver the video

- Once the final render is verified, reveal it in Finder (user request):
  `open -R final/videos/<slug>-captions.mp4` (opens `final/videos/` with the
  file selected). Do it again for the `-nocta` cut if one was rendered.
- Sped-up file path, captioned final path, and the caption/panel timings.
- Flag anything only partly solved (low-contrast frames, brief captions,
  captions straddling a cut, names Whisper may have misspelt).
- **"Comment WORD" endings:** that CTA only works on Instagram (ManyChat DM
  auto-reply). Always also render a cut without it for YouTube Shorts and
  TikTok: copy the config to `<slug>-nocta-captions.json`, truncate the
  transcript JSON before the CTA's first word (`<slug>-fast-nocta.json`), set
  `duration` to just before that word (in the pause after the last line), drop
  the CTA phrases, and clamp the last split/subcomp to the new end. Output
  `final/videos/<slug>-nocta-captions.mp4`. Then write the YouTube and TikTok
  descriptions without the "Comment WORD" line.

## 6. Titles and descriptions (YouTube, Instagram, TikTok)

The user asks for these right after every edit, so do it as part of "the usual".

1. **Research Shorts only.** `scripts/shorts_titles.py "<topic>" "<angle 2>" "<angle 3>"`.
   The generic title-research skill searches long-form, which is the wrong
   pattern pool. Note the formulas of the top 3-5 by views ("The Best Way to
   Find X 😱" 167K, "Use ChatGPT To Get Any Job" 1.5M).
2. **Pick one search phrase first** (how people would type it, e.g. "how to
   check insider trades", "where to open a coffee shop"). It leads the title and
   the first line on every platform. One video, one phrase.
3. **Generate 8-12 title candidates**, 4-10 words. Most should LEAD with the
   search phrase and add a payoff ("How to Check Insider Trades Before You Buy
   Any Stock (Claude)"). Include 2-3 hook-style titles borrowing the researched
   formulas or the spoken hook ("Hedge Funds Pay Thousands For This Data, Claude
   Gets It Free") as backups. Clickbait-but-true; no emoji in titles.
4. **Rank with title-research's scorer**, and show the score in the table:
   `printf '%s\n' "T1" "T2" ... | python3 ~/skills/title-score/scripts/score.py -`
   (same script as `~/.claude-work/skills/title-score`). Iterate once on the top
   half (tweak the weakest sub-score) and re-score.
5. Report a table: `# | Score | Title | Borrows from (real Short, views)`, sorted
   by score. Recommend one search-led pick plus one hook backup; it's fine to
   recommend a lower-scored title. The scorer is fitted on long-form vidIQ data
   and under-rates short Shorts titles, so say so.
6. **YouTube description**: line 1 = search phrase + hook; 1-2 lines of what the
   video shows with the real number/example; numbered steps in the right order
   (1. Sign up for a free Firecrawl account: https://firecrawl.dev, 2. Connect
   Firecrawl to Claude, 3. the prompt); the exact prompt if one is on screen;
   then exactly 3 hashtags: `#shorts` + 2 topic tags. Never invent a link.
7. **Instagram caption** (Reels):
   - Line 1: search-phrase hook under 125 chars ("How to see insider trades
     before you buy a stock"). Never a vague or keyword-free clever line.
   - 2-3 lines of story with the real number/example from the video.
   - One CTA only ("Comment WORD and I'll send you the exact prompt" only if a
     DM auto-reply runs, otherwise "Prompt in the comments").
   - Blank line, then exactly 3 hashtags: 1 broad, 1 mid, 1 niche. No #viral,
     #fyp, or brand tags (#firecrawl) and no tags too broad to rank (#ai).
8. **TikTok caption**: 150-225 chars, one paragraph. Search phrase in the first
   3-5 words, one line of payoff with the number, one CTA, then exactly 3 tags.
9. **No emoji/icons anywhere** in titles or captions (user request).
   **Finance/trading/investing videos:** end every description and caption
   (before the hashtags) with a short disclaimer line: "Not financial advice.
   Firecrawl doesn't give trading or investment advice." Same idea for legal,
   medical or tax topics ("Not legal/medical/tax advice").
10. **Double-check with a subagent before showing the user.** Spawn a fresh
   subagent with the transcript, the titles and the three captions, and have it
   check: search phrase leads each title/caption, every claim and number is in
   the video, steps are in the right order, exactly one CTA, exactly 3 hashtags,
   no emoji, no generic tags, and no invented links. Fix whatever it flags, then
   show the result.
11. **Make every description copy-paste ready (user request):** give each
   platform its own fenced code block (```` ```text ````) under a plain
   "YouTube" / "Instagram" / "TikTok" heading. Inside the block: plain text
   only, with no `>` quote markers, no markdown bold or links, real line breaks,
   and the hashtags included. Notes (a missing link, an alternate prompt) go
   outside the block, never inside it.
12. Skip any title whose claim the video doesn't back (invented stats like
   "95% of creators", "Fake X Are Over"), and say why.

Thumbnails on request. Preferred (user-picked) style: **pop-out**,
`thumbnails/thumb-pop.css` (example `thumb-pop-harness-tax-lime.html`): pixel
meter, 2-line uppercase Poppins 800 headline, italic line + highlight box
(lime default, `class="orange"` for brand), then the video frame in a rounded
card with the head breaking out over its top edge.
**Layout (user feedback):** big app/logo tiles across the top (`.apps` in
`thumb-pop.css` is now 260px tiles with 160px logos; don't shrink them), and the
text stack pushed down so it sits close above the photo, not floating under
the icons with a big gap before the head. With the wide-frame vars below, a
two-line headline at 370px works at `.stack { top: 600px; }`, leaving ~240px
(of 3840) between the subline and the cap. Re-check that gap on every
render and nudge `top` by headline length. Example:
`thumb-pop-f-football-flux3.html`. Pick a reaction frame from a
full-face shot, save it to `assets/hero/<slug>-frame.png`, cut it out with
`npx hyperframes remove-background` to `<slug>-cutout.png`, then tune
`--img-top`/`--card-top` so the cap clears the card edge. Render with
`-f 1 --format png-sequence` and flatten onto `#0b0b0b` at 1080x1920.
**Face quality (user feedback):** a raw video still looks soft and harsh, but
plain AI enhancement (CodeFormer, Real-ESRGAN face_enhance, gpt-image relight
from the frame alone) all drifted to "doesn't look like me". What worked:
crop the frame tight on head + shoulders (800x1200 → 1024x1536), then
`/v1/images/edits` with TWO images, the frame plus the user's reference portrait
`assets/hero/robray-reference-portrait.png` (cinematic orange key light, teal
shadows, orange bokeh), asking for that exact style and his identity from both
images. **First choice: `black-forest-labs/flux-3-image` on Replicate** (best
likeness so far; `images: [frame, reference]`, `resolution: 2k`, `grounding:
false`) via `scripts/flux_edit.py <frame> <ref> <out> '<prompt>' flux-3-image`.
Never use `flux-2-max` (user ban). Alternatives to show side by side: the OpenAI
`gpt-image-2.5-flare` / `gpt-image-2.5-sunburst` / `gpt-image-2` edits. (`black-forest-labs/flux-3` is video-only.) **Use a wide frame** (user preference):
the bottom-half camera of a split section, where he takes up ~50% of the frame
with mic, boom arm and desk visible (`crop=1080:1060:0:<split_y>`), not a
cropped close-up; ask the model to keep the mic setup and swap the wall for
the dark orange-bokeh studio look. Example: `thumb-pop-harness-tax-wide-*.html`
(`--img-top: 1680px; --card-top: 2090px; --img-w: 2160px; --img-x: 0px`, stack
`top: 330px`); upscale 2x with Real-ESRGAN
(`face_enhance: false`). Replicate's API rejects Python's default user agent:
send `User-Agent: curl/8.7.1`. For these tighter photos set
`style="--img-top: 1480px; --card-top: 1980px;"` on `#root`.
Older alternative: `thumbnails/thumb-vert.css`.
