"""Regression checks for evidence coverage and discovery consistency. No network calls."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog', ROOT / 'scripts/catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)

class CatalogContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'library', self.root / 'library')

    def edit(self, relative, mutate):
        path = self.root / relative
        value = json.loads(path.read_text())
        mutate(value)
        path.write_text(json.dumps(value))

    def validate(self):
        with contextlib.redirect_stdout(io.StringIO()):
            catalog.validate(self.root)

    def test_current_library_and_unresolved_null_candidates_pass(self):
        self.validate()

    def test_undeclared_branding_is_caught(self):
        self.edit('library/sites/aquest.json', lambda r: r.update(evidence=[e for e in r['evidence'] if e['kind'] != 'firecrawl-branding']))
        with self.assertRaisesRegex(ValueError, 'seed coverage requires durable nonempty branding'):
            self.validate()

    def test_missing_branding_file_is_caught(self):
        (self.root / 'library/evidence/aquest-branding.json').unlink()
        with self.assertRaisesRegex(ValueError, 'missing or escaping evidence path'):
            self.validate()

    def test_empty_branding_is_not_evidence(self):
        (self.root / 'library/evidence/aquest-branding.json').write_text('{"branding": {}}')
        with self.assertRaisesRegex(ValueError, 'seed coverage requires durable nonempty branding'):
            self.validate()

    def test_missing_audit_is_caught(self):
        self.edit('library/sites/aquest.json', lambda r: r.update(evidence=[e for e in r['evidence'] if e['kind'] != 'browser']))
        with self.assertRaisesRegex(ValueError, 'seed coverage requires durable inspected motion audit'):
            self.validate()

    def test_missing_seed_site_is_caught(self):
        (self.root / 'library/sites/aquest.json').unlink()
        with self.assertRaisesRegex(ValueError, 'missing required site aquest'):
            self.validate()

    def test_stale_link_status_is_caught(self):
        self.edit('library/discovery.json', lambda r: r['collections'][0]['candidates'][0].update(status='discovered'))
        with self.assertRaisesRegex(ValueError, 'linked status/URL differs'):
            self.validate()

    def test_missing_link_is_caught(self):
        self.edit('library/discovery.json', lambda r: r['collections'][0]['candidates'][0].pop('library_site_id'))
        with self.assertRaisesRegex(ValueError, 'requires library_site_id'):
            self.validate()

    def test_invalid_candidate_url_is_caught(self):
        self.edit('library/discovery.json', lambda r: r['collections'][0]['candidates'][1].update(url='javascript:bad'))
        with self.assertRaisesRegex(ValueError, 'invalid candidate URL'):
            self.validate()

    def test_null_site_url_is_rejected(self):
        self.edit('library/sites/aquest.json', lambda r: r.update(url=None))
        with self.assertRaisesRegex(ValueError, 'invalid URL'):
            self.validate()

    def add_screenshot(self, **fields):
        entry = {'id': 'capture', 'kind': 'screenshot', 'source_url': 'https://landonorris.com/',
                 'captured_at': '2026-09-07', 'inspected': True}
        entry.update(fields)
        self.edit('library/sites/lando.json', lambda r: r['evidence'].append(entry))

    def write_capture(self, payload=b'capture'):
        path = self.root / 'library/evidence/capture.png'
        path.write_bytes(payload)
        return hashlib.sha256(payload).hexdigest()

    def test_remote_only_screenshot_is_caught(self):
        self.add_screenshot(url='https://example.com/expiring.png')
        with self.assertRaisesRegex(ValueError, 'screenshot needs durable path'):
            self.validate()

    def test_screenshot_corruption_is_caught(self):
        self.add_screenshot(path='library/evidence/capture.png', sha256=self.write_capture())
        self.validate()
        (self.root / 'library/evidence/capture.png').write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'screenshot checksum mismatch'):
            self.validate()

if __name__ == '__main__':
    unittest.main()
