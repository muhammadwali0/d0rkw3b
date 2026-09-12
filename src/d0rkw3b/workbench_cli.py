"""Structured investigation and methodology commands."""

import argparse
import csv
import http.client
import json
import sqlite3
import sys
from dataclasses import replace

from .core.diagnostics import report_error
from .core.recipes import load_recipes
from .core.registry import load_registry
from .investigation import investigate


def dispatch(argv):
    if (
        not argv
        or argv[0] not in ("investigate", "recipes")
        and argv[:2] != ["dev", "validate-recipes"]
    ):
        return None
    recipes_command = argv[0] != "investigate"
    parser = argparse.ArgumentParser(
        prog="d0rkw3b " + argv[0],
        description=(
            "List and inspect declarative methodology."
            if recipes_command
            else "Build an offline investigation plan. Generated queries are not findings."
        ),
    )
    parser.add_argument(
        "--format", choices=("text", "json", "csv", "markdown"), default="text"
    )
    parser.add_argument("--provider-file", action="append", default=[])
    parser.add_argument("--recipe-file", action="append", default=[])
    if recipes_command:
        parser.add_argument(
            "action", choices=("list", "info", "validate", "validate-recipes")
        )
        parser.add_argument("name", nargs="?")
    else:
        parser.add_argument("target")
        parser.add_argument("--type")
        parser.add_argument("--category")
        parser.add_argument("--pack")
        parser.add_argument(
            "--expression", action="store_true", help="parse TYPE:VALUE [category:NAME]"
        )
        parser.add_argument("--recipe")
        parser.add_argument(
            "--with",
            dest="connectors",
            action="append",
            default=[],
            help="explicit connector ID; displays capabilities before collection",
        )
        parser.add_argument("--case", help="save this run to an existing local case")
        parser.add_argument(
            "--all",
            action="store_true",
            help="show all paths instead of five queries per stage",
        )
        parser.add_argument(
            "--network", choices=("clearnet", "tor", "all"), default="clearnet"
        )
        parser.add_argument(
            "--param", action="append", default=[], metavar="NAME=VALUE"
        )
    args = parser.parse_args(argv[1:])
    try:
        if recipes_command:
            providers, errors = load_registry(args.provider_file)
            recipes, recipe_errors = load_recipes(providers, args.recipe_file)
            errors.extend(recipe_errors)
            for error in errors:
                print(error, file=sys.stderr)
            if args.action in ("validate", "validate-recipes"):
                print(json.dumps({"recipes": len(recipes), "errors": errors}))
                return 1 if errors else 0
            if args.action == "info":
                recipes = [r for r in recipes if r["id"] == args.name]
                if not recipes:
                    raise ValueError("unknown recipe; use recipes list")
            elif args.name:
                raise ValueError("recipes list does not accept a name")
            if args.format == "json":
                print(json.dumps(recipes, indent=2))
            elif args.format != "text":
                raise ValueError("recipes supports text or json output")
            else:
                for recipe in recipes:
                    print(f"{recipe['id']}: {recipe['description']}")
                    if args.action == "info":
                        for stage in recipe["stages"]:
                            print(f"  {stage['name']}: {stage['description']}")
                            for provider in stage["providers"]:
                                print(f"    {provider}")
            return 1 if errors else 0
        parameters = {}
        from .core.models import VARIABLES

        for pair in args.param:
            key, separator, value = pair.partition("=")
            if not separator or key not in VARIABLES or key in parameters:
                raise ValueError("invalid or duplicate parameter")
            parameters[key] = value
        if args.expression:
            from .core.expressions import parse_expression

            kind, value, category = parse_expression(args.target)
            if (
                args.type
                and args.type != kind
                or args.category
                and category
                and args.category != category
            ):
                raise ValueError("expression conflicts with explicit filters")
            args.type, args.target = kind, value
            args.category = category or args.category
        plan = investigate(
            args.target,
            type=args.type,
            recipe=args.recipe,
            all=args.all,
            network=args.network,
            provider_files=args.provider_file,
            recipe_files=args.recipe_file,
            parameters=parameters,
            category=args.category,
            pack=args.pack,
        )
        if args.connectors:
            if len(args.connectors) > 5 or len(set(args.connectors)) != len(
                args.connectors
            ):
                raise ValueError("select at most five distinct connectors")
            if args.case:
                from .cases.store import CaseStore

                with CaseStore() as store:
                    store.case(args.case)
            from .connectors.cli import disclosure
            from .connectors.registry import collect

            for connector in args.connectors:
                result = collect(plan.entity, connector, disclose=disclosure)
                merged = {
                    entity.entity_id: entity
                    for entity in [*plan.entities, *result.entities]
                }
                plan = replace(
                    plan,
                    entities=list(merged.values()),
                    relationships=[*plan.relationships, *result.relationships],
                    observations=[*plan.observations, *result.observations],
                    diagnostics=[*plan.diagnostics, *result.diagnostics],
                )
        if args.case:
            from .cases.store import CaseStore

            with CaseStore(writable=True) as store:
                store.save(args.case, plan)
        for error in plan.diagnostics:
            print(f"notice: {error}", file=sys.stderr)
        if args.format == "json":
            print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2))
        elif args.format in ("csv", "markdown"):
            from .cli import output

            rows = [
                query | {"category": stage["name"]}
                for stage in plan.paths
                for query in stage["queries"]
            ]
            if args.format == "csv":
                writer = csv.DictWriter(
                    sys.stdout,
                    fieldnames=[
                        "kind",
                        "id",
                        "name",
                        "category",
                        "network",
                        "status",
                        "url",
                    ],
                    extrasaction="ignore",
                )
                writer.writeheader()
                writer.writerows(rows)
            else:
                print("# Generated queries (not confirmed findings)\n")
                print(output(rows, args.format), end="")
        else:
            print("D0RKW3B — The Local OSINT Workbench")
            print(f"Target: {plan.entity.normalized_value}\nType: {plan.entity.type}")
            print("Recommended paths (generated queries, not confirmed findings):")
            for stage in plan.paths:
                print(f"\n{stage['name']}: {stage['description']}")
                for query in stage["queries"]:
                    print(f"  {query['name']}\n    {query['url']}")
                if stage["additional"]:
                    print(f"  {stage['additional']} additional queries with --all")
            if not plan.paths:
                print("No query providers match this entity and filter.")
            for relation in plan.relationships:
                print(
                    f"\nPivot: {relation.predicate} (method: {relation.provenance.method})"
                )
        return 0
    except (ValueError, OSError, sqlite3.Error, http.client.HTTPException) as exc:
        report_error(exc)
        return 2
