# finish-feature

Ship a completed feature: lint, test, commit, push, PR, subagent review loop, risk-rated PR description.

## Installation

```sh
npx skills add https://github.com/RichardBray/skills --skill finish-feature
```

## Usage

```
/finish-feature
```

Runs lint/format and test gates, commits and pushes to a feature branch, opens a PR, loops a review subagent against findings (max 3 rounds), then writes a PR description with a Low/Medium/High merge-risk rating.
