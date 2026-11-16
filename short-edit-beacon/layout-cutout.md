# Layout: presenter cutout over full-screen screens (the Hormozi short)

Reference project: `~/client-videos/firecrawl/shorts/hormozi-short.beproj`
(tracks: Backgrounds, camera, audio, Auphonic, Motion graphics, Captions; its
screen sources are in `media/gfx/`). Used for the Gates short in
`~/client-videos/firecrawl/shorts/friend-job-search/gates-job.beproj`.

The presenter is cut out (remove-background) at the bottom, and a 1080x1920
screen plays behind him. The visible part above his head is the top ~1000 px:
keep everything that matters above y 1000.

## Tracks, bottom to top

Backgrounds (full-frame screens), Motion graphics (overlays that replace a
screen for part of its length), camera video, camera audio, Captions, and the
Auphonic track after the clean.

## Presenter (4K camera, face near x 2000)

| Shot | scale | x | y | crop (left / top / right / bottom) |
|---|---|---|---|---|
| Cutout, bottom right | 0.44 | 120 | -518 | 1000 / 150 / 940 / 0 |
| Plain bottom half, room visible | 0.4444 | -36 | -480 | 785 / 0 / 625 / 0 |
| Full screen | 0.8889 | -72 | 0 | 1393 / 0 / 1232 / 0 |

- Crop does not re-centre the clip: after an uneven crop set
  `x = -(left - right) / 2 x scale`, or a black strip shows on one edge.
- Cutout = `remove-background` on every camera clip: `background transparent,
  blur 0.5, softness 0.3, shrink 0.05`. Beacon makes one matte per recording
  (about 8 minutes for 200 s of footage, all recordings in parallel, see
  `job_status` kind `matte`). Add the effect to every clip first, build the
  screens while the mattes run, then judge the look.
- Plain bottom half and full screen have no effect and show the real room.
  Use them for hook beats the user marks ("don't use background remove, centre
  my face on the bottom half", "full screen the camera here"); the cutout
  returns after them.

## Captions

`captions_create`, `maxWords` 4: font Montserrat 700, size 58, colour white,
background `[0,0,0,0]`, cornerRadius 21, anchorY bottom, offsetY 330,
maxWidth 0.8, reveal phrase, enter and exit none, shadow `[0,0,0,1]` blur 7
distance 0 angle -90 (the tool takes degrees), emphasis colour
`[1,0.84,0.2,1]` weight 800, highlight alpha 0. White text vanishes on a light
screen: give every light screen a dark gradient over its bottom
(`linear-gradient(rgba(20,20,20,0), rgba(20,20,20,.85) 40%, rgba(20,20,20,.92))`
from y 1040).

## Screens

One HTML page per screen, `window.__frame(t)` drives it, rendered by
`scripts/render-html.ts` through `scripts/templates/build.sh`. Start from the
templates in `scripts/templates/`:

- `hook-photo-title.html`: photo with a yellow keyword tag and a white title;
  the logos-on-white beat and the resume panel with red rings.
- `terminal.html`: Claude Code-style terminal (`term.js`) with typed prompt,
  tool lines and red rings. State in the report that it is a recreation, and
  only show queries and results that really ran.
- `scroll-list.html` and `screens-cut.html`: a real page screenshot scrolling
  or cutting between lists.
- `brand-numbers.html`: Firecrawl-brand counter graphic (see
  `claims-and-assets.md` for the brand values).

Time each page from `transcript_get` words (page time 0 = the clip's start),
and re-time after the user trims. A screen the user replaces with real pages
(postings, search results) comes from `scripts/shot-clean.ts`.

Overlays on the Motion graphics track hide the screen under them: if the
terminal was typing there, re-time the terminal so the typing finishes before
the overlay and the tool lines land after it.
