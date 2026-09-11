"""SQLite schema version 1. Fresh initialization is atomic; future schemas fail closed."""
SCHEMA_VERSION = 1

SCHEMA = '''
CREATE TABLE cases (
    case_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK(length(name) BETWEEN 1 AND 120),
    created_at TEXT NOT NULL
);
CREATE TABLE entities (
    case_id TEXT NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    entity_id TEXT NOT NULL,
    type TEXT NOT NULL,
    raw_value TEXT NOT NULL,
    normalized_value TEXT NOT NULL,
    created_at TEXT NOT NULL,
    metadata TEXT NOT NULL,
    PRIMARY KEY(case_id, entity_id),
    UNIQUE(case_id, type, normalized_value)
);
CREATE TABLE runs (
    case_id TEXT NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    run_id TEXT NOT NULL,
    input_entity_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    metadata TEXT NOT NULL,
    PRIMARY KEY(case_id, run_id),
    FOREIGN KEY(case_id, input_entity_id) REFERENCES entities(case_id, entity_id)
);
CREATE TABLE relationships (
    case_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    relationship_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object_id TEXT NOT NULL,
    kind TEXT NOT NULL CHECK(kind IN ('observed','inferred','manually-added')),
    observed_at TEXT NOT NULL,
    confidence TEXT NOT NULL CHECK(confidence IN ('low','medium','high')),
    provenance TEXT NOT NULL,
    PRIMARY KEY(case_id, run_id, relationship_id),
    FOREIGN KEY(case_id, run_id) REFERENCES runs(case_id, run_id) ON DELETE CASCADE,
    FOREIGN KEY(case_id, subject_id) REFERENCES entities(case_id, entity_id),
    FOREIGN KEY(case_id, object_id) REFERENCES entities(case_id, entity_id)
);
CREATE TABLE observations (
    case_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    observation_id TEXT NOT NULL,
    kind TEXT NOT NULL CHECK(kind IN ('generated_query','observed','imported','manually-added')),
    source TEXT NOT NULL,
    method TEXT NOT NULL,
    input_entity_id TEXT NOT NULL,
    output_entity_id TEXT,
    relationship_id TEXT,
    timestamp TEXT NOT NULL,
    confidence TEXT NOT NULL,
    provenance TEXT NOT NULL,
    metadata TEXT NOT NULL,
    PRIMARY KEY(case_id, run_id, observation_id),
    FOREIGN KEY(case_id, run_id) REFERENCES runs(case_id, run_id) ON DELETE CASCADE,
    FOREIGN KEY(case_id, input_entity_id) REFERENCES entities(case_id, entity_id),
    FOREIGN KEY(case_id, output_entity_id) REFERENCES entities(case_id, entity_id),
    FOREIGN KEY(case_id, run_id, relationship_id) REFERENCES relationships(case_id, run_id, relationship_id),
    CHECK(kind != 'generated_query' OR (confidence = 'unverified' AND output_entity_id IS NULL AND relationship_id IS NULL))
);
CREATE TABLE notes (
    case_id TEXT NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    note_id TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(case_id, note_id)
);
CREATE TABLE evidence (
    case_id TEXT NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    evidence_id TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    original_path TEXT NOT NULL,
    stored_path TEXT NOT NULL UNIQUE,
    mime_type TEXT NOT NULL,
    size INTEGER NOT NULL CHECK(size >= 0),
    sha256 TEXT NOT NULL CHECK(length(sha256) = 64),
    imported_at TEXT NOT NULL,
    provenance TEXT NOT NULL,
    PRIMARY KEY(case_id, evidence_id),
    FOREIGN KEY(case_id, entity_id) REFERENCES entities(case_id, entity_id)
);
CREATE INDEX runs_input ON runs(case_id, input_entity_id);
CREATE INDEX relationships_subject ON relationships(case_id, subject_id);
CREATE INDEX relationships_object ON relationships(case_id, object_id);
CREATE INDEX observations_input ON observations(case_id, input_entity_id);
CREATE INDEX observations_output ON observations(case_id, output_entity_id);
CREATE INDEX observations_relationship ON observations(case_id, run_id, relationship_id);
CREATE INDEX evidence_entity ON evidence(case_id, entity_id);
CREATE INDEX observations_time ON observations(case_id, timestamp);
'''
