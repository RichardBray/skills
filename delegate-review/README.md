# delegate-review

A multi-model code review skill for [Claude Code](https://claude.com/claude-code), built on top of the [`delegate`](../delegate) skill.
It runs the 8-angle review methodology (3 correctness angles, 4 cleanup angles, 1 altitude angle) with the finder agents routed to cheap models on other harnesses: correctness goes to GPT via the Codex CLI, mechanical cleanup goes to GLM 5.2 via opencode, and only the taste-heavy altitude angle stays on a Claude model.
The expensive orchestrator model verifies every candidate itself before anything reaches the report, and each finding is tagged with the model that found it.

## Prerequisites

- The `delegate` skill installed, including its `glm-runner` and `codex-runner` courier agents in `~/.claude/agents/`.
- `codex` CLI logged in (for GPT) and `opencode` CLI authenticated (for GLM 5.2).
  Missing CLIs degrade gracefully to Claude subagents, with the substitution noted in the report.
- `gh` CLI for reviewing PRs by number.

## Install

```bash
ln -s "$(pwd)/skills/delegate-review" ~/.claude/skills/delegate-review
```

## Usage

> delegate-review PR 132

You get a ranked report of at most 8 verified findings, each as `file:line - summary (failure scenario) [found by: model, verdict]`, plus a suggested routing-table tweak when a model over- or under-performed.
