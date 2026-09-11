"""Stable identity and explicit provenance shared by investigations and cases."""

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from .detector import detect
from .validation import validate


def now():
    return datetime.now(timezone.utc).isoformat()


def identifier(namespace, *values):
    encoded = json.dumps(
        values, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return namespace + "_" + hashlib.sha256(encoded).hexdigest()


def required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")


def timestamp(value, label):
    required_text(value, label)
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"{label} requires a timezone")


@dataclass(frozen=True)
class Entity:
    entity_id: str
    type: str
    raw_value: str
    normalized_value: str
    created_at: str
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        target = validate(self.normalized_value, self.type)
        if target.value != self.normalized_value or self.entity_id != identifier(
            "entity", self.type, self.normalized_value
        ):
            raise ValueError("entity identity must match its normalized type and value")
        required_text(self.raw_value, "raw_value")
        timestamp(self.created_at, "created_at")
        if not isinstance(self.metadata, dict):
            raise ValueError("entity metadata must be an object")

    @classmethod
    def create(cls, value, kind=None, *, created_at=None, metadata=None):
        target = validate(value, kind) if kind else detect(value)
        return cls(
            identifier("entity", target.type, target.value),
            target.type,
            value,
            target.value,
            created_at or now(),
            dict(metadata or {}),
        )

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Provenance:
    source: str
    method: str
    reference: str
    collected_at: str
    source_url: str | None = None
    notes: str = ""

    def __post_init__(self):
        for key in ("source", "method", "reference", "collected_at"):
            required_text(getattr(self, key), key)
        timestamp(self.collected_at, "collected_at")


RELATIONSHIPS = frozenset(
    (
        "uses_domain",
        "resolves_to",
        "uses_nameserver",
        "belongs_to",
        "has_profile",
        "owns",
        "references",
        "has_hash",
    )
)


@dataclass(frozen=True)
class Relationship:
    relationship_id: str
    subject_id: str
    predicate: str
    object_id: str
    kind: str
    observed_at: str
    confidence: str
    provenance: Provenance

    def __post_init__(self):
        if self.predicate not in RELATIONSHIPS:
            raise ValueError("unsupported relationship predicate")
        if self.kind not in ("observed", "inferred", "manually-added"):
            raise ValueError("relationship kind must be explicit")
        if self.confidence not in ("low", "medium", "high"):
            raise ValueError("confidence must be low, medium or high")
        for key in ("subject_id", "object_id", "observed_at"):
            required_text(getattr(self, key), key)
        timestamp(self.observed_at, "observed_at")
        if not isinstance(self.provenance, Provenance):
            raise ValueError("relationship requires provenance")

    @classmethod
    def create(
        cls,
        subject,
        predicate,
        object_,
        *,
        provenance,
        kind="observed",
        confidence="high",
        observed_at=None,
    ):
        return cls(
            identifier(
                "relationship",
                subject.entity_id,
                predicate,
                object_.entity_id,
                provenance.reference,
                kind,
            ),
            subject.entity_id,
            predicate,
            object_.entity_id,
            kind,
            observed_at or provenance.collected_at,
            confidence,
            provenance,
        )

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Observation:
    observation_id: str
    kind: str
    source: str
    method: str
    input_entity_id: str
    timestamp: str
    provenance: Provenance
    output_entity_id: str | None = None
    relationship_id: str | None = None
    confidence: str = "unverified"
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        for key in ("observation_id", "source", "method", "input_entity_id"):
            required_text(getattr(self, key), key)
        timestamp(self.timestamp, "timestamp")
        if not isinstance(self.metadata, dict):
            raise ValueError("observation metadata must be an object")
        if self.kind not in (
            "generated_query",
            "observed",
            "imported",
            "manually-added",
        ):
            raise ValueError("unsupported observation kind")
        if not isinstance(self.provenance, Provenance):
            raise ValueError("observation requires provenance")
        if self.kind == "generated_query" and (
            self.confidence != "unverified"
            or self.output_entity_id
            or self.relationship_id
        ):
            raise ValueError("a generated query is not a finding or relationship")
        if self.confidence not in ("unverified", "low", "medium", "high"):
            raise ValueError("unsupported observation confidence")

    def to_dict(self):
        return asdict(self)
