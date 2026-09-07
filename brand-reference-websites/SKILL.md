---
name: brand-reference-websites
description: Design and build professional client websites by selecting and adapting specific elements from a tagged reference library, with required scroll animations and optional 3D. Also turn client briefs into self-contained build prompts for a fresh session and curate website and component references. Use for brand-specific marketing websites, redesigns, and reference-led landing pages.
---

# Brand reference websites

Create a website specific to the client's brand using identifiable elements from existing designs. Different clients should get different visual directions. Keep coherence within each website without imposing a house style across projects. Prefer adapting proven references; create a new pattern only when the brief has a gap the references cannot reasonably fill, and explain that decision.

## Available tools and portability

This repository provides the workflow, reference library and catalog script. Firecrawl, Developer Index, image generation and Blender are optional host capabilities, not bundled dependencies. Discover available tools before invoking them. Prefer Firecrawl for extraction when available; otherwise use accessible browser tools, official pages or existing saved evidence and record the actual source. For missing image tools, use suitable supplied/licensed assets or report the specific asset gap. Do not silently install companion skills or block unrelated work because one is absent.

## Choose the task

- Creating a build prompt, interviewing for a brief, or preparing a fresh-session handoff: read [prompt preparation](references/prompt-preparation.md) and fill [the build prompt template](references/build-prompt-template.md). Finish with the prompt; do not start implementation.
- Building from a completed prompt: treat its decisions as the brief, avoid repeating answered questions, and follow the build workflow below.
- Building or redesigning directly: follow the workflow below; do not force a separate prompt session when the user requests a build.
- Adding URLs, award collections, or component libraries: read [reference ingestion](references/ingestion.md), update the JSON library, and validate it. Do not build a website unless requested.
- Evaluating an approach: advise without implementing unrelated work.

## Interactive quality requirement

For website builds and redesigns, deliver at least one reference-backed signature interaction appropriate to the brief. It must meaningfully shape how visitors explore the content or products. Basic hover effects, entrance fades, accordions, and navigation transitions do not satisfy this requirement by themselves. 3D is optional; a flat design can provide a distinctive interactive experience. Scroll animation is required for every site by default; only a later explicit user override can change that scope. Reduced-motion accessibility remains required.

Before implementation, define the interaction's purpose, exact reference section, observed trigger and before/after states, required assets, mobile behaviour, and reduced-motion alternative in DESIGN.md. Inspect the reference behaviour directly: screenshots establish composition, not motion. Match assets to the interaction, including cutouts or models when needed; do not substitute rectangular photographs when the defining composition requires isolated objects.

Implement and inspect the signature interaction in the anchor section with representative assets before extending the site. Do not describe the result as complete until the interaction, primary user flow, mobile alternative, and reduced-motion fallback have been exercised in the rendered build. Record actual observations and unresolved limitations; a successful build alone does not satisfy this gate.

If the defining interaction is omitted or substantially simplified, explain the specific reason and treat this as a change in design direction, not a faithful adaptation. Do not silently replace it with generic micro-interactions or claim unverified behaviour.

Keep project references isolated: do not inspect sibling projects unless the user explicitly authorizes them as references. Keep client preferences scoped to that client rather than turning a previous project's design into the default for new work.

## Required multi-page transitions

Every multi-page site, including client-side routed sites, must have reference-backed transitions meeting the acceptance criteria below between its primary pages. Treat route changes as part of the art direction, with a coherent outgoing/incoming sequence and purposeful continuity of shared elements, typography, imagery or colour. Match the chosen reference and brand; do not apply the same generic fade to every site. First-load entrances, menu animations and scroll effects do not fulfil this separate requirement.

Read [page transitions and scroll control](references/page-transitions-scroll.md). Consider the browser View Transitions API when it suits the routing architecture and desired effect; verify current official documentation and target-browser support before choosing it. Use a compatible router/motion approach when needed. Keep navigation functional when the enhancement is unsupported, interrupted or reduced by user motion preferences. Carry the requirement into prompt preparation and final browser review for every multi-page brief.

