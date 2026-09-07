---
name: reference-led-websites
description: Turn a client brief into a website build prompt, then use that prompt in a fresh session to build a brand-specific site from curated design references.
---

# Reference-led websites

Create brand-specific client websites by adapting identifiable elements from existing designs. Keep each site coherent without imposing a house style across clients. Invent a new pattern only when suitable references cannot fill the brief, and explain why.

## Ownership

This skill prepares prompts and builds client websites. It reads the shared library owned by `website-reference-curator` but never updates that library, discovery records, CSVs or coverage contracts.

- Save research and design artifacts in the client project.
- For an explicit shared-library update, use the curator skill as a separate task phase; do not require curation before finishing a build.

## Choose the mode

- **Prepare a prompt:** read [prompt preparation](references/prompt-preparation.md), fill [the build prompt template](references/build-prompt-template.md), and stop before implementation. Stage 1 produces a self-contained prompt for the user to paste into a NEW session to start build mode.
- **Build or redesign:** follow the workflow below. Stage 2 starts when the user pastes the Stage 1 prompt into a NEW session; that prompt supplies the brief; do not repeat answered questions or force a separate preparation session.
- **Evaluate:** give advice; read [evaluation](references/evaluation.md) for trials or quality comparisons.

## Essential requirements

Carry these into both builds and generated prompts. Honour explicit user overrides; keep reduced-motion alternatives accessible.

- Use the tagged JSON reference library and map selected source elements to client adaptations. Inspect actual behaviour; screenshots alone do not establish animation or live 3D.
- Deliver a reference-backed **signature interaction** that meaningfully changes content exploration. Basic fades, hover states or navigation alone are insufficient.
- **Every site needs scroll animations:** a deliberate progression through the main page. Smooth scrolling and page-load effects alone do not count.
- **Multi-page sites need page transitions:** reference-backed exit/entry choreography with visual continuity. Consider View Transitions when compatible with the project.
- Keep readable copy at **16 CSS px minimum**, including mobile, navigation, controls, captions and footer; aim for **18px or larger body text**. Do not shrink roots or transforms to evade the floor.
- **No em dashes in authored copy**, including metadata, accessibility labels and text in generated imagery. Preserve raw reference evidence unchanged.
- Use suitable supplied, licensed or generated assets. Reference URLs do not grant reuse rights. Preserve real client/product identity and distinguish real geometry from 3D-looking images.
- Work autonomously after the brief, within existing authorization. Do not inspect sibling projects without permission or turn client-specific preferences into universal defaults.

## 1. Resolve the brief

Read project instructions and existing context. Ask one compact batch, up to three focused questions, covering only missing decisions: client/audience/action; brand assets and reference preferences; pages/functionality/constraints, scroll-animation character or intensity, and optional 3D.

Wait for consequential answers before committing to direction; inspect the project and library meanwhile. State assumptions when choices are delegated. Do not add mandatory moodboard or implementation approval gates, or ask whether required scroll animation should exist.

## 2. Select and inspect references

Read [library access](references/library-access.md). Resolve the curator root before searching compact records:

```bash
python3 <curator-root>/scripts/catalog.py search --query 'editorial restrained hospitality' --limit 8
```

The search is a lexical shortlist. Judge brand fit, audience, content, conversion goals, assets, mobile suitability and effort; awards and industry alone do not determine fit. Select an anchor for composition/type and compatible references for specific elements.

- Inspect the relevant page sections at desktop and mobile widths, including intermediate and settled motion states.
- Keep observed facts separate from inferred implementation.
- For missing evidence or new references, follow [project research](references/library-access.md#project-research).
- Prefer Firecrawl and its design-clone workflow when available; use available browser/web tools or saved evidence otherwise and record provenance.

For close matches, preserve defining composition, scale, colour relationships and choreography while adapting identity and licensed assets. Read [build decisions](references/build-decisions.md) before planning; document necessary deviations instead of silently simplifying the design.

## 3. Plan design, assets and motion

Write DESIGN.md with the brief, page structure, brand tokens, asset plan, reference-to-element mapping, technical choices and unresolved evidence. Preserve a suitable existing stack; research new APIs and compatibility through Firecrawl Developer Index when available, otherwise current official documentation/source.

Read these resources when applicable:

- **Every build:** [motion requirements](references/motion-requirements.md) for signature, scroll and page-transition acceptance; [animation patterns](references/animation-patterns.md) for evidence and motion contracts.
- **Multi-page sites or custom scrolling:** [page transitions and scroll control](references/page-transitions-scroll.md).
- **3D or substantial motion:** [motion and 3D](references/motion-3d.md), including optional Blender/Replicate asset production.
- **Missing imagery:** [image generation](references/image-generation.md), covering built-in tools, authorized API routes and integration.
- **Reusable components:** inspect component suppliers in `<curator-root>/library/components.json`, including ThreeUI, for fit, dependencies, assets and licences before adapting them.

Companion skills, Firecrawl, image tools and Blender are optional host capabilities, not bundled dependencies. Discover availability and use documented fallbacks; do not silently install dependencies or assume credentials. Keep real content and navigation usable without visual enhancements.

## 4. Build and refine

Prototype the anchor section, signature interaction and one lower section with representative assets before extending the site. Inspect their rendered relationship. Match required cutouts/models and composition; do not substitute generic placeholders or unmodified component demos.

Implement scroll choreography, required route transitions and supporting open/close/state changes across the primary flow. One effect may satisfy multiple motion requirements only if it meets each requirement's observed behaviour. Follow the linked motion contracts, mobile adaptations and reduced-motion fallbacks.

Compare reference and build at matching viewport sizes and scroll states. Fix the largest composition, typography, asset and interaction discrepancies before adding decoration. Record and explain changes to the defining direction.

## 5. Verify and deliver

Read [review criteria](references/review.md) for every build.

- Inspect desktop, mobile and an intermediate width.
- Exercise the primary flow, scrolling, route changes, keyboard/touch, overlays and reduced motion.
- Check computed font sizes and literal/encoded em dashes as well as layout, assets, loading and runtime errors.

Fix observed issues and recheck affected areas. Completion requires the brief and motion acceptance criteria to be met in the rendered build, not merely a successful compilation. If browser verification is unavailable, report it as incomplete.

Deliver the working result, preview, DESIGN.md reference mapping, actual checks and material limitations. Distinguish demos from production integrations; publish or incur paid-provider costs only within authorization.
