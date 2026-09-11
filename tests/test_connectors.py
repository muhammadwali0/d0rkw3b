import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from d0rkw3b.cli import main
from d0rkw3b.connectors.builtin import dns, rdap, rdap_base
from d0rkw3b.connectors.integrations import exiftool, integrations
from d0rkw3b.connectors.models import Collection
from d0rkw3b.connectors.process import run_json
from d0rkw3b.connectors.registry import collect, discover_plugins
from d0rkw3b.core.entities import Entity
from d0rkw3b.core.errors import ConnectorUnavailableError


class ConnectorTests(unittest.TestCase):
    def test_dns_observed_relationships_and_no_shell(self):
        entity = Entity.create("example.com")
        with patch(
            "d0rkw3b.connectors.builtin.run_json",
            return_value=["1.1.1.1", "2606:4700:4700::1111"],
        ) as process:
            result = dns(entity)
        result.validate()
        self.assertEqual(len(result.relationships), 2)
        self.assertTrue(all(r.predicate == "resolves_to" for r in result.relationships))
        self.assertTrue(all(o.kind == "observed" for o in result.observations))
        argv = process.call_args.args[0]
        self.assertEqual(argv[-1], "example.com")
        self.assertEqual(argv[:3], [sys.executable, "-I", "-c"])

    def test_rdap_bootstrap_and_object_validation(self):
        entity = Entity.create("example.com")
        bootstrap = {"services": [[["com"], ["https://rdap.registry.example/v1/"]]]}
        data = {
            "objectClassName": "domain",
            "ldhName": "EXAMPLE.COM",
            "nameservers": [{"ldhName": "ns1.example.net"}],
        }
        with patch(
            "d0rkw3b.connectors.builtin.request",
            side_effect=[
                (200, {}, json.dumps(bootstrap).encode()),
                (200, {}, json.dumps(data).encode()),
            ],
        ) as network:
            result = rdap(entity)
        self.assertEqual(
            network.call_args_list[0].args[0], "https://data.iana.org/rdap/dns.json"
        )
        self.assertEqual(
            network.call_args_list[1].args[0],
            "https://rdap.registry.example/v1/domain/example.com",
        )
        self.assertEqual(result.relationships[0].predicate, "uses_nameserver")
        self.assertEqual(result.entities[1].type, "hostname")
        with patch(
            "d0rkw3b.connectors.builtin.get_json",
            side_effect=[bootstrap, data | {"ldhName": "different.com"}],
        ):
            with self.assertRaises(ConnectorUnavailableError):
                rdap(entity)
        with patch("d0rkw3b.connectors.builtin.request", return_value=(429, {}, b"")):
            with self.assertRaisesRegex(ConnectorUnavailableError, "429"):
                rdap(entity)

    def test_rdap_ip_longest_prefix(self):
        bootstrap = {
            "services": [
                [["0.0.0.0/0"], ["https://general.example/"]],
                [["1.0.0.0/8"], ["https://specific.example/"]],
            ]
        }
        self.assertEqual(
            rdap_base(bootstrap, Entity.create("1.1.1.1")), "https://specific.example/"
        )

    def test_local_file_and_explicit_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "document.txt"
            path.write_text("hello https://example.com", encoding="utf-8")
            with patch(
                "socket.socket", side_effect=AssertionError("network forbidden")
            ):
                entity = Entity.create(str(path), "file")
                disclosure = Mock()
                result = collect(entity, "local-file", disclose=disclosure)
                self.assertEqual(result.relationships[0].predicate, "has_hash")
                disclosure.assert_called_once()
                self.assertTrue(
                    disclosure.call_args.args[0].capabilities.filesystem_read
                )
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    self.assertEqual(main(["file", str(path)]), 0)
                self.assertIn("Capabilities", err.getvalue())
                self.assertEqual(
                    json.loads(out.getvalue())["observations"][0]["kind"], "observed"
                )

    def test_missing_tools_and_exiftool_read_only_options(self):
        with patch("shutil.which", return_value=None):
            self.assertTrue(all(not x["installed"] for x in integrations()))
            with self.assertRaises(ConnectorUnavailableError):
                exiftool(Entity.create("/missing.png", "file"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "-dangerous;name.jpg"
            path.write_bytes(b"test")
            with (
                patch("shutil.which", return_value="/usr/bin/exiftool"),
                patch(
                    "d0rkw3b.connectors.integrations.run_json",
                    return_value=[{"EXIF:Make": "Example"}],
                ) as tool,
            ):
                result = exiftool(Entity.create(str(path), "file"))
            self.assertEqual(result.observations[0].metadata["EXIF:Make"], "Example")
            argv = tool.call_args.args[0]
            self.assertEqual(argv[1:3], ["-config", ""])
            self.assertEqual(argv[-2:], ["--", str(path.resolve())])

    def test_bounded_process(self):
        self.assertEqual(
            run_json([sys.executable, "-I", "-c", 'print("{\\"ok\\": true}")']),
            {"ok": True},
        )
        with self.assertRaisesRegex(ConnectorUnavailableError, "timed out"):
            run_json(
                [sys.executable, "-I", "-c", "import time; time.sleep(5)"], timeout=0.1
            )
        with self.assertRaisesRegex(ConnectorUnavailableError, "size limit"):
            run_json([sys.executable, "-I", "-c", 'print("x" * 10000)'], max_bytes=100)

    def test_investigate_does_not_import_plugins_implicitly(self):
        with patch(
            "d0rkw3b.connectors.registry.entry_points",
            side_effect=AssertionError("plugin discovery"),
        ):
            out = io.StringIO()
            with (
                contextlib.redirect_stdout(out),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(
                    main(["investigate", "example.com", "--format", "json"]), 0
                )


class PluginTests(unittest.TestCase):
    def test_static_discovery_and_explicit_loading(self):
        from d0rkw3b.connectors.builtin import MANIFESTS

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "d0rkw3b-plugin.json"
            manifest = MANIFESTS["local-file"].to_dict() | {"id": "test-plugin"}
            path.write_text(
                json.dumps({"api_version": 1, "connectors": {"test-plugin": manifest}})
            )
            entry = Mock()
            entry.name = "test-plugin"
            entry.dist.files = [path]
            entry.dist.locate_file.return_value = path
            runner = Mock(
                side_effect=lambda entity, timeout: Collection(entity, [entity], [], [])
            )
            entry.load.return_value = runner
            with patch(
                "d0rkw3b.connectors.registry.entry_points", return_value=[entry]
            ):
                plugins, errors = discover_plugins()
                self.assertFalse(errors)
                self.assertIn("test-plugin", plugins)
                entry.load.assert_not_called()
                entity = Entity.create("/example.txt", "file")
                self.assertEqual(collect(entity, "test-plugin").entity, entity)
                entry.load.assert_called_once()
                runner.side_effect = RuntimeError("SECRET-CREDENTIAL")
                with self.assertRaises(ConnectorUnavailableError) as raised:
                    collect(entity, "test-plugin")
                self.assertNotIn("SECRET-CREDENTIAL", str(raised.exception))

    def test_invalid_manifest_does_not_load_code(self):
        entry = Mock()
        entry.name = "bad-plugin"
        entry.dist.files = []
        with patch("d0rkw3b.connectors.registry.entry_points", return_value=[entry]):
            plugins, errors = discover_plugins()
        self.assertFalse(plugins)
        self.assertTrue(errors)
        entry.load.assert_not_called()


class CollectionBoundaryTests(unittest.TestCase):
    def test_invalid_plugin_metadata_is_rejected(self):
        from d0rkw3b.connectors.builtin import observation

        entity = Entity.create("example.com")
        for metadata in ({"not_json": object()}, {"not_finite": float("nan")}):
            item = observation(entity, "test", "test", {})
            item.metadata.update(metadata)
            result = Collection(entity, [entity], [], [item])
            with self.assertRaises(ValueError):
                result.validate()
