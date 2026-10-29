---
name: short-edit-beacon
description: Edit a vertical talking-head Short inside Beacon (a .beproj, through the Beacon MCP tools) the way the user does - rough cut (retakes, silences, chatter), camera in the bottom half with full-screen hook and CTA, the top half filled with 400px-wide screenshots, highlighter wipes, motion graphics, B-roll and real logos, punch-in zooms, middle captions, then Auphonic. Use when the user asks to rough-cut, lay out, dress or finish a short in Beacon, or says "do the usual" on a Beacon project. For HyperFrames renders of a downloaded .mp4, use short-edit instead.
---

# Short edit in Beacon

Approved on the Grok plugins short in `~/Movies/Beacon/3-shorts-new.beproj`
(2026-10-28; the user: "Done an amazing job"). Earlier hand-made shorts in
`~/Movies/Beacon/3-shorts.beproj` set the layout. Open either to copy from.

Order: **plan → rough cut → camera → top half → highlights → logos → zooms → captions → audio → verify**.
Titles and descriptions afterwards: `short-edit` §6.

## 0. Before anything

- `project_open` with the project's path: the app often has two projects open
  and refuses a bare open.
- A project can hold several shorts (Grok, then Midterms). Edit only the one
  asked for. Beacon's Remove Retakes / Silences / Fillers act on the **whole
  timeline**: dry-run them, keep only the ranges inside the short, apply those
  (`transcript_removeSilences` with `at`, `timeline_rippleDelete` with ranges).
  Ripple edits move the later shorts left: fine, but their clips and the gap
  must stay as they were. Check afterwards.
- For anything beyond the rough cut, **write the plan first and wait for the
  go** (user request): a table of time → what fills the top half, the
  highlights, the B-roll count, caption placement, and the open questions.

## 1. Rough cut (shorts are tighter than long videos)

- Read `transcript_get` for the short's range. Keep the **last full take** of
  every line; cut false starts, off-mic chatter, and Whisper's hallucinated
  "Thank you" / "Okay" in quiet stretches. A short's script is small, so cut by
  hand with `transcript_cut` word ranges in one call, rather than trusting
  Remove Retakes' picks.
