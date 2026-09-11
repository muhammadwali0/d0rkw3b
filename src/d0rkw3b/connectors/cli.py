"""Explicit collection commands; all permissions are disclosed on stderr."""

import argparse
import http.client
import json
import sqlite3
import sys

from ..cases.store import CaseStore
from ..core.diagnostics import report_error
from ..core.entities import Entity
from .integrations import integrations
from .registry import collect, manifests


def disclosure(manifest, entity=None):
    print(f"Collecting with {manifest.id}: {manifest.description}", file=sys.stderr)
    if entity is not None:
        print(f"Target: {entity.normalized_value} ({entity.type})", file=sys.stderr)
    print(
        "Required credential variables: "
        + (", ".join(manifest.required_keys) or "none"),
        file=sys.stderr,
    )
    print(
        "Capabilities: " + json.dumps(manifest.to_dict()["capabilities"]),
        file=sys.stderr,
    )
    print("Limits: " + manifest.rate_limit_notes, file=sys.stderr)


def dispatch(argv):
    if not argv or argv[0] not in ("collect", "connectors", "integrations", "file"):
        return None
    parser = argparse.ArgumentParser(
        prog="d0rkw3b " + argv[0],
        description="Explicit collection and optional installed tools. No background collection.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="json")
    if argv[0] in ("collect", "file"):
        parser.add_argument(
            "target", nargs="+", help="[type] target, or local file path"
        )
        parser.add_argument("--type")
        parser.add_argument(
            "--connector", required=argv[0] == "collect", default="local-file"
        )
        parser.add_argument(
            "--with",
            dest="additional",
            action="append",
            default=[],
            help="explicit additional connector, e.g. exiftool",
        )
        parser.add_argument("--case")
        parser.add_argument("--timeout", type=float)
    args = parser.parse_args(argv[1:])
    try:
        if argv[0] == "integrations":
            result = integrations()
        elif argv[0] == "connectors":
            items, errors = manifests()
            for error in errors:
                print(f"plugin warning: {error}", file=sys.stderr)
            result = [m.to_dict() for m in items]
        else:
            from ..core.models import TARGET_TYPES

            tokens, kind = args.target, args.type
            if argv[0] == "file":
                if kind and kind != "file":
                    raise ValueError("file command requires the file entity type")
                kind = "file"
            elif len(tokens) >= 2 and tokens[0] in TARGET_TYPES | {"ip"}:
                if kind and kind != tokens[0]:
                    raise ValueError("conflicting target types")
                kind, tokens = tokens[0], tokens[1:]
            entity = Entity.create(" ".join(tokens), kind)
            if args.case:
                with CaseStore() as store:
                    store.case(
                        args.case
                    )  # Fail before any collection if the destination case is absent.
            ids = [args.connector, *args.additional]
            if len(ids) != len(set(ids)) or len(ids) > 5:
                raise ValueError("select at most five distinct connectors")
            results = [
                collect(entity, key, disclose=disclosure, timeout=args.timeout)
                for key in ids
            ]
            if args.case:
                with CaseStore(writable=True) as store:
                    for key, item in zip(ids, results):
                        store.save(args.case, item, method="collect:" + key)
            result = (
                results[0].to_dict()
                if len(results) == 1
                else [r.to_dict() for r in results]
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, sqlite3.Error, http.client.HTTPException) as exc:
        report_error(exc)
        return 2
