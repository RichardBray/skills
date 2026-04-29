# Skills

A collection of AI agent skills for content creation and developer tooling. Compatible with [Claude Code](https://claude.ai/code) and [Open Code](https://opencode.ai) via [skills.sh](https://skills.sh).

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| Tweet | `/tweet` | Generate 5 tweet options with character counts |
| LinkedIn | `/linkedin` | Transform content into a LinkedIn post |
| Podcast Tweet | `/podcast-tweet` | Generate a podcast episode promotion tweet |
| Shorts Writer | `/shorts-writer` | Write short video scripts for developer-focused tech shorts |
| Short Vid | `/short-vid` | Write a 30-35 second YouTube Shorts script |
| Long Vid | `/long-vid` | Write a long-form YouTube script |
| YT Titles | `/yt-titles` | Generate 10 clickbait YouTube title options |
| Prune Context File | `/prune-context-file` | Audit and prune CLAUDE.md/AGENTS.md using evidence-based criteria |
| Docs Agent Audit | `/docs-agent-audit` | Audit a docs site from an AI agent's perspective and rank PR-sized fixes |
| Title Score | `/title-score` | Score a YouTube title 0-100 with a vidIQ-style heuristic breakdown |

## Installation

Install all skills:
```sh
npx skills add https://github.com/RichardBray/skills
```

Or install individually:
```sh
npx skills add https://github.com/RichardBray/skills --skill tweet
```
