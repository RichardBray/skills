---
name: newsletter-digest
description: Fetch developer newsletter RSS feeds (JavaScript Weekly, React Status, Node Weekly by default) and pick the 10 best articles as YouTube video topic ideas. Use when the user asks for newsletter picks, video topic ideas from newsletters, a weekly dev digest, or to "run the newsletter digest".
---

# Newsletter Digest

Fetch dev newsletter RSS feeds and curate 10 YouTube-video-worthy items, then print the result directly in chat.

## Inputs (defaults if user doesn't specify)

- **Feeds**:
  - JavaScript Weekly — `https://javascriptweekly.com/rss`
  - React Status — `https://react.statuscode.com/rss`
  - Node Weekly — `https://nodeweekly.com/rss`
- **Pick count**: 10

If the user names different feeds or a different count, use those instead.

## Workflow

### 1. Fetch feeds

Use `curl -sL <url>` for each feed in parallel Bash calls. Newsletter RSS items typically bundle many links per issue — fetch the latest issue's RSS, then for each `<item>` parse the `<description>` HTML to extract the individual article links (each issue is itself a roundup of dozens of links).

If a feed fails or returns empty, note it and continue with the others.

### 2. Select 10 picks

Apply criteria **in order**:

1. **Recent** — newly published items only (this issue / past week).
2. **AI / AI-adjacent preferred** — LLM tools, agents, AI-in-dev-workflow, AI infra. Lean toward these when otherwise tied.
3. **~10-min video scope** — a single tool, release, technique, or take. Not a 40-page paper or a 12-topic mega-roundup.
4. **Genuinely interesting** — new tool launches, notable releases, surprising benchmarks/results, strong opinions, "this changes how you'd do X".

**Avoid**: long research papers, sprawling multi-topic roundups, deeply niche internals (compiler arcana, single-vendor minutiae), job posts, sponsor slots, pure opinion blogs without a hook.

Aim for variety across the three sources rather than 10 items from one feed.

### 3. For each pick capture

- Title
- URL (the article link itself, not the newsletter issue link)
- Source newsletter name
- One-sentence YouTube video angle — frame it as "what the video is actually about", hook-first, not just a title restatement.

### 4. Print the digest in chat

Output directly in the assistant message as markdown. Include today's date at the top. Format:

```
# Newsletter Digest — <today's date>

1. **<Title>** — _<Source>_
   <URL>
   <one-sentence video angle>

2. **<Title>** — _<Source>_
   ...
```

Do NOT post to Slack or any external destination. The output is just the chat message.

## Notes

The "best 10" step is judgment. Apply the criteria above explicitly rather than defaulting to whatever's at the top of the feed.
