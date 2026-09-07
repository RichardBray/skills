# Review the rendered result

Compare reference and implementation with their different brands and content in mind. Record specific observations and fixes rather than an invented quality score.

- Brand fit: the visual direction suits the audience, positioning, assets and desired action. The site has its own client identity.
- Reference fidelity: compare reference/build at matching viewport sizes and equivalent start/mid/end scroll states. Check section order and heights, dominant colour fields, type scale including small utility text, focal-object scale, framing, button shape and hover response, decorative motion and persistent navigation. Each source-to-element mapping must reproduce its intended composition or behaviour; explain deviations and fix the largest mismatches first. Do not substitute a generic page because its components function.
- Typography and copy: apply the [detailed checks](#typography-and-copy-checks).
- Layout: clear focal points and reading order; deliberate section rhythm; consistent local alignment; no accidental gaps or overflow.
- Assets: purposeful subject/crop/light; no distorted or unresolved images; rights/source notes for used assets.
- Motion: apply [motion verification](#motion-verification) against the documented contracts and required effects.
- Client functionality: required links, menus, forms and error/success states work. Do not send a live form submission or message merely to test without authorization; use a test endpoint or safe local verification.
- Mobile: content order, tap targets, navigation, scene fallback and text readability are intentionally adapted.
- Delivery: appropriate build checks, actual visual checks, observed loading/runtime issues and remaining limitations are recorded. Do not claim production readiness for untested integrations.

If the output feels generic, identify the cause: weak assets, unrelated typography, default component styles, repetitive section structure, or failure to implement a chosen source element. Fix that cause rather than adding arbitrary decoration.

## Motion verification

Use the canonical [motion contract](animation-patterns.md#motion-contract) to identify expected behaviour, and [motion requirements](motion-requirements.md) to judge whether the required effects are present. Record observations against each effect rather than maintaining a second field list.

- For every effect, inspect start, intermediate and settled states, reverse/interruption/revisit, desktop/mobile and reduced-motion alternatives. Use comparable actions and viewport sizes for reference/build comparison. Check performance and confirm all content remains accessible.
- For scroll effects, scroll down and back up, then resize. Check for stuck pins, layout jumps and inaccessible sections. For custom input handling, also run the [scroll audit](page-transitions-scroll.md#scroll-audit).
- For page transitions, exercise primary routes, direct URLs, back/forward, rapid/repeated clicks, loading/failure states and unsupported-enhancement fallbacks. Check shared-element matching, cleanup of prior animation state, focus destination, scroll restoration and that no overlay or navigation lock remains.
- For dialogs, drawers, checkout steps and confirmations, exercise opening and closing, rapid reversal, Escape/backdrop dismissal, focus containment/restoration and scroll behaviour. Quantity updates should remain stable. Preserve native semantics and keep routine actions responsive.
- For source audits, distinguish tested source behaviour from proposed improvements and mark untested cases. For builds, fix failures and rerun affected checks before reporting completion.

## Typography and copy checks

Use the font-size defaults in [Essential requirements](../SKILL.md#essential-requirements). These are project preferences, not a claim of an accessibility standard. Adapt layout and wrapping instead of shrinking text; a reference's tiny utility type does not override them. Check font loading, hierarchy, measure, wrapping and spacing.

Do not use em dash characters (U+2014) in any authored website copy, including metadata, alt text, labels, errors, generated packaging text and image prompts containing visible text. Rewrite the sentence with a full stop, comma, colon or parentheses as appropriate; do not mechanically replace them with double hyphens. Preserve factual meaning when editing supplied copy. Preserve raw reference captures and third-party source evidence unchanged.

During review, inspect computed font sizes in rendered desktop and mobile states, including open drawers/dialogs and validation messages. Check that the chosen font remains comfortable to read at the minimum size. Search authored content and rendered text for literal em dashes and encoded equivalents such as &mdash;, &#8212;, &#x2014; and escaped Unicode. Inspect visible text in generated imagery too. Fix violations before delivery and report any explicit user-approved exceptions.
