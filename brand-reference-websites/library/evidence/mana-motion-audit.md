# MANA yerba mate: homepage animation audit

Source: https://en.manayerbamate.com/
Date: 2026-09-07
Method: direct CUA browser actions and screenshot state comparisons, desktop 1280x720.

## Actions
Loaded homepage; rejected cookies; captured green flavour; clicked right arrow; captured intermediate and settled Grapefruit states; attempted scroll; compared subsequent can angle.

## Coverage limits
This is a sampled state audit, not a frame-by-frame recording. No exact durations or easing curves were measured. No pointer hover or reduced-motion behaviour was verified. Source implementation proposals are inferences. Screenshots were inspected in the tool session but are not saved as durable media; revisit the live page to compare visually.

## flavour-world-switch
Location: homepage product carousel
Trigger: click
Start: Green Melon & Mint can, green background, floral/surf illustrations and matching product label.
End: After the right arrow, the can, scene, illustrations and CTA resolve to yellow/orange Grapefruit. An intermediate capture retained the old scene while the label cleared.
Scroll: Click-driven; not established as scroll-controlled.
Repeat/reverse: One forward change tested; reverse not tested.
Proposed adaptation (inference): Keep the product anchor and coordinate each variant's palette, artwork and label; use owned product visuals.

## can-idle-motion
Location: homepage product carousel
Trigger: idle
Start: Can shown front-on with a slight tilt in the illustrated scene.
End: Can angle and illustration positions differ in later captures, including after transition completion.
Scroll: Progresses while stationary; pointer contribution not isolated.
Repeat/reverse: Loop boundary unmeasured.
Proposed adaptation (inference): Use subtle product rotation plus independent artwork layers without moving controls.

