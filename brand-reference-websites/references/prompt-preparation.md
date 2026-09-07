# Prepare a build prompt

This mode turns a brief into a self-contained prompt for a new session. It stops before asset generation, implementation or deployment. Use build-prompt-template.md as the handoff structure, not a questionnaire to recite.

## Fill the brief through conversation

Read supplied context and any user-provided assets first. Pre-fill known fields. Ask up to three focused questions in the first batch, prioritising audience/goal, identity/direction and scope. Offer concrete choices when useful. Ask a short follow-up only for material unresolved decisions. Do not ask the user to supply technical details the build agent can determine from the project.

Bracketed fields describe what to fill, and may contain a question to guide the interview. They are editorial placeholders, not mandatory user questions. Fill them with supplied facts, explicitly delegated choices or clearly labelled provisional assumptions. Remove irrelevant sections. For low-impact decisions use judgement; do not convert silence into approval for spending, publishing or external actions. Unresolved consequential choices must remain explicit blockers or build-stage decisions with clear boundaries.

Select a small, suitable reference shortlist using the catalog and the retrieval rules in SKILL.md. Include exact URLs/record paths and relevant sections. Separate observed patterns from candidates needing inspection; do not pretend motion was verified. When installed and useful for selected visual references, read the Firecrawl website design clone skill; otherwise follow ingestion.md with available tools. In either case, retain branding/images/screenshot evidence and keep per-reference reports separate from the client's eventual DESIGN.md. Animation, transitions, scrolling and 3D require their own evidence. Avoid re-scraping adequate existing captures just to fill the template.

Specify the intended visual result and signature interaction concretely while leaving implementation choices to research and project inspection. Preserve brand-specific identity; a reusable prompt structure must not impose a reusable aesthetic. Preserve any close-match instruction and approved deviations.

## Hand off

Produce one complete copyable prompt, with no unresolved bracket placeholders. Use explicit phrases such as 'choose after inspecting the project' for delegated technical choices. Include absolute paths for the skill, chosen local references and supplied assets; web URLs for external references; the project directory if known, otherwise require the fresh session to establish its target before writing files. Do not assume the new session inherits conversation memory, credentials, installed tools or current working directory.

Record only permissions actually supplied, including paid-provider scope/budget and deployment authorization. Default to the built-in image route when available; a reported API key is not a verified credential or a spending instruction. Include Blender/Replicate only when relevant, with availability to recheck. Never put secrets in the prompt.

Check the prompt for contradictions, unsupported claims, excessive scope and missing assets. Completion criteria must include the primary user flow, signature interaction where applicable, responsive behaviour, reduced motion and actual browser inspection. Carry existing skill requirements through the handoff without copying its entire implementation manual.

Return the prompt and a brief note of any explicit assumptions. If saving a file is requested, save the filled prompt separately from the reusable template. Do not start the build in this mode.
