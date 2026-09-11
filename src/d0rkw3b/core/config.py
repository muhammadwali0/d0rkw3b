"""Platform-local paths. Merely asking for a path does not create it."""
import os
import sys
from pathlib import Path


def data_directory():
    override = os.environ.get('D0RKW3B_DATA_DIR')
    if override:
        return Path(override).expanduser().resolve()
    if sys.platform == 'win32':
        return Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'D0RKW3B'
    if sys.platform == 'darwin':
        return Path.home() / 'Library' / 'Application Support' / 'D0RKW3B'
    base = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
    if not base.is_absolute():
        base = Path.home() / '.local' / 'share'
    return base / 'd0rkw3b'


def storage_directory(root=None):
    path = Path(root if root is not None else data_directory()).expanduser().resolve()
    if any((parent / '.git').exists() for parent in (path, *path.parents)):
        raise ValueError('case storage must be outside a source repository')
    return path


def config_directory():
    if sys.platform == 'win32':
        return Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'D0RKW3B'
    if sys.platform == 'darwin':
        return Path.home() / 'Library' / 'Application Support' / 'D0RKW3B'
    base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
    return (base if base.is_absolute() else Path.home() / '.config') / 'd0rkw3b'


def load_settings():
    import json
    import re
    path = Path(os.environ.get('D0RKW3B_CONFIG', config_directory() / 'config.json')).expanduser()
    if not path.exists():
        return {'default_format': 'text', 'disabled_providers': [], 'disabled_connectors': []}
    with path.open('rb') as stream:
        raw = stream.read(65537)
    if len(raw) > 65536:
        raise ValueError('configuration exceeds 64 KiB')
    config = json.loads(raw)
    if not isinstance(config, dict) or set(config) - {'default_format', 'disabled_providers', 'disabled_connectors'}:
        raise ValueError('configuration supports default_format, disabled_providers and disabled_connectors only')
    if config.get('default_format', 'text') not in ('text', 'json', 'csv', 'markdown'):
        raise ValueError('invalid configured output format')
    for key in ('disabled_providers', 'disabled_connectors'):
        if not isinstance(config.get(key, []), list) or any(not isinstance(v, str) or not re.fullmatch('[a-z0-9-]+', v) for v in config.get(key, [])):
            raise ValueError(f'{key} must be an array of IDs')
    return {'default_format': 'text', 'disabled_providers': [], 'disabled_connectors': [], **config}
