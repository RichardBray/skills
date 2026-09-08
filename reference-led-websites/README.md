# reference-led-websites

Turn a client brief into a website build prompt, then use that prompt in a fresh session to build a brand-specific site from curated design references.

Pairs with [`website-reference-curator`](../website-reference-curator), which owns the shared reference library this skill reads.

## Installation

Install both halves:

```sh
npx skills add https://github.com/RichardBray/skills --skill reference-led-websites
npx skills add https://github.com/RichardBray/skills --skill website-reference-curator
```

The builder resolves the library at `../website-reference-curator` relative to its own directory, so installing them as siblings needs no configuration. Installed elsewhere, tell it the curator root. Without the curator the skill still runs, but only on references you supply yourself.

## Prerequisites

- Python 3 for the curator's `catalog.py` search (no third-party packages).
- A browser tool for verifying rendered builds and inspecting references. Firecrawl is used when available; other browser tools work.
- Image generation, Blender and Replicate are optional and only used when a build needs them.

## Usage

Two stages, deliberately in two sessions.

**Stage 1, write the prompt.** In any session:

```
/reference-led-websites prepare a build prompt for <client>
```

It asks up to three questions, picks references from the library, and returns one complete copyable prompt in chat. Ask it to save the prompt to a file if you would rather not copy it out of the transcript. It stops there, before any implementation.

**Stage 2, build.** Open a **new** session in the client project directory and paste that prompt as your first message. No slash command: the prompt already names the skill's absolute path, the resolved library root and the reference paths, so the fresh session loads the skill itself. It assumes no memory of stage 1, which is exactly why it is a separate session.

Stage 2 writes DESIGN.md, prototypes the anchor section and signature interaction, builds out the site, then verifies the rendered result at desktop, mobile and an intermediate width.

Ask for advice or a quality comparison instead and the skill runs its evaluation path rather than building.

## What it enforces

Every build ships a reference-backed signature interaction, scroll choreography through the main page, and page transitions on multi-page sites. Body copy stays at 16 CSS px minimum. Completion means the criteria are met in the rendered build, not that it compiled.

The skill never writes to the shared library. To promote research it did in a client project, switch to the curator skill for that phase.
