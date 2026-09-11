"""Static manifests first; installed entry-point code loads only on explicit execution."""
import json
import os
from importlib.metadata import entry_points

from ..core.errors import ConnectorPermissionError, ConnectorUnavailableError
from .builtin import MANIFESTS, RUNNERS
from .integrations import EXIFTOOL, exiftool
from .models import Capabilities, Collection, Manifest


def discover_plugins():
    plugins, errors = {}, []
    for entry in entry_points(group='d0rkw3b.connectors'):
        try:
            if entry.name in MANIFESTS or entry.name == 'exiftool' or entry.name in plugins:
                raise ValueError('duplicate or reserved connector ID')
            distribution = entry.dist
            paths = [p for p in (distribution.files or ()) if p.name == 'd0rkw3b-plugin.json']
            if len(paths) != 1:
                raise ValueError('plugin distribution must include exactly one d0rkw3b-plugin.json')
            path = distribution.locate_file(paths[0])
            if path.stat().st_size > 65536:
                raise ValueError('plugin manifest exceeds 64 KiB')
            document = json.loads(path.read_text(encoding='utf-8'))
            if set(document) != {'api_version', 'connectors'} or document['api_version'] != 1:
                raise ValueError('unsupported plugin manifest API')
            item = document['connectors'][entry.name]
            capabilities = Capabilities(**item['capabilities'])
            if (not isinstance(capabilities.network, list) or any(not isinstance(v, str) or not v for v in capabilities.network)
                    or type(capabilities.filesystem_read) is not bool or type(capabilities.subprocess) is not bool):
                raise ValueError('invalid plugin capability declarations')
            capabilities = Capabilities(tuple(capabilities.network), capabilities.filesystem_read, capabilities.subprocess)
            arguments = dict(item, capabilities=capabilities)
            for key in ('accepted_types', 'produced_types', 'required_keys', 'optional_keys'):
                arguments[key] = tuple(arguments.get(key, ()))
            manifest = Manifest(**arguments)
            if manifest.id != entry.name:
                raise ValueError('entry point and manifest IDs do not match')
            plugins[entry.name] = (manifest, entry)
        except (ValueError, TypeError, KeyError, OSError, AttributeError) as exc:
            errors.append(f'{entry.name}: {exc}')
    return plugins, errors


def manifests():
    plugins, errors = discover_plugins()
    result = [*MANIFESTS.values(), EXIFTOOL, *(item[0] for item in plugins.values())]
    return sorted(result, key=lambda m: m.id), errors


def collect(entity, connector_id, *, disclose=None, timeout=None):
    """Execute exactly one requested connector. Capability declarations are not a sandbox."""
    plugins = {}
    if connector_id not in MANIFESTS and connector_id != 'exiftool':
        plugins, errors = discover_plugins()
        if connector_id not in plugins:
            detail = '; '.join(errors) if errors else 'use connectors to list available IDs'
            raise ConnectorUnavailableError(f'connector unavailable: {connector_id}; {detail}')
    manifest = (MANIFESTS.get(connector_id) or
                (EXIFTOOL if connector_id == 'exiftool' else plugins[connector_id][0]))
    if entity.type not in manifest.accepted_types:
        raise ConnectorUnavailableError(f'{connector_id} does not accept {entity.type}')
    missing = [name for name in manifest.required_keys if not os.environ.get(name)]
    if missing:
        raise ConnectorPermissionError('required credential environment variables are absent: ' + ', '.join(missing))
    limit = manifest.timeout_seconds if timeout is None else timeout
    if not isinstance(limit, (int, float)) or not 0 < limit <= 60:
        raise ValueError('connector timeout must be greater than zero and at most 60 seconds')
    if disclose is not None:
        disclose(manifest, entity)
    runner = RUNNERS.get(connector_id)
    if connector_id == 'exiftool':
        runner = exiftool
    elif runner is None:
        # Importing the plugin is itself executable behavior, deliberately delayed
        # until after its packaged static capabilities have been shown.
        try:
            runner = plugins[connector_id][1].load()
        except Exception as exc:
            raise ConnectorUnavailableError(f'plugin {connector_id} could not load ({type(exc).__name__})') from exc
    if connector_id in plugins:
        try:
            result = runner(entity, timeout=limit)
        except Exception as exc:
            raise ConnectorUnavailableError(f'plugin {connector_id} failed ({type(exc).__name__}); its message is suppressed to avoid leaking secrets') from exc
    else:
        result = runner(entity, timeout=limit)
    if not isinstance(result, Collection) or result.entity.entity_id != entity.entity_id:
        raise ConnectorUnavailableError('connector returned an invalid collection or changed the input entity')
    return result.validate()
