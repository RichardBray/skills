# Skills

A collection of AI agent skills for content creation and developer tooling. Compatible with [Claude Code](https://claude.ai/code) and [Open Code](https://opencode.ai) via [skills.sh](https://skills.sh).

## Skills

### Content

| Skill | Command | Description |
|-------|---------|-------------|
| Tweet | `/tweet` | Generate 5 tweet options with character counts |
| Shorts Writer | `/shorts-writer` | Write short video scripts for developer-focused tech shorts |
| Longs Writer | `/longs-writer` | Write a long-form YouTube script with voice-driven workflow |
| Documentary Writer | `/documentary-writer` | Write documentary-style scripts about industry events and controversies |
| Title Score | `/title-score` | Score a YouTube title 0-100 with a vidIQ-style heuristic breakdown |
| Title Research | `/title-research` | Mine real top-performing YouTube titles for a topic, then generate and rank candidates |
| Newsletter Digest | `/newsletter-digest` | Fetch dev newsletter RSS feeds and pick the 10 best articles as YouTube video topic ideas |

### Websites

| Skill | Command | Description |
|-------|---------|-------------|
| Reference-led Websites | `/reference-led-websites` | Turn a client brief into a build prompt, then build a brand-specific site from curated references |
| Website Reference Curator | `/website-reference-curator` | Collect and maintain the shared library of website references, evidence and components |

These two are a pair: the curator owns the library, the builder reads it. Install both, ideally as siblings, and see [`reference-led-websites`](reference-led-websites/README.md) for the two-session workflow.

### Developer tooling

| Skill | Command | Description |
|-------|---------|-------------|
| Prune Context File | `/prune-context-file` | Audit and prune CLAUDE.md/AGENTS.md using evidence-based criteria |
| Sync Docs | `/sync-docs` | Update a docs site to reflect code changes on the current branch before opening a PR |
| Finish Feature | `/finish-feature` | Ship a feature: lint, test, commit, push, PR, review loop, risk-rated PR description |
| Delegate | `/delegate` | Route subtasks to other models (glm, gpt, grok, Claude subagents) with cost/quality routing |

### Working with the agent

| Skill | Command | Description |
|-------|---------|-------------|
| wdyt | `/wdyt` | Give an honest opinion without implementing anything |
| Questions | (auto) | Ask casual clarifying questions before acting on an ambiguous or question-ended request |

## Installation

Install all skills:
```sh
npx skills add https://github.com/RichardBray/skills
```

Or install individually:
```sh
npx skills add https://github.com/RichardBray/skills --skill tweet
```

Each skill directory has its own README covering usage, prerequisites and anything it needs beyond installation.
