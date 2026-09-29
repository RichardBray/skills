---
name: reddit-firecrawl-support
description: Find recent Reddit posts and comments where people are negative, neutral, confused, or asking for help with Firecrawl; exclude discussions already answered by u/SnooMuffins9844; verify claims; and draft friendly, useful replies. Use for fresh Firecrawl Reddit support or community-response research. Do not use for posting replies automatically.
---

# Reddit Firecrawl Support

Surface current Reddit conversations where a helpful response from someone who works on Firecrawl would add value. Research and draft only; never post, vote, message users, or otherwise mutate Reddit unless the user explicitly asks at that point.

## Defaults

- Search posts and comments published within the last three calendar months, calculated from the day the skill runs. Honor a different window when the user supplies one.
- Search broadly across relevant subreddits rather than using a fixed subreddit list.
- Exclude every post or comment chain where `u/SnooMuffins9844` has already replied. Check the full thread and nested replies, not just the opening post.
- Exclude deleted or inaccessible discussions, duplicate crossposts, obvious promotion, and threads where Firecrawl is only mentioned incidentally.
- Prefer unresolved, recent discussions where accurate advice could materially help someone.

## Research

Use available web search, Reddit search, scraping, or browser tools. A Reddit login is not normally required for public threads. If access is blocked or context is incomplete, use another available read-only method; ask the user to log in only when authentication is genuinely necessary.

Search beyond the exact word `Firecrawl`. Useful query themes include:

- Firecrawl errors, failed scrapes, timeouts, credit usage, pricing, unexpected cost, and rate limits
- self-hosting, Docker, memory usage, worker configuration, and deployment problems
- anti-bot protection, CAPTCHA, protected sites, browser rendering, and Fire-engine
- comparisons and alternatives where the author is choosing a tool
- Claude, Claude Code, MCP, Hermes, agents, RAG, research, and extraction workflows that mention Firecrawl

Open each candidate and read the full post plus the relevant comment chain before evaluating it. Do not draft from search snippets alone.

## Verify Claims

Do not guess about product behavior. Verify material technical claims against current authoritative sources. Prefer, when available:

- `/Users/robray/fc/firebrain` for internal product context
- `/Users/robray/fc/firecrawl-docs` for public documentation
- `/Users/robray/fc/firecrawl` for implementation and self-hosting details
- current official Firecrawl documentation or source when local material is stale or insufficient

Clearly separate confirmed behavior from inference. Avoid guarantees about bypassing anti-bot systems, scraping every site, performance, or cost. Mention the user's Firecrawl affiliation in proposed replies when it is relevant.

## Rank Opportunities

Return the strongest 3–5 opportunities, ordered by expected usefulness. Favor:

1. a specific unresolved problem with enough detail to diagnose;
2. a recent neutral or negative evaluation containing a correctable misconception;
3. a purchasing or architecture decision where honest tradeoffs would help;
4. an active discussion where a concise Firecrawl-specific answer is timely.

Deprioritize hostile threads with no real question, old conversations revived without new context, and discussions already answered adequately.

For each opportunity include:

- direct Reddit link and publication date;
- subreddit and author;
- concise issue summary;
- why it is worth answering;
- relevant verified facts or caveats;
- a concise, friendly draft reply.

Drafts should sound human, empathetic, and helpful. Acknowledge frustration when appropriate, answer the actual question first, disclose `I work on Firecrawl`, avoid marketing language, and invite only the diagnostic detail needed for a useful follow-up.

End with a short note listing candidates excluded because `u/SnooMuffins9844` had already replied. If no strong unanswered opportunities exist, say so rather than padding the report.