Page-transition acceptance: specify and observe at least one reference-derived visual continuity device (for example a matched image, directional mask or coordinated typography) across the primary route changes. Document exit, intermediate and entry states, the chosen timing, and the source element. Exercise forward/back, rapid navigation, focus/scroll restoration and reduced-motion/unsupported-browser fallbacks. All destinations must remain reachable with no stuck overlay, duplicated content or navigation lock. Visual QA must compare these states with the chosen reference and record deviations.

The three motion requirements have different purposes: the signature interaction changes content exploration; scroll animation responds to scroll; page transitions connect routes. One implementation may satisfy multiple requirements only when its observed behaviour meets each criterion. Do not add redundant effects merely to count three features.

## Required scroll animations

Every website built or redesigned with this skill must include deliberate, reference-backed scroll-triggered or scroll-progress animation. Carry this requirement into every generated build prompt. Do not ask whether to include scrolling animation; ask only about its character or intensity when unresolved. Choose motion to suit the brand and content, such as staged section reveals, product movement, image transitions or a scroll-linked narrative. Design a coherent progression through the main page rather than relying on a single token fade. Page-load entrances, hover effects, smooth scrolling alone and route transitions do not satisfy this requirement.

Record the chosen reference, affected sections, trigger/start/end states, replay or reversal behaviour, required assets and mobile adaptation in DESIGN.md. Scroll animation may also satisfy the signature-interaction requirement when it meaningfully changes exploration; basic reveal effects alone do not replace the existing signature-interaction requirement. Use native scroll where suitable; scroll animation does not require scroll jacking, pinning or a specific library.

Exercise actual scrolling down and back up in desktop and mobile layouts, including intermediate animation states and resize. Check for stuck pins, inaccessible content, layout jumps and poor rendering performance. Honour prefers-reduced-motion with simpler or static states that preserve all content and functionality. That accessibility fallback does not waive animation for the normal-motion experience. Do not call the build complete until scroll behaviour and its fallback have been inspected in the browser.

## Readable typography and copy

Apply these user-wide defaults to builds, redesigns and generated build prompts. Use a minimum rendered size of 16 CSS px (normally 1rem with an unshrunk browser default) for readable website copy, including navigation, buttons, labels, captions, badges, footer and legal text. Aim for 18 CSS px or larger for body paragraphs when the layout permits. These are project preferences, not a claim of an accessibility standard. Do not shrink mobile text, root font size or scale transforms to evade the floor. Adapt layout, wrapping and spacing instead. A reference's tiny utility text does not override these defaults; change them only when the user explicitly requests an exception.

Do not use em dash characters (U+2014) in any authored website copy, including metadata, alt text, labels, errors, generated packaging text and image prompts containing visible text. Rewrite the sentence with a full stop, comma, colon or parentheses as appropriate; do not mechanically replace them with double hyphens. Preserve factual meaning when editing supplied copy. Preserve raw reference captures and third-party source evidence unchanged.

During review, inspect computed font sizes in rendered desktop and mobile states, including open drawers/dialogs and validation messages. Check that the chosen font remains comfortable to read at the minimum size. Search authored content and rendered text for literal em dashes and encoded equivalents such as &mdash;, &#8212;, &#x2014; and escaped Unicode. Inspect visible text in generated imagery too. Fix violations before delivery and report any explicit user-approved exceptions.

## Brief first

Read the user's existing brief and project instructions. Ask one compact opening batch covering only missing information:
1. Who is the client, who is the audience, and what should visitors do?
2. What brand assets/constraints exist, and which references or elements do they like or dislike?
3. What pages, functionality, platform and deadline are needed; what character/intensity should the required scroll animation have, and would optional 3D serve the brand?

Use these as topics, not a compulsory questionnaire. Honour answers already supplied. Give the user time to answer before committing to a visual direction; meanwhile inspect the project and reference inventory. If the user explicitly delegates choices, state reasonable assumptions and proceed. After the opening exchange, work autonomously without mandatory moodboard or implementation approval gates. Ask again only for a material unresolved choice or necessary missing access.

## Retrieve and select

