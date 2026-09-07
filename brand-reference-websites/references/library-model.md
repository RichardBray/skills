# Library model

JSON is the canonical store: one site per library/sites/<id>.json. It supports nested elements and evidence, portable diffs, and selective reads. CSV is a derived browsing view. Consider SQLite only when scale, joins, or concurrent writes justify a migration; do not maintain two competing sources of truth.

Each site record uses:
- schema_version: 1; stable slug id; name; url (null only for unresolved discovery candidates).
- status: discovered | extracted | reviewed. Reviewed means the relevant visual evidence was actually inspected; it does not automatically certify mobile or interactions.
- collected_at: ISO date; discovery_source; user_notes (verbatim preference or null).
- tags: industry, personality, layout, typography, imagery, motion, technology arrays.
- tokens: source-extracted values, with evidence provenance and caveats. Null/empty means unknown, never absent.
- evidence: entries with id, kind, source_url, captured_at, path or url, and inspected boolean.
- elements: entries with id, type, location, description, tags, evidence_ids, verification (extracted | observed | inferred), brand_fit, adaptation, effort (low | medium | high | unknown), mobile and reduced_motion notes.
- caveats: unresolved extraction problems, changed site, unavailable old version, or missing checks.

Separate observations from proposed adaptations. Personality and fit tags are editorial judgments, even when a scraper returns them. Preserve the tool's confidence separately from your own assessment. A full-page screenshot may miss scroll-triggered content; an extracted font size may describe just one element. Do not convert an empty motion array into a no-animation tag.

Suggested tag vocabulary (extend when necessary; use lowercase hyphenated tags):
- Industry: agency, sports, logistics, hospitality, fashion, technology, culture, product.
- Personality: restrained, expressive, playful, technical, premium, warm, bold, professional.
- Layout: editorial, asymmetric, full-bleed, grid, split-screen, typographic-hero.
- Typography: serif-display, sans-display, monospace-details, oversized-type.
- Imagery: photography, illustration, product-render, video, collage.
- Motion: subtle, scroll-linked, hover-reveal, page-transition, interactive-3d, shader.
- Technology: only verified technology labels; otherwise leave empty.

Tag elements too: a subdued footer on an expressive site should remain retrievable. A single record can fit multiple industries; use the fit notes to explain cross-industry transfer.

library/components.json holds implementation suppliers with URL, scope, licences, integration caveats and verification state. It is separate from visual site references. library/discovery.json holds collections and unresolved candidates. Discovery records must not masquerade as analysed references.

Use catalog.py validate after changes. Use catalog.py export-csv for a flat site-level review table. It is generated, so edit JSON rather than CSV. Read matching records/elements and their evidence before deciding; don't load the entire raw evidence directory.

## Animation fields and browsing

Elements may include a motion object with trigger, start_state, end_state, scroll_relationship, repeat_reverse, duration_ms, easing, rendering_technology, implementation_status and evidence_actions. Null timing values are unknown. Exact timing/easing needs measurement_evidence identifying runtime measurement or verified source code, with timing_basis stating which. Source-defined duration does not assert actual playback duration. Use type animation for observed motion with an identified trigger, or visual-pattern when only appearance/state is established.

Review coverage belongs to each site: desktop, mobile, reduced_motion, hover, timing and recording. Do not infer whole-site coverage from status reviewed.

Generate the dedicated element-level table:

```bash
python3 <skill-dir>/scripts/catalog.py export-motion-csv --output <skill-dir>/library/motion-catalog.csv
```

This includes visual candidates with unknown controls, explicitly labelled visual-pattern. It is derived from the canonical JSON and must not be edited directly.

Site records may include scroll_control and technology_findings. Unknown must remain explicit until evidence establishes the mechanism or library. See page-transitions-scroll.md for the audit.
