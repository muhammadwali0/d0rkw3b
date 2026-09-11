import contextlib
import io
import socket
import ssl
import unittest
from unittest.mock import Mock, patch

from d0rkw3b.cli import main
from d0rkw3b.core.health import check_providers, interpret_status
from d0rkw3b.core.network import NetworkPolicyError, request
from d0rkw3b.core.registry import load_registry


class HealthTests(unittest.TestCase):
    def setUp(self):
        self.providers, _ = load_registry()
        self.provider = next(p for p in self.providers if p['enabled'] and p['network'] == 'clearnet')

    def test_status_interpretation(self):
        for status, expected in [(200, 'healthy'), (204, 'healthy'), (301, 'redirect'),
            (401, 'auth-required'), (403, 'manual-verification-required'),
            (405, 'manual-verification-required'), (429, 'rate-limited'),
            (404, 'degraded'), (503, 'degraded')]:
            self.assertEqual(interpret_status(status), expected)

    def test_no_semantic_claim_and_no_targets(self):
        probe = Mock(return_value=(200, {}, b''))
        provider = self.provider | {'homepage': 'https://example.com/private?target=SECRET'}
        result = check_providers([provider], probe=probe)
        probe.assert_called_once_with('https://example.com/', method='HEAD', timeout=5)
        row = result['results'][0]
        self.assertTrue(row['reachable'])
        self.assertEqual(row['semantic_status'], 'unverified')
        self.assertIsNone(row['last_verified'])
        self.assertIsNotNone(row['last_checked'])

    def test_bounds_rate_limits_and_skips(self):
        probe = Mock(return_value=(429, {'Retry-After': '3600'}, b''))
        sleep = Mock()
        result = check_providers(self.providers, max_requests=2, probe=probe, sleep=sleep)
        self.assertEqual(probe.call_count, 2)
        sleep.assert_called_once_with(0.5)
        checked = [r for r in result['results'] if r['last_checked']]
        self.assertTrue(all(r['health'] == 'rate-limited' for r in checked))
        self.assertTrue(all(r['failure_count'] == 0 for r in checked))
        self.assertTrue(any(r['health'] == 'tor-unchecked' for r in result['results']))
        for kwargs in ({'max_requests': 0}, {'max_requests': 101}, {'timeout': 0}, {'delay': 0}):
            with self.assertRaises(ValueError):
                check_providers([], **kwargs)

    def test_network_errors(self):
        for error, status in [(socket.gaierror(), 'dns-failure'), (ssl.SSLError(), 'tls-failure'),
                              (TimeoutError(), 'timeout'), (OSError(), 'unreachable')]:
            row = check_providers([self.provider], probe=Mock(side_effect=error))['results'][0]
            self.assertEqual(row['health'], status)
            self.assertFalse(row['reachable'])
            self.assertEqual(row['failure_count'], 1)

    def test_public_destination_boundary(self):
        with patch('socket.socket', side_effect=AssertionError('must not connect')):
            for url in ('http://foo.onion/', 'file:///tmp/a', 'https://user:pass@example.com', 'https://example.com:9999'):
                with self.assertRaises(NetworkPolicyError):
                    request(url)
            with patch('socket.getaddrinfo', return_value=[(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 443))]):
                with self.assertRaises(NetworkPolicyError):
                    request('https://example.com')

    def test_cli_help_never_probes(self):
        with patch('socket.socket', side_effect=AssertionError('network')), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as exited:
                main(['providers', 'health', '--help'])
            self.assertEqual(exited.exception.code, 0)
            self.assertEqual(main(['providers', 'list', '--format', 'json']), 0)
            self.assertEqual(main(['dev', 'registry-stats']), 0)
