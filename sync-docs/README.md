# sync-docs

Update a project's documentation to reflect code changes on the current branch before opening a PR.

## Installation

```sh
npx skills add https://github.com/RichardBray/skills --skill sync-docs
```

## Usage

```
/sync-docs
```

Discovers the project's docs location and conventions, diffs against the base branch, maps user-facing changes to doc pages, edits them, and flags anything it can't confidently map. Never auto-commits.
