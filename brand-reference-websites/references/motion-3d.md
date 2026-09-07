# Motion and 3D decisions

Choose intensity for the brand and content: conventional with subtle motion; one signature scene; or an immersive sequence. These are choices, not quality tiers. Reference each selected effect to a verified source element.

Before implementation, define the scene's purpose, subject, asset source, framing, materials/lighting, interaction trigger, camera/object states, relationship to copy, and mobile/static alternative. Identify whether the source uses actual realtime 3D, a shader, video, image sequence or CSS depth; use unknown if unverified. Choose the cheapest implementation that reproduces the needed behaviour.

Use the project's compatible tools. CSS suits simple transforms; a motion library may suit coordinated DOM animation; a WebGL renderer may suit spatial scenes. Verify current official APIs before adding a new dependency. Don't add a heavyweight renderer merely because the brief says premium.

For realtime scenes: budget assets and resolution for target devices; lazy-load where possible; stop unnecessary offscreen rendering; dispose resources; handle resize and context failure. Measure actual loading/frame behaviour on the available target conditions and record them instead of inventing a universal performance guarantee. Avoid tying essential content to completion of a scene loader.

For pointer interactions, provide usable touch/keyboard paths. Respect reduced-motion preferences with a static or simpler state. Keep meaningful text in accessible HTML, avoid scroll traps, and let users reach navigation and CTAs. Sound needs an explicit user action and a mute control.

Custom models need a concrete asset plan. If no suitable model is available, choose a compatible reference with achievable assets or document the missing asset; don't silently replace a product with an unrelated decorative shape.

## Blender and generated 3D assets

Blender is an optional asset-production tool; an MCP is not a prerequisite. Discover the installed executable and version, then use background Python scripts for repeatable modelling, material setup, preview renders and glTF/GLB exports. On this user's Mac, Blender was verified at `/Applications/Blender.app/Contents/MacOS/Blender` (5.2.1 LTS on 2026-09-07); recheck availability rather than assuming this path on other machines. Keep scripts and editable .blend sources with the project. Work in separate output files to preserve supplied originals.

Use a Blender MCP when it is already available and live scene inspection or iterative editing benefits the task. Do not require or install it as part of every website build. A successful command-line version check does not establish that rendering, export or MCP connectivity has been tested.

Choose the asset route for the subject: supplied CAD/models for faithful products; scripted Blender geometry for controllable geometric subjects; licensed assets when suitable; optional image-to-3D generation for subjects that tolerate reconstruction. A possible route is supplied photo or generated concept → Replicate reconstruction → Blender inspection/refinement → optimized GLB → browser scene. Skip stages that do not improve the result.

The user reports a Replicate API key in their shell. Do not print it or assume its validity has been tested. Replicate is optional: inspect the selected model's current input/output schema, version, commercial-use terms and price before use. Honour existing authorization and spending limits; if paid generation has not been authorized, establish the intended scope before submitting predictions. Record model/version, inputs, prediction ID and asset provenance; save outputs into the project. Do not hard-code a model as permanently best. TRELLIS deployments are candidates for image-to-3D GLB generation, not verified production-quality defaults.

Inspect reconstructed assets from multiple angles for incorrect shape, baked shadows, broken surfaces and unsuitable textures. In Blender, correct scale/orientation/origin, reduce geometry where appropriate, prepare supported materials and texture sizes, and export a web-compatible model. Blender shaders and animation features do not all transfer directly to glTF: inspect the exported result in the actual browser renderer. Check loading cost, visual fidelity and mobile behaviour before calling the asset finished. Provide a static fallback when required by the motion plan.

References: [Blender command line](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html), [Replicate predictions](https://replicate.com/docs/topics/predictions), [TRELLIS candidate](https://replicate.com/firtoz/trellis).
