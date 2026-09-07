# Lando Norris: homepage animation audit

Source: https://landonorris.com/
Date: 2026-09-07
Method: direct CUA browser actions and screenshot state comparisons, desktop 1280x720.

## Actions
Loaded portrait hero; clicked menu; captured intermediate and settled menu; clicked close and captured an intermediate closing state.

## Coverage limits
This is a sampled state audit, not a frame-by-frame recording. No exact durations or easing curves were measured. No pointer hover or reduced-motion behaviour was verified. Source implementation proposals are inferences. Screenshots were inspected in the tool session but are not saved as durable media; revisit the live page to compare visually.

## full-screen-menu
Location: top-right menu control
Trigger: click
Start: Light portrait hero with compact top-right menu button.
End: A dark olive covering layer enters with a curved lower edge; image tiles and large navigation resolve into the full-screen menu.
Scroll: Click-driven; entry sequence includes an intermediate frame before text finishes appearing.
Repeat/reverse: Open tested; close action produced a transitional frame, final closed state not verified.
Proposed adaptation (inference): Stage the covering layer, imagery and links; preserve keyboard focus and instant reduced-motion navigation.

## portrait-helmet-composite
Location: homepage hero
Trigger: unknown
Start: Portrait fills the hero; a horizontal visor/helmet band crosses the face.
End: A depth-styled band and background shadow are visible, but controlling input was not isolated in this pass.
Scroll: Unknown; do not label scroll-controlled or realtime 3D.
Repeat/reverse: Unverified.
Proposed adaptation (inference): Revisit the interaction before implementing; use client-owned portraits and object assets.

