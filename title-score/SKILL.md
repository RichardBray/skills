---
name: title-score
description: Score a YouTube title 0-100 using a heuristic reimplementation of the vidIQ-style title score. Use when the user asks to score, rate, grade, or evaluate a YouTube title, or wants to compare/iterate title options. Returns a numeric score with per-factor breakdown and improvement suggestions. NOT the real vidIQ score - a tunable approximation.
user-invocable: true
argument-hint: "[title to score, or list of titles]"
---

Heuristic 0-100 scorer for YouTube titles, modeled after vidIQ's title score. The exact vidIQ algorithm is proprietary; this is a transparent approximation with tunable weights.

## How to score

Run the script. It accepts a single title as an arg, or multiple titles via stdin (one per line).

```bash
scripts/score.py "Your Title Here"
scripts/score.py --json "Your Title Here"
printf "Title one\nTitle two\nTitle three\n" | scripts/score.py -
```

Output shows the final score, chars/words, and the per-factor sub-scores (length, word_count, number, power, sentiment, caps, punct, stopword, specificity, cliche).

## Refreshing trending data

The scorer uses a `data/trends.json` file for up-to-date YouTube trending phrases and topics.

### Setup (one-time)

1. Go to [console.cloud.google.com](https://console.cloud.google.com/) and create a project (or select an existing one).
2. Go to **APIs & Services > Library**, search for **YouTube Data API v3**, and enable it.
3. Go to **APIs & Services > Credentials**, click **Create Credentials > API key**, and copy the key.
4. Add it to your shell config:

```bash
# ~/.zshrc or ~/.bashrc
export YOUTUBE_API_KEY=your-key-here
```

Then `source ~/.zshrc` (or open a new terminal).

### Refreshing

```bash
python3 scripts/fetch_trends.py
```

This fetches ~150 trending video titles, extracts recurring phrases and topics, and writes `data/trends.json`. The scorer reads this file automatically. Each run uses ~700 YouTube API quota units (free tier allows 10,000/day).

If `data/trends.json` is missing or older than 14 days, the scorer falls back to a built-in static phrase list. Refresh weekly for best results.

## When the user asks to score titles

1. Run the script for each title.
2. Report each title's score plus a one-line "what's helping / what's hurting" based on which sub-scores are notably high or low.
3. If the user wants to improve a title, suggest concrete edits targeted at the weakest sub-scores (e.g., low `power` → add a curiosity/emotion word; low `length` → expand to 50-60 chars; low `specificity` → add a proper noun).

## Calibration loop

The weights and sub-score curves are best-effort, not authoritative. When the user provides real vidIQ scores for comparison:

1. Score each title with the script and tabulate: `title | our_score | vidiq_score | delta`.
2. Look for systematic bias (consistently high/low) and per-factor patterns (e.g., titles with numbers always over-scored).
3. Adjust `WEIGHTS` at the top of `scripts/score.py`, or tune the curve in the relevant sub-score function (e.g., `length_score`, `power_score`).
4. Re-run on the full set and report the new deltas.

Aim to minimize mean absolute error across the calibration set. Don't overfit to a single example.

## Factors and where they live in the script

| Factor | Function | What it measures |
|---|---|---|
| length | `length_score` | char count, peak ~50-60 |
| word_count | `word_count_score` | word count, peak ~7-9 |
| number | inline | presence of any digit |
| power | `power_score` | hits in `POWER_WORDS` set |
| sentiment | `sentiment_score` | hits in `POSITIVE`/`NEGATIVE` sets |
| caps | `caps_score` | Title Case good, ALL CAPS bad |
| punct | `punct_score` | `:` and `?` help, `!!!` hurts |
| stopword | `stopword_score` | high stopword ratio penalized |
| specificity | `specificity_score` | proper-noun-ish capitalized tokens |
| cliche | `cliche_score` | hits in `CLICHE_PHRASES` list (penalty) |
| trending | `trending_score` | hits in `data/trends.json` phrases/topics (dynamic) or `FALLBACK_TRENDING_PHRASES` (static) |

To extend vocabulary (new power words, sentiment terms), edit the sets at the top of `scripts/score.py`.

## Calibration state

Last calibrated against a 30-title corpus with real vidIQ scores. **Mean absolute error: ~5.6 points**, most titles within ±8. Known weak spots:

- Long descriptive titles (70+ chars) still tend to over-score by ~10
- "Listicle + cliché" combos ("N X That Will Change Your Life") may still over-score
- Intentionally lowercase styles ("git rebase explained in 4 minutes") under-score

Treat the score as a relative ranking signal more than an absolute number — ordering of title options tracks vidIQ well even when individual scores diverge by a few points.

## Honesty

Always tell the user this is an approximation, not the real vidIQ score, especially on first use in a session.
