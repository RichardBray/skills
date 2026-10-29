---
name: site-design
description: Build and refine polished public-facing websites from a brief or existing site, using reference-led art direction, concise copy, purposeful motion and browser annotation rounds. Use for visual website design and refinement, not backend-only changes or reference-library curation.
---

# Site design

Use the design process learned from the Hummingbird project, not its visual identity. The outcome is a coherent site that fits the client's audience and makes the next action obvious. Do not automatically reproduce its cream palette, serif headings, watercolour illustrations, wavy dividers or booking flow.

This skill works directly from a brief or existing project. If a separate build prompt or curated-library selection is requested, use `reference-led-websites` when available. Do not require that companion or restart an already established design process.

## Establish the direction

Read project instructions, existing implementation and accepted decisions first. Preserve a suitable stack; Astro was appropriate for Hummingbird's mostly static public pages, not a universal requirement. Ask only for missing information that would change the design: audience, primary action, brand constraints or reference preferences. Make routine reversible decisions and proceed.

Inspect one composition reference and compatible references for specific interactions. Use supplied references or an available library; if unavailable, gather project-local evidence with available browser/research tools. Inspect actual desktop/mobile states, including motion between states. A screenshot proves appearance, not interaction behaviour. Do not copy reference assets without appropriate rights.

Record in DESIGN.md:

- Audience, primary action and essential page structure.
- Reference URL and exact section, observed feature, intended adaptation and reason for deviation.
- Palette colours, their semantic roles and approximate proportions; typography scale and spacing rhythm.
- Asset provenance, motion intentions and material evidence gaps.

**No automatic beige or pastel palette.** Derive colours from observed references and the client's brand. Preserve saturation, contrast and colour balance deliberately instead of muting everything into a familiar model-generated style. Cream and pastels remain valid when supported by the brief or references. Treat a palette experiment as reversible: record the baseline, change only the intended variables, and compare the full journey before choosing.

## Build the useful structure first

Use one consistent primary action label across navigation, hero and closing sections. Keep its destination real. Consolidate duplicate pages or sections; retain useful URLs through appropriate redirects. Put essential facts where decisions happen, including verified prices, eligibility and location details. Never reuse Hummingbird's historical prices or policies for another client.

Reduce marketing copy to what helps visitors understand, trust or act. Remove redundant eyebrow labels, filler subheadings, decorative captions and repeated reassurance. For a verbose draft, aim for roughly 30–40% less nonessential copy, not a forced quota. Preserve practical and legal information. Use selective bold emphasis for scanning, not whole paragraphs. Prefer a strong authentic quotation to a carousel unless several quotes genuinely improve the story.

Use shared components for wordmarks, navigation, closing invitations and footer. Check consistency across every route, including Contact. A closing contact action on the Contact page should lead to an actionable destination rather than reload that same page. Reuse layout patterns intentionally, without repeating unnecessary copy.

## Compose with scale and restraint

Default readable copy to at least 18 CSS px, including mobile navigation, controls and footer; aim for 20px body text. Honour explicit project constraints. Make a larger hero's headline and CTA proportionate to its area. Keep supporting copy subordinate to the headline and consistent with comparable introductions elsewhere.

Balance the entire hero, not individual elements. Check optical vertical centring, text measure, line breaks and the distance between imagery and copy. Cap oversized viewport-based heroes on tall displays. Keep decorative art close enough to frame the content without crowding it. Remove decoration that does not earn its space. Do not add diagonal arrows to every link or button by default.

Use whitespace as a shared rhythm. Inspect adjacent sections together: their combined padding may double an intended gap. Curved edges can soften a playful brand, but use them only when supported by its direction. Account for their painted bounds when spacing nearby text and footers. Do not prescribe curves for every site.

A short page's footer should reach the viewport bottom through normal document layout; a long page's footer follows its content. Avoid fixed positioning that obscures content. Preserve comfortable space above footer columns and below the final line.

## Make imagery and motion intentional

Use the client's authentic imagery where suitable. When image improvement is requested, preserve identity and activity while making restrained lighting, exposure, crop or depth-of-field changes. Keep originals and record edits. Do not silently fabricate documentary details. Better photographs may justify more prominent placement; decorative illustrations should support the brand rather than replace useful evidence.

Check real rendered image bounds. Border radius around a letterboxed `object-fit: contain` element can leave the actual photo's corners square. Match the element to the image's aspect ratio or use an intentional cropped container. Review all four corners, masks, responsive crops and compositing against the actual background.

Plan motion as a coherent system: initial hero entrance, scroll progression, component state changes and route continuity. Match intensity to the brief and reference evidence. Make motion perceptible at ordinary browsing speed without delaying access to the main action. Sequence text and images where it adds hierarchy; do not repeatedly hide every line on every scroll.

Menus should animate both ways, but page navigation must not capture an outgoing open menu or leave it covering the new page. Use one coordinated page entrance to avoid double flashes. Accordions should open and close smoothly, support interrupted clicks and retain semantic keyboard behaviour. Loop subtle ambient illustration motion only when appropriate; respect reduced motion and avoid competing movement. Keep all content and primary actions usable without animation or JavaScript.

For concrete lessons and targeted fixes, read [refinement patterns](references/refinement-patterns.md).

## Refine in the browser

Prototype the hero, a meaningful interaction and a lower section before extending a new direction across the site. Then walk every page at desktop, mobile and an intermediate width. Also inspect a tall desktop viewport and the shortest page.

Use user annotations as targeted revision instructions. Identify the actual element and root cause, make the smallest coherent change, and check shared-component consequences. Preserve accepted decisions; a new annotation does not restart the design. Report what changed in plain language.

Before handoff, check layout overflow, computed type sizes, contrast, image crops, adjacent spacing, navigation, menu dismissal, accordion/tab states, keyboard focus, reduced motion and route transitions. Run checks appropriate to the changes. Browser verification and a successful build establish different things; report unavailable checks accurately.

## Keep preview and publication distinct

Maintain a local preview during annotation rounds. State whether a change is local or published. If the user asks to deploy the baseline before an experiment, validate and deploy that exact baseline first, save a recoverable copy, then change the local experiment. Never include the experiment in a deployment unless subsequently authorised.

Use the requested host/account and existing project. Deploy only within the user's current authorisation and verify success. Do not publish client photos, private research or development files just because a skill or template is being shared.

Retain functioning external booking/payment systems unless replacement is requested. Verify destinations and current factual information; do not imply a simple payment URL is the whole backend. Do not claim that a fast static front end has improved an unchanged external checkout without measurements.
