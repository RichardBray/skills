---
name: title-score
description: Score a YouTube title 0-100 using a model fitted to real vidIQ title scores, for tech/AI/developer titles. Use when the user asks to score, rate, grade, or evaluate a YouTube title, or wants to compare/iterate title options. Returns a numeric score with a per-factor breakdown and improvement suggestions. An approximation of vidIQ, not the real API.
user-invocable: true
argument-hint: "[title to score, or list of titles]"
---

Offline 0-100 scorer for YouTube titles, fitted by ridge regression against
real vidIQ scores on a 360-title tech / AI / developer corpus.

Runtime needs only the Python standard library.

## How to score

```bash
scripts/score.py "Your Title Here"
scripts/score.py --json "Your Title Here"
printf "Title one\nTitle two\n" | scripts/score.py -
```

Output gives the score, chars/words, `vocab` (how much the topic words moved
it), and the named factors that mattered most.

## How to report results

1. Run the script for every title at once via stdin.
2. Give each score plus one line of what is helping and what is hurting, taken
   from the largest contributions.
3. **Lead with the ranking, not the numbers.** Ordering is what this model does
   well (76% accurate on same-topic pairs); absolute scores are off by ~7
   points on a fresh title.
4. Say once per session that this approximates vidIQ rather than reproducing
   it. If the exact number matters, `vidiq_score_title` is authoritative at
   5 credits a call.

## How to improve a title

Ranked by what actually moved the real vidIQ score in minimal-pair testing:

- **Add second-person accusation or a first-person result.** The biggest lever
  by far: `Redis Persistence` 72 -> `Your Redis Persistence Config Is Wrong` 92.
- **Don't just append "Explained".** Near zero effect, sometimes negative.
- **Don't sand off the clickbait.** vidIQ rewards caps, exclamation marks, and
  "for beginners" rather than punishing them.
- **Avoid bare two-word titles**, and dry openers like "Understanding..." or
  "Introduction to...".
- Aim for a real sentence rather than a noun phrase; length helps up to a point.

## Limits that change how you should answer

- **Long-form only.** The corpus was built entirely with `type="long"`. Do not
  trust this for Shorts.
- **No channel context.** It approximates vidIQ's generic scorer, not the score
  for any specific channel.
- **Ranking >> absolute.** True-holdout error is ~7 points / 9.9%. Never
  present the number as if it were vidIQ's own.

## Calibration

`data/calibration.json` is the labeled corpus, `data/model.json` the fitted
weights.

```bash
uv run --with numpy python scripts/calibrate.py          # report only
uv run --with numpy python scripts/calibrate.py --write  # refit data/model.json
uv run --with numpy python scripts/calibrate.py --demo   # self-check the solver
uv run --with numpy python scripts/eval_ranking.py       # ranking accuracy
```

Report held-out MAE, never in-sample - the n-gram block memorizes training
titles, so in-sample error badly understates real error.

To add data: score titles with the real `vidiq_score_title` MCP tool, append
`{"title": ..., "vidiq": ...}` rows to `data/calibration.json`, then refit.
Check the learning curve in `RESEARCH.md` first - past ~350 rows the return is
very small.

## Further reading

`RESEARCH.md` holds the full reverse-engineering writeup: what vidIQ does and
does not publish, every measured finding with its evidence, accuracy and
ranking tables, approaches that were tried and failed, and the highest-value
next steps. Read it before changing the model or spending credits.
