"""Declarative methodology; no executable recipe steps."""
import json
import re
from importlib.resources import files
from pathlib import Path

from .models import TARGET_TYPES


def validate_recipe(recipe, providers):
    required = {'id', 'name', 'description', 'target_types', 'stages'}
    if not isinstance(recipe, dict) or set(recipe) != required:
        raise ValueError('recipe requires exactly id, name, description, target_types and stages')
    for key in ('id', 'name', 'description'):
        if not isinstance(recipe[key], str) or not recipe[key].strip():
            raise ValueError(f'recipe {key} must be nonempty text')
    if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', recipe['id']):
        raise ValueError('invalid recipe ID')
    types = recipe['target_types']
    if not isinstance(types, list) or not types or any(not isinstance(t, str) or t not in TARGET_TYPES for t in types):
        raise ValueError('recipe has unsupported target types')
    if not isinstance(recipe['stages'], list) or not recipe['stages']:
        raise ValueError('recipe requires stages')
    registry = {p['id']: p for p in providers}
    stage_ids = set()
    for stage in recipe['stages']:
        if not isinstance(stage, dict) or set(stage) != {'name', 'description', 'providers'}:
            raise ValueError('stage requires name, description and providers')
        if any(not isinstance(stage[k], str) or not stage[k].strip() for k in ('name', 'description')):
            raise ValueError('stage name and description must be text')
        if stage['name'] in stage_ids:
            raise ValueError('duplicate stage name')
        stage_ids.add(stage['name'])
        if not isinstance(stage['providers'], list) or not stage['providers']:
            raise ValueError('stage requires provider IDs')
        for key in stage['providers']:
            if not isinstance(key, str) or key not in registry:
                raise ValueError(f'unknown recipe provider: {key}')
            if not set(types).issubset(registry[key]['target_types']):
                raise ValueError(f'provider {key} does not accept every recipe target type')
    return recipe


def load_recipes(providers, extra_paths=()):
    sources = sorted(files('d0rkw3b').joinpath('recipes').iterdir(), key=lambda p: p.name)
    sources.extend(Path(p) for p in extra_paths)
    recipes, errors, seen = [], [], set()
    for source in sources:
        if not source.name.endswith('.json'):
            continue
        try:
            recipe = validate_recipe(json.loads(source.read_text(encoding='utf-8')), providers)
            if recipe['id'] in seen:
                raise ValueError('duplicate recipe ID: ' + recipe['id'])
            recipes.append(recipe)
            seen.add(recipe['id'])
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f'{source}: {exc}')
    return sorted(recipes, key=lambda r: r['id']), errors
