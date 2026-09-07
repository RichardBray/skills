# Reusable website build prompt

Fill bracketed fields using the interview and existing context. Remove irrelevant sections. The final handoff must contain no unfilled brackets.

---

Read and use the website skill at:
[Absolute path to brand-reference-websites/SKILL.md]

This is the build stage. Use the following completed brief without repeating answered questions. Work autonomously within its scope; ask only about a consequential unresolved issue. Inspect the project before choosing implementation tools.

## Project and outcome

Build [site type and scope] for [brand name; established brand or fictional concept].
Target directory: [absolute project path, or establish the target directory before writing files].
Audience: [who they are, their situation and what matters to them].
Offer: [products/services, variants and distinguishing qualities].
Primary visitor action: [buy, enquire, book, subscribe or other measurable goal].
Success means: [specific visitor experience and business outcome].

## Brand and content

Personality and positioning: [concrete traits and differentiation].
Existing identity to preserve: [logo, colours, fonts, packaging, tone; or permission to develop them].
Supplied assets/content: [absolute paths or URLs, availability and usage rights].
Missing assets/content: [what to source, generate, draft or request].
Avoid: [specific dislikes or brand constraints].
Claims and data: [verified facts and demo-content boundaries; do not fabricate reviews, certifications or product specifications].

Typography and copy: Keep all readable website copy at least 16 CSS px, including mobile, navigation, controls and footer; aim for 18px or larger body paragraphs. Do not use em dashes in authored copy or visible text in generated assets. Follow the skill’s rendered typography and copy checks.

## Reference-led art direction

Overall direction: [composition, type treatment, palette, imagery and why they fit this brand].
Anchor reference: [URL/record path and precise page/section].
Borrow and adapt: [specific defining elements to preserve and brand changes to make].
Supporting references: [URL + section + element + role; omit if unnecessary].
Evidence: [what has actually been inspected, capture/report paths and what needs live verification].
Reference fidelity: [close match or selective adaptation, plus approved deviations].

Use the library and relevant Firecrawl design extraction workflow to inspect selected references. Keep source design reports separate from this project's DESIGN.md. Verify motion in live interaction rather than inferring it from still images. Preserve the defining reference qualities when adapting them to the brand.

## Pages and functionality

Pages/sections and content priorities: [explicit scope and sequence, or a delegated structure within stated bounds].
Primary end-to-end flow: [visitor steps and expected outcomes].
Functional integrations: [real integrations, local demos, missing access and out-of-scope features].
Content editing requirements: [CMS/management needs or none].

## Signature interaction and motion

Signature interaction: [purpose, reference section, trigger, before/after states and effect on exploration; or a later explicit user override].
Required assets: [cutouts, models, image sequences or other inputs].
Multi-page requirement: If the site has multiple pages/routes, deliver reference-backed page transitions meeting the skill’s explicit acceptance criteria with deliberate exit/entry choreography and shared-element continuity where appropriate. Consider View Transitions when suitable; verify compatibility and provide functional fallbacks and reduced-motion behaviour. Test real route changes, back/forward, focus, scroll restoration and interrupted navigation.

Supporting motion: [navigation/page transitions, product changes, drawers/dialogs, cart/forms and closing states relevant to the scope].
Required scroll animations: [reference-backed effects, affected sections, trigger/start/end states and replay or reversal behaviour]. Every site must have a deliberate scroll animation sequence appropriate to its brand. Smooth scrolling alone, page-load entrances and hover effects do not fulfil this requirement. Preserve usable native scrolling unless a verified design requires otherwise.
Mobile/touch adaptation: [intended alternative or delegate within usability constraints].
Reduced-motion alternative: [static/simpler treatment preserving access and meaning].

## Imagery and 3D

Asset art direction: [subject, composition, lighting, materials, packaging consistency and crop requirements].
Generation choices: [built-in image tool default; any explicitly requested API model/provider].
3D role and route: [none, real interactive geometry, rendered imagery or video; supplied models, Blender or optional reconstruction as appropriate].
Tools reported available: [relevant tools to verify in the new environment, never credentials].
Paid API authorization: [exact authorized provider/scope/budget, or no authorization supplied, ask before paid generation].
Preserve real product identity. Inspect generated assets and actual browser rendering. A 3D-looking image does not count as interactive geometry.

## Implementation constraints

Existing stack/platform: [known requirement, or preserve a suitable existing stack and research choices for a new project].
Timeline and scope priorities: [constraints and what to prioritise if tradeoffs arise].
Deployment: [local preview only, or explicit destination and authorization].
Other constraints: [only relevant requirements].

## Build and verify

Write DESIGN.md with the brief, reference-to-element mapping, asset provenance, technical decisions and motion contracts. Prototype the defining interaction and anchor section with representative assets before extending the site. Follow the skill's research and implementation workflow.

Inspect the rendered result on desktop, mobile and an intermediate width. Scroll down and back up, inspect intermediate animation states and reduced-motion fallbacks, and exercise the full primary flow, opening/closing transitions, touch/keyboard alternatives and reduced motion. Check visual fidelity, type, spacing, crops, loading, overflow and runtime errors. Fix observed weaknesses and recheck affected areas.

Deliver [working local preview and project files, plus any specifically requested deliverables]. Report actual checks and material limitations. Distinguish demo functionality from production integrations. Do not publish or incur paid-provider costs beyond the authorization above.

## Explicit assumptions or delegated decisions

[Only meaningful provisional assumptions, unresolved blockers and decisions intentionally left to the builder; otherwise remove this section.]
