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
| "Don't use <harness> without these" (our control) | | 81K, the weakest |

## Hooks used

| Video | Hook | Intro | Result |
|---|---|---|---|
| ChatGPT marketing | Stop using ChatGPT without these 5 marketing plugins. | payoff deck | |
| ChatGPT job search | Stop using ChatGPT without these 5 job search plugins. | payoff deck | |
| ChatGPT small business | Your business doesn't need every ChatGPT app. Just these 5. | burst | |
| Claude recruiting | Claude can now handle your hiring. You just need these 5 connectors. | desk | |

Fill in Result (views, average view duration) once a video has been up a week, and lean toward what wins.
