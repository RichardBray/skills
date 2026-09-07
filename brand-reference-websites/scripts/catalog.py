#!/usr/bin/env python3
"""Search, validate and export the reference library using Python's standard library."""
import argparse
import hashlib
from urllib.parse import urlparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = ('industry', 'personality', 'layout', 'typography', 'imagery', 'motion', 'technology')

def records(root):
    return [(p, json.loads(p.read_text())) for p in sorted((root / 'library/sites').glob('*.json'))]

def all_tags(record):
    return [tag for values in record['tags'].values() for tag in values]

def valid_url(value):
    return isinstance(value, str) and urlparse(value).scheme in ("http", "https") and bool(urlparse(value).netloc)

def validate(root):
    errors = []
    seen = set()
    rows = records(root)
    for path, r in rows:
        prefix = path.name
        def require(condition, message):
            if not condition:
                errors.append(f'{prefix}: {message}')
        require(r.get('schema_version') == 1, 'unsupported schema_version')
        rid = r.get('id', '')
        require(bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', rid)), 'invalid id')
        require(rid not in seen, 'duplicate id')
        seen.add(rid)
        require(path.stem == rid, 'filename must match id')
        require(r.get('status') in ('discovered', 'extracted', 'reviewed'), 'invalid status')
        require(isinstance(r.get('name'), str) and bool(r['name']), 'missing name')
        require(valid_url(r.get('url')), 'invalid URL')
        require(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', r.get('collected_at', ''))), 'missing capture date')
        tags = r.get('tags', {})
        require(set(tags) == set(GROUPS), 'missing/unknown tag groups')
        for group, values in tags.items():
            require(isinstance(values, list) and all(isinstance(v, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', v) for v in values), f'invalid {group} tags')
        evidence = r.get('evidence', [])
        eids = [e.get('id') for e in evidence]
        require(len(eids) == len(set(eids)), 'duplicate evidence ids')
        for e in evidence:
            require(isinstance(e.get('inspected'), bool), 'evidence inspected must be boolean')
            if e.get('path'):
                target = (root / e['path']).resolve()
                require(root.resolve() in target.parents and target.is_file(), 'missing or escaping evidence path')
            if e.get('kind') == 'screenshot':
                require(bool(e.get('path')) or (bool(e.get('unavailable_reason')) and e.get('inspected') is False), 'screenshot needs durable path or explicit unavailability')
                if e.get('path') and e.get('sha256'):
                    target = (root / e['path']).resolve()
                    if root.resolve() in target.parents and target.is_file():
                        require(hashlib.sha256(target.read_bytes()).hexdigest() == e['sha256'], 'screenshot checksum mismatch')
        element_ids = []
        for el in r.get('elements', []):
            element_ids.append(el.get('id'))
            require(el.get('verification') in ('extracted', 'observed', 'inferred'), 'invalid element verification')
            require(bool(el.get('evidence_ids')) and set(el['evidence_ids']) <= set(eids), 'unlinked element evidence')
            require(el.get('effort') in ('low', 'medium', 'high', 'unknown'), 'invalid effort')
            if el.get('verification') == 'observed':
                require(any(e.get('inspected') and e.get('id') in el['evidence_ids'] for e in evidence), 'observed element requires inspected evidence')
            if 'motion' in el:
                motion = el['motion']
                for field in ('trigger', 'start_state', 'end_state', 'scroll_relationship', 'repeat_reverse', 'rendering_technology', 'evidence_actions'):
                    require(isinstance(motion.get(field), str) and bool(motion[field].strip()), f'missing motion {field}')
                duration = motion.get('duration_ms')
                require(duration is None or (type(duration) in (int, float) and duration >= 0), 'invalid duration_ms')
                if duration is not None or motion.get('easing') is not None:
                    require(bool(motion.get('measurement_evidence')), 'exact timing requires measurement_evidence')
                require(el.get('type') != 'animation' or motion.get('trigger') != 'unknown', 'unknown-trigger visual must not masquerade as an audited animation')
        require(len(element_ids) == len(set(element_ids)), 'duplicate element ids')
        if r.get('status') == 'reviewed':
            require(any(e.get('inspected') and e.get('kind') in ('screenshot', 'browser', 'video') for e in evidence), 'reviewed site requires inspected visual evidence')
    for filename, key in [('components.json', 'suppliers'), ('discovery.json', 'collections')]:
        data = json.loads((root / 'library' / filename).read_text())
        if data.get('schema_version') != 1 or not isinstance(data.get(key), list):
            errors.append(f'{filename}: invalid container')
    sites = {r['id']: r for _, r in rows}
    discovery = json.loads((root / 'library/discovery.json').read_text())
    for collection in discovery.get('collections', []):
        if not valid_url(collection.get('url')):
            errors.append('discovery.json: invalid collection URL')
        for candidate in collection.get('candidates', []):
            label = 'discovery.json: ' + str(candidate.get('name', '<unnamed>'))
            status = candidate.get('status')
            link = candidate.get('library_site_id')
            url = candidate.get('url')
            if not candidate.get('name') or status not in ('discovered', 'extracted', 'reviewed'):
                errors.append(label + ': invalid name/status')
            if not valid_url(url) and not (url is None and status == 'discovered' and not link):
                errors.append(label + ': invalid candidate URL')
            if link:
                if link not in sites:
                    errors.append(label + ': unknown library_site_id')
                elif status != sites[link]['status'] or url != sites[link]['url']:
                    errors.append(label + ': linked status/URL differs from site record')
            elif status != 'discovered' or any(url and url == r['url'] for r in sites.values()):
                errors.append(label + ': enriched or matching candidate requires library_site_id')
    coverage = json.loads((root / 'library/coverage.json').read_text())
    required = coverage.get('required_sites')
    if coverage.get('schema_version') != 1 or not isinstance(required, list) or not required or len(required) != len(set(required)):
        errors.append('coverage.json: invalid required_sites contract')
        required = []
    if coverage.get('required_evidence') != ['branding', 'motion-audit']:
        errors.append('coverage.json: expected branding and motion-audit requirements')
    for rid in required:
        if rid not in sites:
            errors.append(f'coverage.json: missing required site {rid}')
            continue
        evidence = sites[rid].get('evidence', [])
        branding_ok = audit_ok = False
        for e in evidence:
            if not e.get('path'):
                continue
            path = (root / e['path']).resolve()
            if root.resolve() not in path.parents or not path.is_file():
                continue
            if e.get('kind') == 'firecrawl-branding':
                try:
                    data = json.loads(path.read_text())
                    branding_ok = isinstance(data.get('branding'), dict) and bool(data['branding'])
                except (ValueError, UnicodeError, AttributeError):
                    pass
            if (e.get('kind') in ('browser', 'video') and e.get('inspected') and path.stat().st_size
                    and any('motion' in el and e.get('id') in el.get('evidence_ids', []) for el in sites[rid].get('elements', []))):
                # Seed audits are durable action logs; ids differ (Ali uses navigation).
                audit_ok = True
        if not branding_ok:
            errors.append(f'{rid}: seed coverage requires durable nonempty branding JSON')
        if not audit_ok:
            errors.append(f'{rid}: seed coverage requires durable inspected motion audit')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'Validated {len(rows)} sites plus component and discovery inventories.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    search = sub.add_parser('search')
    search.add_argument('--query', default='')
    search.add_argument('--tag', action='append', default=[])
    search.add_argument('--status', choices=['discovered', 'extracted', 'reviewed'])
    search.add_argument('--limit', type=int, default=8)
    sub.add_parser('validate')
    export = sub.add_parser('export-csv')
    export.add_argument('--output', type=Path, required=True)
    motion_export = sub.add_parser('export-motion-csv')
    motion_export.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'validate':
        validate(args.root)
        return
    rows = records(args.root)
    if args.command == 'export-motion-csv':
        fields = ['site', 'url', 'element', 'type', 'location', 'tags', 'trigger', 'start_state', 'end_state', 'scroll_relationship', 'repeat_reverse', 'duration_ms', 'easing', 'timing_basis', 'rendering_technology', 'brand_fit', 'adaptation', 'effort', 'mobile', 'reduced_motion', 'evidence_actions']
        count = 0
        with args.output.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for _, r in rows:
                for el in r['elements']:
                    if 'motion' not in el:
                        continue
                    motion = el['motion']
                    row = {'site': r['name'], 'url': r['url'], 'element': el['id'], 'type': el['type'], 'tags': '; '.join(el['tags'])}
                    for field in fields:
                        if field not in row:
                            row[field] = el.get(field, motion.get(field))
                    row = {k: ('unknown' if v is None else str(v)) for k, v in row.items()}
                    writer.writerow({k: ("'" + v if v.startswith(('=', '+', '-', '@', '\t', '\r')) else v) for k, v in row.items()})
                    count += 1
        print(f'Exported {count} motion/visual patterns to {args.output}')
        return
    if args.command == 'export-csv':
        with args.output.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'url', 'status', *GROUPS, 'elements', 'caveats'])
            for _, r in rows:
                row = [r['id'], r['name'], r['url'], r['status'], *['; '.join(r['tags'][g]) for g in GROUPS], '; '.join(e['description'] for e in r['elements']), '; '.join(r['caveats'])]
                # Prevent spreadsheet formula execution from imported reference text.
                writer.writerow(["'" + value if isinstance(value, str) and value.startswith(('=', '+', '-', '@', '\t', '\r')) else value for value in row])
        print(f'Exported {len(rows)} sites to {args.output}')
        return
    if args.limit < 1:
        parser.error('--limit must be positive')
    terms = re.findall(r'[a-z0-9-]+', args.query.lower())
    matches = []
    for path, r in rows:
        tags = all_tags(r) + [t for e in r['elements'] for t in e.get('tags', [])]
        if not set(args.tag) <= set(tags) or (args.status and args.status != r['status']):
            continue
        searchable = json.dumps({'name': r['name'], 'tags': tags, 'elements': r['elements']}).lower()
        score = sum(3 if term in tags else 1 for term in terms if term in searchable)
        if terms and score == 0:
            continue
        matches.append({'id': r['id'], 'name': r['name'], 'score': score, 'status': r['status'], 'tags': tags, 'path': str(path), 'elements': r['elements']})
    print(json.dumps(sorted(matches, key=lambda r: (-r['score'], r['id']))[:args.limit], indent=2))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
