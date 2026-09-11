"""Local case commands; shared by direct and interactive interfaces."""
import argparse
import json
import sqlite3
import sys

from ..investigation import investigate
from .evidence import add_evidence
from .exports import export_data, graph, timeline
from .store import CaseStore


def dispatch(argv):
    if not argv or argv[0] not in ('case', 'evidence'):
        return None
    parser = argparse.ArgumentParser(prog='d0rkw3b ' + argv[0], description='Explicit local case and evidence storage. No network access.')
    parser.add_argument('action', choices=(('new', 'list', 'show', 'add', 'note', 'export', 'graph', 'timeline') if argv[0] == 'case' else ('add',)))
    parser.add_argument('name', nargs='?', help='case name')
    parser.add_argument('value', nargs='?', help='target, note text or evidence path')
    parser.add_argument('--type')
    parser.add_argument('--format', choices=('text', 'json', 'jsonl', 'csv', 'markdown', 'graphml', 'gexf'), default='json')
    args = parser.parse_args(argv[1:])
    if args.action != 'list' and not args.name:
        parser.error('a case name is required')
    if args.action in ('add', 'note') and args.value is None:
        parser.error('a target, note or file path is required')
    if args.action == 'list' and (args.name or args.value):
        parser.error('case list does not accept extra arguments')
    if args.action not in ('add', 'note') and args.value:
        parser.error('unexpected extra value')
    if args.format in ('graphml', 'gexf') and args.action != 'graph':
        parser.error('use case graph for graph formats')
    try:
        with CaseStore(writable=args.action in ('new', 'add', 'note')) as store:
            if argv[0] == 'evidence':
                result = add_evidence(store, args.name, args.value)
            elif args.action == 'new':
                result = store.new(args.name)
            elif args.action == 'list':
                result = store.list()
            elif args.action == 'add':
                run = store.save(args.name, investigate(args.value, type=args.type), method='case add')
                result = {'case': args.name, 'run_id': run}
            elif args.action == 'note':
                result = store.note(args.name, args.value)
            else:
                result = store.show(args.name)
                if args.action == 'graph':
                    print(graph(result, args.format if args.format in ('graphml', 'gexf') else 'graphml'), end='')
                    return 0
                if args.action == 'timeline':
                    result = timeline(result)
                if args.action in ('show', 'export', 'timeline'):
                    print(export_data(result, args.format), end='')
                    return 0
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2
