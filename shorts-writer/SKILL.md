---
name: shorts-writer
description: Write short video scripts in the style of a developer-focused tech shorts channel. Use when the user asks to write a short, create a short video script, or make a script for a short about a tool, technique, or concept.
---

Before writing, read all files in the `references/` directory inside this skill to absorb the tone, rhythm, and structure of existing scripts. Use those as your style guide, not this description.

## Rules

- Start with a hook that subverts an assumption the audience already has — the pattern is "everyone thinks or does X, but what they don't know is Y". Don't use those exact words every time, but keep that contrast
- One idea per line, short and punchy
- No punctuation at the end of lines
- Lowercase throughout
- Name the tool or product mid-script, not in the opening line
- Give an honest take on any limitations or annoying things
- End with "subscribe for more" and a short relevant sign-off
- No section headers — one flowing script

## Output

Write the script directly. Create a new directory named after the topic inside the user's current working directory and save the script as a `.md` file inside it.
