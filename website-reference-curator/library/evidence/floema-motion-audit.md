# Floema: homepage animation audit

Source: https://floema.com/en
Date: 2026-09-07
Method: direct CUA browser actions and screenshot state comparisons, desktop 1280x720.

## Actions
Loaded homepage; denied cookies; scrolled back to collage; scrolled down to Urban and emerging Nature image; compared settled states.

## Coverage limits
This is a sampled state audit, not a frame-by-frame recording. No exact durations or easing curves were measured. No pointer hover or reduced-motion behaviour was verified. Source implementation proposals are inferences. Screenshots were inspected in the tool session but are not saved as durable media; revisit the live page to compare visually.

## collage-opening
Location: homepage hero
Trigger: load-and-scroll
Start: Small product/scene image tiles surround the central brand statement on a warm neutral field.
End: Scrolling leaves the collage and brings a full-width urban project photograph and collection details into view.
Scroll: Scroll handoff observed; exact tile depth/pointer interaction not isolated.
Repeat/reverse: Scrolling up returned to the collage.
Proposed adaptation (inference): Keep central text clear, vary tile scale, then give each collection room in a large photographic section.

## collection-image-handoff
Location: Urban to Nature collection sections
Trigger: scroll
Start: Urban city photograph with collection label, descriptive copy and catalogue card.
End: Outdoor landscape imagery rises beneath/overlaps the city image while the Urban information remains visible during the sampled handoff.
Scroll: Layered transition visible after downward scroll; pin/scrub boundaries unmeasured.
Repeat/reverse: Reverse for this handoff not tested.
Proposed adaptation (inference): Coordinate the image mask and text handoff explicitly; verify all intermediate states avoid unintended overlap.

