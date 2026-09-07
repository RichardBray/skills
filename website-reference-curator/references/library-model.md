# Library model

JSON is the canonical store: one site per library/sites/<id>.json. It supports nested elements and evidence, portable diffs, and selective reads. CSV is a derived browsing view.

- Consider SQLite only when scale, joins, or concurrent writes justify a migration.
- Do not maintain two competing sources of truth.

Each site record uses:

- schema_version: 1; stable slug id; name; url (required HTTP(S) URL for site records).
- status: discovered | extracted | reviewed. Reviewed means the relevant visual evidence was actually inspected; it does not automatically certify mobile or interactions.
- collected_at: ISO date; discovery_source; user_notes (verbatim preference or null).
- tags: industry, personality, layout, typography, imagery, motion, technology arrays.
- tokens: source-extracted values, with evidence provenance and caveats. Null/empty means unknown, never absent.
- evidence: entries with id, kind, source_url, captured_at, path or url, and inspected boolean.
- elements: entries with id, type, location, description, tags, evidence_ids, verification (extracted | observed | inferred), brand_fit, adaptation, effort (low | medium | high | unknown), mobile notes, and reduced_motion notes.
- caveats: unresolved extraction problems, changed site, unavailable old version, or missing checks.

- Separate observations from proposed adaptations.
- Personality and fit tags are editorial judgments, even when a scraper returns them.
- Preserve the tool's confidence separately from your own assessment.
- A full-page screenshot may miss scroll-triggered content; an extracted font size may describe just one element.
- Do not convert an empty motion array into a no-animation tag.

Suggested tag vocabulary (extend when necessary; use lowercase hyphenated tags):

- Industry: agency, sports, logistics, hospitality, fashion, technology, culture, product.
- Personality: restrained, expressive, playful, technical, premium, warm, bold, professional.
- Layout: editorial, asymmetric, full-bleed, grid, split-screen, typographic-hero.
- Typography: serif-display, sans-display, monospace-details, oversized-type.
- Imagery: photography, illustration, product-render, video, collage.
- Motion: subtle, scroll-linked, hover-reveal, page-transition, interactive-3d, shader.
- Technology: only verified technology labels; otherwise leave empty.

Tag elements too: a subdued footer on an expressive site should remain retrievable. A single record can fit multiple industries. Use the fit notes to explain cross-industry transfer.

library/components.json holds implementation suppliers with URL, scope, licences, integration caveats, and verification state. It is separate from visual site references. library/discovery.json holds collections and unresolved candidates. Discovery records must not masquerade as analysed references.

- Use catalog.py validate after changes.
- Use catalog.py export-csv for a flat site-level review table.
- It is generated, so edit JSON rather than CSV.
- Read matching records/elements and their evidence before deciding.
- Don't load the entire raw evidence directory.

## Animation fields and browsing

- This section defines stored evidence fields, distinct from the project-specific motion contract owned by the builder.
- Elements may include a motion object with trigger, start_state, end_state, scroll_relationship, repeat_reverse, duration_ms, easing, rendering_technology, implementation_status, and evidence_actions.
- Null timing values are unknown.
- Exact timing/easing needs:
  - measurement_evidence identifying runtime measurement or verified source code;
  - timing_basis stating which.
- Source-defined duration does not assert actual playback duration.
- Use type animation for observed motion with an identified trigger, or visual-pattern when only appearance/state is established.

- Review coverage belongs to each site: desktop, mobile, reduced_motion, hover, timing, and recording.
- Do not infer whole-site coverage from status reviewed.

Generate the dedicated element-level table:

```bash
python3 <skill-dir>/scripts/catalog.py export-motion-csv --output <skill-dir>/library/motion-catalog.csv
```

This includes visual candidates with unknown controls, explicitly labelled visual-pattern. It is derived from the canonical JSON and must not be edited directly.

Site records may include scroll_control and technology_findings. Unknown must remain explicit until evidence establishes the mechanism or library. See [source audits](source-audits.md) for the inspection workflow.

## Discovery and seed coverage contract

- Unresolved candidates live in discovery.json, where url may be null only while status is discovered and no library_site_id is assigned.
- Site records always require an HTTP(S) URL.
- Linked candidates must have the same URL as their library_site_id record.
- Linked candidates must have the same status as their library_site_id record.
- The status refers to review of the linked current site, not verification of its historical award version.
- Collection/listing verification remains in notes.

- library/coverage.json declares the eight seed records that must each have:
  - durable branding JSON containing a nonempty branding object;
  - a local inspected browser/video motion audit.
- Evidence IDs may vary (Ali uses navigation); kind and content determine coverage.
- Missing files or omitted evidence declarations fail validation.
- This contract is explicit rather than silently requiring every future discovery candidate to be fully researched.

- Screenshot evidence must have either:
  - a durable local path;
  - or both an explicit unavailable_reason and inspected=false.
- Temporary signed URLs may be retained as historical provenance, never as the sole durable evidence.
- Store a SHA-256 checksum for local screenshots; the validator verifies it when present.
- Saving or viewing a still image does not establish motion or a fully settled page.

- Run offline regression checks with `python3 -m unittest discover -s <skill-dir>/tests -v`.
- These checks mutate temporary copies to verify missing evidence, stale discovery links, invalid URLs and screenshot durability failures.
