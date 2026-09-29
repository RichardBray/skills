---
name: weekly-video-topics
description: Find this week's best YouTube video topics for the Firecrawl channel. Combines what is trending in AI and dev tooling (Hacker News, Reddit, X, Hugging Face papers, lab blogs), what Firecrawl shipped (merged PRs, docs changes), how people actually use Firecrawl (product usage stats, Alexandria tool calls and feedback) and what has performed on the channel, then returns 10 Firecrawl-specific and 10 general developer/AI topics with evidence. Use when the user asks for video ideas, topics for this week, what to make next, or runs their weekly topic research. Optionally scaffolds a script.md for a chosen topic.
user-invocable: true
argument-hint: "[optional focus, e.g. 'alexandria' or 'small business'] [--days 7]"
---

# weekly-video-topics

Research first, pitch second. Every topic in the final list must trace back to evidence gathered in this run: a trend with real engagement numbers, a shipped feature with a PR or doc link, or a usage number. Never invent engagement numbers, view counts or quotes; if a source could not be reached, say so.

Paths are relative to this skill's directory:

```bash
SKILL_DIR=<absolute path of the directory containing this SKILL.md>
OUT_DIR=~/client-videos/firecrawl/topics      # weekly reports + history live here
VIDEOS_DIR=~/client-videos/firecrawl          # one folder per video already made
```

Default window is the last 7 days (use 14 if the user asks, or if the week was quiet). If the user gave a focus, still produce both lists but weight the focus.

Run the independent research steps (2 to 5) in parallel with subagents when available; each should return a compressed summary and save raw notes to the scratchpad.

## Step 1: Know what's already been made

- `ls -t "$VIDEOS_DIR"` and read the three most recent `script.md` files: their topics are off the table, and their structure is the template for Step 8.
- Read `$OUT_DIR/history.md` if it exists: topics already pitched in past weeks. Don't re-pitch one unless something new happened to it, and say what.

## Step 2: Channel performance

```bash
python3 "$SKILL_DIR/scripts/channel_videos.py"     # latest 15 uploads: views, likes, likes per 1k views
```

The RSS feed has no comment counts and only the last 15 uploads. If the user can share a YouTube Studio screenshot or CSV export (Content tab), use it for views and comments across more videos.

If `$SKILL_DIR/internal/` exists, also run `sh "$SKILL_DIR/internal/product_stats.sh"`; its last section is the all-time top videos from the warehouse (check the snapshot date, it can be stale).

Read `references/what-performs.md` (and `internal/usage-notes.md` if present) and update them if this week's numbers change the picture (a new hit, or a format that flopped).

## Step 3: How people use Firecrawl (internal)

Only if `$SKILL_DIR/internal/` exists; otherwise skip and say so in the report.

```bash
sh "$SKILL_DIR/internal/product_stats.sh"            # endpoint teams now vs 4 weeks ago, agent users, PDF, Alexandria feedback
python3 "$SKILL_DIR/internal/alexandria_usage.py" --days 7   # which Alexandria providers/tools teams actually run
```

`alexandria_usage.py` needs the Firebrain CLI logged in (`cd ~/fc/firebrain && bun apps/cli/firebrain.ts whoami`; if expired, ask the user to run `! cd ~/fc/firebrain && bun apps/cli/firebrain.ts login --device`). It takes about a minute per day of data.

Read the numbers carefully:
- A new endpoint's first week is a launch spike, not growth. Compare like with like (week over week once it's older than a month).
- Keyless identities inflate team counts; the scripts exclude them. Don't quote keyless numbers.
- MCP is where most growth shows up. A feature growing mainly through MCP suits an agent-workflow video.
- Alexandria feedback (`insufficient_functionality`, requested functionality) tells you what users wish worked; tool-call counts tell you what they actually do. Both are topic material.

## Step 4: What Firecrawl shipped

```bash
since=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d '7 days ago' +%Y-%m-%d)
for r in firecrawl/firecrawl firecrawl/cli firecrawl/firecrawl-docs firecrawl/firecrawl-mcp-server; do
  gh pr list -R $r --state merged --search "merged:>=$since" --limit 100 --json number,title,mergedAt,url
done
```

Also skim `git -C ~/fc/firecrawl-docs log --since="$since" --oneline` for new or changed feature pages, and read the relevant `features/*.mdx` before pitching a feature (param names, pricing, limits). Open issues with the most comments are pain points worth a "fix" video: `gh issue list -R firecrawl/firecrawl --state open --limit 50 --json title,comments,url`.

