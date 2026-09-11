"""Explicit local registry activation and logical pack inspection."""

import argparse
import json
import sys

from .core.diagnostics import report_error
from .core.packs import packs
from .core.registry import load_bundled_registry, load_registry
from .core.updates import install_snapshot, rollback


def dispatch(argv):
    if argv[:2] == ["packs", "list"]:
        parser = argparse.ArgumentParser(
            prog="d0rkw3b packs list",
            description="Logical groups of existing query providers.",
        )
        parser.add_argument("--format", choices=("text", "json"), default="text")
        args = parser.parse_args(argv[2:])
        providers, errors = load_registry()
        for error in errors:
            print(error, file=sys.stderr)
        result = packs(providers)
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            for pack in result:
                print(
                    f"{pack['id']}: {pack['providers']} providers — {pack['description']}"
                )
        return 0
    if argv[:2] not in (["providers", "update"], ["providers", "rollback"]):
        return None
    parser = argparse.ArgumentParser(
        prog="d0rkw3b " + " ".join(argv[:2]),
        description=(
            "Activate a local provider-array snapshot after explicit SHA-256 and schema checks. "
            "No update server or network request. Rollback restores a previous snapshot or bundled registry."
        ),
    )
    if argv[1] == "update":
        parser.add_argument("file")
        parser.add_argument(
            "--sha256",
            required=True,
            help="expected SHA-256 of the input file, obtained independently",
        )
    args = parser.parse_args(argv[2:])
    try:
        bundled, errors = load_bundled_registry()
        if errors:
            raise ValueError("bundled registry has validation errors")
        result = (
            install_snapshot(args.file, args.sha256, bundled)
            if argv[1] == "update"
            else rollback(bundled)
        )
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, TypeError, KeyError, OSError) as exc:
        report_error(exc)
        return 2
