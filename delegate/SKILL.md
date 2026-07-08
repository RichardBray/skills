---
name: delegate
description: Route subtasks to other models - glm-5.2 (opencode), gpt (codex exec), Claude subagents - with cost/quality routing and verification. Use when the user says "delegate", "farm this out", "have glm/codex do it", or asks to split a task across models. Not for ordinary tasks the main agent should do itself.
---

# Delegate

Split the current task into self-contained subtasks, route each to the cheapest model that meets the quality bar, run them (in parallel where independent), then verify and integrate the results.

## Orchestrator check

Before decomposing: check your own model (stated in your system prompt, e.g. "claude-sonnet-5").
This skill's routing assumes a strong orchestrator (opus-4.8 or fable-5) doing decomposition and synthesis, with cheap models on leaf work - that split is what makes delegation a net win rather than just moving cost around.

If you are not opus-4.8 or fable-5, warn the user once before proceeding:

> You're running delegate on [model]. This skill assumes a strong orchestrator (Opus/Fable) for decomposition and synthesis - on a weaker model both layers end up similar strength, which weakens the payoff. Switch to Opus or Fable for better routing/synthesis quality, or continue if this task is simple enough not to matter.

Then proceed regardless - this is a warning, not a block, unless the user says to stop.

## Model routing table

Intelligence and taste: higher = better. Cost: higher = more expensive (burns usage limit faster). All three providers are on flat subscriptions (Z.AI coding plan, ChatGPT plan via codex login, Claude subscription), so cost measures how fast a model burns its plan's usage limits, not dollars per token.

Each row wins exactly one kind of work; if a model never wins a rule below, it doesn't get a row.

| model         | cost | intelligence | taste |
|---------------|------|--------------|-------|
| glm-5.2       | 1    | 5            | 6     |
| gpt-5.x       | 3    | 8            | 6     |
| composer-2.5  | 1    | 7            | 5     |
| opus-4.8      | 5    | 7            | 8     |
| fable-5       | 8    | 10           | 7     |

Per-model caveats (from the 2026-07-06 shootout eval, `fable5-orchestrator/eval/`):

- **composer-2.5**: returns code, not finished work - never ran tests or committed in 6/6 eval cells; budget an orchestrator integration pass. Intelligence lowered 8 → 7 (0/2 automated passes and worst judge median on the migration task).
- **gpt-5.x**: codex's sandbox cannot git-commit inside worktrees - the orchestrator commits for it.
- **glm-5.2**: taste raised 5 → 6 (won or tied the blind API-design task in 3/3 runs, beating opus-4.8). Floor is low - one in nine runs collapsed lazily; always verify output.
- **opus-4.8**: most reliable executor - only lane 100% green on tests and commits (9/9), fastest edit-task median.
- **fable-5** (external research, Jun 2026, not shootout-tested): top intelligence in the field (AA Index 65 vs GPT-5.5's 60; SWE-bench Pro 80.0 vs opus's 69.2) but ~2x opus pricing ($10/$50 per M) and ~2x token burn. Taste is split: excellent vision/document formatting (beat opus head-to-head) and creative prose, but weak one-shot frontend/UI design and dense, hard-to-read spec/PRD writing. Note: if fable-5 is the current orchestrator, delegating to it is usually pointless - keep that work in the main agent.

Routing rules:

- These are defaults, not limits. Standing permission to override: if a cheaper model's output doesn't meet the bar, rerun with a smarter model without asking. Judge the output, not the price tag.
- Cost is a tie-breaker only; for anything that ships, intelligence > taste > cost.
- Bulk/mechanical work (clear-spec implementation, data analysis, migrations) and trivial lookups: glm-5.2, or gpt when the spec is fuzzy enough to need more intelligence.
- Bulk/high-volume writing (website copy, boilerplate marketing copy, first drafts across many pages): glm-5.2. Higher-stakes single pieces still need opus-4.8's taste.
- Fast agentic implementation with a decent spec (multi-file edits, terminal-heavy tasks): composer-2.5 - near-frontier agentic coding (Artificial Analysis Coding Agent Index 62 vs 65-66 for GPT-5.5/Opus-4.7 high effort, ~10-60x cheaper per task; May 2026) at glm-like cost. Intelligence and taste scores are provisional pending bake-off calibration.
- Anything user-facing (UI, copy, API design) needs taste >= 7: opus-4.8.
- Reviews of plans/implementations: opus-4.8, plus gpt via codex as an independent perspective from a different model family. Don't spawn a subagent on your own model to "review" your own work.
- Hard, single-threaded problems: keep them in the main agent; delegation overhead beats the savings. If the main agent is opus-4.8 and the problem is at the edge of its ability (deep debugging, gnarly algorithms, vision/document-formatting work), escalate that one subtask to fable-5 - but not for frontend design or long-form specs, where opus's taste wins despite fable's intelligence.

