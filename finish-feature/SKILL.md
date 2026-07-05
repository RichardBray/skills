---
name: finish-feature
description: Ship a completed feature - lint, test, commit, push, PR, subagent review loop, risk-rated PR description. Use when the user says "finish this feature", "ship it", "wrap this up", or "create the PR".
---

# Finish Feature

Ship the current working-tree feature through gates, PR, review loop, and a risk-rated description.
Steps run in order; a failed gate stops the pipeline and reports to the user.

## Step 1: Lint and format gate

Prefer the repo's own tooling. Check `package.json` scripts (and workspace packages) for `lint`, `format`, `check` scripts and run them.
If none exist and the code is TS/JS, fall back to `bunx oxlint` and `bunx oxfmt --write` (or `npx` if bun is unavailable) on the changed files.
Never install oxlint/oxfmt into the project or expect them to be dependencies - always run them via bunx/npx.
Fix any errors they report before continuing. Non-JS repos: use the repo's configured linter or skip.

## Step 2: Test gate (hard)

Run the repo's test suites relevant to the change (unit, integration, e2e - check `package.json` scripts and project CLAUDE.md for commands).
All tests must pass. If tests fail and the failure is caused by the feature, fix it and re-run.
If failures are pre-existing on the base branch, note them and continue.
Never skip, comment out, or weaken a test to get past this gate - stop and report instead.

## Step 3: Commit, push, PR

1. Confirm on a feature branch - never commit to main. If on main, create a branch (`feature/...` or `fix/...`).
2. Commit with Conventional Commits format: `<type>(<scope>): <description>`. No co-author lines, no agent attribution.
3. Push and open a PR against main with `gh pr create`. Use a short placeholder body - the real description is written in Step 5.

## Step 4: Review loop

Spawn a general-purpose subagent to review the PR. Prompt it with:

> Review PR #<n> (`gh pr diff <n>`) for correctness bugs, behavior changes beyond the stated scope, missing test coverage, security issues at trust boundaries, and needless complexity. Return a ranked list of findings, each with file:line, the problem, and a suggested fix. Return "CLEAN" if nothing found.

Then loop (max 3 rounds):

1. Main agent addresses each finding: fix it, or record a one-line reason for rejecting it (false positive, intentional).
2. Re-run lint and tests on any fixes, commit and push.
3. Spawn a fresh review subagent on the updated diff.
4. Stop when the review returns CLEAN or after round 3 - carry any remaining findings into the description as known issues.

Keep a running log of every finding and its resolution (fixed / rejected+why / open) for Step 5.

## Step 5: PR description

Rewrite the PR body with `gh pr edit <n> --body`:

```markdown
## Summary
<what the feature does, 2-4 sentences>

## Review findings
<per finding: what was found, what changed in response; or "Review came back clean">
<any open/rejected findings with reasoning>

## Merge risk: **High | Medium | Low**
<2-4 sentences justifying the rating and telling the reviewer what to double-check>
```

Risk rubric - rate by blast radius and how much human double-checking is warranted:

- **Low**: isolated/leaf code (single page, one component), no schema/auth/backend changes, behavior change matches stated scope, tests cover it. Skim is enough.
- **Medium**: touches shared services or code many callers use, minor behavior changes beyond stated scope, new duplication with sync burden, or partial test coverage. Review the flagged spots.
- **High**: schema migrations, auth/permission changes, grading/payment/data-integrity logic, wide refactors, or review findings left open. Line-by-line review needed.

Also flag in the risk section: behavior changes beyond the stated fix, and any intentional duplication (where, and what must stay in sync).

Finish by reporting the PR URL, final risk rating, and a one-line summary of the review loop (rounds run, findings fixed/open) to the user.
