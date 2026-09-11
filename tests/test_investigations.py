import contextlib
import io
import json
import unittest
from unittest.mock import patch

from d0rkw3b import investigate, providers
from d0rkw3b.cli import main
from d0rkw3b.core.entities import Entity, Observation, Provenance, Relationship
from d0rkw3b.core.recipes import load_recipes, validate_recipe

STAMP = "2026-09-11T00:00:00+00:00"


class EntityTests(unittest.TestCase):
    def test_normalization_identity(self):
        self.assertEqual(
            Entity.create("Example.COM", "domain").entity_id,
            Entity.create("example.com", "domain").entity_id,
        )
        self.assertEqual(
            Entity.create("@alice").entity_id,
            Entity.create("alice", "username").entity_id,
        )
        self.assertNotEqual(
            Entity.create("@alice").entity_id,
            Entity.create("alice@example.com").entity_id,
        )
        self.assertNotEqual(
            Entity.create("Alice", "username").entity_id,
            Entity.create("alice", "username").entity_id,
        )
        entity = Entity.create(" Example.COM ", "domain")
        self.assertEqual(entity.raw_value, " Example.COM ")
        self.assertEqual(entity.normalized_value, "example.com")

    def test_provenance_required(self):
        with self.assertRaises(ValueError):
            Provenance("source", "method", "", STAMP)
        with self.assertRaises(ValueError):
            Provenance("source", "method", "ref", "2026-09-11")
        entity = Entity.create("example.com")
        provenance = Provenance("test", "manual", "reference", STAMP)
        with self.assertRaises(ValueError):
            Relationship.create(entity, "probably_owns", entity, provenance=provenance)
        with self.assertRaises(ValueError):
            Observation(
                "id",
                "generated_query",
                "test",
                "render",
                entity.entity_id,
                STAMP,
                provenance,
                output_entity_id="not-a-finding",
            )


class InvestigationTests(unittest.TestCase):
    def test_api_offline_and_stable_with_clock(self):
        with patch("socket.socket", side_effect=AssertionError("network forbidden")):
            plan = investigate(
                "example.com", recipe="domain-footprint", created_at=STAMP
            )
            self.assertEqual(
                plan.to_dict(),
                investigate(
                    "example.com", recipe="domain-footprint", created_at=STAMP
                ).to_dict(),
            )
            self.assertTrue(plan.paths)
            self.assertTrue(all(o.kind == "generated_query" for o in plan.observations))
            self.assertFalse(plan.relationships)
            self.assertEqual(len(providers()), 425)

    def test_email_pivot_is_syntactic(self):
        plan = investigate("alice@example.com")
        self.assertEqual(len(plan.entities), 2)
        relation = plan.relationships[0]
        self.assertEqual(relation.predicate, "uses_domain")
        self.assertEqual(relation.provenance.method, "email syntax parsing")
        self.assertIn("no mailbox or DNS verification", relation.provenance.notes)

    def test_parameter_override_rejected(self):
        with self.assertRaises(ValueError):
            investigate("alice", type="username", parameters={"username": "bob"})

    def test_recipes(self):
        registry = providers()
        recipes, errors = load_recipes(registry)
        self.assertFalse(errors)
        self.assertEqual(len(recipes), 7)
        for recipe in recipes:
            kind = recipe["target_types"][0]
            sample = {
                "domain": "example.com",
                "username": "alice",
                "email": "alice@example.com",
                "repository": "repo",
                "document": "annual report",
                "url": "https://example.com/image.png",
                "company": "acme",
            }[kind]
            self.assertTrue(investigate(sample, type=kind, recipe=recipe["id"]).paths)
        broken = dict(
            recipes[0],
            stages=[{"name": "bad", "description": "bad", "providers": ["invented"]}],
        )
        with self.assertRaises(ValueError):
            validate_recipe(broken, registry)
        with self.assertRaises(ValueError):
            investigate("@alice", recipe="domain-footprint")

    def test_cli_groups(self):
        for args in [
            ("recipes", "list"),
            ("recipes", "info", "domain-footprint"),
            ("dev", "validate-recipes"),
            ("investigate", "example.com"),
            ("investigate", "alice", "--type", "username"),
        ]:
            with (
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(main(list(args)), 0)
        for fmt in ("json", "csv", "markdown"):
            out = io.StringIO()
            with (
                contextlib.redirect_stdout(out),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(
                    main(["investigate", "example.com", "--format", fmt]), 0
                )
            if fmt == "json":
                self.assertEqual(json.loads(out.getvalue())["entity"]["type"], "domain")
            self.assertIn("https://", out.getvalue())
