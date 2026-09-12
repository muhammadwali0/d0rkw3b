import contextlib
import io
import json
import unittest

from d0rkw3b import investigate
from d0rkw3b.cli import main
from d0rkw3b.core.expressions import parse_expression
from d0rkw3b.core.packs import packs
from d0rkw3b.core.registry import load_registry


class ExpressionPackTests(unittest.TestCase):
    def test_small_grammar(self):
        self.assertEqual(
            parse_expression("domain:example.com category:domain"),
            ("domain", "example.com", "domain"),
        )
        self.assertEqual(
            parse_expression('search:"Acme Corporation"'),
            ("search", "Acme Corporation", None),
        )
        self.assertEqual(
            parse_expression("ip:2001:4860:4860::8888")[1], "2001:4860:4860::8888"
        )
        for bad in [
            "eval:1+1",
            "domain:example.com AND category:archive",
            "domain:example.com sort:date",
        ]:
            with self.assertRaises(ValueError):
                parse_expression(bad)
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            self.assertEqual(
                main(
                    [
                        "investigate",
                        "domain:example.com category:domain",
                        "--expression",
                    ]
                ),
                0,
            )

    def test_pack_counts_and_offline_filter(self):
        registry, _ = load_registry()
        counts = {p["id"]: p["providers"] for p in packs(registry)}
        self.assertEqual(counts["darkweb"], 13)
        self.assertEqual(counts["infrastructure"], 59)
        self.assertTrue(investigate("example.com", pack="infrastructure").paths)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(
                main(
                    ["providers", "list", "--pack", "development", "--format", "json"]
                ),
                0,
            )
        self.assertEqual(len(json.loads(out.getvalue())), 13)
