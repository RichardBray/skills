# Lusion: homepage animation audit

Source: https://lusion.co/
Date: 2026-09-07
Method: direct CUA browser actions and screenshot state comparisons, desktop 1280x720.

## Actions
Loaded homepage; captured hero; scrolled down twice; captured again much later without further input to compare object orientation.

## Coverage limits
This is a sampled state audit, not a frame-by-frame recording. No exact durations or easing curves were measured. No pointer hover or reduced-motion behaviour was verified. Source implementation proposals are inferences. Screenshots were inspected in the tool session but are not saved as durable media; revisit the live page to compare visually.

## sculptural-loop
Location: hero
Trigger: continuous-scene
Start: Rounded dark hero panel filled with glossy black, white and cobalt connector-like objects.
End: Object orientations and overlap changed between captures without further scroll, while the panel stayed at the same location.
Scroll: Continues with no scroll input; pointer coupling not tested.
Repeat/reverse: Continuous progression observed; seamless loop boundary not established.
Proposed adaptation (inference): Use a client-relevant sculptural scene; test whether video suffices before choosing a live renderer.

## reel-heading-entry
Location: section after hero
Trigger: scroll-entry
Start: Hero panel and scroll cue dominate the viewport.
End: Oversized two-line heading becomes visible beneath the hero as the page advances.
Scroll: Entry during scroll observed; exact trigger range and easing unmeasured.
Repeat/reverse: Reverse not tested.
Proposed adaptation (inference): Pair a restrained text section with the scene; avoid competing simultaneous motion.

