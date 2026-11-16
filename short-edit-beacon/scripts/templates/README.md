Copy the pages you need into the project's `media/gfx/` with `base.css`, `lib.js`,
`term.css`, `term.js` and a `raw/` folder for photos and screenshots, edit the
text, timings (`window.__frame`) and image names, then
`./build.sh <gfx dir> <page name> <seconds>` and import the mp4.

- `hook-photo-title.html`: photo + yellow tag title, logos on white, resume panel with rings.
- `terminal.html`: Claude Code-style terminal (typed prompt, tool lines, rings).
- `scroll-list.html`: a real page screenshot scrolling up.
- `screens-cut.html`: cut between two real list screenshots.
- `brand-numbers.html`: Firecrawl-brand grid with a flame lockup and counting numbers.

Pages reference `raw/<file>` images and brand files under `~/fc/firebrain/packages/brand/assets/`.
