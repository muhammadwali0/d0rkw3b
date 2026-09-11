"""Explicit, integrity-checked local registry snapshots. No update server assumed."""
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

from .config import data_directory

MAX_BYTES = 10_485_760


def canonical(providers):
    return json.dumps(providers, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def validate_snapshot(providers, bundled):
    from .registry import validate_provider
    if not isinstance(providers, list):
        raise ValueError('registry snapshot must contain a provider array')
    seen = {}
    for provider in providers:
        validate_provider(provider)
        if provider['id'] in seen:
            raise ValueError('duplicate snapshot provider ID: ' + provider['id'])
        seen[provider['id']] = provider
    for original in bundled:
        updated = seen.get(original['id'])
        if updated is None:
            raise ValueError('snapshot would remove bundled provider: ' + original['id'])
        if (not set(original['target_types']).issubset(updated['target_types']) or
                original['category'] != updated['category'] or original['network'] != updated['network']):
            raise ValueError('snapshot would reduce or change bundled coverage: ' + original['id'])
    return providers


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def snapshot_path(root=None):
    return Path(root if root is not None else data_directory()) / 'registry' / 'current.json'


def read_snapshot(path, bundled):
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('registry snapshot exceeds 10 MiB')
    envelope = json.loads(raw)
    if not isinstance(envelope, dict) or set(envelope) != {'schema_version', 'sha256', 'providers'} or envelope['schema_version'] != 1:
        raise ValueError('invalid snapshot envelope')
    providers = validate_snapshot(envelope['providers'], bundled)
    if hashlib.sha256(canonical(providers)).hexdigest() != envelope['sha256']:
        raise ValueError('snapshot integrity check failed')
    return providers


def active_snapshot(bundled, root=None):
    path = snapshot_path(root)
    if not path.exists():
        return bundled, []
    try:
        return read_snapshot(path, bundled), []
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return bundled, [f'active registry ignored; using bundled definitions: {exc}']


def install_snapshot(source, expected_sha256, bundled, root=None):
    if not re.fullmatch('[a-fA-F0-9]{64}', expected_sha256):
        raise ValueError('supply the expected file SHA-256 as 64 hexadecimal characters')
    with Path(source).expanduser().open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES or hashlib.sha256(raw).hexdigest() != expected_sha256.lower():
        raise ValueError('snapshot file size or SHA-256 verification failed')
    providers = validate_snapshot(json.loads(raw), bundled)
    destination = snapshot_path(root)
    if destination.exists():
        # Only keep a validated previous snapshot, never replace a good rollback
        # with corrupt active state.
        read_snapshot(destination, bundled)
        atomic_write(destination.with_name('previous.json'), destination.read_bytes())
    envelope = {'schema_version': 1, 'sha256': hashlib.sha256(canonical(providers)).hexdigest(), 'providers': providers}
    atomic_write(destination, canonical(envelope))
    return {'providers': len(providers), 'sha256': envelope['sha256'], 'path': str(destination)}


def rollback(bundled, root=None):
    path = snapshot_path(root)
    previous = path.with_name('previous.json')
    if previous.exists():
        read_snapshot(previous, bundled)
        atomic_write(path, previous.read_bytes())
        previous.unlink()
        return 'previous snapshot restored'
    path.unlink(missing_ok=True)
    return 'bundled registry restored'
