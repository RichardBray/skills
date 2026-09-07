# Image generation for client websites

## Choose assets for the actual composition

Prefer suitable supplied client assets. Generate missing decorative or conceptual imagery when it improves the reference-led design. Adapt the reference's framing, lighting, visual weight and material treatment to the client. Preserve actual product details and logos using supplied references; do not fabricate documentary images of the client's real team, premises or completed work.

Use the canonical [asset inventory](build-decisions.md#asset-plan-and-provenance). For each image, add aspect ratio, focal point, desktop/mobile crop, palette and space needed for live text. Keep headings and calls to action as accessible HTML rather than baking them into artwork.

## Generation route

If the host provides an imagegen skill, follow its execution details; it is optional and not bundled here. Default to the built-in image-generation tool when available; it does not require OPENAI_API_KEY. Its model may be managed by the host: do not claim it used GPT-Image-2 unless the tool reports that model.

When the user explicitly requests the API/CLI route, use an available supported SDK/API client, or a host-provided CLI if present. Preserve an explicitly requested model such as `gpt-image-2`; otherwise select a supported model from current official documentation. This repository does not require a particular external CLI. Verify current official model support and options before execution; do not silently substitute another model. Check whether the selected provider is configured; use an authorized environment key without printing it or asking the user to paste it. API usage is billed separately from the ChatGPT subscription. If the built-in tool is unavailable or fails, honour any existing authorization for API use; otherwise ask before switching to the paid API route. A key being present alone is not a request to switch routes.

## Generate, inspect and integrate

Build the prompt from the asset plan’s composition constraints, adding subject, lighting, materials and details to preserve. Use supplied images for edits where identity matters. Inspect existing local images before editing them. Generate actual bitmap assets through the image tool; use native vector assets for logos and interface icons when appropriate.

Inspect outputs, then inspect them in the rendered desktop and mobile layout. Check crop, focal point, text contrast, unwanted lettering, visual artifacts and consistency with the client's identity. Iterate on observed problems. Copy chosen outputs into the project's asset directory, create suitably sized web derivatives, preserve needed transparency, and provide appropriate alt text (empty for decorative images). Do not leave production references pointing to temporary or Codex generation folders.

Update the [asset inventory](build-decisions.md#asset-plan-and-provenance) with the chosen output and generation provenance; leave unverified model identity unknown.

## Relationship to 3D

A generated image with a 3D appearance is a raster image, not an interactive mesh or scene. Use generated artwork for backgrounds, approved texture inputs, concept frames or static fallbacks where appropriate. For rotation, camera movement, lighting interaction or other live 3D behaviour, source or build actual geometry/materials and follow motion-3d.md; never mark a rendered image as a delivered 3D model.

Official references (checked 2026-09-07):
- [GPT-Image-2 model](https://developers.openai.com/api/docs/models/gpt-image-2)
- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [Separate ChatGPT and API billing](https://help.openai.com/en/articles/9039756-managing-billing-settings-on-chatgpt-web-and-platform)

If neither a built-in tool nor an authorized API route is available, use suitable supplied/licensed imagery or report the missing asset. Do not claim imagery was generated or change the intended composition silently.
