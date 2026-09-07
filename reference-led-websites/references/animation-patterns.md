# Animation reference workflow

Animation is a first-class design input. Search by interaction as well as visual style. The same material or 3D object can behave differently under idle, pointer, click, drag or scroll control.

Read selected records and their inspection caveats through [library access](library-access.md).

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

Link source observations to the schema located through [library access](library-access.md). Source records describe observed facts; a client contract may add clearly labelled implementation decisions and accessibility improvements.

A sentence such as 'smooth GSAP animation' is not a motion contract. Describe what the visitor sees and controls before choosing a library.

## Build and compare

Prototype the defining motion with representative client assets before building all sections, then apply the [motion verification checks](review.md#motion-verification). Use the same action sequence on source and implementation at comparable widths. Preserve the intended feel and user control; copy neither unmeasured timings nor source usability defects.

If exact matching is important, capture a short video or an ordered screenshot series with timestamps/scroll positions using available tools and retain it in the client project; shared-record updates belong to the curator. For state-only evidence, say so. Do not mark it frame-verified or infer smoothness/frame rate.

Prefer reusing a tested local motion recipe once it exists. The current library contains observations and adaptation proposals, not a tested animation component package. Promote a pattern into reusable code only after a real build proves it useful; preserve API, dependencies, asset needs, checks and limitations in the project. Shared-library promotion requires a separate curation task.

For route choreography, scroll interception and library evidence, read [page transitions and scroll control](page-transitions-scroll.md).
