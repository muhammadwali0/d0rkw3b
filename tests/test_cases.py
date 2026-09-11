import contextlib
import io
import json
import os
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from d0rkw3b import investigate
from d0rkw3b.cases.store import CaseStore
from d0rkw3b.cli import main
from d0rkw3b.core.config import data_directory, storage_directory
from d0rkw3b.core.entities import Entity, Provenance, Relationship
from d0rkw3b.core.errors import CaseNotFoundError, StorageError


class CaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "data"

    def test_no_implicit_storage(self):
        with patch.dict(os.environ, {"D0RKW3B_DATA_DIR": str(self.root)}):
            investigate("example.com")
            with CaseStore() as store:
                self.assertEqual(store.list(), [])
            self.assertFalse(self.root.exists())

    def test_persistence_deduplication_and_runs(self):
        with CaseStore(self.root, writable=True) as store:
            store.new("Acme 世界")
            plan = investigate("alice@example.com")
            store.save("Acme 世界", plan)
            store.save("Acme 世界", plan)
            store.note("Acme 世界", "Review registration history")
            self.assertEqual(store.db.execute("PRAGMA user_version").fetchone()[0], 1)
            self.assertEqual(store.db.execute("PRAGMA foreign_keys").fetchone()[0], 1)
        with CaseStore(self.root) as store:
            data = store.show("Acme 世界")
            self.assertEqual(len(data["entities"]), 2)
            self.assertEqual(len(data["runs"]), 2)
            self.assertEqual(len(data["relationships"]), 2)
            self.assertTrue(data["observations"])
            self.assertEqual(
                data["relationships"][0]["provenance"]["method"], "email syntax parsing"
            )
            self.assertEqual(len(data["notes"]), 1)
            with self.assertRaises(StorageError):
                store.new("cannot write")

    def test_transaction_rollback_and_case_isolation(self):
        with CaseStore(self.root, writable=True) as store:
            store.new("one")
            store.new("two")
            plan = investigate("example.com")
            stranger = Entity.create("elsewhere.example")
            relation = Relationship.create(
                plan.entity,
                "references",
                stranger,
                provenance=Provenance("test", "manual", "ref", plan.entity.created_at),
            )
            with self.assertRaises(sqlite3.IntegrityError):
                store.save("one", replace(plan, relationships=[relation]))
            self.assertFalse(store.show("one")["entities"])
            self.assertFalse(store.show("one")["runs"])
            store.save("one", plan)
            self.assertFalse(store.show("two")["entities"])
            with self.assertRaises(CaseNotFoundError):
                store.save("missing", plan)
            with self.assertRaises(StorageError):
                store.new("one")

    def test_future_schema_and_foreign_database(self):
        with CaseStore(self.root, writable=True) as store:
            store.new("preserved")
            store.db.execute("PRAGMA user_version = 999")
        with self.assertRaises(StorageError):
            CaseStore(self.root, writable=True)
        db = sqlite3.connect(self.root / "cases.sqlite3")
        self.assertEqual(
            db.execute("SELECT name FROM cases").fetchone()[0], "preserved"
        )
        db.execute("PRAGMA user_version = 0")
        db.close()
        with self.assertRaises(StorageError):
            CaseStore(self.root, writable=True)

    def test_platform_paths_and_repository_exclusion(self):
        with patch.dict(os.environ, {"D0RKW3B_DATA_DIR": str(self.root)}):
            self.assertEqual(data_directory(), self.root)
        repo = Path(self.temp.name) / "repo"
        (repo / ".git").mkdir(parents=True)
        with self.assertRaises(ValueError):
            storage_directory(repo / "case-data")

    def test_cli(self):
        with patch.dict(os.environ, {"D0RKW3B_DATA_DIR": str(self.root)}):
            for args in [
                ("case", "new", "test-case"),
                ("case", "add", "test-case", "example.com"),
                ("case", "note", "test-case", "Check history"),
                (
                    "investigate",
                    "alice@example.com",
                    "--case",
                    "test-case",
                    "--format",
                    "json",
                ),
                ("case", "show", "test-case"),
                ("case", "list"),
            ]:
                out = io.StringIO()
                with (
                    contextlib.redirect_stdout(out),
                    contextlib.redirect_stderr(io.StringIO()),
                ):
                    self.assertEqual(main(list(args)), 0)
                json.loads(out.getvalue())
