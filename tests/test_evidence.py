import hashlib
import os
import tempfile
import unittest
from pathlib import Path

from d0rkw3b.cases.evidence import add_evidence
from d0rkw3b.cases.store import CaseStore
from d0rkw3b.core.errors import CaseNotFoundError, EvidenceError
from d0rkw3b.localfiles import inspect_file


class EvidenceTests(unittest.TestCase):
    def test_import_preserves_bytes_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "private 世界.txt"
            original = b"hello alice@example.com https://example.com/path\n\x00"
            source.write_bytes(original)
            with CaseStore(root / "data", writable=True) as store:
                store.new("../../case-name-is-not-a-path")
                evidence = add_evidence(store, "../../case-name-is-not-a-path", source)
                destination = store.root / evidence["stored_path"]
                self.assertEqual(source.read_bytes(), original)
                self.assertEqual(destination.read_bytes(), original)
                self.assertEqual(
                    evidence["sha256"], hashlib.sha256(original).hexdigest()
                )
                self.assertTrue(destination.resolve().is_relative_to(store.root))
                self.assertNotIn(source.name, destination.name)
                saved = store.show("../../case-name-is-not-a-path")
                self.assertEqual(
                    saved["evidence"][0]["provenance"]["method"],
                    "byte-preserving import and SHA-256",
                )
                self.assertEqual(len(saved["entities"]), 1)
                with self.assertRaises(CaseNotFoundError):
                    add_evidence(store, "missing", source)

    def test_rejects_non_regular_and_symlink_storage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises((EvidenceError, OSError)):
                inspect_file(root)
            source = root / "source"
            source.write_bytes(b"content")
            if os.name != "nt":
                with CaseStore(root / "data", writable=True) as store:
                    case = store.new("case")
                    (store.root / "evidence").mkdir()
                    (store.root / "evidence" / case["case_id"]).symlink_to(
                        root, target_is_directory=True
                    )
                    with self.assertRaises(EvidenceError):
                        add_evidence(store, "case", source)

    def test_local_metadata_and_references(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.png"
            path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + b"\x00\x00\x00\x0dIHDR"
                + (640).to_bytes(4, "big")
                + (480).to_bytes(4, "big")
            )
            result = inspect_file(path)
            self.assertEqual(result["dimensions"], [640, 480])
            self.assertEqual(result["mime_basis"], "PNG signature")
            path = Path(directory) / "doc.txt"
            path.write_text(
                "Contact alice@example.com and visit https://example.com",
                encoding="utf-8",
            )
            result = inspect_file(path)
            self.assertEqual(result["references"]["emails"], ["alice@example.com"])
            self.assertEqual(result["references"]["urls"], ["https://example.com"])
