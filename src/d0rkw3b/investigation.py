"""Offline investigation planning API. No implicit connector execution or storage."""

from dataclasses import asdict, dataclass

from .core.entities import Entity, Observation, Provenance, Relationship, identifier
from .core.ranking import rank_providers, ranking
from .core.recipes import load_recipes
from .core.registry import load_registry
from .core.renderer import fields, render
from .core.validation import validate


@dataclass(frozen=True)
class Investigation:
    entity: Entity
    entities: list
    relationships: list
    observations: list
    paths: list
    diagnostics: list
    recipe: str | None = None

    def to_dict(self):
        return {"schema_version": 1, **asdict(self)}


def investigate(
    value,
    *,
    type=None,
    recipe=None,
    all=False,
    network="clearnet",
    provider_files=(),
    recipe_files=(),
    parameters=None,
    created_at=None,
    category=None,
    pack=None,
):
    """Return a plan. Creation times are real; normalized values and IDs are stable.

    ``all`` includes all enabled matching providers. No case is created, no
    network request occurs, and no executable plugins are imported.
    """
    if network not in ("clearnet", "tor", "all"):
        raise ValueError("network must be clearnet, tor or all")
    entity = Entity.create(value, type, created_at=created_at)
    target = validate(entity.normalized_value, entity.type)
    if target.variable in (parameters or {}) or "next_year" in (parameters or {}):
        raise ValueError(
            "parameters cannot override the input entity or derived next_year"
        )
    providers, diagnostics = load_registry(provider_files)
    from .core.packs import in_pack, packs

    if category and category not in {p["category"] for p in providers}:
        raise ValueError("unknown category: " + category)
    if pack and pack not in {p["id"] for p in packs(providers)}:
        raise ValueError("unknown pack: " + pack)
    stages = None
    if recipe:
        recipes, errors = load_recipes(providers, recipe_files)
        diagnostics.extend(errors)
        selected = next((r for r in recipes if r["id"] == recipe), None)
        if selected is None:
            raise ValueError("unknown or invalid recipe: " + recipe)
        if target.type not in selected["target_types"]:
            raise ValueError("recipe does not accept " + target.type)
        stages = selected["stages"]
    available = [
        p
        for p in rank_providers(providers)
        if p["enabled"]
        and p["status"] not in ("broken", "disabled", "deprecated")
        and target.type in p["target_types"]
        and (not category or p["category"] == category)
        and (not pack or in_pack(p, pack))
        and (network == "all" or p["network"] == network)
    ]
    if stages is None:
        categories = list(dict.fromkeys(p["category"] for p in available))
        stages = [
            {
                "name": category,
                "description": "Generated query paths; manually assess returned information.",
                "providers": [p["id"] for p in available if p["category"] == category],
            }
            for category in categories
        ]
    observations, paths, seen = [], [], set()
    for stage in stages:
        queries = []
        for provider in available:
            if provider["id"] not in stage["providers"]:
                continue
            needed = (
                fields(provider["template"])
                - {target.variable}
                - (parameters or {}).keys()
            )
            if "year" in (parameters or {}):
                needed.discard("next_year")
            if needed:
                diagnostics.append(
                    f"{provider['id']}: requires {', '.join(sorted(needed))}"
                )
                continue
            try:
                url = render(provider, target, parameters)
            except ValueError as exc:
                diagnostics.append(f"{provider['id']}: {exc}")
                continue
            queries.append(
                {
                    "id": provider["id"],
                    "name": provider["name"],
                    "url": url,
                    "kind": "generated_query",
                    "network": provider["network"],
                    "status": provider["status"],
                    "ranking": ranking(provider),
                }
            )
        total = len(queries)
        queries = queries if all else queries[:5]
        for query in queries:
            if query["id"] not in seen:
                provenance = Provenance(
                    query["id"],
                    "template rendering",
                    query["url"],
                    entity.created_at,
                    source_url=query["url"],
                    notes="Generated locally; destination not contacted.",
                )
                observations.append(
                    Observation(
                        identifier(
                            "observation", entity.entity_id, query["id"], query["url"]
                        ),
                        "generated_query",
                        query["id"],
                        "template rendering",
                        entity.entity_id,
                        entity.created_at,
                        provenance,
                        metadata={"url": query["url"]},
                    )
                )
                seen.add(query["id"])
        if total:
            paths.append(
                {
                    "name": stage["name"],
                    "description": stage["description"],
                    "queries": queries,
                    "additional": total - len(queries),
                }
            )
    entities, relationships = [entity], []
    if entity.type == "email":
        domain = Entity.create(
            entity.normalized_value.rsplit("@", 1)[1],
            "domain",
            created_at=entity.created_at,
        )
        provenance = Provenance(
            "input",
            "email syntax parsing",
            entity.entity_id,
            entity.created_at,
            notes="Syntactic domain component only; no mailbox or DNS verification.",
        )
        relationship = Relationship.create(
            entity, "uses_domain", domain, provenance=provenance
        )
        entities.append(domain)
        relationships.append(relationship)
    return Investigation(
        entity, entities, relationships, observations, paths, diagnostics, recipe
    )
