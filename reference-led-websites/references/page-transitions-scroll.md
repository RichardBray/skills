# Implement page transitions and scroll behaviour

## Required implementation for multi-page sites

Plan a distinctive route transition system for every multi-page build. Use the canonical [motion contract](animation-patterns.md#motion-contract), including its route-specific extension, in DESIGN.md. Keep duration appropriate for repeated navigation; visual impact must not make visitors wait for essential actions. Use contextual differences when the reference calls for them, while preserving a coherent motion vocabulary.

Consider View Transitions for shared-element continuity, image expansion, clipping or coordinated page changes when compatible with the chosen architecture. During implementation research, distinguish same-document route updates from cross-document navigation and verify the applicable official APIs, browser support and restrictions. Do not assume that a framework or browser automatically supplies the desired transition. Use an alternative motion implementation or immediate functional navigation when the enhancement is unavailable. Do not intercept external links or modified clicks merely to animate them.

Apply the route checks in [motion verification](review.md#motion-verification), inspecting actual page changes rather than only settled screenshots. Record observed results and limitations. Do not mark a multi-page build complete with route transitions left as a follow-up task.

## Scrolling

Do not install scroll interception automatically because a reference uses it. Reproduce the visual story with native scrolling when that meets the brief; if custom scrolling is needed, preserve keyboard, anchor, touch and history behaviour. This is an implementation choice within the user's reference-led direction, not a ban on immersive design.

Verify wheel/trackpad, keyboard, touch, anchors and history behaviour when implementing custom scrolling. For inspecting the reference mechanism, resolve source-audits.md through [library access](library-access.md). Keep source technology distinct from the chosen implementation.
