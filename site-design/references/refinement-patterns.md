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

## Lessons from a trades site (bathroom installer, Nov 2026)

The client asked for a Beams Renovation-style site (beamsrenovation.com) with Hummingbird motion. These are general lessons, not that client's identity.

### Symptoms and fixes

| Symptom | Likely cause and focused remedy |
| --- | --- |
| Client "doesn't know why" colours and fonts were chosen | The direction was justified only by loosely related references. Derive from the reference the client names, test pairings side by side and write the reason down. |
| "There is no scroll animation" | Reveals existed but were too subtle (small travel, few targets). Reveal every readable block with opacity plus 40–60px travel; add one load moment such as the hero photo coming into focus from a blur. Also ask whether the system's Reduce Motion setting is on. |
| Hero text sits low on a big screen | A portrait photo's intrinsic height made the grid taller than the viewport. Absolutely position the image inside its column. |
| Hero stops short of the window bottom | A max height cap. Use `max(min, 100svh - header)`, not a clamp with an upper bound. |
| Whole page is thousands of pixels wide | A `width: max-content` marquee inside a `display: grid` body with an `auto` column. Give the body `grid-template-columns: minmax(0, 1fr)`. |
| Page looks blank in full-page screenshots | Scroll reveals never fired, or the browser restored an old scroll position. Scroll through the page before capturing and check `scrollY`. |
| Long proof strip gets skimmed | Figure + bold label only; keep longer sentences for the markdown/agent version. |
| Contact details repeated at the bottom of every page | A closing invitation band duplicates the header and footer. Remove it when both already carry the primary action and phone number. |
| Two adjacent sections blur together | They share a background. Alternate grounds (stone/paper) at the boundary. |

### Image pipeline

Replicate models used successfully, cheapest and most faithful first. Record every output in DESIGN.md with what it changed.

1. **Split composites** (slideshow triptychs) into single panels by detecting the white separator columns; crop out baked-in logos.
2. **Faithful upscale:** `nightmareai/real-esrgan` at 4x sharpens without inventing content. Topaz `image-upscale` gave no visible gain on 470px sources.
3. **Widen:** `bria/expand-image` in canvas mode keeps the original pixels centred and generates only the edges. Inspect the edges for duplicated fixtures (it added a second tap).
4. **Re-render for very large bands:** `google/nano-banana-pro` at 4K turns a soft expanded image into a sharp one while keeping the room, but can still add stray fixtures.
5. **Reframe:** `google/nano-banana-pro` (best) or `black-forest-labs/flux-kontext-max` can turn an angled photo square-on. Expect small changes such as tap shapes or a redrawn mirror; show options beside the original.
6. **Style:** `black-forest-labs/flux-3-image` adds props (plant, soap, candle) and a vignette while leaving the room intact. Keep the unstyled version and a one-line switch.
7. **Video:** `bytedance/seedance-2.0`/`2.5` first/last-frame generation from one or two photos reads as a camera move, not a walkthrough, and can hide details. Ask for real footage or more photos of the room before promising a tour.

### Agent-facing extras

- Label the footer `llms.txt` link for people ("For AI agents"); agents find `/llms.txt` and markdown alternates by convention.
- An FAQ built only from facts already published on the site helps both visitors and agents; emit `FAQPage` JSON-LD and include it in the page's markdown twin.
- WebMCP: declarative `toolname`/`tooldescription`/`toolparamdescription` on the main form (no auto-submit for a mailto form), plus read-only `registerTool` tools for contact details and service areas, feature-detected on `document.modelContext` then `navigator.modelContext`. Fallow does not follow Astro client-script imports; list `src/scripts/*.ts` as entries.
- A mailto form needs no CAPTCHA. Add a honeypot and Cloudflare Turnstile when a real backend arrives.
