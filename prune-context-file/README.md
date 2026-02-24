# prune-context-file

A skill for auditing and pruning bloated `CLAUDE.md` or `AGENTS.md` repository context files using evidence-based criteria.

## Installation

Install individually:
```sh
npx skills add https://github.com/RichardBray/skills --skill prune-context-file
```

Or install all skills:
```sh
npx skills add https://github.com/RichardBray/skills
```

## What it does

Analyses your context file section by section and recommends what to cut, keep, or rewrite — then rewrites it with your approval.

Trigger it by asking something like:
- "audit my CLAUDE.md"
- "trim my AGENTS.md"
- "prune my context file"

## Research basis

Based on findings from:

> **"Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"**
> Gloaguen, Mündler, Müller, Raychev, Vechev — 2025
> [arxiv.org/abs/2602.11988](https://arxiv.org/abs/2602.11988)

Key findings the skill applies:
- LLM-generated context files reduce task success rates and increase cost by 20%+
- Codebase overviews and directory listings don't help agents navigate faster
- Tooling instructions (specific commands and CLIs) are reliably followed and are the highest-value content
- Context files are redundant with existing documentation — only add what agents can't discover themselves

