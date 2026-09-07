# Reference adaptation and build decisions

Read before writing DESIGN.md or selecting new implementation tools.

## Available tools and portability

This repository provides the workflow, reference library and catalog script. Firecrawl, Developer Index, image generation and Blender are optional host capabilities, not bundled dependencies. Discover available tools before invoking them. Prefer Firecrawl for extraction when available; otherwise use accessible browser tools, official pages or existing saved evidence and record the actual source. For missing image tools, use suitable supplied/licensed assets or report the specific asset gap. Do not silently install companion skills or block unrelated work because one is absent.

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
