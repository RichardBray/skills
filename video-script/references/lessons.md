# Lessons from writing scripts with the user

What the user has corrected or approved while writing scripts. Read this before drafting, and add to it at the end of every script session (see "Updating this skill" in SKILL.md). Newest videos at the bottom of each section; the video slug in brackets says where a lesson came from.

## Working with the user

- **Show line edits as before and after, then wait.** For any change to lines already in the script, quote the current lines and the replacement, grouped by section, and apply them only after the user says yes. A blanket "looks good, update it" covers everything shown so far. [adfinder]
- **A line that is just "..." is a gap for you to fill**, not a pause. The user leaves "another company..." or "so..." where they want a line written. Fill it with something concrete (a real company, a real number) and change the `[show ...]` cue next to it if it no longer matches. [adfinder]
- **Ask once, then commit to an angle.** When offering intro options, give two or three short ones (A, B, C) and let the user pick or merge them. Then write the rest of the script in the picked style without asking again. [adfinder]
- **Say how long the script runs and what to cut first** whenever it goes over 6 minutes, naming the section to drop. [adfinder]

## Hooks and intros

- **Name the big, familiar companies in line 1.** "meta, google and tiktok all have the same problem" beat "this is X" and "if you want to find ads you'd have to go to multiple places". Familiar names, then the shared problem. [adfinder]
- **Line 2 states the problem plainly**, then the intro shows the thing working on a real example with a real number ("hellofresh, who've had the same google ad running for three years"). [adfinder]
- **The last line of the Intro has to promise what Exp delivers.** If the Intro ends "let me show you where the data comes from, and how to build your own", Exp must open by naming that data source. [adfinder]
- **Size claims must be true of what you'll show.** "Under 60 lines of code" applies to the tutorial server, not the full app; say "the core of it". Check with `wc -l` before writing the number. [adfinder]

## Exp

- **The first line of Exp names the product.** Don't open with "one single api…" and leave the viewer to guess which one. [adfinder]
- **For "why build your own" videos, the thesis is focus:** a general agent with search, scrape and hundreds of Alexandria providers has to choose every time, whereas your own app calls only the providers you picked. The "things to consider" lines should argue for whatever the video actually builds (an app or an MCP server, not both). [adfinder]
- **Show a claim about agent behaviour on camera instead of asserting it**, and give a fallback line in case the recording doesn't show it ("it works, but that's a lot of tools to choose from"). [adfinder]

## Structure of build videos

- **One build per video.** If a second build exists (an MCP server alongside the app), give it one teaser line in the Outro ("that's the next video") and decide later from how the video does. [adfinder]
- **Order: Intro, Exp, Build your own, Demo, Outro.** The build comes first and the finished app is the payoff. Keep the Demo on the UI: what to click, with numbered `### 1.` beats. [adfinder]
- **Write the build section from the real repo.** Read every tutorial branch before writing: what each one adds, the exact calls and options, line counts. Each branch becomes a numbered step with `[checkout <branch>, highlight ...]` cues and a `[results]` placeholder for the run. [adfinder]

## Voice

- **Punchy:** cut connecting phrases ("so...", "which is already really impressive", "let's go through exactly how I built it"). One idea per line, and lines short enough to say in one breath. [adfinder]
- **Titles pitch the build when the video is a build** ("I Built My Own Ad Spy Tool With Firecrawl"), not the feature list. [adfinder]

## Notes section

- **Add "Recording the build" and "Recording the demo" blocks** for anything the user demos: how to run it, which examples are cached or free, per-demo gotchas (missing data for a brand, things that are slow the first time), what to re-check on the day, and the settings to record at (light mode, window width). [adfinder]
- **Check caches before claiming something is instant.** Look before writing "it's cached" (for example, list the KV keys). [adfinder]
- **Optional "Build time" block** from session timestamps, worded so it stays accurate ("about two hours to the first working version", not "under an hour"). [adfinder]
- **Avoid list:** claims the product can't back up (TikTok ads when it shows TikTok creator posts, leads or sales from ads), naming the AI model when the product doesn't show it, and brands that have no data for a given demo. [adfinder]
