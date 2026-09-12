"""Minimal connector contract shared by core and entry-point plugins."""

import json
from dataclasses import asdict, dataclass, field

from ..core.entities import Entity, Observation, Relationship
from ..core.models import TARGET_TYPES


@dataclass(frozen=True)
class Capabilities:
    network: tuple[str, ...] = ()
    filesystem_read: bool = False
    subprocess: bool = False


@dataclass(frozen=True)
class Manifest:
    id: str
    name: str
    accepted_types: tuple[str, ...]
    produced_types: tuple[str, ...]
    capabilities: Capabilities
    description: str
    rate_limit_notes: str
    timeout_seconds: int = 10
    required_keys: tuple[str, ...] = ()
    optional_keys: tuple[str, ...] = ()
    api_version: int = 1

    def __post_init__(self):
        import re

        if not re.fullmatch("[a-z0-9]+(?:-[a-z0-9]+)*", self.id):
            raise ValueError("invalid connector ID")
        if self.api_version != 1 or not 1 <= self.timeout_seconds <= 60:
            raise ValueError("unsupported connector API or timeout")
        if not self.accepted_types or not set(self.accepted_types).issubset(
            TARGET_TYPES
        ):
            raise ValueError("connector has unsupported accepted entity types")
        if not set(self.produced_types).issubset(TARGET_TYPES):
            raise ValueError("connector has unsupported produced entity types")
        if not isinstance(self.capabilities, Capabilities):
            raise ValueError("connector must declare capabilities")
        if not self.name or not self.description or not self.rate_limit_notes:
            raise ValueError("connector must describe output, limits and purpose")

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Collection:
    entity: Entity
    entities: list[Entity]
    relationships: list[Relationship]
    observations: list[Observation]
    diagnostics: list[str] = field(default_factory=list)

    def to_dict(self):
        return {"schema_version": 1, **asdict(self)}

    def validate(self):
        for values, expected in (
            (self.entities, Entity),
            (self.relationships, Relationship),
            (self.observations, Observation),
        ):
            if (
                not isinstance(values, list)
                or len(values) > 10000
                or any(not isinstance(value, expected) for value in values)
            ):
                raise ValueError(
                    "connector returned invalid or excessive structured records"
                )
        if not isinstance(self.diagnostics, list) or any(
            not isinstance(v, str) for v in self.diagnostics
        ):
            raise ValueError("connector diagnostics must be text")
        try:
            encoded = json.dumps(self.to_dict(), allow_nan=False)
        except (TypeError, ValueError, RecursionError) as exc:
            raise ValueError(
                "connector metadata must be finite JSON-compatible data"
            ) from exc
        if len(encoded.encode("utf-8")) > 4_194_304:
            raise ValueError("connector collection exceeds 4 MiB")
        ids = {e.entity_id for e in self.entities}
        if self.entity.entity_id not in ids:
            raise ValueError("connector omitted input entity")
        relationships = {r.relationship_id for r in self.relationships}
        for relation in self.relationships:
            if relation.subject_id not in ids or relation.object_id not in ids:
                raise ValueError("connector relationship has an unknown entity")
        for observation in self.observations:
            if observation.input_entity_id not in ids or (
                observation.output_entity_id and observation.output_entity_id not in ids
            ):
                raise ValueError("connector observation has an unknown entity")
            if (
                observation.relationship_id
                and observation.relationship_id not in relationships
            ):
                raise ValueError("connector observation has an unknown relationship")
        return self
