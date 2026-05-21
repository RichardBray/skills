# title-score

Score a YouTube title 0-100 using a heuristic vidIQ-style breakdown.

## Installation

```sh
npx skills add https://github.com/RichardBray/skills --skill title-score
```

## Usage

```
/title-score [title to score]
```

Or run the script directly:

```bash
scripts/score.py "Your Title Here"
scripts/score.py --json "Your Title Here"
printf "Title one\nTitle two\n" | scripts/score.py -
```

Scores are based on 11 factors: length, word count, numbers, power words, sentiment, capitalisation, punctuation, stopwords, specificity, cliche penalty, and trending phrases.

**This is an approximation, not the real vidIQ score.** Mean absolute error vs real vidIQ is ~5.6 points across a 30-title calibration set.

## Trending data

The scorer can use live YouTube trending data for better results. See `SKILL.md` for setup instructions (requires a YouTube Data API key).
