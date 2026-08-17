# title-research

Generate YouTube titles by mining what actually performs, rather than guessing.

Scrapes real high-view titles for a topic, extracts the patterns that keep
showing up, applies them to your video, then ranks the candidates with the
[`title-score`](../title-score) skill. Every suggestion is traceable to a real
video, so the output is evidence-backed instead of invented.

## Installation

```sh
npx skills add https://github.com/RichardBray/skills --skill title-research
```

Install `title-score` alongside it - the ranking step calls its scorer.

## Prerequisites

- `firecrawl` CLI, authenticated.
- The `title-score` skill installed as a sibling directory.

## Usage

```
/title-research convex firecrawl web scraping tutorial
```

Or run the research step directly (standard library only, no dependencies):

```bash
scripts/research.py "web scraping AI" --sort views
scripts/research.py "convex tutorial" --limit 20 --dump
```

Output is one line per video: `title | channel | views`.

## How it works

Five steps: **research -> extract patterns -> generate -> score -> report**.

The research step scrapes YouTube search results sorted by view count and uses
`firecrawl interact` to pull title / channel / views off the rendered page.
YouTube scrapes fail often - dead job IDs, 401 consent pages - so it falls back
to `firecrawl search site:youtube.com ...`, which returns titles but no view
counts. When that happens the report says so rather than implying the numbers
are real.

Candidates are generated across at least four distinct patterns, scored with
`title-score`, tweaked once against their weakest sub-scores, and reported as a
table ranked by score with each title's real-video inspiration beside it.

## Accuracy

The final number is the `title-score` approximation, **not the real vidIQ
score** - useful for ranking variants, not for absolute values. See that
skill's README for held-out error rates.
