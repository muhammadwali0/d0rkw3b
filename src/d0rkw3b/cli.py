"""CLI orchestration; targets stay local unless the user explicitly opens a link."""
import argparse
import csv
import io
import json
import shlex
import sys
import webbrowser

from . import __version__
from .core.config import load_settings
from .core.diagnostics import DEBUG, report_error
from .core.detector import detect
from .core.models import TARGET_TYPES, VARIABLES
from .core.registry import load_registry
from .core.renderer import fields, render
from .core.ranking import rank_providers
from .core.validation import validate


def parser():
    result = argparse.ArgumentParser(description='The Local OSINT Workbench. Queries and investigations are offline; --open and providers health are explicit network actions.',
        epilog='Commands: investigate TARGET | recipes list/info | providers list/health | dev validate-providers/validate-recipes/registry-stats | interactive. Example: d0rkw3b investigate example.com --recipe domain-footprint')
    result.add_argument('target', nargs='*', help='[type] target, or interactive / providers / validate-providers')
    result.add_argument('--verbose', action='store_true', help='diagnostics on stderr')
    result.add_argument('--debug', action='store_true', help='traceback frames on stderr for errors; no locals or chained exceptions')
    result.add_argument('--version', action='version', version=__version__)
    result.add_argument('--type', choices=sorted(TARGET_TYPES | {'ip'}))
    result.add_argument('--pack', help='logical provider group; see packs list')
    result.add_argument('--category', help='filter by category (use providers to list)')
    result.add_argument('--provider', action='append', default=[], help='select exact provider ID; repeatable')
    result.add_argument('--provider-file', action='append', default=[], help='additional JSON provider file or directory')
    result.add_argument('--network', choices=('clearnet', 'tor', 'all'), default='clearnet', help='default: clearnet; Tor links are never automatically opened')
    result.add_argument('--include-disabled', action='store_true', help='include retained reference definitions')
    result.add_argument('--param', action='append', default=[], metavar='NAME=VALUE', help='extra parameter, e.g. year=2024, query=term, username2=other')
    result.add_argument('--format', choices=('text', 'json', 'csv', 'markdown'), default=load_settings()['default_format'])
    result.add_argument('--all', action='store_true', help='show every matching provider (text defaults to top 10; machine formats remain complete)')
    result.add_argument('--open', action='store_true', help='open one explicitly selected clearnet provider in your browser; sends target to provider')
    return result


def output(rows, fmt):
    if fmt == 'json':
        return json.dumps(rows, ensure_ascii=False, indent=2) + '\n'
    if fmt == 'csv':
        stream = io.StringIO(newline='')
        writer = csv.DictWriter(stream, fieldnames=['id', 'name', 'category', 'network', 'status', 'url'])
        writer.writeheader()
        writer.writerows({k: row.get(k, '') for k in writer.fieldnames} for row in rows)
        return stream.getvalue()
    if fmt == 'markdown':
        def cell(value):
            return str(value).replace('|', '&#124;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', ' ')
        return '| Provider | Status | URL |\n|---|---|---|\n' + ''.join(
            f'| {cell(row["name"])} | {cell(row["status"])} | {cell(row["url"])} |\n' for row in rows)
    return ''.join(f'{row["id"]} [{row["status"]}, {row["network"]}]\n  {row["url"]}\n' for row in rows)


def menu_query(category, providers):
    """Expose every legacy function as a discoverable guided action."""
    actions = sorted({p['source'] for p in providers if p['category'] == category})
    for index, action in enumerate(actions, 1):
        print(f'{index}. {action.split(":")[-1].replace("_", " ")}')
    choice = input('Action (0 to return): ').strip()
    if choice == '0':
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(actions):
        raise ValueError('invalid action number')
    action = actions[int(choice) - 1]
    entries = [p for p in providers if p['source'] == action]
    first = entries[0]
    kind = first['target_types'][0]
    if kind in ('ipv4', 'ipv6'):
        kind = 'ip'
    parameters = first['parameters']
    value = input(f'{parameters[0]}: ')
    args = [kind, value, '--category', category]
    for parameter in parameters[1:]:
        args.extend(['--param', f'{parameter}={input(parameter + ": ")}'])
    if any(p['network'] == 'tor' for p in entries):
        network = input('Network (clearnet/tor/all; default clearnet): ').strip() or 'clearnet'
        args.extend(['--network', network])
    for entry in entries:
        args.extend(['--provider', entry['id']])
    main(args)


def interactive():
    print('D0RKW3B — The Local OSINT Workbench. Type help for examples; quit to exit.')
    providers, _ = load_registry()
    categories = sorted({p['category'] for p in providers})
    print('Commands: investigate TARGET, recipes list, providers health --help.')
    print('Choose a category number, or enter a CLI command. No links open automatically.')
    for index, category in enumerate(categories, 1):
        print(f'{index}. {category}')
    while True:
        try:
            line = input('d0rkw3b> ').strip()
            if line in ('quit', 'exit', '0'):
                return 0
            if not line:
                continue
            if line.isdigit():
                if not 1 <= int(line) <= len(categories):
                    raise ValueError('invalid category number')
                menu_query(categories[int(line) - 1], providers)
                continue
            if line == 'help':
                parser().print_help()
                continue
            args = shlex.split(line)
            if args[0] == 'interactive':
                print('Already in interactive mode.')
                continue
            try:
                main(args)
            except SystemExit:
                pass  # argparse errors should not end the session
        except ValueError as exc:
            report_error(exc)
        except (EOFError, KeyboardInterrupt):
            print()
            return 0


