# Page transitions, scroll control and implementation evidence

Treat these as separate dimensions:
- Page transition: route-to-route exit, overlap/cover and entry sequence.
- Scroll-linked animation: visual progress follows scroll position; this alone does not establish scroll jacking.
- Pinned scene: part of the composition stays fixed for a scroll interval; it may still use native scrolling.
- Smooth/custom scrolling: scroll position or content translation is interpolated by code.
- Scroll interception/jacking: normal wheel/touch/key behaviour is overridden or remapped. Record the actual mechanism rather than applying a subjective label.

## Required implementation for multi-page sites

Plan a distinctive route transition system for every multi-page build. Use the canonical [motion contract](animation-patterns.md#motion-contract), including its route-specific extension, in DESIGN.md. Keep duration appropriate for repeated navigation; visual impact must not make visitors wait for essential actions. Use contextual differences when the reference calls for them, while preserving a coherent motion vocabulary.

Consider View Transitions for shared-element continuity, image expansion, clipping or coordinated page changes when compatible with the chosen architecture. During implementation research, distinguish same-document route updates from cross-document navigation and verify the applicable official APIs, browser support and restrictions. Do not assume that a framework or browser automatically supplies the desired transition. Use an alternative motion implementation or immediate functional navigation when the enhancement is unavailable. Do not intercept external links or modified clicks merely to animate them.

Apply the route checks in [motion verification](review.md#motion-verification), inspecting actual page changes rather than only settled screenshots. Record observed results and limitations. Do not mark a multi-page build complete with route transitions left as a follow-up task.

## Page-transition audit

Inspect at least a primary route change and a work/detail route if relevant. Collect observations for the [motion contract](animation-patterns.md#motion-contract), including the route-specific extension; leave unobserved source behaviour explicitly unknown. Separate first-load entrances from route transitions and menus from actual route changes.

Use the route cases in [motion verification](review.md#motion-verification) when auditing source behaviour too. Mark untested paths explicitly. Record source-code timing evidence according to the [library schema](library-model.md#animation-fields-and-browsing) when screenshot sampling misses intermediate frames. Do not conclude a transition is absent because screenshots show only endpoints.

Ali Two Times has source-backed contextual header, contact, project, campaign and back transition branches. Read its site record and source-analysis evidence for the branches actually audited. Work/Bio uses horizontal clipping and counter-moving heading/mask; Contact/project use vertical outgoing clipping. Avoid assuming one universal fade covers the site.

## Scroll audit

Record per site scroll_control.mode: native | native-with-smoothing | custom-wheel-transform | snapping | remapped-axis | unknown. Add evidence and verification (observed, source-confirmed, inferred or not-assessed).

Test small/large wheel deltas, pause, reverse, trackpad where available, PageDown/Space/arrows, touch, anchors and page back. Compare viewport scroll position with transformed content if read-only DOM inspection permits. Record input capture, smoothing, pinned ranges, horizontal remapping, snapping, and whether the user can leave a scene. Identify mobile differences and reduced-motion behaviour independently.

Do not install scroll interception automatically because a reference uses it. Reproduce the visual story with native scrolling when that meets the brief; if custom scrolling is needed, preserve keyboard, anchor, touch and history behaviour. This is an implementation choice within the user's reference-led direction, not a ban on immersive design.

## Library identification

Store technology_findings with library name, version if verified, evidence IDs and scope. A bundle banner or import confirms presence; effect-specific calls are stronger evidence of use. A smooth-looking interaction is not evidence of GSAP, ScrollTrigger, Lenis or any other package. A GSAP core bundle alone does not establish ScrollTrigger usage. Do not turn the absence of an unminified name into proof a package is absent.

Separate source_library from recommended_implementation. Choose compatible current tools when building; verify official APIs and licence terms then. CSS/Web Animations, a framework's motion system, GSAP or a custom renderer can reproduce overlapping behaviours. Router transitions, scroll smoothing, DOM animation and 3D rendering solve different problems; do not treat them as interchangeable libraries.

The Ali capture verifies GSAP 3.3.3 plus custom wheel/transform scrolling. It does not establish Lenis or ScrollTrigger. Other current records retain unknown technology/scroll-control fields until inspected.
