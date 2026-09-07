# United Carriers: homepage animation audit

Source: https://unitedcarriers.com/
Date: 2026-09-07
Method: direct CUA browser actions and screenshot state comparisons, desktop 1280x720.

## Actions
Loaded globe hero; scrolled to statistics; compared intermediate/final numbers; scrolled to reach stacker, then further to raised container. Attempted 390x844 resize and reload; only dark circular background visible in sampled mobile state.

## Coverage limits
This is a sampled state audit, not a frame-by-frame recording. No exact durations or easing curves were measured. No pointer hover or reduced-motion behaviour was verified. Source implementation proposals are inferences. Screenshots were inspected in the tool session but are not saved as durable media; revisit the live page to compare visually.

## metric-count-up
Location: introductory statistics section
Trigger: scroll-entry
Start: An early frame after scroll shows intermediate values, including 38.9% and 2+.
End: At the same resting section the values settle at 98.2% and 8+, with labels visible.
Scroll: Continues after scroll stops; appears time-triggered on entry, exact threshold unknown.
Repeat/reverse: Replay/reverse not tested.
Proposed adaptation (inference): Animate from a starting value to client-approved figures; show final values immediately for reduced motion.

## container-lift
Location: freight scene below company introduction
Trigger: scroll
Start: Reach stacker boom and spreader sit above a grey container stacked on blue/orange containers.
End: A further downward scroll shows the grey container raised clear of the stack, with its visible angle changed.
Scroll: State change follows scroll; continuous scrub and reverse need further sampling.
Repeat/reverse: Reverse not tested.
Proposed adaptation (inference): Build a storyboard of cargo handling; the DOM exposes image parts, so do not assume every depth effect requires live 3D.

## globe-hero
Location: homepage hero
Trigger: unknown
Start: Glowing globe with point-like land texture, country labels and orange route lines beside the headline.
End: Single settled globe state inspected; motion control and renderer were not verified.
Scroll: Unknown.
Repeat/reverse: Unverified.
Proposed adaptation (inference): Choose a globe treatment only if it clarifies coverage; inspect animation before reusing.