def _main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    from .registry_cli import dispatch as registry_dispatch
    managed = registry_dispatch(argv)
    if managed is not None:
        return managed
    from .connectors.cli import dispatch as connector_dispatch
    managed = connector_dispatch(argv)
    if managed is not None:
        return managed
    from .cases.cli import dispatch as case_dispatch
    managed = case_dispatch(argv)
    if managed is not None:
        return managed
    from .workbench_cli import dispatch as workbench_dispatch
    managed = workbench_dispatch(argv)
    if managed is not None:
        return managed
    from .management import dispatch
    managed = dispatch(argv)
    if managed is not None:
        return managed
    cli = parser()
    args = cli.parse_args(argv)
    try:
        if args.target == ['interactive']:
            if not sys.stdin.isatty():
                cli.error('interactive requires a terminal; use direct commands for scripts')
            return interactive()
        providers, errors = load_registry(args.provider_file)
        for error in errors:
            print(f'provider warning: {error}', file=sys.stderr)
        if args.target == ['validate-providers']:
            if args.format == 'json':
                print(json.dumps({'providers': len(providers), 'errors': errors}, indent=2))
            else:
                print(f'{len(providers)} valid providers; {len(errors)} errors')
            return 1 if errors else 0
        selected = set(args.provider)
        unknown = selected - {p['id'] for p in providers}
        if unknown:
            raise ValueError('unknown provider IDs: ' + ', '.join(sorted(unknown)))
        if args.category and args.category not in {p['category'] for p in providers}:
            raise ValueError('unknown category: ' + args.category)
        from .core.packs import in_pack, packs
        if args.pack and args.pack not in {p['id'] for p in packs(providers)}:
            raise ValueError('unknown pack: ' + args.pack)
        providers = [p for p in rank_providers(providers) if (not selected or p['id'] in selected)
                     and (not args.category or p['category'] == args.category)
                     and (not args.pack or in_pack(p, args.pack))
                     and (args.network == 'all' or p['network'] == args.network)
                     and (args.include_disabled or (p['enabled'] and p['status'] not in ('disabled', 'broken', 'deprecated')))]
        if args.target == ['providers']:
            if args.format == 'json':
                print(json.dumps(providers, ensure_ascii=False, indent=2))
            else:
                print(output([dict(p, url=p['template']) for p in providers], args.format), end='')
            return 0
        parts = args.target
        kind = args.type
        if len(parts) >= 2 and parts[0] in TARGET_TYPES | {'ip'}:
            if kind and kind != parts[0]:
                raise ValueError('positional type conflicts with --type')
            kind, parts = parts[0], parts[1:]
        if not parts:
            cli.error('provide a target or use interactive')
        value = ' '.join(parts)
        target = validate(value, kind) if kind else detect(value)
        extras = {}
        for parameter in args.param:
            key, separator, value = parameter.partition('=')
            if not separator or key not in VARIABLES - {'next_year', target.variable} or key in extras:
                raise ValueError(f'invalid or duplicate extra parameter: {key}')
            if key in ('username2', 'username'):
                value = validate(value, 'username').value
            extras[key] = value
        rows = []
        for provider in providers:
            if target.type not in provider['target_types']:
                continue
            needed = fields(provider['template']) - {target.variable} - extras.keys()
            if 'year' in extras:
                needed.discard('next_year')
            if needed and not selected:
                continue
            try:
                url = render(provider, target, extras)
            except ValueError as exc:
                if selected:
                    raise ValueError(f'{provider["id"]}: {exc}') from exc
                print(f'provider skipped: {provider["id"]}: {exc}', file=sys.stderr)
                continue
            rows.append({k: provider[k] for k in ('id', 'name', 'category', 'network', 'status')} | {'url': url})
        if not rows:
            raise ValueError('no matching providers; check type, filters and required parameters')
        if args.open:
            if len(selected) != 1 or len(rows) != 1:
                raise ValueError('--open requires exactly one --provider and one matching link')
            provider = next(p for p in providers if p['id'] == rows[0]['id'])
            if provider['network'] == 'tor':
                raise ValueError('Tor links must be copied into a separately configured Tor Browser; automatic opening is disabled')
            if not provider['enabled'] or provider['requires_api_key']:
                raise ValueError('disabled/reference providers cannot be automatically opened')
            if not webbrowser.open(rows[0]['url'], new=2):
                raise ValueError('browser could not be opened')
        if args.format == 'text' and not args.all and not selected and len(rows) > 10:
            print(f'{len(rows) - 10} additional providers available with --all', file=sys.stderr)
            rows = rows[:10]
        print(output(rows, args.format), end='')
        return 0
    except BrokenPipeError:
        return 0
    except (ValueError, OSError) as exc:
        report_error(exc)
        return 2
    except KeyboardInterrupt:
        return 130


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    # Only actual options before the -- delimiter are interpreted globally.
    boundary = argv.index('--') if '--' in argv else len(argv)
    prefix, suffix = argv[:boundary], argv[boundary:]
    debug, verbose = '--debug' in prefix, '--verbose' in prefix
    argv = [v for v in prefix if v not in ('--debug', '--verbose')] + suffix
    token = DEBUG.set(debug)
    try:
        if verbose:
            print('D0RKW3B: command dispatch; targets and credentials are omitted from diagnostic logs.', file=sys.stderr)
        return _main(argv)
    except BrokenPipeError:
        return 0
    except (ValueError, OSError) as exc:
        report_error(exc)
        return 2
    except KeyboardInterrupt:
        return 130
    finally:
        DEBUG.reset(token)
