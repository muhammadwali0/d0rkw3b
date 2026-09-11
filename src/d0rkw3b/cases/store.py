"""Transactional SQLite cases. Opening a reader never initializes storage."""
import json
import os
import sqlite3
import uuid
from dataclasses import asdict

from ..core.config import storage_directory
from ..core.entities import now
from ..core.errors import CaseNotFoundError, StorageError
from ..core.validation import clean
from .schema import SCHEMA, SCHEMA_VERSION


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


class CaseStore:
    def __init__(self, root=None, *, writable=False):
        self.root = storage_directory(root)
        self.path = self.root / 'cases.sqlite3'
        self.writable = writable
        self.db = None
        if not self.path.exists() and not writable:
            return
        if writable:
            self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
            if not self.path.exists():
                try:
                    descriptor = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                    os.close(descriptor)
                except FileExistsError:
                    pass
        if self.path.is_symlink():
            raise StorageError('case database must not be a symbolic link')
        try:
            mode = 'rw' if writable else 'ro'
            self.db = sqlite3.connect(self.path.as_uri() + '?mode=' + mode, uri=True, timeout=5)
            self.db.row_factory = sqlite3.Row
            self.db.execute('PRAGMA foreign_keys = ON')
            self.db.execute('PRAGMA trusted_schema = OFF')
            version = self.db.execute('PRAGMA user_version').fetchone()[0]
            if version > SCHEMA_VERSION:
                raise StorageError(f'database schema {version} is newer than supported {SCHEMA_VERSION}')
            if version == 0:
                if not writable:
                    raise StorageError('uninitialized database; use an explicit case write command')
                if self.db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise StorageError('refusing to initialize an unrecognized nonempty database')
                self.db.executescript('BEGIN IMMEDIATE;\n' + SCHEMA + '\nPRAGMA user_version=1;\nCOMMIT;')
        except (sqlite3.Error, StorageError):
            if self.db is not None:
                self.db.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.db is not None:
            self.db.close()

    def _write(self):
        if not self.writable or self.db is None:
            raise StorageError('this case store was opened read-only')

    def list(self):
        if self.db is None:
            return []
        return [dict(row) for row in self.db.execute('SELECT case_id, name, created_at FROM cases ORDER BY name')]

    def case(self, name):
        if self.db is not None:
            row = self.db.execute('SELECT case_id, name, created_at FROM cases WHERE name=?', (name,)).fetchone()
            if row:
                return dict(row)
        raise CaseNotFoundError(f'case not found: {name}; create it with case new')

    def new(self, name):
        self._write()
        name = clean(name)
        if len(name) > 120:
            raise ValueError('case name must be at most 120 characters')
        with self.db:
            try:
                self.db.execute('INSERT INTO cases VALUES (?,?,?)', (uuid.uuid4().hex, name, now()))
            except sqlite3.IntegrityError as exc:
                raise StorageError('case name already exists') from exc
        return self.case(name)

    def _entity(self, case_id, entity):
        self.db.execute('''INSERT INTO entities VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(case_id, entity_id) DO NOTHING''',
            (case_id, entity.entity_id, entity.type, entity.raw_value, entity.normalized_value,
             entity.created_at, encode(entity.metadata)))

    def save(self, name, result, *, method='investigate'):
        self._write()
        case_id = self.case(name)['case_id']
        run_id = uuid.uuid4().hex
        with self.db:
            for entity in result.entities:
                self._entity(case_id, entity)
            self.db.execute('INSERT INTO runs VALUES (?,?,?,?,?)',
                (case_id, run_id, result.entity.entity_id, now(), encode({
                    'method': method, 'raw_input': result.entity.raw_value,
                    'recipe': getattr(result, 'recipe', None), 'diagnostics': result.diagnostics})))
            for relationship in result.relationships:
                r = relationship
                self.db.execute('INSERT INTO relationships VALUES (?,?,?,?,?,?,?,?,?,?)',
                    (case_id, run_id, r.relationship_id, r.subject_id, r.predicate, r.object_id,
                     r.kind, r.observed_at, r.confidence, encode(asdict(r.provenance))))
            for observation in result.observations:
                o = observation
                self.db.execute('INSERT INTO observations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    (case_id, run_id, o.observation_id, o.kind, o.source, o.method, o.input_entity_id,
                     o.output_entity_id, o.relationship_id, o.timestamp, o.confidence,
                     encode(asdict(o.provenance)), encode(o.metadata)))
        return run_id

    def note(self, name, text):
        self._write()
        case_id = self.case(name)['case_id']
        row = {'case_id': case_id, 'note_id': uuid.uuid4().hex, 'text': clean(text), 'created_at': now()}
        with self.db:
            self.db.execute('INSERT INTO notes VALUES (?,?,?,?)', tuple(row.values()))
        return row

    def show(self, name):
        case = self.case(name)
        result = {'schema_version': SCHEMA_VERSION, 'case': case}
        for table, order in [('entities', 'entity_id'), ('runs', 'created_at,run_id'),
                             ('relationships', 'run_id,relationship_id'), ('observations', 'timestamp,run_id,observation_id'),
                             ('notes', 'created_at,note_id'), ('evidence', 'imported_at,evidence_id')]:
            rows = []
            # Table and ordering are fixed application constants, never user input.
            for row in self.db.execute(f'SELECT * FROM {table} WHERE case_id=? ORDER BY {order}', (case['case_id'],)):
                value = dict(row)
                for key in ('metadata', 'provenance'):
                    if key in value:
                        value[key] = json.loads(value[key])
                rows.append(value)
            result[table] = rows
        return result