- Lists said in several takes ("Shopify / Benzinga / particle, Oriane and much
  more / Apollo, FullEnrich and much more"): keep the last ending and say which
  one was dropped.
- Silences: over **0.25 s**, leave **0.2 s** (measured on the user's shorts:
  ~0.1 s of quiet each side of a cut; long videos leave 0.3). Then trim the
  short's tail to ~0.1 s after the last word. Recompute times after every
  ripple: a range computed before a cut lands in the wrong place after it.
- Stretched words hide repeats and pauses (Whisper writes a word said twice
  once, and swallows pauses into words): dump `transcript_get` words, flag any
  word over ~2x its expected length, check its loudness from the `.brec`'s
  `microphone.wav` (Beacon's ffmpeg has no silencedetect: raw PCM + Python RMS),
  and ripple-delete what's left. To hear what a stretched word hides, cut that
  stretch out with Beacon's ffmpeg and run Beacon's `whisper-cli -ml 1 -sow`
  on it alone (model in `~/Library/Caches/Beacon/models`); captions over it
  need re-splitting and `caption_setText` by hand.
- A screen recording with voice-over (no camera) plays full screen; zoom the
  screen clip onto each item as it is named (scale and move about the point:
  pos' = P + k(pos - P)).
- A typed prompt (ChatGPT etc.) is a hand-written full-screen `motion_code`
  graphic of the app's home page, the text typed per word as it's said, input
  box in the middle of the screen, no captions over it.

## 2. Camera

Canvas 1080x1920. Transform coordinates: origin at the centre, **y up**, so
the top half is y +480 and the bottom half y -480.

| Shot | 4K camera (`camera.mp4`) | 1080p camera (x2, derived) |
|---|---|---|
| Bottom half (default) | scale 0.45, x -40, y -474, crop top 23.15 | scale 0.9, y -474, crop top 11.57 |
| Punch-in (every other cut) | scale 0.53, x -47, y -545 | scale 1.06, y -545 |
| **Full screen** (hook, CTA, one beat mid-video) | scale 0.92, x -125, y -6 | scale 1.84, y -6 |

- **Full-screen camera for the hook line and the CTA** (the user's own edit,
  as in earlier shorts), and for one emotional beat in the middle ("communicate
  with people on my behalf"). Nothing goes over the top half then: no title
  graphic, no logo.
- Alternate bottom-half and punch-in across cuts: it hides the jump cuts. Keep
  the cap clear of the panel line (y -545, not -512).
- A slow push-in (0.45 → 0.5, x -44, y -500, easeInOut) on any take over ~8 s.
- Set the framing on one clip, `frame_at`, then apply it to the rest in one
  `clip_set`.

## 3. The top half (y +480, 1080x960): never empty while the camera is halved

Every second of a half-camera shot has something above it. After placing,
list the top-half clips and check for gaps: a 3-frame gap showed black.

**Screenshots** (real pages, never the user's inbox or workspace):
- Browser width **400 CSS px** (user rule; 300 for narrow pages) at 2x pixel
  density, iPhone user agent, so pages show their mobile layout:
  `~/skills/short-edit-beacon/scripts/screenshot.sh <out.png> <url> [height]`. Headless Chromium from
  Playwright's cache; Agent Browser or Chrome over CDP also work.
- Crop to 800x711 (the panel's shape) from where the page's message starts,
  above any cookie banner: `scripts/crop_panel.py <in> <top_px> <out>` (save into the project's `media/screens/`).
  Place with `media_import` (`at`, a Screenshots track), `clip_trim` to the
  line, transform x 0, y 480, scale 1.35, and a slow push-in to 1.42.
- News sites dim the page under a cookie wall, and some (USA Today) block
  headless Chromium. Capture with the page's banners and full-screen fixed
  layers removed before the shot (a small CDP script), or pick another
  outlet. ChatGPT's plugin pages render blank without a login; use the
  vendor's own announcement page.
- Check a reused screenshot is what it claims (a "Firecrawl plugin in Grok
  Bot" shot was ChatGPT's apps page).

**Highlighter wipes** on the words being said (user favourite):
- `edit_addAnnotation` preset `highlight`, then `clip_set` region width 2,
  height **54** (body text) or **86** (headlines), and animate `region.width`
  and `transform.x` together (easeOut, 0.35-0.8 s, ending as the word ends) so
  the left edge stays put.
- From a 540-wide `frame_at`: canvas px = frame px x 2, then
  `x = left + width/2 - 540`, `y = 960 - centre_y`. Start x = left + 1 - 540.
- One bar per line for wrapped headlines, staggered 0.3-0.5 s.

**Motion graphics**: `motion_add` (time, duration, a typed prompt), then
`clip_set` `motionBox {1080, 960}` and transform y 480 on all of them, then
`motion_make` each (OpenAI, look Bold; ~2 min for 8 in parallel). Prompts
name the exact words, numbers and brand colours (Firecrawl #FA5D19) and say
"as it is said". What worked: a comparison bar chart, a counter racing to the
number, names popping in one per word, an email drafted then "Sent ✓",
channels collapsing into a Summary card, chat bubbles labelled per word.

**B-roll** for lines about a feeling or a real-world moment (paywall, "saved
me a lot of time"): `broll_add` region `[0, 0, 1080, 960]` with a written
prompt, `broll_estimate`, then `broll_generate` (Seedance 2.5, ~$0.22/s;
the user allows as many as are best). Flag generic stock-person shots.

**Logos**: real ones only. App icons: the iTunes Search API
(`https://itunes.apple.com/search?term=<app>&entity=software`, swap
`512x512bb.jpg` for `1024x1024bb.png` in `artworkUrl512`); check the seller.
On a Logos track at the top, round-corners + drop-shadow, popping in on the
spoken name: scale 0.01 and rotation -12, then backOut to scale ~0.16 over
0.35 s. **Sparingly**: the user kept one (on the Gmail screenshot) and
removed the others (hook, Slack).

## 4. Captions

`captions_create` with `from`/`to` = the short's range, `maxWords` 3, style:
Montserrat 800, size 72, uppercase, white, highlight `[1, 0.84, 0.1, 1]`,
background `[0, 0, 0, 0.75]`, radius 18, maxWidth 0.9, **anchorY middle,
offset 0** (on the seam between the halves; user choice). Captions over a
**full-screen camera** shot go lower: `caption_place` each one (one clip per
call; `clips` is refused) to middle, offsetY **101**, and give them a **blue**
label (`selection_set`, then `edit_label`). The track's highlight stays off
(alpha 0): `captions_create`'s `style` changes the whole track, so never pass
a visible highlight. Leave a full-screen motion graphic with no captions:
create captions on either side of it. Then fix Whisper's
spellings with `caption_setText` (GrokBot, paywall, FullEnrich), and after
any re-cut look for one-frame sliver captions.

## 5. Audio (last, once the picture is locked)

`auphonic_review` with **only the short's audio clips** and the **Usual-5**
preset (`auphonic_presets`; Polish on, de-esser 0.2), then `auphonic_apply`.
The cleaned file is one clip on a new Auphonic track, not linked to the
camera, and the originals are muted. Re-cutting later means cutting that clip
too (the user splits it along), or cleaning again.

## 6. Verify

- `frames_sheet` over the short (16 frames) after each stage, plus
  `frame_at` on every highlight and logo moment.
- `python3 ~/skills/short-edit-beacon/scripts/link_sync.py <project.beproj>` after any ripple: a clip
  Ripple Delete only closes the gap on the tracks it touched, and once shifted
  a recording's audio 35 frames late from its camera on another track.
- Report: what fills each time range, the costs (B-roll dollars, motion
  graphics on OpenAI), and the spots worth a look.
