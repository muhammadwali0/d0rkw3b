import contextlib
import io
import json
import unittest

from d0rkw3b.cli import main
from d0rkw3b.core.ranking import rank_providers, ranking
from d0rkw3b.core.registry import load_registry, validate_provider


class RankingTests(unittest.TestCase):
    def test_transparent_and_deterministic(self):
        providers, _ = load_registry()
        ranked = rank_providers(providers)
        self.assertEqual(ranked, rank_providers(list(reversed(providers))))
        result = ranking(ranked[0])
        self.assertEqual(result['score'], sum(result['components'].values()))
        self.assertTrue(result['basis'])
        with self.assertRaises(ValueError):
            validate_provider(providers[0] | {'quality': {'priority': 99, 'reason': 'bad'}})

    def test_text_recommendations_preserve_complete_machine_output(self):
        def run(args):
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                self.assertEqual(main(args), 0)
            return out.getvalue(), err.getvalue()
        text, notice = run(['domain', 'example.com'])
        all_text, _ = run(['domain', 'example.com', '--all'])
        machine, _ = run(['domain', 'example.com', '--format', 'json'])
        self.assertIn('additional providers', notice)
        self.assertEqual(text.count('\n  https://'), 10)
        self.assertEqual(all_text.count('\n  https://'), len(json.loads(machine)))
        self.assertGreater(len(json.loads(machine)), 10)
