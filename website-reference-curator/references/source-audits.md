# Audit source motion and technology

Treat these as separate dimensions:
- Page transition: route-to-route exit, overlap/cover and entry sequence.
- Scroll-linked animation: visual progress follows scroll position; this alone does not establish scroll jacking.
- Pinned scene: part of the composition stays fixed for a scroll interval; it may still use native scrolling.
- Smooth/custom scrolling: scroll position or content translation is interpolated by code.
- Scroll interception/jacking: normal wheel/touch/key behaviour is overridden or remapped. Record the actual mechanism rather than applying a subjective label.

## Page-transition audit

Inspect at least a primary route change and a work/detail route if relevant. Collect observed states and actions under the [library evidence schema](library-model.md#animation-fields-and-browsing); leave unobserved source behaviour explicitly unknown. Separate first-load entrances from route transitions and menus from actual route changes.

Inspect direct entry, primary route changes, back/forward, rapid repeat clicks, focus/scroll restoration, mobile and reduced-motion behaviour where available. Record exit/intermediate/entry states, shared elements, masks and when input unlocks. Mark untested paths explicitly. Record source-code timing evidence according to the [library schema](library-model.md#animation-fields-and-browsing) when screenshot sampling misses intermediate frames. Do not conclude a transition is absent because screenshots show only endpoints.

Ali Two Times has source-backed contextual header, contact, project, campaign and back transition branches. Read its site record and source-analysis evidence for the branches actually audited. Work/Bio uses horizontal clipping and counter-moving heading/mask; Contact/project use vertical outgoing clipping. Avoid assuming one universal fade covers the site.

## Scroll audit

Record per site scroll_control.mode: native | native-with-smoothing | custom-wheel-transform | snapping | remapped-axis | unknown. Add evidence and verification (observed, source-confirmed, inferred or not-assessed).

Test small/large wheel deltas, pause, reverse, trackpad where available, PageDown/Space/arrows, touch, anchors and page back. Compare viewport scroll position with transformed content if read-only DOM inspection permits. Record input capture, smoothing, pinned ranges, horizontal remapping, snapping, and whether the user can leave a scene. Identify mobile differences and reduced-motion behaviour independently.

Describe the source mechanism without prescribing that future client builds must reproduce its input interception.

## Library identification

Store technology_findings with library name, version if verified, evidence IDs and scope. A bundle banner or import confirms presence; effect-specific calls are stronger evidence of use. A smooth-looking interaction is not evidence of GSAP, ScrollTrigger, Lenis or any other package. A GSAP core bundle alone does not establish ScrollTrigger usage. Do not turn the absence of an unminified name into proof a package is absent.

Separate source_library from recommended_implementation. Choose compatible current tools when building; verify official APIs and licence terms then. CSS/Web Animations, a framework's motion system, GSAP or a custom renderer can reproduce overlapping behaviours. Router transitions, scroll smoothing, DOM animation and 3D rendering solve different problems; do not treat them as interchangeable libraries.

The Ali capture verifies GSAP 3.3.3 plus custom wheel/transform scrolling. It does not establish Lenis or ScrollTrigger. Other current records retain unknown technology/scroll-control fields until inspected.
