---
name: sync-docs
description: Update a project's documentation to reflect code changes on the current branch before opening a PR. Use when the user finishes a feature/fix and is about to create a PR, or asks to "sync docs", "update the docs for these changes", or check whether documentation needs updating.
---

# Sync Docs

Bring a project's documentation in line with the code changes on the current branch, so doc updates land in the same PR as the code and get reviewed together. Project-agnostic: discover the project's doc conventions first, then apply this workflow.

## Workflow

1. **Locate the docs and learn the conventions.** Don't assume a layout — find it:
   ```bash
   git ls-files | grep -iE '(^|/)(docs?|documentation|content)/' | head -50
   ```
   Common homes: a `docs/` dir, a `packages/docs` or `website/` package (Astro/Starlight, Docusaurus, VitePress, mkdocs), a top-level `README.md`, or `man/`. Identify which generator (if any) by checking for `astro.config.*`, `docusaurus.config.*`, `mkdocs.yml`, `*.vitepress`, etc.
   - **Read any docs-specific guidance first** — a `CLAUDE.md`/`AGENTS.md`/`README.md` inside the docs dir, or a `## Docs` section in the repo's root `CLAUDE.md`. Follow its house style and gotchas.
   - **Note which files are generated** (build artifacts like `dist/`, `llms.txt`, per-page `.md` exports, API reference dumps). Never hand-edit generated output — edit the source it's built from.

2. **Get the diff.** Determine the base branch (usually `main` or `master`; check `git remote show origin` or the repo's default) and diff against it:
   ```bash
   git diff <base>...HEAD --stat
   git diff <base>...HEAD
   ```
   If on the base branch or there's no diff, stop and tell the user there's nothing to sync.

3. **Decide if docs are even in scope.** Doc-relevant changes are user-facing: CLI commands/flags, public API signatures, config options, env vars, UI flows, install/build/setup steps, and behavior changes a user would notice. Pure internal refactors, tests, and CI changes usually need no doc update — say so and stop rather than inventing edits.

4. **Map changes to pages.** For each user-facing change, find the page(s) that describe it. Grep the docs for the old name/flag/value to catch every mention:
   ```bash
   grep -rn "<old-flag-or-name>" <docs-dir>
   ```
   Renamed/removed things are the highest-value catch — stale references mislead users.

5. **Edit the source pages.** Make the smallest change that makes the docs correct. Match the existing voice, structure, and any callout/aside syntax the generator uses. If you add or rename a page, update whatever the project uses for navigation (sidebar config, `_sidebar`, frontmatter `slug`, nav YAML) and fix in-content links to it.

6. **Flag what you can't map.** If a code change clearly affects users but you can't confidently place it (or it needs a screenshot, a decision, or content you don't have), don't guess — list it for the user to handle, with the file/change and your best suggestion.

7. **Verify the build, if there is one.** If the docs are part of a buildable site, run its build to surface broken links/nav (e.g. the docs package's `build` script). This catches errors dev mode hides. Don't claim done until it passes. If there's no build step, re-read your edits for correctness.

8. **Report.** Summarize: pages edited (and why), pages checked but left unchanged, and anything flagged for the user. Leave committing/PR creation to the user unless they ask.

## Principles

- Silence-or-flag beats fabricating. A wrong doc is worse than a missing one.
- One PR, reviewable diff: doc edits go on the current branch as normal edits the user reviews — never auto-commit or auto-merge.
