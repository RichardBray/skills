# Motion requirements and acceptance

Read for every build and when specifying motion in a build prompt.

## Interactive quality requirement

For website builds and redesigns, deliver at least one reference-backed signature interaction appropriate to the brief. It must meaningfully shape how visitors explore the content or products. Basic hover effects, entrance fades, accordions, and navigation transitions do not satisfy this requirement by themselves. 3D is optional; a flat design can provide a distinctive interactive experience. Scroll animation is required for every site by default; only a later explicit user override can change that scope. Reduced-motion accessibility remains required.

Before implementation, define the interaction's purpose, exact reference section, observed trigger and before/after states, required assets, mobile behaviour, and reduced-motion alternative in DESIGN.md. Inspect the reference behaviour directly: screenshots establish composition, not motion. Match assets to the interaction, including cutouts or models when needed; do not substitute rectangular photographs when the defining composition requires isolated objects.

Implement and inspect the signature interaction in the anchor section with representative assets before extending the site. Do not describe the result as complete until the interaction, primary user flow, mobile alternative, and reduced-motion fallback have been exercised in the rendered build. Record actual observations and unresolved limitations; a successful build alone does not satisfy this gate.

If the defining interaction is omitted or substantially simplified, explain the specific reason and treat this as a change in design direction, not a faithful adaptation. Do not silently replace it with generic micro-interactions or claim unverified behaviour.

Keep project references isolated: do not inspect sibling projects unless the user explicitly authorizes them as references. Keep client preferences scoped to that client rather than turning a previous project's design into the default for new work.

## Required multi-page transitions

Every multi-page site, including client-side routed sites, must have reference-backed transitions meeting the acceptance criteria below between its primary pages. Treat route changes as part of the art direction, with a coherent outgoing/incoming sequence and purposeful continuity of shared elements, typography, imagery or colour. Match the chosen reference and brand; do not apply the same generic fade to every site. First-load entrances, menu animations and scroll effects do not fulfil this separate requirement.

Read [page transitions and scroll control](page-transitions-scroll.md). Consider the browser View Transitions API when it suits the routing architecture and desired effect; verify current official documentation and target-browser support before choosing it. Use a compatible router/motion approach when needed. Keep navigation functional when the enhancement is unsupported, interrupted or reduced by user motion preferences. Carry the requirement into prompt preparation and final browser review for every multi-page brief.

Page-transition acceptance: specify and observe at least one reference-derived visual continuity device (for example a matched image, directional mask or coordinated typography) across the primary route changes. Document exit, intermediate and entry states, the chosen timing, and the source element. Exercise forward/back, rapid navigation, focus/scroll restoration and reduced-motion/unsupported-browser fallbacks. All destinations must remain reachable with no stuck overlay, duplicated content or navigation lock. Visual QA must compare these states with the chosen reference and record deviations.

The three motion requirements have different purposes: the signature interaction changes content exploration; scroll animation responds to scroll; page transitions connect routes. One implementation may satisfy multiple requirements only when its observed behaviour meets each criterion. Do not add redundant effects merely to count three features.

## Required scroll animations

Every website built or redesigned with this skill must include deliberate, reference-backed scroll-triggered or scroll-progress animation. Carry this requirement into every generated build prompt. Do not ask whether to include scrolling animation; ask only about its character or intensity when unresolved. Choose motion to suit the brand and content, such as staged section reveals, product movement, image transitions or a scroll-linked narrative. Design a coherent progression through the main page rather than relying on a single token fade. Page-load entrances, hover effects, smooth scrolling alone and route transitions do not satisfy this requirement.

Record the chosen reference, affected sections, trigger/start/end states, replay or reversal behaviour, required assets and mobile adaptation in DESIGN.md. Scroll animation may also satisfy the signature-interaction requirement when it meaningfully changes exploration; basic reveal effects alone do not replace the existing signature-interaction requirement. Use native scroll where suitable; scroll animation does not require scroll jacking, pinning or a specific library.

Exercise actual scrolling down and back up in desktop and mobile layouts, including intermediate animation states and resize. Check for stuck pins, inaccessible content, layout jumps and poor rendering performance. Honour prefers-reduced-motion with simpler or static states that preserve all content and functionality. That accessibility fallback does not waive animation for the normal-motion experience. Do not call the build complete until scroll behaviour and its fallback have been inspected in the browser.

## Complete motion across user flows

For a motion-led site, plan supporting transitions alongside the signature interaction rather than waiting for follow-up requests. Inventory the actual interactive surfaces: product details, dialogs/drawers, basket, checkout steps, menus and confirmations. Opening, closing and changing steps should feel coherent with the reference's pace, direction and easing. These transitions complement the signature interaction; they do not replace it. Honour reduced-motion preferences and any later explicit user override of the animation requirement.

Adapt the treatment to the site: a soft lift/scale for product details, a side drawer on desktop or bottom sheet on mobile for a basket, and a brief directional fade between steps are options, not a universal template. Keep routine quantity updates steady instead of replaying the whole entrance. Define the closing motion as well as opening; retain native dialog semantics, focus containment, Escape/backdrop dismissal, focus restoration and scroll behaviour throughout. Use subtle fades or immediate state changes for reduced motion. Do not delay essential actions for decorative sequencing.

Prototype and exercise these transitions in the rendered primary flow, including rapid open/close, back navigation, narrow screens and reduced motion. Record the treatment and observed checks with the other motion contracts in DESIGN.md.
