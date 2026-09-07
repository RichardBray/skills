# AQuest: homepage animation audit

Source: https://www.aquest.it/
Date: 2026-09-07
Method: direct CUA browser actions and screenshot state comparisons, desktop 1280x720.

## Actions
Loaded homepage; scrolled; denied cookies; scrolled to Selected Works; compared immediate and later settled screenshots.

## Coverage limits
This is a sampled state audit, not a frame-by-frame recording. No exact durations or easing curves were measured. No pointer hover or reduced-motion behaviour was verified. Source implementation proposals are inferences. Screenshots were inspected in the tool session but are not saved as durable media; revisit the live page to compare visually.

## section-title-reveal
Location: Selected Works section
Trigger: scroll-entry
Start: Section label is visible while the large heading area is initially blank/entering.
End: After settling at the same section, the large black heading is fully visible above serif project titles and media.
Scroll: Observed between immediate post-scroll and settled capture; scrub vs timed reveal not isolated.
Repeat/reverse: Reverse not tested.
Proposed adaptation (inference): Reveal a large heading in restrained stages, preserve whitespace and keep metadata still.

## project-editorial-composition
Location: Selected Works / Bulgari
Trigger: section-entry
Start: Project title and metadata occupy the left column; visual work occupies the wider right column.
End: Settled composition keeps serif title and small labels beside a large warm-toned project visual.
Scroll: Layout reference observed; animation of the media itself unverified.
Repeat/reverse: Not applicable to static composition.
Proposed adaptation (inference): Borrow the editorial proportions and type contrast; source client project media separately.

