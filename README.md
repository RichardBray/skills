# Skills

A collection of AI agent skills for content creation and developer tooling. Compatible with [Claude Code](https://claude.ai/code) and [Open Code](https://opencode.ai) via [skills.sh](https://skills.sh).

## Skills

### Content

| Skill | Command | Description |
|-------|---------|-------------|
| Tweet | `/tweet` | Generate 5 tweet options with character counts |
| Shorts Writer | `/shorts-writer` | Write short video scripts for developer-focused tech shorts |
| Say as Me | `/say-as-me` | Speak a script in your own cloned voice (Qwen3-TTS on Replicate) |
| Short Edit | `/short-edit` | Edit a recorded talking-head short: 1.2x speed-up, green-screen paper-cutout animation, phrase captions with logo pops, Shorts title research, descriptions and thumbnails |
| Short | `/short` | Make a vertical 9:16 YouTube Short from a topic or script: editable script, cloned or recorded voice, captions, motion graphics, music, sound effects |
| Title Score | `/title-score` | Score a YouTube title 0-100 with a vidIQ-style heuristic breakdown |
| Title Research | `/title-research` | Mine real top-performing YouTube titles for a topic, then generate and rank candidates |

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
| New Project | `/new-project` | Start a project on the usual stack (Astro, React, Electrobun, Rust, Bun) and set up agent-harness |
| Verify | `/verify` | Check a change end to end in the running app with Agent Browser, or computer use for native parts |
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

## Working on these skills locally

`scripts/link.sh` symlinks every skill in this repo into `~/.claude/skills` and `~/.claude-work/skills` (or the config dirs you pass it), so edits here are live with no install or sync step. Rerun it after adding a skill. It also removes these skills from the `npx skills` lock file, so `npx skills update` won't overwrite the links with copies from GitHub.

```sh
scripts/link.sh
```

## Usage telemetry (optional, Claude Code only)

`scripts/log-skill-use.sh` is a hook that appends every skill use to `<config-dir>/skill-usage.jsonl`, whether the agent loads the skill or you type `/skill-name`. It takes the config dir as an argument (default `~/.claude`) and needs `jq`. Add it to each config dir's `settings.json`:

```json
"hooks": {
  "PostToolUse": [
    { "matcher": "Skill", "hooks": [{ "type": "command", "command": "/path/to/skills/scripts/log-skill-use.sh ~/.claude" }] }
  ],
  "UserPromptSubmit": [
    { "hooks": [{ "type": "command", "command": "/path/to/skills/scripts/log-skill-use.sh ~/.claude" }] }
  ]
}
```

Then see what you actually use:

```sh
uv run scripts/skill-stats.py                      # ~/.claude and ~/.claude-work, all time
uv run scripts/skill-stats.py --days 30            # recent only
uv run scripts/skill-stats.py --config ~/.claude   # one config dir
```

It also backfills from existing Claude Code transcripts, which are only kept for about 30 days by default, so the log is what builds long-term history. Skills in this repo with no recorded use are listed at the end.
