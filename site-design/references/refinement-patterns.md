# Refinement patterns from Hummingbird

These are contextual lessons, not a fixed theme or component kit. The original project used Astro, authentic session photographs, watercolor artwork and a retained external booking calendar. New projects should select their own identity and integrations.

## Reference mapping

Floema (https://floema.com/en) informed the central statement with surrounding imagery and the handoff to larger photography. MANA (https://en.manayerbamate.com/) informed coordinated image/text/background changes. Ali Two Times (https://alitwotimes.com/) informed continuity between routes. These were inspected in September 2026; inspect current states before making new claims or reusing their direction.

An experiment sampled MANA's leaf green, blue, yellow and navy into Hummingbird, then the user chose to restore the original palette. The lesson is to offer a traceable comparison, not to decide that stronger colour or beige is inherently better. Preserve the skill's evidence-based colour requirement even when a particular client prefers cream.

## Common symptoms and fixes

| Symptom | Likely cause and focused remedy |
| --- | --- |
| Hero feels empty despite large art | Viewport height and peripheral placement overwhelm the central group. Cap tall-screen hero height, adjust optical alignment, and bring artwork inward. |
| Supporting hero copy dominates | Type hierarchy is inconsistent. Compare with other page introductions before enlarging every text style to match. |
| Image corners look square within a rounded outline | The element is wider than the contained bitmap. Match its rendered aspect ratio or crop intentionally before rounding. Keep reveal masks consistent with settled corners. |
| Huge gap above FAQs | Two neighbouring sections both contribute full spacing. Reduce their combined padding, scoped to this adjacency. |
| Footer crowds a wavy closing section | The curve extends outside normal section bounds. Add clearance for the visible curve, not just its parent box. |
| Footer floats above the bottom on a short page | Use a full-height flex/grid document shell, with main content taking remaining space. Do not pin the footer over content. |
| Page appears to animate twice | CSS page entry and JavaScript-added reveal states both affect the same hero. Assign one entrance owner and reserve scroll reveals for later content. |
| Menu survives into destination snapshot | Navigation starts while an asynchronous closing animation is still running. Dismiss/cancel the outgoing menu before ordinary navigation; retain animated close for menu-button/Escape interactions. |
| A shared section is missing from one route | Check the full route inventory, not only homepage polish. Reuse the component and adapt self-referential actions. |

## Motion contracts

For each important interaction record: trigger; elements that move; what stays anchored; start, intermediate and settled states; interruption/reversal; mobile adaptation; reduced-motion and no-JavaScript behaviour. Timings are implementation choices unless measured from the reference.

- Session comparison: explicit labelled tabs coordinate copy, photo and background. Keep controls and booking action stable, support reverse selection and keyboard use, and leave both descriptions accessible without JavaScript. An informational selector must not imply live availability.
- Accordion: native semantic disclosure, smooth height change and icon state. Test rapid reversal, several open items and reduced motion. Avoid clipping focus or leaving closed content keyboard-accessible.
- Illustration entrance: a modest inward drift can tie peripheral artwork to the headline. Keep ambient loops slow and low-amplitude when requested; disable them for reduced motion.
- Curved boundaries: use a shared scalable shape whose fill tracks its section colour. A very small looping deformation can add life for a playful brand. Check seams, stacking, pointer interception and clearance above/below.

## Image and publication boundaries

Lighting and depth-of-field edits should retain the subject's likeness, pose and factual context. Preserve source assets and record which images are edited. Do not bundle a client's photographs or contact data into a reusable skill.

Keep one explicit record of what is live versus local. A source backup supports reverting an experiment; a confirmed deployment identifies the live baseline. Build only the approved version for publication. An existing external calendar's apparent speed can vary with caching and server response; don't attribute that improvement to an unrelated front-end rebuild.
