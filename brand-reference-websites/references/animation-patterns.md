# Animation reference workflow

Animation is a first-class design input. Search by interaction as well as visual style. The same material or 3D object can behave differently under idle, pointer, click, drag or scroll control.

The current library contains sampled homepage observations from eight sites. Read each record's review_coverage and linked action notes. Reviewed means listed states were inspected, not complete animation, mobile or accessibility coverage. The initial seven-site audit did not measure exact timings/easing. Ali Two Times now includes source-defined parameters, explicitly distinguished from runtime measurements. Visual patterns with unknown triggers are candidates for further inspection, not verified animation recipes.

## Motion contract

This is the canonical field list for documenting build effects in DESIGN.md. Use it for signature interactions, scroll effects, route changes and supporting UI motion. For each effect, specify:
- The business purpose and target element, with source record and section.
- Trigger: load, viewport entry, scroll progress, hover/focus, pointer movement, click, drag or idle.
- Start, intermediate and end states; which elements move, reveal, swap, scale or change colour; which remain anchored.
- Sequencing: simultaneous vs staggered, and relationships between text, imagery, background and controls.
- Scroll model: time-triggered on entry vs progress-scrubbed, pinned range if applicable, and what happens on reverse, interruption and revisit.
- Timing and easing: source measurements when actually measured, or source-defined values when verified in code; otherwise label chosen values as implementation decisions, never facts about the source.
- Renderer/asset plan: CSS/SVG, image layers, video, image sequence, shader or realtime 3D; keep source technology unknown unless verified. Link the asset entries in the [asset plan](build-decisions.md#asset-plan-and-provenance), including missing models and mobile resource constraints.
- Narrow-screen and reduced-motion alternatives, plus keyboard/touch behaviour. Distinguish observed source behaviour from a proposed improvement.

For route effects, also identify source/destination routes and clicked control; cover/mask and persistent/shared elements; direction and active-navigation treatment; when input unlocks; and focus/scroll restoration. For 3D scenes, add subject, framing, materials/lighting, camera/object states and relationship to live copy. These are conditional extensions of this contract, not separate field lists.

Link source observations to the [library evidence schema](library-model.md#animation-fields-and-browsing). Source records describe observed facts; a client contract may add clearly labelled implementation decisions and accessibility improvements.

A sentence such as 'smooth GSAP animation' is not a motion contract. Describe what the visitor sees and controls before choosing a library.

## Reusable patterns in this library

- Mana flavour switch: product, scene artwork, palette and label change together after an arrow click. Adapt for product variants with an anchored central object.
- Lusion scene: glossy abstract forms continue changing orientation while scroll position stays fixed. Treat as ambient scene evidence; do not infer pointer physics from that alone.
- AQuest text entry: oversized heading resolves after scrolling into Selected Works. Exact trigger/timeline still requires inspection before close reproduction.
- Floema collection handoff: collage opening gives way to large scene photography; successive collection imagery layers during scroll. Check intermediate mask/text states carefully.
- Goodboy marquee: horizontal logos move while the viewport is stationary. Readability and reduced motion matter more than copying speed.
- Lando menu: dark covering layer enters before image grid and navigation settle. The sequence is part of the brand expression, not just a visibility toggle.
- United Carriers: count-ups continue after scroll stops; a later container scene changes from stacked to lifted with further scroll. Separate metric animation from process storytelling.

Read actual records for evidence and caveats. A static-looking globe or portrait composite is not automatically an audited 3D interaction.

## Build and compare

Prototype the defining motion with representative client assets before building all sections, then apply the [motion verification checks](review.md#motion-verification). Use the same action sequence on source and implementation at comparable widths. Preserve the intended feel and user control; copy neither unmeasured timings nor source usability defects.

If exact matching is important, capture a short video or an ordered screenshot series with timestamps/scroll positions using available tools and retain it with the record. For state-only evidence, say so. Do not mark it frame-verified or infer smoothness/frame rate.

Prefer reusing a tested local motion recipe once it exists. The current library contains observations and adaptation proposals, not a tested animation component package. Promote a pattern into reusable code only after a real build proves it useful; preserve API, dependencies, asset needs, checks and limitations alongside it.

For route choreography, scroll interception and library evidence, read [page transitions and scroll control](page-transitions-scroll.md).
