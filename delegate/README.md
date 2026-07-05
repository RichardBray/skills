# delegate

A [Claude Code](https://claude.com/claude-code) skill that turns the main agent into an orchestrator.
It splits a task into subtasks and routes each one to the cheapest model that meets the quality bar - GLM 5.2, GPT via Codex, or Claude subagents - then verifies the results before integrating them.

## What's inside

- `SKILL.md` - the skill: a model routing table (cost / intelligence / taste), routing rules, invocation mechanics, and a six-step orchestration workflow.
- `agents/glm-runner.md` and `agents/codex-runner.md` - courier agents.
  Thin Haiku subagents that wrap the external CLIs so they behave like first-class Claude Code subagents: agent UI, background runs, parallelism, follow-up messages.

## Prerequisites

- [opencode](https://opencode.ai) CLI authenticated with a Z.AI coding plan (for GLM 5.2).
- [codex](https://github.com/openai/codex) CLI logged in with a ChatGPT plan or OpenAI API key (for GPT).
- Missing one? The skill routes around it with the models you have.

## Install

```bash
git clone https://github.com/RichardBray/skills
ln -s "$(pwd)/skills/delegate" ~/.claude/skills/delegate
cp skills/delegate/agents/*.md ~/.claude/agents/
```

Start a new Claude Code session and the skill plus both couriers register automatically.

## Usage

Say things like:

- "delegate: migrate these 40 test files to vitest"
- "have glm implement the endpoints from this spec"
- "get codex to review this diff as a second opinion"

The routing table assumes flat-rate subscriptions on all three providers.
If your billing differs (e.g. per-token API keys), adjust the cost column in `SKILL.md` - it's a starting hypothesis, not gospel.

## Calibrating the table

The table self-corrects from real work: the workflow's last step proposes score changes when a model repeatedly fails or aces a task type.
To deliberately benchmark a new model, run a bake-off:

> Delegate this same task to glm, gpt, and \<new model\> in parallel.
> Compare the outputs on correctness, completeness, and how much fixing each needed.
> Report a comparison table and suggest routing-table score changes.

Run it on two or three tasks representative of your actual work - that beats synthetic benchmarks for deciding your routing.
