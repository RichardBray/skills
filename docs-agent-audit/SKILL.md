---
name: docs-agent-audit
description: Audit a documentation website from the perspective of an AI agent consumer and produce a ranked list of PR-sized improvements. Use when the user wants to evaluate how well a docs site serves LLM agents, identify highest-leverage fixes, or prepare doc-improvement PRs. Triggers on requests like "audit these docs for agents", "how do agents consume this site", "improve docs for LLMs", or when running /docs-agent-audit.
---

# docs-agent-audit

Audit a docs site the way an AI agent actually consumes it — by trying to complete real tasks against it — then produce a ranked list of PR-sized improvements.

## Core principles

- **Behave like an agent, not an auditor.** Approach each task exactly the way you would if a user handed it to you with no mention of a docs audit. Whatever you'd naturally reach for — search, a URL guess, an index file, an MCP — do that. The audit is the recording of what happened, not a separate methodology layered on top. Findings are a byproduct of authentic task attempts.
- **Findings must be grounded in observed failure.** Every finding traces back to a moment in the task walk where the agent struggled, got wrong info, or gave up. "This page lacks X" is only a finding if the missing X cost the agent something you just watched happen.
- **Teach while working.** The user wants to understand how agents consume docs. After each logical step, give a one-line "here's what I did and why" so they can follow the reasoning without drowning in raw output.
- **PR-sized.** Every finding should map to a change one person could ship in <1 day. Rank by (impact for agents) × (ease to ship).

## Workflow

### 1. Frame the task
Ask the user (once) for:
- The docs site URL (or confirm it from project context)
- 1–3 realistic agent tasks to evaluate against, e.g. "an agent wants to scrape a JS-rendered page and get structured JSON back." If they don't have any, propose 2–3 based on the product and confirm.

Pick tasks that exercise different surfaces (quickstart/install, API reference, error handling, a less-common feature). Tasks are the whole audit — choose them deliberately.

### 2. Walk each task end-to-end, as an agent would

For each task, start cold and follow the path you'd actually take:

1. **Enter the way an agent enters.** Either a WebSearch query a user would hand the agent ("how do I do X with <product>"), or a plausible URL guess (`<product>.com/docs/<topic>`). Record which.
2. **Follow the trail.** Fetch whatever the first step surfaces. Click through as the agent would — via links in the returned content, not via navigation you inferred from having read the sidebar.
3. **Try to complete the task.** Can you assemble a working call / config / command using only what you fetched? What's missing, wrong, or ambiguous?
4. **Narrate the moment of truth.** "An agent looking for X would land here via Y. It would succeed/fail because Z." Be specific about where the trail went cold.

Use the rubric below as a lens while walking — not as a checklist to execute.

### 3. Synthesize findings

Group observed failures into PR-sized items. For each:
- **Title** (imperative, PR-ready)
- **What went wrong** (the specific task-walk moment that produced this finding)
- **Why it matters for agents** (1 sentence)
- **Rough scope** (files/sections touched)
- **Impact**: H/M/L — how much it improves agent success rate
- **Effort**: H/M/L — how much work to ship

Sort by impact desc, then effort asc. Present as a table in chat.

If during the walks you noticed something infrastructural (e.g. "search returned nothing useful and there's clearly no llms.txt funneling agents to the right pages"), that can become a finding — but only because the task walk exposed the pain, not because you went looking for the file.

### 4. Offer next step
End with: "Want me to open a PR for #1?" — don't batch multiple PRs unless asked.

## Agent-consumer rubric (lens, not checklist)

Keep these in mind while walking tasks; call them out when they bite:

- **Discoverability**: Does a realistic search query surface the right page? Is the URL stable and guessable?
- **Fetchability**: Does WebFetch return clean markdown? Code blocks preserved with language tags? Tables survive? Is content server-rendered or does it require JS?
- **Canonicalization**: One page per concept, or duplicates splitting signal?
- **Code examples**: Present above prose? Copy-pasteable? Show full request AND response?
- **Parameters/schemas**: Every field documented with type, required/optional, example value?
- **Errors**: Error codes enumerated with cause and remedy?
- **Versioning**: Clear which version the page applies to? Deprecated paths flagged?
- **End-to-end**: Can an agent go from zero to a working call using only this page?

## Narration style

- One line after each logical step, not each tool call.
- Format: "Fetched X via Y → [what happened]. [What this means for agents]."
- Skip narration for routine success; narrate surprises, dead ends, and teaching moments.
- When introducing a new concept (MCP, llms.txt if it comes up organically, etc.) on first use, give a one-sentence definition inline.

## Scope boundaries

**In scope**: content structure, URL design, code examples, error docs, schema completeness, fetchability, anything an agent hits while doing real work.

**Out of scope unless user asks**: visual design, marketing copy, i18n/translations, SEO for humans, analytics.

## Cross-session continuity

The user runs this across multiple sessions. At the start of a run, if the user references prior findings, check auto-memory for `docs-agent-audit` project entries. At the end of a run, if findings are worth carrying forward (e.g. "user decided to defer #3 until Q3"), offer to save a project memory — don't save unilaterally.
