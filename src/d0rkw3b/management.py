"""Provider maintenance commands, separate from ordinary offline query startup."""
import argparse
import json
import sys
from collections import Counter

from .core.health import check_providers
from .core.registry import load_registry


def dispatch(argv):
    if argv[:2] == ['providers', 'list']:
        from .cli import main
        return main(['providers', *argv[2:]])
    if argv[:2] == ['dev', 'validate-providers']:
        from .cli import main
        return main(['validate-providers', *argv[2:]])
    if argv[:2] not in (['providers', 'health'], ['dev', 'registry-stats']):
        return None
    health = argv[0] == 'providers'
    parser = argparse.ArgumentParser(prog='d0rkw3b ' + ' '.join(argv[:2]), description=(
        'Explicit public homepage HEAD checks. No targets, redirects, retries or Tor probes. '
        'Reachability is not semantic verification.' if health else 'Offline registry counts.'))
    parser.add_argument('--provider-file', action='append', default=[])
    parser.add_argument('--format', choices=('text', 'json'), default='text')
    if health:
        parser.add_argument('--provider', action='append', default=[])
        parser.add_argument('--max-requests', type=int, default=10, help='unique hosts, 1–100 (default 10)')
        parser.add_argument('--timeout', type=float, default=5, help='socket timeout, seconds; OS controls DNS timeout')
        parser.add_argument('--delay', type=float, default=0.5, help='seconds between requests, minimum 0.25')
    args = parser.parse_args(argv[2:])
    try:
        providers, errors = load_registry(args.provider_file)
        for error in errors:
            print(f'provider warning: {error}', file=sys.stderr)
        if health:
            selected = set(args.provider)
            if selected - {p['id'] for p in providers}:
                raise ValueError('unknown provider ID')
            if selected:
                providers = [p for p in providers if p['id'] in selected]
            result = check_providers(providers, max_requests=args.max_requests,
                                     timeout=args.timeout, delay=args.delay)
            result['registry_errors'] = errors
            if args.format == 'json':
                print(json.dumps(result, indent=2))
            else:
                print(f'{result["request_count"]} request attempts; no semantic verification performed')
                for row in result['results']:
                    print(f'{row["id"]}: {row["health"]} (semantic: {row["semantic_status"]})')
        else:
            result = {'total': len(providers), 'errors': errors,
                      **{key: dict(sorted(Counter(str(p[key]) for p in providers).items()))
                         for key in ('category', 'network', 'status', 'auth', 'enabled')},
                      'target_types': dict(sorted(Counter(t for p in providers for t in p['target_types']).items()))}
            print(json.dumps(result, indent=2))
        return 1 if errors else 0
    except (ValueError, OSError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2
