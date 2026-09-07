# Page transitions, scroll control and implementation evidence

Treat these as separate dimensions:
- Page transition: route-to-route exit, overlap/cover and entry sequence.
- Scroll-linked animation: visual progress follows scroll position; this alone does not establish scroll jacking.
- Pinned scene: part of the composition stays fixed for a scroll interval; it may still use native scrolling.
- Smooth/custom scrolling: scroll position or content translation is interpolated by code.
- Scroll interception/jacking: normal wheel/touch/key behaviour is overridden or remapped. Record the actual mechanism rather than applying a subjective label.

## Required implementation for multi-page sites

Plan a distinctive route transition system for every multi-page build. In DESIGN.md, map primary route pairs to the reference, exit/cover/entry states, shared elements, direction, timing, navigation/focus/scroll behaviour, mobile treatment and reduced-motion fallback. Keep duration appropriate for repeated navigation; visual impact must not make visitors wait for essential actions. Use contextual differences when the reference calls for them, while preserving a coherent motion vocabulary.

Consider View Transitions for shared-element continuity, image expansion, clipping or coordinated page changes when compatible with the chosen architecture. During implementation research, distinguish same-document route updates from cross-document navigation and verify the applicable official APIs, browser support and restrictions. Do not assume that a framework or browser automatically supplies the desired transition. Use an alternative motion implementation or immediate functional navigation when the enhancement is unavailable. Do not intercept external links or modified clicks merely to animate them.

Inspect actual primary page changes, not just their settled screenshots. Test desktop/mobile, direct URLs, back/forward, scroll restoration, focus, rapid repeat clicks, loading/failure states and reduced motion. Check that shared-element matches are correct, old animation state is cleaned up and navigation never remains locked. Record observed results and limitations. Do not mark a multi-page build complete with route transitions left as a follow-up task.

## Page-transition audit

Inspect at least a primary route change and a work/detail route if relevant. Record source and destination URLs, clicked trigger, outgoing content, covering layer/mask, persistent/shared elements, incoming sequence, active navigation colour, and when input unlocks. Separate first-load entrances from route transitions and menus from actual route changes.

Check back/forward, scroll restoration, focus destination, interrupted/repeated clicks and direct entry. Mark untested paths explicitly. Source-code inspection can establish parameters when screenshot sampling misses the intermediate frames; label them source-defined rather than runtime-measured. Do not conclude a transition is absent because screenshots show only endpoints.

Ali Two Times has source-backed contextual header, contact, project, campaign and back transition branches. Read its site record and source-analysis evidence for the branches actually audited. Work/Bio uses horizontal clipping and counter-moving heading/mask; Contact/project use vertical outgoing clipping. Avoid assuming one universal fade covers the site.

## Scroll audit

Record per site scroll_control.mode: native | native-with-smoothing | custom-wheel-transform | snapping | remapped-axis | unknown. Add evidence and verification (observed, source-confirmed, inferred or not-assessed).

Test small/large wheel deltas, pause, reverse, trackpad where available, PageDown/Space/arrows, touch, anchors and page back. Compare viewport scroll position with transformed content if read-only DOM inspection permits. Record input capture, smoothing, pinned ranges, horizontal remapping, snapping, and whether the user can leave a scene. Identify mobile differences and reduced-motion behaviour independently.

Do not install scroll interception automatically because a reference uses it. Reproduce the visual story with native scrolling when that meets the brief; if custom scrolling is needed, preserve keyboard, anchor, touch and history behaviour. This is an implementation choice within the user's reference-led direction, not a ban on immersive design.

## Library identification

Store technology_findings with library name, version if verified, evidence IDs and scope. A bundle banner or import confirms presence; effect-specific calls are stronger evidence of use. A smooth-looking interaction is not evidence of GSAP, ScrollTrigger, Lenis or any other package. A GSAP core bundle alone does not establish ScrollTrigger usage. Do not turn the absence of an unminified name into proof a package is absent.

Separate source_library from recommended_implementation. Choose compatible current tools when building; verify official APIs and licence terms then. CSS/Web Animations, a framework's motion system, GSAP or a custom renderer can reproduce overlapping behaviours. Router transitions, scroll smoothing, DOM animation and 3D rendering solve different problems; do not treat them as interchangeable libraries.

The Ali capture verifies GSAP 3.3.3 plus custom wheel/transform scrolling. It does not establish Lenis or ScrollTrigger. Other current records retain unknown technology/scroll-control fields until inspected.
