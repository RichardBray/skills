---
name: delegate
description: Route subtasks to other models - glm-5.2 (opencode), gpt (codex exec), Claude subagents - with cost/quality routing and verification. Use when the user says "delegate", "farm this out", "have glm/codex do it", or asks to split a task across models. Not for ordinary tasks the main agent should do itself.
---

# Delegate

Split the current task into self-contained subtasks, route each to the cheapest model that meets the quality bar, run them (in parallel where independent), then verify and integrate the results.

## Model routing table

Higher = better on every axis; a high cost score means cheap to use. All three providers are on flat subscriptions (Z.AI coding plan, ChatGPT plan via codex login, Claude subscription), so cost measures how fast a model burns its plan's usage limits, not dollars per token.

Each row wins exactly one kind of work; if a model never wins a rule below, it doesn't get a row.

| model     | cost | intelligence | taste |
|-----------|------|--------------|-------|
| glm-5.2   | 9    | 7            | 5     |
| gpt-5.x   | 7    | 8            | 6     |
| opus-4.8  | 5    | 7            | 8     |
| fable-5   | 3    | 9            | 9     |

Routing rules:

- These are defaults, not limits. Standing permission to override: if a cheaper model's output doesn't meet the bar, rerun with a smarter model without asking. Judge the output, not the price tag.
- Cost is a tie-breaker only; for anything that ships, intelligence > taste > cost.
- Bulk/mechanical work (clear-spec implementation, data analysis, migrations) and trivial lookups: glm-5.2, or gpt when the spec is fuzzy enough to need more intelligence.
- Anything user-facing (UI, copy, API design) needs taste >= 7: opus-4.8 or fable-5.
- Reviews of plans/implementations: fable-5 or opus-4.8, plus gpt via codex as an independent perspective from a different model family.
- Hard, single-threaded problems: keep them in the main agent (fable-5); delegation overhead beats the savings.

## Invocation mechanics

Non-Claude models start cold with zero conversation context. Every prompt must be self-contained: state the task, absolute file paths, constraints, and the exact output format expected. Read stdout for the result.

**glm-5.2 and gpt**: prefer the courier agents `glm-runner` and `codex-runner` (Agent tool, `subagent_type`). Their definitions ship in this skill's `agents/` folder; if they are not registered as agent types, copy them to `~/.claude/agents/` once (new sessions pick them up automatically). - they show up in the agent UI, run in background, parallelize, and support SendMessage follow-ups. Give them the full task; they compose the cold-start prompt and relay the answer verbatim.

Raw Bash fallback (when a courier is unavailable or for a quick one-liner):

```bash
cd <dir> && opencode run -m zai-coding-plan/glm-5.2 "<self-contained prompt>"
codex exec "<self-contained prompt>"          # -s read-only: review only; --full-auto: allow edits
```

Add `--skip-git-repo-check` to codex outside a git repo. Answers: glm after the `> build` banner, codex after the `tokens used` line.

**Claude models**: Agent tool with `model: haiku|sonnet|opus|fable`. Always prefer this over `claude -p` inside a session - subagents get tool access, parallel launch, background tracking, and SendMessage continuation. Use `claude -p "<prompt>" --model <model>` only from scripts/hooks outside a session, or when a run needs custom flags (e.g. `--append-system-prompt`) isolated from the current session.

## Workflow

1. Decompose the task into subtasks; note which are independent (parallelizable) and which are sequential.
2. Route each subtask with the table above.
3. Write self-contained prompts. Include acceptance criteria so output quality is checkable.
4. Launch independent subtasks in parallel (multiple Bash/Agent calls in one block; `run_in_background` for long ones).
5. Verify every result before integrating - run the code, check the claims. Escalate to a smarter model on failure rather than patching mediocre output.
6. Integrate and report: which model did what, what was verified, anything escalated.
7. When a model repeatedly fails at or aces a task type, propose an update to its scores in the routing table - real delegations are the eval.
