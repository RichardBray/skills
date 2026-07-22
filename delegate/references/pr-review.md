# PR review: parallel independent review

Recipe for reviewing a PR/diff with two model families, verified and triaged before anything is fixed.

## Why not a live cross-model session

Two models chatting live over the same diff looks appealing but is worse than two blind one-shot reviews:

- No parallelism - panes alternate turns; couriers run at once.
- Groupthink risk - once model A states a finding, model B tends to defer rather than independently re-derive it from the diff. Independence is the bias check; live visibility removes it.
- The actual value ("catch model A's mistake") already happens at synthesis, when the orchestrator verifies every claim against source - see the verification step below. That step does the work, not the back-and-forth.

## Workflow

1. **Launch two parallel couriers**, different model families, same diff, same bounded findings format. Default pair: `codex-runner` (gpt) + `grok-runner` (grok-4.5). If codex-runner is unavailable (e.g. model-id errors, see `references/codex-troubleshooting.md`), fall back to `glm-runner` + `grok-runner` - never two couriers on the same underlying model, and never a courier on the orchestrator's own model reviewing its own work.
2. **Findings format** (demand this in both prompts): a list of `file:line - severity (critical/high/medium/low) - claim - one-line evidence`, capped (e.g. max 25 lines each). No narration, no praise, no fix suggestions yet.
3. **Merge and dedupe** the two lists. Overlapping findings from both models raise confidence; a finding only one model raised isn't discarded, just flagged as single-sourced.
4. **Verify every claim against the actual source** before repeating it - open the file, confirm the line and the claimed defect are real. This is the step that catches a model's hallucinated or stale finding; a claim that doesn't survive a source read is dropped, not downgraded.
5. **Triage by severity.** Critical/high: must fix before merge. Medium: fix or explicitly accept. Low: optional, note and move on.
6. **Confirmed fixes → cheap courier** (`glm-runner`) applies them, runs the test suite, and reports pass/fail. Don't hand-fix trivial stuff yourself if a cheap model can.
7. **Report to the user**: what was found, what was fixed, what's still open, and a mergeable/not-mergeable verdict.

## Auto-land vs pause

Default: pause for user go-ahead before pushing any fix rated above "low" severity, especially on a branch that's already an open PR. Low-severity fixes (typos, comment nits) can auto-land. The user can override this default for a given task by explicit instruction - that override applies only to the task at hand and doesn't carry over to future PRs unless they say so.
