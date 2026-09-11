import json
import re
from datetime import date
from importlib.resources import files
from pathlib import Path
from urllib.parse import urlsplit

from .models import TARGET_TYPES, VARIABLES
from .renderer import fields

REQUIRED = {'id', 'name', 'target_types', 'category', 'description', 'template',
            'tags', 'network', 'auth', 'requires_api_key', 'homepage', 'enabled',
            'status', 'last_verified', 'notes', 'source', 'parameters'}


def validate_provider(item):
    if not isinstance(item, dict):
        raise ValueError('provider must be an object')
    missing = REQUIRED - item.keys()
    if missing:
        raise ValueError('missing fields: ' + ', '.join(sorted(missing)))
    if item.keys() - REQUIRED:
        raise ValueError('unknown fields: ' + ', '.join(sorted(item.keys() - REQUIRED)))
    for key in ('id', 'name', 'category', 'description', 'template', 'homepage', 'notes', 'source'):
        if not isinstance(item[key], str) or not item[key].strip():
            raise ValueError(f'{key} must be a nonempty string')
        if any(ord(c) < 32 or ord(c) == 127 for c in item[key]):
            raise ValueError(f'{key} contains control characters')
    if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', item['id']):
        raise ValueError('id must contain lowercase letters/digits separated by hyphens')
    for key, allowed in (('target_types', TARGET_TYPES), ('parameters', VARIABLES)):
        if not isinstance(item[key], list) or not item[key] or any(not isinstance(v, str) or v not in allowed for v in item[key]):
            raise ValueError(f'invalid {key}')
    if not isinstance(item['tags'], list) or any(not isinstance(v, str) for v in item['tags']):
        raise ValueError('tags must be a list of strings')
    for key in ('enabled', 'requires_api_key'):
        if type(item[key]) is not bool:
            raise ValueError(f'{key} must be boolean')
    for key, allowed in (('network', {'clearnet', 'tor'}), ('auth', {'none', 'unknown', 'may_require', 'required'}),
                         ('status', {'active', 'unverified', 'deprecated', 'broken', 'disabled'})):
        if item[key] not in allowed:
            raise ValueError(f'invalid {key}')
    if item['last_verified'] is not None:
        date.fromisoformat(item['last_verified'])
    used = fields(item['template'])
    if used - VARIABLES:
        raise ValueError('unsupported variables: ' + ', '.join(sorted(used - VARIABLES)))
    if used - set(item['parameters']) - {'next_year'}:
        raise ValueError('template variables must be declared in parameters')
    for key in ('template', 'homepage'):
        parts = urlsplit(item[key])
        if parts.scheme not in ('https', 'http') or not parts.hostname or parts.username is not None or parts.password is not None:
            raise ValueError(f'{key} must be an http(s) URL without credentials')
        parts.port
        if re.search(r'\s|\\', item[key]):
            raise ValueError(f'{key} contains whitespace or backslashes')
        if ((parts.hostname or '').endswith('.onion')) != (item['network'] == 'tor'):
            raise ValueError(f'{key} network does not match hostname')
    return item


def load_registry(extra_paths=()):
    providers, errors, seen = [], [], set()
    sources = sorted(files('d0rkw3b').joinpath('providers').iterdir(), key=lambda p: p.name)
    for path in extra_paths:
        path = Path(path)
        sources.extend(sorted(path.glob('*.json')) if path.is_dir() else [path])
    for source in sources:
        if not source.name.endswith('.json'):
            continue
        try:
            items = json.loads(source.read_text(encoding='utf-8'))
            if not isinstance(items, list):
                raise ValueError('file must contain a list of providers')
        except (OSError, ValueError) as exc:
            errors.append(f'{source}: {exc}')
            continue
        for index, item in enumerate(items):
            try:
                validate_provider(item)
                if item['id'] in seen:
                    raise ValueError(f'duplicate provider ID: {item["id"]}')
                seen.add(item['id'])
                providers.append(item)
            except (ValueError, TypeError, KeyError) as exc:
                errors.append(f'{source}[{index}]: {exc}')
    return sorted(providers, key=lambda p: p['id']), errors
