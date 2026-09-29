# weekly-video-topics

A weekly research pass that finds YouTube video topics for the Firecrawl channel: 10 Firecrawl-specific and 10 general developer/AI ideas, each backed by evidence (engagement numbers, shipped PRs, usage stats, past channel performance) instead of guesses.

## Usage

```
/weekly-video-topics
/weekly-video-topics alexandria --days 14
```

It saves the report to `~/client-videos/firecrawl/topics/<date>.md`, keeps a `history.md` there so topics aren't re-pitched, and can scaffold a `script.md` for the topic you pick.

## Prerequisites

- `firecrawl` CLI, authenticated (search and scrape)
- `gh` CLI, authenticated (merged PRs and issues)
- Python 3 (the scripts use the standard library only)
- `agent-browser`, for the optional YouTube Studio pull

## Scripts

| Script | What it does |
|---|---|
| `scripts/hn_top.py` | Top Hacker News stories for the last N days, optionally filtered by keywords |
| `scripts/hf_papers.py` | Most-upvoted Hugging Face Daily Papers for the last N days |
| `scripts/channel_videos.py` | Latest uploads, views and likes for a channel from its public RSS feed |
| `scripts/studio_pull.sh` | Read-only YouTube Studio pull (impressions, CTR, retention, traffic sources) through agent-browser and a signed-in profile |

## Internal data

The skill also reads Firecrawl product usage (BigQuery and the product database) through scripts in `internal/`. That folder is gitignored and only exists on machines with warehouse access; without it, the skill skips the usage step and says so.