Read [library model](references/library-model.md). Resolve paths relative to this skill directory. Search compact records before reading raw captures:

```bash
python3 <skill-dir>/scripts/catalog.py search --query 'editorial restrained hospitality' --limit 8
python3 <skill-dir>/scripts/catalog.py search --tag logistics --limit 5
```

The script is a lexical shortlist, not a creative ranking model. Assess audience, brand personality, content shape, conversion goal, asset availability, mobile suitability, and implementation effort. Industry is a clue, not a restriction. Never select solely because a site won an award. Unverified candidates require inspection before adopting their visual patterns.

Select an anchor reference for composition and typography, then compatible references for specific sections or interactions. The number should fit the project. Inspect the actual relevant section and its behaviour. Do not infer live 3D from a screenshot, or animations from marketing descriptions. If the library lacks a suitable pattern, discover and ingest a targeted reference through Firecrawl before inventing a pattern.

## Preserve the reference direction

When the user asks for a close match, treat the selected reference as the design specification, not a moodboard. Preserve its defining composition, section order and relative heights, colour-field relationships, type scale and density, object scale, image framing, control shapes and scroll choreography wherever the brief permits. Adapt brand identity, copy and licensed assets without replacing the design language with a habitual house style. Do not automatically soften bold references into neutral palettes, small type, standard card grids or static sections.

Inspect the full relevant page at desktop and mobile widths before planning the page structure. Capture opening, transition and settled states of important scroll sequences, plus hover/focus details and persistent navigation. Record actual measurements where accessible; distinguish observed behaviour from inferred implementation. A hero screenshot alone is insufficient evidence for a scrolling homepage. User-approved deviations take precedence; document necessary deviations and their concrete reason rather than silently simplifying them.

## Plan the technical approach

Prefer Firecrawl Developer Index when available during initial technical planning, before selecting a new stack or committing to the signature interaction. If installed, read the firecrawl-developer-index skill; otherwise use the research fallback below. Research the specific rendering, scroll, 3D, accessibility and routing requirements that affect the approach. Prefer official documentation, repository READMEs and released fixes; check version compatibility, maintenance status, experimental warnings and licences. Record the selected approach, relevant source URLs and material tradeoffs in DESIGN.md. Visual references decide what to build; Developer Index informs how to build it.

Preserve a suitable existing stack. For a fresh project, prefer established, supported tools and the simplest architecture that meets the actual brief. Do not introduce an experimental framework or compatibility layer for novelty, a starter-template default or an unrelated reference site's stack. Select one only when the user explicitly requests it or a documented requirement justifies its limitations; explain that choice before implementation. Verify actual package names and versions rather than conflating similarly named tools. A local client-side demo does not by itself require server rendering or a full-stack framework.

If Developer Index or its companion skill is unavailable or has insufficient coverage, inspect official documentation or source directly and record the gap. Identify returned web fallback results as such; do not present them as indexed primary-source passages. Routine code using already verified project APIs does not require repeated searches.

## Make decisions concrete

Write DESIGN.md in the project containing the brief, page structure, brand tokens, assets, and a source-to-element table:

| Target element | Source URL / record / section | What to borrow | Brand adaptation | Evidence / open issue |
| --- | --- | --- | --- | --- |

Describe composition, proportions, type treatment, image framing and interaction behaviour concretely. Explain why the combination fits this client. Keep the client's existing identity unless a redesign includes changing it. Translate reference elements into one local type scale, spacing system, shape language and motion vocabulary. Do not transplant unrelated brand colours or distinctive identity assets just because they look attractive.

Use licensed/user-owned assets or separately sourced replacements; a reference asset URL is evidence, not reuse permission. Track source-code, font and asset licences independently. Match replacements to the framing, lighting and visual weight needed by the composition. Avoid leaving placeholder imagery in a result described as finished.

## Generate imagery when needed

Use image generation when the composition needs brand-specific photography, illustrations, textures, backgrounds or cutouts that supplied assets do not cover. Read [image generation](references/image-generation.md) for the self-contained workflow; use a host-provided imagegen skill if available. Proceed within the website brief without a separate approval for every image; preserve real client/product identity and any user restrictions.

