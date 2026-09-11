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
