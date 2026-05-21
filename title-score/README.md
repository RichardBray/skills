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

The scorer can use live YouTube trending data for better results. This requires a YouTube Data API key.

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

### Refreshing trends

```bash
python3 scripts/fetch_trends.py
```

This fetches ~150 trending video titles and writes `data/trends.json`. Each run uses ~700 YouTube API quota units (free tier allows 10,000/day). If the file is missing or older than 14 days, the scorer falls back to a built-in static phrase list.