## Invocation mechanics

Non-Claude models start cold with zero conversation context. Every prompt must be self-contained: state the task, absolute file paths, constraints, and the exact output format expected. Read stdout for the result.

The output format is not optional: every delegated prompt must demand compressed, structured output with a size bound - e.g. "return a findings list (file, line, claim, evidence), max 30 lines" or "return only the final answer, no narration". Workers are filters, not pipes: compression happens at the worker so the orchestrator never pays to read raw exploration output. If a result comes back unbounded or chatty, treat that as a failed acceptance criterion and rerun with a tightened prompt.

Exploration tasks also need a convergence rule, especially on glm: "do at most N exploration commands (default 8), then STOP exploring and synthesize; your FINAL message must be exactly the requested output and nothing else". Without an explicit budget, weaker models keep gathering until the run is cut off mid-loop and return working notes instead of an answer - exit code 0, no synthesis.

**glm-5.2, gpt, and composer-2.5**: prefer the courier agents `glm-runner`, `codex-runner`, and `composer-runner` (Agent tool, `subagent_type`). Their definitions ship in this skill's `agents/` folder; if they are not registered as agent types, copy them to `~/.claude/agents/` once (new sessions pick them up automatically). - they show up in the agent UI, run in background, parallelize, and support SendMessage follow-ups. Give them the full task; they compose the cold-start prompt and relay the answer verbatim.

Raw Bash fallback (when a courier is unavailable or for a quick one-liner):

```bash
cd <dir> && opencode run -m zai-coding-plan/glm-5.2 "<self-contained prompt>"
codex exec "<self-contained prompt>"          # -s read-only: review only; --full-auto: allow edits
cd <dir> && agent -p --trust --model composer-2.5 "<self-contained prompt>"   # --mode plan: read-only
```

Add `--skip-git-repo-check` to codex outside a git repo, and `< /dev/null` to any of them when run in background (they hang waiting on stdin otherwise). Answers: glm after the `> build` banner, codex after the `tokens used` line, composer straight to stdout (`-p` prints the final answer; `--trust` skips the workspace-trust prompt that blocks headless runs; add `--output-format json` for structured output).

**Claude models**: Agent tool with `model: haiku|sonnet|opus|fable`. Always prefer this over `claude -p` inside a session - subagents get tool access, parallel launch, background tracking, and SendMessage continuation. Use `claude -p "<prompt>" --model <model>` only from scripts/hooks outside a session, or when a run needs custom flags (e.g. `--append-system-prompt`) isolated from the current session.

**Courier vs raw Bash - pick per task, not by default:** couriers (haiku-driven) run in background, parallelize, show in the agent UI, and support SendMessage follow-ups, but they're a relay through a weaker model that can occasionally drop a formatting instruction (e.g. skip the `[model | status]` prefix). Raw Bash is synchronous and blocks your turn, but what you read is the literal CLI output - nothing summarized or possibly mangled in between.

- Parallel/independent/background-worthy subtasks, or anything where you'll want to SendMessage a follow-up: courier.
- A single quick lookup, or anything where you need to see the exact unfiltered CLI output (debugging the delegation itself, verifying a courier's claim, a one-off sanity check): raw Bash.
- If a courier's result looks off (missing prefix, chatty, unbounded) - don't retry the same courier blind. Either tighten the prompt, or re-run the same task via raw Bash to see the ground truth and confirm whether the courier or the underlying model was at fault.

## Workflow

1. Decompose the task into subtasks; note which are independent (parallelizable) and which are sequential.
2. Route each subtask with the table above.
3. Write self-contained prompts. Include acceptance criteria so output quality is checkable, and a bounded output format (see invocation mechanics) so results come back compressed.
4. Launch independent subtasks in parallel (multiple Bash/Agent calls in one block; `run_in_background` for long ones).
5. Verify every result before integrating - run the code, check the claims. Escalate to a smarter model on failure rather than patching mediocre output.
6. Integrate and report: which model did what, what was verified, anything escalated.
7. When a model repeatedly fails at or aces a task type, propose an update to its scores in the routing table - real delegations are the eval.
