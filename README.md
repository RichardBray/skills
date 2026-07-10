# Skills

A collection of AI agent skills for content creation and developer tooling. Compatible with [Claude Code](https://claude.ai/code) and [Open Code](https://opencode.ai) via [skills.sh](https://skills.sh).

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| Tweet | `/tweet` | Generate 5 tweet options with character counts |
| Shorts Writer | `/shorts-writer` | Write short video scripts for developer-focused tech shorts |
| Longs Writer | `/longs-writer` | Write a long-form YouTube script with voice-driven workflow |
| Documentary Writer | `/documentary-writer` | Write documentary-style scripts about industry events and controversies |
| Prune Context File | `/prune-context-file` | Audit and prune CLAUDE.md/AGENTS.md using evidence-based criteria |
| Title Score | `/title-score` | Score a YouTube title 0-100 with a vidIQ-style heuristic breakdown |
| Newsletter Digest | `/newsletter-digest` | Fetch dev newsletter RSS feeds and pick the 10 best articles as YouTube video topic ideas |
| Sync Docs | `/sync-docs` | Update a docs site to reflect code changes on the current branch before opening a PR |
| Finish Feature | `/finish-feature` | Ship a feature: lint, test, commit, push, PR, review loop, risk-rated PR description |
| Delegate | `/delegate` | Route subtasks to other models (glm, gpt, grok, Claude subagents) with cost/quality routing |
| Delegate Review | `/delegate-review` | Multi-model code review across several LLMs |
| wdyt | `/wdyt` | Give an honest opinion without implementing anything |

## Installation

Install all skills:
```sh
npx skills add https://github.com/RichardBray/skills
```

Or install individually:
```sh
npx skills add https://github.com/RichardBray/skills --skill tweet
```
