import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from d0rkw3b.cli import main
from d0rkw3b.connectors.registry import collect
from d0rkw3b.core.entities import Entity
from d0rkw3b.core.errors import ConnectorPermissionError
from d0rkw3b.core.registry import load_registry


class ConfigurationTests(unittest.TestCase):
    def test_explicit_preferences_and_connector_disable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.json'
            providers, _ = load_registry()
            id = providers[0]['id']
            path.write_text(json.dumps({'default_format': 'json', 'disabled_providers': [id], 'disabled_connectors': ['dns']}))
            with patch.dict(os.environ, {'D0RKW3B_CONFIG': str(path)}):
                self.assertFalse(next(p for p in load_registry()[0] if p['id'] == id)['enabled'])
                with self.assertRaises(ConnectorPermissionError):
                    collect(Entity.create('example.com'), 'dns')
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    self.assertEqual(main(['example.com']), 0)
                self.assertIsInstance(json.loads(out.getvalue()), list)

    def test_debug_and_invalid_config_keep_stdout_clean(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(main(['ip', 'bad', '--format', 'json', '--debug', '--verbose']), 2)
        self.assertFalse(out.getvalue())
        self.assertIn('File ', err.getvalue())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            path.write_text('{broken')
            with patch.dict(os.environ, {'D0RKW3B_CONFIG': str(path)}), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(['example.com']), 2)
