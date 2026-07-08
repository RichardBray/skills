---
name: delegate-review
description: Multi-model code review - the /review methodology with finder agents routed to cheap models on other harnesses (gpt via codex, glm via opencode) through the delegate skill, verified and synthesized by the main agent. Use when the user says "delegate-review", "multi-model review", or "review this PR with cheap workers".
---

# Delegate-review

Review a PR or diff with eight finder angles, but run the finders on cheap external models instead of same-model Claude subagents.
The orchestrator (you, ideally Fable/Opus - see delegate's orchestrator check) gathers the diff, writes each finder's cold-start prompt, dispatches in parallel, verifies every candidate itself, and writes the report.
If the `delegate` skill's couriers or routing table aren't already in context, load it first: invoke the `delegate` skill via the Skill tool, or read `../delegate/SKILL.md` relative to this skill's base directory (the two ship side by side). Its rules (self-contained prompts, size-bounded structured output, verify before integrating) all apply here.

## Phase 0 - Gather the diff

For a PR: `gh pr view <n> --json title,body,author,baseRefName,headRefName,state,additions,deletions,changedFiles` and `gh pr diff <n>`.
For a ref range or the working tree: `git diff <range>` / `git diff HEAD`.
The diff is the review scope.
Note the repo's absolute path and the head commit - finder prompts must reference PR-version files via `git show <commit>:<path>` and `git grep <pattern> <commit>`, never the local working tree (it may not match the PR).

## Phase 1 - Dispatch finders (parallel, one block)

Eight angles, each returning up to 6 candidates as JSON `{file, line, summary, failure_scenario}`:

Correctness (route to **gpt via codex-runner**, read-only mode - an independent model family catching what Claude-family models miss is the point):

- **A. Hunk-by-hunk scan**: read every changed line plus its enclosing function; for each line, ask what input, state, timing, or platform would make it wrong (flipped conditionals, off-by-one, null derefs, missing awaits, falsy-zero traps, copy-paste variable slips, swallowed errors, regex escaping).
- **B. Deleted-behavior audit**: for each line the diff removes or replaces, identify the guarantee it provided and hunt for where the new code restores it; a guarantee with no new home (lost guard, dropped error path, weakened validation, deleted meaningful test) is a candidate.
- **C. Blast-radius trace**: for each changed function, grep out its callers and callees at the head commit and check whether the change breaks a contract - new preconditions, altered return shapes, new exceptions, ordering assumptions.

Mechanical cleanup (route to **glm via glm-runner**):

- **Reuse**: new code that duplicates a helper the repo already ships; name the existing helper.
- **Simplification**: needless complexity the diff adds - state that could be derived, near-duplicate blocks, deep nesting, leftover dead code; name the simpler equivalent.
- **Efficiency**: waste the diff introduces - recomputed values, repeated I/O, serialized independent work, heavy work on hot/startup paths, closures that pin large scopes alive; name the cheaper form.
- **Conventions**: read the CLAUDE.md files governing the changed paths (user-level, repo root, ancestor dirs); flag only violations where the exact rule and the exact offending line can both be quoted.

Taste (route to a **Claude subagent via the Agent tool**, `model: sonnet` or better):

- **Altitude**: is each fix made at the right layer, or is it a special case patched over shared machinery? Prefer flagging shallow bandaids where generalizing the underlying mechanism is the real fix.

Prompt construction - every finder prompt is fully self-contained (external models start cold):

- PR number or ref range, absolute repo path, head commit hash.
- The exact `git show`/`git grep` commands for reading PR-version files, with an explicit "do not trust the working tree" line.
- The diff saved to a file INSIDE the repo root (e.g. `<repo>/.pr<N>-review.diff`; delete it after the run) - external CLI sandboxes reject reads outside their cwd, so a scratchpad path fails.
- The angle instructions (one angle per finder).
- The exact output contract: "Return ONLY a JSON array, max 6 objects, each `{file, line, summary, failure_scenario}`. failure_scenario is concrete inputs/state leading to a wrong outcome (for cleanup angles: the concrete cost). No narration. `[]` if nothing found."
- A convergence rule, mandatory for glm finders and cheap insurance on the rest: "Do at most 8 exploration commands, then STOP exploring and synthesize. Your FINAL message must be exactly the JSON array and nothing else - no code fences, no summary of what you did." Weak models given an open-ended hunt keep grepping until the run is cut off and never emit the JSON; the explicit budget is what forces the turn from exploration to synthesis.

Launch all finders in one message block; use `run_in_background` on the couriers.
Raw-Bash fallback gotcha: append `< /dev/null` to `codex exec` / `opencode run` in background runs, or the CLI hangs waiting on stdin and dies on timeout.
Tell finders to pass through every candidate with a nameable failure scenario - dropping half-believed candidates skips the verify phase and causes most misses.

## Phase 2 - Verify (never delegated)

Pool the candidates, dedup ones pointing at the same line/mechanism (keep the most concrete), and record which model found each survivor.
Verify each candidate yourself against the actual PR-version code, or spawn Claude subagents for it - external models do not verify.
Assign one verdict each:

- **CONFIRMED**: you can name the triggering inputs/state and quote the offending line.
- **PLAUSIBLE**: mechanism real, trigger uncertain (timing/env/config); state what would confirm it.
- **REFUTED**: the code doesn't say that, or a guard elsewhere covers it; quote the proof.

Keep CONFIRMED and PLAUSIBLE only. Cap at 8, correctness outranking cleanup when the cap forces cuts, then by severity.

## Graceful degradation

If `codex` or `opencode` is missing (courier errors with command-not-found), rerun those angles as Claude subagents with an explicit `model: haiku` (cleanup) or `model: sonnet` (correctness), and say so in the report - the attribution must stay honest.

## Report

2-3 sentence overview of what the PR does, then findings most-severe first:

`file:line - summary (failure scenario) [found by: gpt|glm|claude-<model>, verdict]`

The per-model attribution is required - it feeds delegate's routing-table calibration.
If nothing survives verification, say so.
Close with one line proposing any routing changes the run suggests (a model that aced or flunked its angles).
