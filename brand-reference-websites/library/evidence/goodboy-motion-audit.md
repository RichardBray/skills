# Goodboy: homepage animation audit

Source: https://goodboyagency.com/
Date: 2026-09-07
Method: direct CUA browser actions and screenshot state comparisons, desktop 1280x720.

## Actions
Loaded homepage; scrolled to logo strip; captured twice with no intervening scroll and compared logo positions.

## Coverage limits
This is a sampled state audit, not a frame-by-frame recording. No exact durations or easing curves were measured. No pointer hover or reduced-motion behaviour was verified. Source implementation proposals are inferences. Screenshots were inspected in the tool session but are not saved as durable media; revisit the live page to compare visually.

## client-logo-marquee
Location: Brands we have worked with strip
Trigger: idle
Start: Disney, Marvel and Chicago Cutlery visible near the left/middle of the strip.
End: Without another scroll, Chicago Cutlery, Nautica and Louis Garneau occupy later positions as logos travel left.
Scroll: Time-driven movement independent of scroll at sampled position.
Repeat/reverse: Continuous movement observed; wrap boundary not tested.
Proposed adaptation (inference): Use real client logos with permission; keep a readable static list for reduced motion.

