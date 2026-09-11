import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from d0rkw3b.core.registry import load_bundled_registry, load_registry
from d0rkw3b.core.updates import install_snapshot, rollback, snapshot_path


class UpdateTests(unittest.TestCase):
    def test_verified_activation_fallback_and_rollback(self):
        bundled, _ = load_bundled_registry()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'providers.json'
            updated = copy.deepcopy(bundled)
            updated[0]['notes'] = 'Explicit local snapshot edit.'
            raw = json.dumps(updated).encode()
            source.write_bytes(raw)
            with patch.dict(os.environ, {'D0RKW3B_DATA_DIR': str(root / 'state')}):
                with self.assertRaises(ValueError):
                    install_snapshot(source, '0' * 64, bundled)
                self.assertFalse(snapshot_path().exists())
                install_snapshot(source, hashlib.sha256(raw).hexdigest(), bundled)
                self.assertEqual(load_registry()[0][0]['notes'], updated[0]['notes'])
                second = copy.deepcopy(updated)
                second[0]['notes'] = 'Second snapshot'
                source.write_text(json.dumps(second))
                install_snapshot(source, hashlib.sha256(source.read_bytes()).hexdigest(), bundled)
                self.assertEqual(load_registry()[0][0]['notes'], 'Second snapshot')
                rollback(bundled)
                self.assertEqual(load_registry()[0][0]['notes'], updated[0]['notes'])
                snapshot_path().write_text('{broken')
                providers, errors = load_registry()
                self.assertEqual(providers, bundled)
                self.assertTrue(errors)
                rollback(bundled)
                self.assertEqual(load_registry(), (bundled, []))

    def test_coverage_and_duplicates_cannot_be_lost(self):
        bundled, _ = load_bundled_registry()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'input.json'
            for data in (bundled[1:], bundled + [bundled[0]], [dict(p, network='tor') if i == 0 else p for i, p in enumerate(bundled)]):
                raw = json.dumps(data).encode()
                path.write_bytes(raw)
                with self.assertRaises(ValueError):
                    install_snapshot(path, hashlib.sha256(raw).hexdigest(), bundled, root=root)
                self.assertFalse(snapshot_path(root).exists())
