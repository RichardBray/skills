---
name: shorts-writer
description: >-
  Write short video scripts in the style of a developer-focused tech shorts
  channel. Use when the user asks to write a short, create a short video script,
  or make a script for a short about a tool, technique, or concept.
---
Before writing, read all files in the `references/` directory inside this skill to absorb the tone, rhythm, and structure of existing scripts. Use those as your style guide, not this description.

## Rules

- Prefer an Angus-style curiosity open when the topic is a stealable workflow, a famous person's playbook, or a "look what they are actually doing" demo. Strong spoken opens:
  - `apparently anybody can just …`
  - `apparently founders are …`
  - `so apparently …`
  - `it turns out …`
  - `anybody can reverse engineer …`
- After that open, use a short beat like `look up how long …` / `look up what X actually does`, then `so can we just pull them with ai` (or similar), then the demo. Do not copy another creator's script; borrow the rhythm only.
- If the topic is not a steal-or-spy workflow, fall back to a hook that subverts an assumption the audience already has — the pattern is "everyone thinks or does X, but what they don't know is Y". Don't use those exact words every time, but keep that contrast.
- One idea per line, short and punchy
- No punctuation at the end of lines
- Lowercase throughout
- Name the tool or product mid-script, not in the opening line
- Put real demo numbers in the script (days live, counts, hooks). Never invent results; leave a `[results: …]` cue only when the run is still pending
- Give an honest take on any limitations or annoying things
- For Firecrawl brand Shorts, end with `comment fire for the setup link` (or the keyword the shoot uses), `or just go to firecrawl.dev/plugins`, then `subscribe for more`. Mention Firecrawl Alexandria when the demo uses it
- For non-Firecrawl Shorts, end with "subscribe for more" and a short relevant sign-off
- No section headers in the spoken body — one flowing script
- Scripts must be no more than 30 spoken lines (excluding blank lines, titles, cues, and `##` blocks)

## Output

Write the script directly. Create a new directory named after the topic inside the user's current working directory and save the script as a `.md` file inside it.

Start the file with 1–4 candidate `#` titles. Spoken lines only after that. Production cues go in square brackets on their own line. Add a `## test prompt` block with the exact prompt used in the demo when there was one, and a short `## notes` block for idea ids, accounts, and source files.

After saving, if `~/.config/voice-clone/reference.wav` exists, offer once to voice the script with the `say-as-me` skill. Don't generate audio unless the user says yes; it costs a few cents.
