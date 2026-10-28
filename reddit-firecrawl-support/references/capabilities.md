# Capability knowledge for Reddit replies

Verified starting point: 2026-09-23. Refresh current docs before using technical claims; this is routing guidance, not a permanent catalogue or pricing reference.

## Alexandria

The [provider reference](alexandria-providers.md) contains the complete catalogue verified on 2026-10-07, plus search themes and known limits. The machine-readable snapshot is [alexandria-providers.json](alexandria-providers.json). Refresh selected contracts before using any snapshot claim.

[Official overview](https://www.firecrawl.dev/alexandria) describes discovery of provider APIs, specialized indexes, and site-specific tools, followed by tool selection and data retrieval through one connection. Public examples include company financials, economic data, podcast transcripts, research literature, and developer sources. Those examples do not establish support for every field, country, source, or use case.

For each proposed match, inspect current discovery results and the selected tool contract. Check required identifiers, field coverage, freshness, pricing, and access. Discovery is not execution. Do not equate an abstract index with universal full-text access, a transcript provider with every podcast, or a provider logo with unrestricted data availability. Avoid hardcoding catalogue counts.

Use the installed current Firecrawl search/Alexandria guidance and CLI help or available connector schema. Older beta-specific instructions can become stale; verify current official docs before copying commands. If tools are unavailable, cite official documentation and label provider-level fit unverified.

Current [Alexandria docs](https://docs.firecrawl.dev/features/alexandria) describe `search` for discovery, `find-tools` for inputs and pricing, and `scrape` for tool execution. The stable CLI also exposes `list <provider> <capability>` for selected contracts, verified with CLI help on the date above. Tool-only discovery is free; combining it with web search or scraping incurs those operations' normal charges. Provider execution has its own listed price and access terms.

## Other capabilities

Verify the narrowest feature that solves the author's problem against [official documentation](https://docs.firecrawl.dev/): search for discovery, scrape for a known URL, map for site URLs, crawl for linked pages, structured extraction for fields, and browser interaction for page actions. Check current monitor and parse documentation for change detection and documents.

Never promise universal anti-bot bypass, free usage, complete datasets, guaranteed freshness, or performance without evidence. Match the author's constraints and include a direct API or simpler alternative when it is the better answer.
