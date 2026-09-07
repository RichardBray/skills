# Review the rendered result

Compare reference and implementation with their different brands and content in mind. Record specific observations and fixes rather than an invented quality score.

- Brand fit: the visual direction suits the audience, positioning, assets and desired action. The site has its own client identity.
- Reference fidelity: compare reference/build at matching viewport sizes and equivalent start/mid/end scroll states. Check section order and heights, dominant colour fields, type scale including small utility text, focal-object scale, framing, button shape and hover response, decorative motion and persistent navigation. Each source-to-element mapping must reproduce its intended composition or behaviour; explain deviations and fix the largest mismatches first. Do not substitute a generic page because its components function.
- Typography: verify the SKILL.md typography floor using computed sizes at desktop and mobile widths, including navigation, footer, captions, controls and open overlays. Body paragraphs should normally be 18px or larger; readable copy must be at least 16px unless the user explicitly requested an exception. Check hierarchy, measure, wrapping, font loading and spacing.
- Copy: no em dashes in authored visible text, metadata, accessibility labels or generated artwork. Search literal and encoded/escaped forms, rewrite naturally and inspect rendered states; preserve raw source evidence.
- Layout: clear focal points and reading order; deliberate section rhythm; consistent local alignment; no accidental gaps or overflow.
- Assets: purposeful subject/crop/light; no distorted or unresolved images; rights/source notes for used assets.
- Scroll animations: required on every site unless explicitly overridden by the user. Verify a reference-backed progression through the main page, with actual desktop/mobile scroll tests, reverse scrolling, intermediate states and a reduced-motion fallback. Smooth scrolling or page-load effects alone do not count.
- Multi-page transitions: mandatory for multi-page builds. Inspect the reference-backed outgoing/incoming sequence in actual route changes on desktop/mobile, plus shared-element continuity where used. Exercise back/forward, direct URLs, scroll restoration, focus, rapid navigation, unsupported-enhancement fallback and reduced motion. First-load entrances or menu animation alone do not count.
- Motion: transitions connect meaningful states; no distracting perpetual motion; scroll/hover/touch and reduced-motion states function.
- Flow transitions: product details, basket/drawers, checkout steps and confirmations have deliberate opening, closing and state-change behaviour when appropriate to the brief. Check Escape, backdrop dismissal, restored focus, rapid reversal, stable quantity updates and reduced motion; a polished hero alone does not complete the interaction design.
- Client functionality: required links, menus, forms and error/success states work. Do not send a live form submission or message merely to test without authorization; use a test endpoint or safe local verification.
- Mobile: content order, tap targets, navigation, scene fallback and text readability are intentionally adapted.
- Delivery: appropriate build checks, actual visual checks, observed loading/runtime issues and remaining limitations are recorded. Do not claim production readiness for untested integrations.

If the output feels generic, identify the cause: weak assets, unrelated typography, default component styles, repetitive section structure, or failure to implement a chosen source element. Fix that cause rather than adding arbitrary decoration.
