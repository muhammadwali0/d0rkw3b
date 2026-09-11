"""One-time inventory extractor for the audited 9e49913 provider modules.

Reads the baseline from git so it remains reproducible after legacy removal.
Executes only the previously audited pure URL functions, never main.py.
"""
import ast
import inspect
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MODULES = 'communities documents domain emailaddresses facebook github images instagram ipaddresses linkedin search_links usernames videos x'.split()
PARAMETERS = {
    'term': 'query', 'search_terms': 'query', 'username': 'username',
    'username1': 'username', 'username2': 'username2', 'email': 'email',
    'domain': 'domain', 'ip': 'ip', 'image_url': 'url', 'post_url': 'url',
    'video_id': 'video_id', 'year': 'year', 'number': 'phone',
    'user_id': 'user_id', 'location_id': 'location_id', 'list_id': 'list_id',
    'real_name': 'query', 'repo_name': 'repository', 'company_name': 'company',
}


def leaves(value, path=()):
    if isinstance(value, tuple):
        for label, item in zip(('clearnet', 'tor'), value):
            yield from leaves(item, path + (label,))
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from leaves(item, path + (key,))
    else:
        yield path, value


def build():
    inventory, providers = [], []
    for module in MODULES:
        source = subprocess.check_output(['git', 'show', f'9e49913:{module}.py'], cwd=ROOT, text=True)
        tree = ast.parse(source)
        tree.body = [node for node in tree.body if not (isinstance(node, ast.Import) and any(a.name == 'requests' for a in node.names))]
        scope = {'__name__': module}
        exec(compile(tree, module + '.py', 'exec'), scope)
        for name, func in scope.items():
            if not inspect.isfunction(func) or func.__module__ != module:
                continue
            variables = [PARAMETERS[p] for p in inspect.signature(func).parameters]
            markers = {v: f'D0RKMARKER{v.upper()}END' for v in variables}
            for path, raw in leaves(func(*(markers[v] for v in variables))):
                identifier = re.sub('[^a-z0-9]+', '-', '-'.join((module, name, *path)).lower()).strip('-')
                # No source credential is copied into inventory or registry.
                raw = re.sub(r'([?&]key=)[^&#]+', r'\1', raw)
                template = raw.replace('{', '{{').replace('}', '}}')
                for variable, marker in markers.items():
                    template = template.replace(marker, '{' + variable + '}')
                notes = ['Migrated from legacy code; endpoint availability has not been verified.']
                enabled = True
                needs_key = 'key=' in raw and 'googleapis.com' in raw
                if needs_key:
                    enabled = False
                    notes.append('Requires an owner-supplied API key; bundled credential removed. Endpoint retained for reference only.')
                if 'graphql/query/' in raw:
                    enabled = False
                    notes.append('Undocumented authenticated GraphQL query hash; retained for reference only.')
                if any(token in raw for token in ('/portscan/', '/traceroute/', 'ssltest/analyze')):
                    enabled = False
                    notes.append('Visiting this launcher can initiate a remote probe; disabled by default.')
                if 'wigle.net' in raw:
                    enabled = False
                    notes.append('Legacy IP input was used as an SSID or postal code; questionable mapping.')
                if module == 'images' and path[-1] == 'Google Images' and 'image_keyword' in name:
                    template = 'https://www.google.com/search?q={query}&udm=2'
                    notes.append('Removed copied tracking and session parameters.')
                if name == 'x_username_by_year':
                    template = template.replace('until%3A{year}-12-31', 'until%3A{next_year}-01-01')
                    notes.append('Exclusive end date corrected to January 1 of the following year.')
                target = variables[0]
                target = 'search' if target == 'query' else target
                if module == 'documents':
                    target = 'document'
                types = ['ipv4', 'ipv6'] if target == 'ip' else [target]
                if 'ipaddress.com/ipv4/' in raw:
                    types = ['ipv4']
                network = 'tor' if (urlsplit(raw).hostname or '').endswith('.onion') else 'clearnet'
                auth = 'unknown'
                if any(host in raw for host in ('facebook.com/', 'instagram.com/', 'linkedin.com/', 'dehashed.com/')):
                    auth = 'may_require'
                record = dict(id=identifier, name=' / '.join(path), target_types=types,
                              category=module, description=f'{module}: {" / ".join(path)}',
                              template=template, tags=[name], network=network, auth=auth,
                              requires_api_key=needs_key, homepage=f'{urlsplit(raw).scheme}://{urlsplit(raw).netloc}/'.replace('D0RKMARKERUSERNAMEEND.', ''),
                              enabled=enabled, status='unverified', last_verified=None,
                              notes=' '.join(notes), source=f'{module}.py:{name}',
                              parameters=variables)
                providers.append(record)
                inventory.append(dict(id=identifier, source=record['source'], legacy_path=list(path),
                                      legacy_template=raw.replace('D0RKMARKER', 'MIGRATION_'),
                                      target_types=types, changes=notes[1:]))
    assert len({p['id'] for p in providers}) == len(providers)
    (ROOT / 'docs/migration-inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
    for module in MODULES:
        (ROOT / f'src/d0rkw3b/providers/{module}.json').write_text(json.dumps([p for p in providers if p['category'] == module], indent=2) + '\n')
    print(f'Inventoried {len(providers)} URLs from {len(set(p["source"] for p in providers))} functions across {len(MODULES)} modules.')


if __name__ == '__main__':
    build()
