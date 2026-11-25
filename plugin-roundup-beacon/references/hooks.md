# Hooks

The first sentence decides whether people keep watching. Test a new one per custom-hook video, and log it here.

## Researching a hook

Use the Firecrawl CLI and Alexandria (about 10 requests a minute, so run them one after another and retry on a rate limit):

1. `firecrawl scrape youtube-com/videos/search_videos --options '{"query":"<topic> plugins","type":"shorts"}' -o <file>`: Shorts on the topic with view counts. Search a few angles (the harness, the audience, "MCP", "connectors", "apps").
2. `firecrawl scrape youtube-com/video_transcript --options '{"videoId":"<id>"}' -o <file>` for the top ten by views: the first sentence of each transcript is its hook.
3. TikTok search (`scrapecreators tiktok/search-videos`) shows what's popular but returns no transcripts.

Pick a pattern that has done well, write it for the video's audience, and keep it under about 5 s spoken.

## Patterns that worked (research, Nov 2026)

| Pattern | Example seen | Views |
|---|---|---|
| Too many options, you only need five | "Claude has over 100,000 skills, but honestly you only need five" | 852K |
| "<Harness> can now <job>" | several top Claude Shorts open this way | |
| "Most people don't realize..." | "Most people don't realize that there's over 60,000 Claude skills. I tested over 100..." | |
| "Don't use <harness> without these" (our control) | | 81K, the weakest |

## Hooks used

| Video | Hook | Intro | Result |
|---|---|---|---|
| ChatGPT marketing | Stop using ChatGPT without these 5 marketing plugins. | payoff deck | |
| ChatGPT job search | Stop using ChatGPT without these 5 job search plugins. | payoff deck | |
| ChatGPT small business | Your business doesn't need every ChatGPT app. Just these 5. | burst | |
| Claude recruiting | Claude can now handle your hiring. You just need these 5 connectors. | desk | |
| Claude finance | Most people don't realize Claude can run their finances. You only need these 5 connectors. | ledger | |

Fill in Result (views, average view duration) once a video has been up a week, and lean toward what wins.

## TikTok titles and captions (research, Nov 2026)

From 136 English TikTok posts across eight AI-tool searches (`scrapecreators tiktok/search-videos`, most-liked, last six months), the 113 about ChatGPT, Claude or AI tools with 150K+ views:

- **Open with the claim the video makes,** in the same words as the hook. "Claude can now..." opened five posts with 200K-808K views; "Still using Claude without these settings? You're missing out." had 2.26M; "Everybody's installing the same Claude skills. Here are 5 that almost nobody knows about" had 1.43M.
- **Then list the five, numbered, one short line each** (what it does for you). List captions were saved at 5.8% of views against 4.0% for the rest of the top 30.
- **End with one ask:** a question ("Which one are you using already?") or "save this for later". Only 7 of the top 30 had an explicit CTA, so keep it to one.
- **About five hashtags,** broad then niche: `#ai #aitools` plus `#chatgpt` or `#claude #claudeai`, plus one for the audience (`#jobsearch`, `#smallbusinessowner`). Skip `#fyp`.
- The caption before the list runs about 150 characters (median).

Vary the closing ask between videos and note which one each used, so it can be compared later.
