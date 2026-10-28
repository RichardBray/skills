---
name: reddit-firecrawl-support
description: Find recent Reddit support discussions about Firecrawl and relevant problems that never mention it, including opportunities for Alexandria, search, scraping, and other verified features. Discover relevant subreddits, exclude discussions already answered by u/SnooMuffins9844, and draft useful replies. Research only, no automatic posting.
---

# Reddit Firecrawl Support

Surface current Reddit conversations where a helpful response from someone who works at Firecrawl would add value. Research and draft only; never post, vote, message users, or otherwise mutate Reddit unless the user explicitly asks at that point.

## Defaults

- Search posts and comments published within the last three calendar months, calculated from the day the skill runs. Prefer exact publication timestamps from the live page; cached relative ages are not reliable dates. Honor a different window when the user supplies one.
- Search broadly across relevant subreddits rather than using a fixed subreddit list.
- Exclude every post or comment chain where `u/SnooMuffins9844` has already replied. Check the full thread and nested replies, not just the opening post. Match comment authors inside the discussion; a logged-in username in the sidebar, flair picker, or navigation is not evidence of a reply.
- Exclude deleted or inaccessible discussions, duplicate crossposts, obvious promotion, and threads with no concrete problem that Firecrawl can help solve. An incidental mention alone is not a reason to include a thread, and no Firecrawl mention is required.
- Prefer unresolved, recent discussions where accurate advice could materially help someone.

## Research

Use available web search, Reddit search, scraping, or browser tools. A Reddit login is not normally required for public threads. If access is blocked or context is incomplete, use another available read-only method; ask the user to log in only when authentication is genuinely necessary.

Run both discovery tracks unless the user explicitly narrows the scope:

1. **Direct support:** Firecrawl mentions, errors, neutral comparisons, confusion, and correctable claims.
2. **Problem-first discovery:** posts and comments that do not mention Firecrawl, in any relevant subreddit, where a verified capability could address a specific need. Use problem-language queries without the brand and additional `-firecrawl` searches. Inspect the thread to establish whether it actually lacks a Firecrawl mention; a query filter alone is not evidence. Discover communities from results and report promising subreddits with linked examples, rather than searching only scraping or Firecrawl communities.

For problem-first searches, vary themes across web data for agents/RAG, structured extraction, JavaScript pages, site discovery, changing prices or jobs, company research, product catalogs, government records, economic data, research papers, coding documentation, and podcast transcripts. These are search leads, not promises of coverage. Use only the themes relevant to actual unresolved questions.

Useful direct-support query themes include:

- Firecrawl errors, failed scrapes, timeouts, credit usage, pricing, unexpected cost, and rate limits
- self-hosting, Docker, memory usage, worker configuration, and deployment problems
- anti-bot protection, CAPTCHA, protected sites, browser rendering, and Fire-engine
- comparisons and alternatives where the author is choosing a tool
- Claude, Claude Code, MCP, Hermes, agents, RAG, research, and extraction workflows that mention Firecrawl

### Company intelligence and Alexandria discovery

Include a company-intelligence and enrichment discovery pass each run, alongside direct Firecrawl support. Look for people choosing data sources or asking what others use for KYB, due diligence, company research, firmographics, and person/company enrichment. Search beyond scraping communities, including OSINT, business research, sales operations, and automation communities discovered in results.

Use the author's problem and alternative tools as search terms. Examples (apply the run's date window):

- `company intelligence KYB enrichment`
- `company name domain registration number API`
- `company enrichment dedicated APIs OpenCorporates Crunchbase`
- `Apify company info actor alternatives`
- `due diligence company data sources`

Run some searches without Firecrawl or Alexandria in the query. A post describing another tool and asking “what are you using?” can be a useful comparison opportunity, even when the author reports positive results or links an Apify actor. Read the actual question before classifying it as promotion. A sponsored placement is a promotion signal to record, not proof that the underlying discussion has no useful question; exclude pure advertisements without a substantive discussion.