## Implement

Follow the researched technical plan and existing deployment conventions. Revisit the plan when new evidence changes compatibility or feasibility; no universal framework is required by this skill.

When researching implementation code, prefer Firecrawl Developer Index when available; otherwise search current official documentation and public source directly. When available, read the firecrawl-developer-index skill and use its developer search for library selection, API usage, animation/scroll/3D implementation examples, errors and known fixes. Search for the specific behaviour and relevant library/version; prefer official documentation, repository READMEs and merged pull requests. Inspect the source passages, version compatibility, dependencies and code licence before adopting an example. An issue report alone does not establish current behaviour or a released fix.

Keep implementation research tied to the initial plan; apply the same source and fallback rules when resolving new questions.

Build the anchor section and one representative lower section early, inspect their rendered relationship, then extend the direction. Preserve real client copy and content hierarchy. Use component sources from library/components.json when they fit; inspect their implementation, dependencies and licence before incorporation. Re-style them for the client rather than assembling unmodified demos.

For multi-page transitions, scroll jacking/smoothing, or library identification, read [page transitions and scroll control](references/page-transitions-scroll.md). Audit these separately from menu animations and section reveals.

For animation-led references, read [animation patterns](references/animation-patterns.md) and write a motion contract for each selected effect in DESIGN.md. Prototype the defining interaction with representative assets early. For any 3D or substantial motion, also read [motion and 3D](references/motion-3d.md). Keep public-facing content and navigation usable without the effect.

## Complete motion across user flows

For a motion-led site, plan supporting transitions alongside the signature interaction rather than waiting for follow-up requests. Inventory the actual interactive surfaces: product details, dialogs/drawers, basket, checkout steps, menus and confirmations. Opening, closing and changing steps should feel coherent with the reference's pace, direction and easing. These transitions complement the signature interaction; they do not replace it. Honour reduced-motion preferences and any later explicit user override of the animation requirement.

Adapt the treatment to the site: a soft lift/scale for product details, a side drawer on desktop or bottom sheet on mobile for a basket, and a brief directional fade between steps are options, not a universal template. Keep routine quantity updates steady instead of replaying the whole entrance. Define the closing motion as well as opening; retain native dialog semantics, focus containment, Escape/backdrop dismissal, focus restoration and scroll behaviour throughout. Use subtle fades or immediate state changes for reduced motion. Do not delay essential actions for decorative sequencing.

Prototype and exercise these transitions in the rendered primary flow, including rapid open/close, back navigation, narrow screens and reduced motion. Record the treatment and observed checks with the other motion contracts in DESIGN.md.

## Inspect and refine

Open the rendered build with available browser tools. Compare selected reference sections and the implementation at matching viewport sizes and corresponding scroll states. For close-match briefs, explicitly compare section proportions, dominant colour coverage, headline and utility text sizes, asset scale/crop, controls and motion progression. Record the largest discrepancies and fix them before adding optional decoration. Client-approved adaptations and asset rights remain constraints; closeness does not permit copying protected brand assets.

Inspect desktop, mobile and an intermediate width; scroll the whole page; exercise navigation, hover/focus, touch alternatives, forms and animation states. Check type hierarchy, line breaks, section rhythm, crop, alignment, contrast, loading, reduced motion, console/runtime failures and layout overflow. Read [review criteria](references/review.md) when reviewing substantial builds.

Fix observed weaknesses and recheck affected areas. Record actual checks and remaining limitations in DESIGN.md or the project's existing delivery notes. If visual tools fail, report visual QA as incomplete; do not equate a successful build with design verification. Finish when the brief is fulfilled and material observed issues are resolved, not after an arbitrary number of passes.

Deliver the built result, preview, source map and a concise account of checks. Publish only within the user's authorization. When the user approves or rejects a reference, save their specific preference without turning it into a universal rule for all clients.

## Improve the skill through evidence

When asked to assess or trial this skill, read [evaluation](references/evaluation.md). A larger catalog alone does not establish better output. Test brand fit and animation execution on realistic briefs, then make narrow improvements based on observed results.
