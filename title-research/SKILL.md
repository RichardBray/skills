---
name: title-research
description: Research real top-performing YouTube titles for a topic with Firecrawl, extract the winning patterns, generate candidates that apply those patterns to the user's video, then rank them with the title-score skill. Use when the user wants YouTube title ideas, clickbait titles, title inspiration from what's already working, or asks to "research titles". Produces evidence-backed titles (each traced to a real high-view video) instead of guessing.
user-invocable: true
argument-hint: "[video topic] e.g. 'convex firecrawl web scraping tutorial'"
---

# title-research

Generate YouTube titles by mining what actually performs, not by guessing.

Pipeline: **research → extract patterns → generate → score → report**.

Depends on:
- `firecrawl` CLI (authenticated)
- the `title-score` skill, installed as a sibling directory of this one

Paths below are relative to **this skill's base directory**, not the user's
project. Resolve them from the SKILL.md you are reading, e.g.:

```bash
SKILL_DIR=<absolute path of the directory containing this SKILL.md>
SCORE="$SKILL_DIR/../title-score/scripts/score.py"
```

If `$SCORE` does not exist, `title-score` is not installed: say so and stop
before Step 4 rather than reporting unscored titles as ranked.

## Step 1 — Research top titles

```bash
python3 "$SKILL_DIR/scripts/research.py" "web scraping AI" --sort views
```

The script scrapes YouTube search results sorted by view count, uses
`firecrawl interact` to extract `title | channel | views`, and falls back to
`firecrawl search site:youtube.com ...` when interact fails (common: YouTube
scrape jobs die with "Job not found" or 401 consent pages).

Run 2-3 query variants for broader coverage (e.g. "web scraping AI",
"AI agent web search", "scrape anything"). If both strategies fail, tell the
user instead of inventing data.

## Step 2 — Extract winning patterns

From the highest-view titles, note concrete formulas, e.g.:

- "Use AI To Scrape ANYTHING" → [VERB] + [TECH] + To + [VERB] + ANYTHING
- "This AI Agent Can Scrape ANYTHING (100% Automatic)" → This X Can Y (promise)
- "AI Web Scraping Is Insanely Good" → X Is Insanely Good
- "How To Scrape Any Website With X" → How To + task + With + tech
- "in 10 Minutes" / "in 100 Lines" → concrete effort qualifier
- CAPS emphasis words: ANY, ANYTHING, FREE, BLIND, INFINITE

## Step 3 — Generate candidates

Apply the patterns to the user's video. Rules:

- Honor hard constraints (e.g. "must include Convex", no clickbait lies).
- Generate 10-15 candidates across at least 4 distinct patterns.
- Keep each title truthful to the actual video content.
- Reuse exact power words (ANYTHING, Insanely, FREE) and number qualifiers
  (minutes, lines, pages) from the real winners.

## Step 4 — Score and rank

```bash
printf '%s\n' "Title 1" "Title 2" ... | python3 "$SCORE" -
```

Iterate once: tweak the weakest sub-scores of the top half (add a digit, a
colon/question mark, a power word) and re-score. Keep the best 10.

## Step 5 — Report

Table ranked by score:

| # | Score | Title | Inspired by (real video + views) |

Note which sub-scores help/hurt each title, flag that the score is a
heuristic approximation (see title-score skill), and recommend the top 1-2
with a one-line rationale tying title to actual video content.

## Honesty

- Never present invented titles as "real videos". Every inspiration must come
  from Step 1 output.
- If view counts are unavailable (search fallback), say so.
- The final score is the title-score approximation, not vidIQ.
