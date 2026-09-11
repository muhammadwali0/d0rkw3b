import contextlib
import io
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import quote, unquote

from d0rkw3b.cli import main
from d0rkw3b.core.detector import detect
from d0rkw3b.core.registry import load_registry, validate_provider
from d0rkw3b.core.renderer import render
from d0rkw3b.core.validation import validate

ROOT = Path(__file__).resolve().parents[1]


class CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.providers, cls.errors = load_registry()

    def invoke(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = main(list(args))
        return status, out.getvalue(), err.getvalue()

    def test_inventory_coverage(self):
        inventory = json.loads((ROOT / 'docs/migration-inventory.json').read_text())
        self.assertFalse(self.errors)
        self.assertEqual(len(self.providers), 425)
        self.assertEqual({p['id'] for p in self.providers}, {p['id'] for p in inventory})
        self.assertEqual(len({p['source'] for p in self.providers}), 35)
        # Compare every legacy URL, not just provider names. Documented changes
        # are checked separately below. Decode once to compare query space style.
        samples = dict(query='Acme', username='someone', username2='other', email='a@example.com',
                       domain='example.com', ip='1.1.1.1', url='https://example.com/image.png',
                       video_id='abcdefghijk', phone='1234567', user_id='123', location_id='123',
                       list_id='123', repository='repo', company='acme', year='2024')
        by_id = {p['id']: p for p in inventory}
        for provider in self.providers:
            kind = provider['target_types'][0]
            variable = {'search': 'query', 'document': 'query', 'ipv4': 'ip'}.get(kind, kind)
            target = validate(samples[variable], kind)
            rendered = render(provider, target, {k: samples[k] for k in provider['parameters'] if k != variable})
            old = by_id[provider['id']]['legacy_template']
            for key, value in samples.items():
                old = old.replace('MIGRATION_' + key.upper() + 'END', quote(value, safe=''))
            if not any('Removed copied' in note or 'Exclusive end' in note for note in by_id[provider['id']]['changes']):
                self.assertEqual(unquote(rendered), unquote(old), provider['id'])

    def test_detection(self):
        for value, kind in [('foo@example.com', 'email'), ('8.8.8.8', 'ipv4'),
                            ('2001:4860:4860::8888', 'ipv6'), ('https://example.com/page', 'url'),
                            ('example.com', 'domain'), ('@someone', 'username'),
                            ('wali', 'search'), ('Acme Corporation', 'search')]:
            self.assertEqual(detect(value).type, kind)
        self.assertEqual(validate('例え.テスト', 'domain').value, 'xn--r8jz45g.xn--zckzah')

    def test_invalid_inputs(self):
        for value, kind in [('', 'search'), ('a\nfoo', 'search'), ('999.1.1.1', 'ip'),
                            ('bad..com', 'domain'), ('a@@b.com', 'email'),
                            ('file:///etc/passwd', 'url'), ('https://user:pass@example.com', 'url'),
                            ('https://example.com:99999', 'url'), ('a/b', 'username'),
                            ('abc', 'video_id'), ('a', 'user_id')]:
            with self.assertRaises(ValueError, msg=(value, kind)):
                validate(value, kind)

    def test_encoding(self):
        provider = dict(self.providers[0], template='https://example.com/{query}?q={query}#x={query}')
        for value in ['a b', 'a+b', 'a&b', '東京', 'a@b', 'a#b', 'a/b', 'https://a.com/?x=1&y=2']:
            result = render(provider, validate(value, 'search'))
            encoded = quote(value, safe='')
            self.assertEqual(result, f'https://example.com/{encoded}?q={encoded}#x={encoded}')

    def test_schema_and_graceful_loading(self):
        valid = self.providers[0]
        for change in [{'template': 'javascript:alert(1)'}, {'template': 'https://a.com/{bad}'},
                       {'template': 'https://a.com/{query'}, {'template': 'https://a.com/{query!r}'},
                       {'target_types': ['bogus']}, {'enabled': 'yes'}, {'id': 'BAD'},
                       {'network': 'tor'}, {'homepage': 'file:///tmp/a'}]:
            with self.assertRaises(ValueError):
                validate_provider(valid | change)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            path.write_text('[invalid')
            providers, errors = load_registry([path])
            self.assertEqual(len(providers), 425)
            self.assertEqual(len(errors), 1)
            path.write_text(json.dumps([valid, {'id': 'missing'}, valid | {'id': 'community-test'}]))
            providers, errors = load_registry([path])
            self.assertEqual(len(providers), 426)
            self.assertEqual(len(errors), 2)

    def test_cli_local_deterministic(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('network forbidden')), patch('webbrowser.open', side_effect=AssertionError('browser forbidden')):
            for args in [('username', 'muhammadwali0'), ('email', 'example@example.com'),
                         ('domain', 'example.com'), ('ip', '1.1.1.1'), ('url', 'https://example.com/page'),
                         ('search', 'Acme Corporation'), ('wali', '--type', 'username')]:
                first = self.invoke(*args, '--format', 'json')
                self.assertEqual(first[0], 0, first)
                self.assertEqual(first, self.invoke(*args, '--format', 'json'))
                self.assertTrue(json.loads(first[1]))
        rows = json.loads(self.invoke('search', 'hello', '--format', 'json')[1])
        self.assertTrue(all(p['network'] == 'clearnet' for p in rows))

    def test_parameters_and_browser(self):
        year = next(p for p in self.providers if p['source'] == 'x.py:x_username_by_year')
        result = self.invoke('username', 'someone', '--provider', year['id'], '--param', 'year=2024')
        self.assertEqual(result[0], 0)
        self.assertIn('until%3A2025-01-01', result[1])
        self.assertEqual(self.invoke('username', 'someone', '--provider', year['id'])[0], 2)
        with patch('webbrowser.open', return_value=True) as browser:
            self.assertEqual(self.invoke('search', 'hello', '--open')[0], 2)
            tor = next(p for p in self.providers if p['network'] == 'tor')
            self.assertEqual(self.invoke('search', 'hello', '--provider', tor['id'], '--network', 'tor', '--open')[0], 2)
            browser.assert_not_called()
            clear = next(p for p in self.providers if p['source'] == 'search_links.py:generate_links' and p['network'] == 'clearnet')
            self.assertEqual(self.invoke('search', 'hello', '--provider', clear['id'], '--open')[0], 0)
            browser.assert_called_once()

    def test_exports_and_entrypoint(self):
        for fmt in ('text', 'json', 'csv', 'markdown'):
            status, out, _ = self.invoke('example.com', '--format', fmt)
            self.assertEqual(status, 0)
            self.assertIn('https://', out)
        result = subprocess.run([sys.executable, '-m', 'd0rkw3b', '--version'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), '1.0.0')

class InteractionTests(unittest.TestCase):
    def test_interactive_recovery_and_exit(self):
        from d0rkw3b.cli import interactive
        out = io.StringIO()
        with patch('builtins.input', side_effect=['help', 'domain example.com', '"bad', 'quit']), contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(interactive(), 0)
        self.assertIn('https://', out.getvalue())
        with patch('builtins.input', side_effect=EOFError), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(interactive(), 0)

    def test_guided_menu(self):
        from d0rkw3b.cli import menu_query
        providers, _ = load_registry()
        out = io.StringIO()
        with patch('builtins.input', side_effect=['1', 'example.com']), contextlib.redirect_stdout(out):
            menu_query('domain', providers)
        self.assertIn('https://', out.getvalue())

    def test_ipv6_and_disabled_reference(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(['ip', '2001:4860:4860::8888', '--format', 'json']), 0)
        rows = json.loads(out.getvalue())
        self.assertFalse(any('ipaddress.com/ipv4' in p['url'] for p in rows))
        self.assertTrue(any('2001%3A4860' in p['url'] for p in rows))
        providers, _ = load_registry()
        self.assertTrue(all(not p['enabled'] for p in providers if p['requires_api_key']))
        self.assertFalse(any('AIza' in p['template'] for p in providers))


if __name__ == '__main__':
    unittest.main()
