# scenes.json reference

`scenes.json` is `{ "tail": 1.2, "scenes": [ ... ] }`. Scenes play in order. The first starts at 0; every other scene has a `from` phrase, and it starts where that phrase is first spoken after the previous scene began. A scene ends where the next starts. `tail` is seconds of picture after the last word.

Phrases (`from`, `at`, `to`) are consecutive words from the script, lowercase, punctuation ignored, e.g. `"the second time i told"`. They are matched against the aligned voiceover, so editing the script or re-recording never breaks timing, but a phrase that is no longer spoken makes the render stop with "anchor not found". Keep phrases specific enough to be unique after the previous scene started. `at` marks where an item appears; `to` marks where it ends (the end of the last word of the phrase).

Captions are always on, in the safe area (y 1180-1480). Scenes fill the top of the frame (y 130-1100), so keep visuals to that zone and never repeat the caption text.

| type | shows | fields |
|---|---|---|
| `logos` | grid of 12 logo tiles, a `?`, one tile highlighted | `logos` (12 names of `assets/png/<name>.png`), `pick` (index) |
| `prompt` | chat prompt box with typed text | `chip`, items: `type` {text, at, to}, `append` {text, at}, `note` {html, at, sfx} |
| `terminal` | log panel with lines, a running timer, stat cards | `title`, `accent` (orange border), items: `line` {html, at, sfx}, `timer` {value, at, to}, `stat` {value, label, at, color} |
| `compare` | two bars growing | `sides` [{name, color, fill, frac, value, unit, dec}] x2, items [{at},{at}] |
| `chips` | stacked cards that pop in | items [{tag, text, at}] (up to 4) |
| `cta` | flame logo, wordmark, URL | none (needs `assets/logos/firecrawl-logo.svg`) |

`html` fields take `<span class="o|g|r|y|d">` for orange, green, red, yellow, dim.

Every visual must be true to something that actually happened: numbers, commands and outputs come from real runs or real data, never invented. Sound effects come from the same anchors: the render writes `events.json` and `sfx.py` turns it into audio.
