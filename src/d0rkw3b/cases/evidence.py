"""Explicit byte-preserving evidence acquisition into a case."""
import os
import tempfile
import uuid
from dataclasses import asdict
from pathlib import Path

from ..core.entities import Entity, Provenance, now
from ..core.errors import EvidenceError
from ..localfiles import inspect_stream, open_regular
from .store import encode


def add_evidence(store, case_name, path):
    store._write()
    case_id = store.case(case_name)['case_id']
    directory = store.root / 'evidence' / case_id
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    if directory.resolve() != directory or not directory.is_relative_to(store.root):
        raise EvidenceError('evidence storage must not traverse symbolic links')
    source, stream = open_regular(path)
    evidence_id = uuid.uuid4().hex
    destination = directory / evidence_id
    temporary = None
    copied = False
    try:
        with stream, tempfile.NamedTemporaryFile(dir=directory, delete=False) as output:
            temporary = Path(output.name)
            metadata = inspect_stream(stream, source, copy_to=output)
            output.flush()
            os.fsync(output.fileno())
        # A unique generated name avoids interpreting any original filename as a path.
        os.replace(temporary, destination)
        copied = True
        collected = now()
        entity = Entity.create(str(source), 'file', created_at=collected)
        provenance = Provenance('local-file', 'byte-preserving import and SHA-256',
                                evidence_id, collected, notes='Explicit local import; no upload.')
        row = {'case_id': case_id, 'evidence_id': evidence_id, 'entity_id': entity.entity_id,
               'original_filename': Path(path).name, 'original_path': str(source),
               'stored_path': str(destination.relative_to(store.root)),
               'mime_type': metadata['mime_type'], 'size': metadata['size'],
               'sha256': metadata['sha256'], 'imported_at': collected,
               'provenance': asdict(provenance)}
        with store.db:
            store._entity(case_id, entity)
            store.db.execute('INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                tuple(encode(v) if k == 'provenance' else v for k, v in row.items()))
        return row
    except BaseException:
        if copied:
            destination.unlink(missing_ok=True)
        raise
    finally:
        stream.close()
        if temporary is not None:
            temporary.unlink(missing_ok=True)