## Step 5: What's trending

```bash
python3 "$SKILL_DIR/scripts/hn_top.py" --days 7                                   # everything big on HN
python3 "$SKILL_DIR/scripts/hn_top.py" --days 7 --min-points 50 \
  --query scraping --query crawler --query "web agent" --query MCP --query browser --query "AI agent"
python3 "$SKILL_DIR/scripts/hf_papers.py" --days 7                                # most-upvoted HF papers
```

Then with the `firecrawl` CLI (search with `--tbs qdr:w`):
- Reddit blocks both curl and `firecrawl scrape`. Use `firecrawl search "site:reddit.com/r/LocalLLaMA ..."` (also r/ClaudeAI, r/ChatGPTCoding, r/programming, r/webdev) and accept that upvote counts are usually missing.
- X: search `site:x.com <topic>`; `firecrawl scrape https://x.com/<user>/status/<id>` usually returns the post with like counts. Cite handle, date, likes and URL.
- Lab and research pages: anthropic.com/research, openai.com/news, deepmind.google, the Hugging Face blog.
- Competitors and web-data news (Exa, Tavily, Browserbase, Parallel, Perplexity, Cloudflare bot policy, Google search changes): these make the strongest Firecrawl tie-ins.

## Step 6: Pick and pitch

Produce **10 Firecrawl-specific** and **10 general developer/AI** topics, ranked. Rank by (evidence of demand) x (fit with what performs) x (timeliness).

Fit comes from the scoring table in `references/what-performs.md`. For every candidate:
- score the four signals (pain or money hook, Claude Code / coding-agent audience, something new, a concrete visual payoff) and apply the penalties (partner integration as the subject, Firecrawl feature explained, company news, a bare model-launch reaction);
- name the nearest past video as a comparable and give an expected view range from it;
- if a candidate scores low but the evidence of demand is strong (a heavily used feature, for example), reframe it until it hits at least two signals, and show the reframe. The Developer Index got 1.8k as "One Fix That Instantly Improves Claude's Coding"; the same feature as a pain story about Claude Code writing broken code against stale docs hits more signals.

The channel's audience is people who use Claude Code and other coding agents every day. Topics outside that (lead generation, small business tools) can work, but say so, lean harder on the money hook, and expect a smaller comparable.

Then apply these rules:

- Firecrawl must be necessary to the video, not a mention. If the video works without Firecrawl, it goes in the general list.
- Pitch through a hook (money, free, speed, a trending model or tool, a pain), never as "Feature X explained".
- Prefer topics with a debate in them (cost, "is X worth it", "you don't need X"): the comment-heavy videos all have one.
- Timely topics (a launch this week) go first; note how long the window stays open.
- Flag risk plainly: legal or optics (scraping a named company, security incidents: keep those at news level, never walk through exploits), unverified claims, flaky providers or known bugs.
- Say when the evidence is thin (one source, snippet-only, no numbers).

For each topic give: working title, the hook in one sentence, what gets built or shown on screen, the evidence (numbers plus links), signals hit, nearest comparable with expected range, and risks. End with a "make these three first" recommendation and the gaps in this week's data (sources that were blocked or stale).

## Step 7: Verify the top picks

Before recommending a topic, open its primary sources (not just search snippets) and check the headline numbers. Mark anything still unverified as such. For a topic the user picks to script, offer a fact-check with the `delegate` skill (a different model family reviewing against primary sources) once the script exists.

## Step 8: Save, and optionally scaffold

- Write the report to `$OUT_DIR/<YYYY-MM-DD>.md` (create the folder if needed) with every source URL.
- Append this week's pitched titles to `$OUT_DIR/history.md` as `- YYYY-MM-DD: <title>`.
- If the user picks a topic to make, create `$VIDEOS_DIR/<short-slug>/script.md` following the structure of the three latest scripts: several `#` title options, `## Intro`, `## Exp`, `## Demo`, `## Outro`, then `## Notes` with the caveats, key numbers, every source, HN threads and X posts. Match the user's voice: short spoken lines, lowercase, `[url]` or `[show ...]` cues for what's on screen, a mention of the 500 extra credits link. Leave demo results as placeholders; never fabricate them.
