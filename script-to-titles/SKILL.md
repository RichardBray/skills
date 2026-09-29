# script-to-titles

Turn a video script into a ranked shortlist of YouTube titles plus a
keyword-loaded description. Combines live competitor research, the title-score
heuristic, and description mining in one pipeline.

Use when the user says "come up with titles for my script", "titles and
description for this video", or provides a script + asks for YouTube metadata.

## Inputs

- A script file (markdown/text). Study it fully first: topic, claims, numbers,
  gotchas, and the recap/outro. Every title must be truthful to the script.

## Step 1 — Research what performs

Run 2–3 query variants through the sibling title-research skill:

```bash
python3 /Users/robray/skills/title-research/scripts/research.py "<topic keywords>" --sort views
```

If interact fails, use the search fallback (titles still usable; note that
view counts are unknown — never invent them).

Extract concrete formulas from winners (power words, number qualifiers,
negative hooks, effort qualifiers like "in 5 Minutes").

## Step 2 — Generate TWO sets of 10

- **Set A (research-driven):** apply the winner patterns from Step 1.
- **Set B (script-driven):** written purely from the script's own language,
  numbers, and structure. No research patterns.

Both sets must stay truthful to the content.

## Step 3 — Score and rank

```bash
printf '%s\n' "T1" "T2" ... | python3 /Users/robray/skills/title-score/scripts/score.py -
```

Iterate once on the weak sub-scores of the top half (add a digit, power word,
or colon) and re-score. Keep 10 per set. Report as ranked tables with scores
and (for Set A) the real video that inspired each title. Always note the score
is a heuristic approximation of vidIQ, not the real thing.

### Owner preference weighting

Rob consistently picks **clear, searchable, comparison/educational titles**
over pure clickbait. His three picks were all of the form:

- "X vs Y: <stakes/number>" (e.g. "Firecrawl Parse vs Scrape: Don't Waste 300 Credits on 1 PDF")
- "X vs Y Explained in N Minutes"
- "X or Y? A Practical Guide to <topic>"

When generating or ranking, **boost titles that**:
- contain a "vs" / "or" comparison matching the video's core decision
- name the exact tool + keywords people search (tool name, topic noun)
- include a concrete number qualifier (credits, pages, minutes)
- promise a time-boxed explainer ("in 5 Minutes")

Down-rank vague negativity or hype that buries the searchable comparison.
Suggested manual bump: +5 to titles matching the comparison/Practical-Guide
pattern when presenting the final ranked list (state that you applied it).

## Step 4 — Similar-video research (no screenshots)

Using the firecrawl CLI:

1. `firecrawl scrape "https://www.youtube.com/results?search_query=<topic>"`
2. `firecrawl interact --prompt "List every video: URL, title, channel, view count, top 10"`
3. Pick the 3–4 closest matches. For each, pull the real thumbnail with
   `curl -sL -o research/thumb_<id>.jpg "https://i.ytimg.com/vi/<id>/maxresdefault.jpg"`
   and the description with
   `curl -sL "https://www.youtube.com/watch?v=<id>" | grep -o '"shortDescription":"[^"]*"'`
4. Do NOT use `interact` screenshots — they run in a remote sandbox and don't
   land on the local filesystem. ytimg + curl is faster and reliable.
5. Stop the session: `firecrawl interact stop`

Note the winning description formula (typically: pain/number hook →
"In this video..." → emoji bullet agenda → keyword paragraph → links →
hashtags) and thumbnail patterns.

## Step 5 — Description

Write a keyword-loaded description based on the script, following the mined
formula. Must include: the script's actual numbers and gotchas, emoji bullet
agenda of what's covered, real doc/tool links from the script, and a hashtag
block of searchable keywords. Save everything (title tables, research notes,
description) to `research/titles-and-description.md` in the project dir.

### Description link rules

Grep the script for URLs and rank them into three tiers:

- **Must include:** the product/app URL shown on screen, the GitHub repo
  (prefer the cleanest stable URL over deep `/tree/...` paths; verify the
  path still resolves before publishing), and the sponsor/referral link
  with promo code (place it high in the description).
- **Nice to have:** secondary repos or projects explicitly mentioned and
  that curious viewers will want (one line each).
- **Skip:** anchor-fragment versions of URLs already linked, deep source
  file links (fold under the parent link instead).

Also scan the script for commands viewers will want to copy (e.g. install
commands) and put them in the description as code snippets. If the outro
teases a "next video", leave a placeholder link slot for it, and note any
links the creator still needs to create (referral URL, teased video) in
the research notes.

## Naming and honesty rules (from past sessions)

- **Brand names:** when the script features a primary tool, put the brand in
  2-3 of the 10 titles (captures high-intent search traffic with near-zero
  competition), but keep pure-hook versions for browse. Sponsors/secondary
  tools (e.g. Firecrawl) never go in titles; they belong in the description
  and outro only.
- **Feature honesty:** never claim full automation the video doesn't show.
  If a human gate exists (e.g. the creator clicks merge), say "you just
  merge" or "closes issues while you sleep" instead of "auto-merge".
  The human-gate differentiator is often a selling point: lean into it.
- **Pain-point angles:** research shows "stop doing X yourself" review/
  fatigue hooks and "while I sleep" hooks outperform generic hype. Generate
  at least 2-3 titles each on: transformation (issue becomes PR), pain
  relief (stop reviewing code yourself), and passive ("while you sleep").
- **Jargon check:** prefer phrasing every viewer understands ("GitHub issues
  become merged PRs") over insider terms ("software factory", "dark factory")
  unless the title also explains itself.

## Style rule

Never use em-dashes (— or --) anywhere in generated titles, descriptions,
research notes, or the final report. Rewrite sentences or use commas,
colons, or parentheses instead.

## Deliverable

Final message: both ranked tables with scores, thumbnail/description findings,
one recommended title with a one-line rationale tied to the video content.