Calibration example: [Anyone using Apify for company intelligence / KYB enrichment?](https://www.reddit.com/r/GreatOSINT/comments/1wclfda/anyone_using_apify_for_company_intelligence_kyb/). The useful intent is choosing company data by name, domain, or registration number and comparing APIs, registries, and actors. Use it to guide discovery, not as an evergreen recommendation to reply to that thread.

Match Alexandria to the requested fields and identifiers before drafting. Verify company enrichment and official registry tools separately; do not imply that firmographics establish legal identity, ownership, sanctions status, or complete KYB. Name/domain/registration-number support and jurisdiction coverage depend on the selected contract.

### Discovery and candidate review

Use both broad web discovery and Reddit's newest posts and comments search when available. Include neutral comparisons, architecture guides, benchmarks, and extraction or search API discussions alongside error reports. Treat subreddits discovered in results as leads to investigate, not a fixed allowlist. Communities such as r/ProxyEngineering, r/SearchAPIs, and r/Rag are examples, not required or exhaustive coverage.

Open every plausible recent candidate in the results you inspect before deciding whether to include or exclude it. A comparison-style title is not evidence of promotion. Read the body for a concrete question or correctable Firecrawl claim, such as unsupported claims about search capabilities, browser rendering, or guaranteed anti-bot success. Judge promotion from the post's actual purpose and content; a promotional reply does not make the opening post promotional.

Read the full post and available nested replies. Do not draft from search snippets alone. Recheck shortlisted threads live when possible: saved comments and search indexes can miss newer replies from `u/SnooMuffins9844`. Check duplicate crossposts for prior replies and avoid proposing the same answer in another copy. If a comment count exceeds the visible replies, try another read-only view; if it remains incomplete, mark the prior-reply check as unverified rather than calling the thread unanswered.

Keep a compact candidate ledger in the research notes: URL, date, subreddit, author, issue or correction, prior-reply check (including completeness), discovery track, matching capability and evidence, community-rule check, and disposition (shortlisted, excluded with reason, or unverified). For search-result exclusions, record enough evidence to distinguish promotion, resolved issues, duplicates, and incidental mentions. Do not stop reviewing surfaced candidates just because the shortlist has reached its target size.

Before ranking, reconcile the ledger with the plausible candidates surfaced by the searches you inspected. Resolve any unreviewed entries, or explicitly disclose the remaining coverage limit. The shortlist size limits the report, not discovery. Describe results as the strongest opportunities found; do not imply an exhaustive count unless the evidence supports it.

## Match the Problem to a Capability

Read [references/capabilities.md](references/capabilities.md) before research and recheck authoritative sources for any claim used in a draft. For Alexandria discovery, also read [references/alexandria-providers.md](references/alexandria-providers.md), a dated complete provider snapshot with problem-language search themes and coverage limits. Use it to find exact structured-data matches, then refresh the selected tool contract before drafting. Alexandria is part of the product knowledge, not a reason to recommend it for every question.

- Search discovers relevant web pages; Scrape reads a known page; Map discovers site URLs; Crawl handles linked sections; structured extraction produces requested fields; Interact addresses workflows requiring page actions.
- Consider monitoring or document parsing when the actual problem is change detection or local document content, verifying current support.
- Consider Alexandria when the author needs structured provider data, specialized indexes, or a supported site-specific tool beyond ordinary page extraction. Discover and inspect the exact tool's inputs, coverage, access, and pricing before claiming it solves the problem. Reading the catalogue is usually enough for a draft; do not execute unrelated provider calls to demonstrate the product.
- Give a practical next step, acknowledge constraints, and prefer a direct source API or simpler approach when that fits better. Skip solved problems, requests that explicitly reject commercial tools when no suitable free option is verified, and communities whose rules prohibit the proposed reply. Inspect relevant subreddit rules before recommending outreach.

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
4. an active discussion where a concise Firecrawl-specific answer is timely;
5. a concrete unmet need with no Firecrawl mention, where a verified feature would help and a practical, affiliation-disclosed reply is welcome.

Include strong problem-first opportunities alongside direct support when available. Do not fill a quota with weak product matches. Report missing coverage or unverified candidates separately from verified opportunities.

Deprioritize hostile threads with no real question, old conversations revived without new context, and discussions already answered adequately.

For each opportunity include:

- direct Reddit link and publication date;
- subreddit and author;
- concise issue summary;
- why it is worth answering;
- discovery track, matched capability, relevant verified facts or caveats, and prior-reply verification status;
- a concise, friendly draft reply.

Never use em dashes (Unicode U+2014) in responses produced by this skill, including research summaries and draft Reddit replies. Use commas, parentheses, colons, or separate sentences instead. Before returning a response, check it and replace any em dashes.

### Reply voice

Match the user's casual, direct writing style:

- Usually open with `Hey u/<username> I work at Firecrawl` and continue directly into the answer or acknowledgment.
- Default to one short paragraph of two or three sentences, using plain words and contractions. Add a second paragraph only when it contributes a necessary diagnosis or material limitation.
- After disclosing affiliation, directly state what Firecrawl can do for the OP. Connect the verified capability to their workflow in everyday language. Avoid self-conscious promotional preambles such as `it may sound cliché recommending my own project`.
- For straightforward capability questions, give a straightforward answer. Do not turn a simple recommendation into an architecture walkthrough, feature catalogue, comparison, or diagnostic questionnaire. Ask a follow-up only when missing information prevents a useful, accurate answer.
- State the part Firecrawl actually handles, then briefly explain how that output supports the OP’s next step. For example, Firecrawl retrieves and extracts website content; the OP’s agent compares that content against internal policies. Do not imply Firecrawl performs the entire workflow when only one part is verified.
- Explain features in everyday language, such as `get current job openings without building your own scrapers`, rather than listing API fields, endpoint names, or architecture steps. When Alexandria fits, describe the useful data and capabilities and connect them to the person's goal. Do not name specific Alexandria providers in public-facing replies, even if the user previously asked for names. Provider names and contracts may be inspected internally to verify fit. Include implementation details only when the question needs them.
- Do not lead with testing, benchmarks, a pilot, a small company list, or starting small. Mention testing only when it is absolutely necessary to resolve a material uncertainty or diagnose the reported issue, and put it after the useful feature explanation. Keep necessary coverage limits concise.
- Acknowledge the specific concern simply, such as `I can understand why the extra calls and credit usage are annoying`. Do not overdo apologies or empathy.
- Include one relevant Markdown link naturally in draft replies: [Firecrawl](https://www.firecrawl.dev/) for general Firecrawl recommendations, or [Alexandria](https://www.firecrawl.dev/alexandria) when recommending Alexandria. Use a specific official documentation link instead when it better answers the question. Keep links concise, avoid adding several promotional links, and honor community rules on external links.
- For problem-first threads, explain the practical approach and why the specific capability fits. Disclose affiliation and avoid unsolicited sales pitches or unnecessary feature lists.
- Give the useful answer first. Then, if needed, ask one straightforward diagnostic question, such as `Which setup were you using? The hosted connector or a local MCP server?`
- Explain the follow-up briefly: `That would help diagnose the issue` or `That would help identify how we can address this`.
- Avoid marketing, polished corporate phrasing, lengthy caveats, and generic closing offers. Keep any caveat that materially affects accuracy, especially for historical billing or version-specific behavior.
- Preserve the casual voice while correcting spelling and grammar. Do not imitate accidental typos or literal backslashes used as paragraph separators.
- Do not promise a fix, refund, escalation, or action that has not been authorized or performed.

Examples of tone, not factual templates to reuse blindly. Use the first example as the default style for capability recommendations, and the final example when diagnosing a reported issue:

> Hey u/Little-Bullfrog6759 I work at [Firecrawl](https://www.firecrawl.dev/), and we can handle the website retrieval and extraction part of this. You pass in the user-provided URL and get back clean content or structured data, which your Copilot Studio agent can then compare against your internal policies and flag potential issues.

When Alexandria is the verified fit, keep the same direct style:

> Hey u/Ok_Low_9949 I work at Firecrawl. [Alexandria](https://www.firecrawl.dev/alexandria) can pull current job openings from supported sources without you building your own scrapers. Your workflow can then compare them against previously seen jobs for your morning and evening shortlist.

Verify provider coverage before reusing those claims. Say `current openings` or `data from the source` when supported; never turn live retrieval into a promise that data is always correct, accurate, or complete.

> Hey u/<username> I work at Firecrawl and you're right, the instruction in the revision you linked explicitly tells the model to prefer Firecrawl search. If you installed it for mapping, I can understand why the extra calls and credit usage are annoying.
>
> Which setup were you using? The hosted connector or a local MCP server? That would help identify how we can address this.

End with a short note listing candidates excluded because `u/SnooMuffins9844` had already replied. If no strong unanswered opportunities exist, say so rather than padding the report.
