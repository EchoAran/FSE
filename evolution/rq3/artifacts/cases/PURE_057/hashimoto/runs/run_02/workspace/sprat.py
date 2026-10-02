#!/usr/bin/env python3
import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

STATE_FILE = Path('.sprat_state.json')


def now():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {'analyses': {}}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True))


def ensure_user(role, username):
    return {'username': username, 'role': role}


def can_view_draft(user, item):
    if item.get('sensitive'):
        return user['role'] in ('administrator',) or user['username'] in (item['author'],) or user['username'] in item.get('reviewers', [])
    if user['role'] == 'guest':
        return False
    if user['role'] == 'project_manager':
        return True
    return True


def basic_item_view(item, user, show_full=False):
    if show_full:
        return item
    view = {
        'id': item['id'],
        'title': item.get('title'),
        'owner': item.get('author'),
        'status': item.get('status'),
        'type': item.get('type'),
        'sensitive': item.get('sensitive', False),
    }
    if item.get('status') == 'draft':
        if item.get('sensitive') and user['role'] not in ('administrator',) and user['username'] not in (item['author'],) and user['username'] not in item.get('reviewers', []):
            return {'id': item['id'], 'status': 'draft', 'hidden': True}
        if user['role'] == 'guest' and not item.get('guest_project_allowed', False):
            return {'id': item['id'], 'status': 'draft', 'hidden': True}
        if not can_view_draft(user, item):
            return {'id': item['id'], 'status': 'draft', 'hidden': True}
        if user['role'] in ('project_manager', 'administrator') or user['username'] in item.get('reviewers', []) or user['username'] == item['author']:
            view['summary'] = item.get('content', '')[:120]
        else:
            view['summary'] = item.get('title')
    else:
        view['content'] = item.get('content')
    return view


def cmd_init(args):
    save_state({'analyses': {}})
    print('initialized')


def get_analysis(state, analysis_id):
    analyses = state['analyses']
    if analysis_id not in analyses:
        analyses[analysis_id] = {'items': {}, 'history': []}
    return analyses[analysis_id]


def record_history(analysis, action, user, reason=None, item_id=None):
    analysis['history'].append({'timestamp': now(), 'user': user['username'], 'role': user['role'], 'action': action, 'item_id': item_id, 'reason': reason})


def cmd_add(args):
    state = load_state()
    analysis = get_analysis(state, args.analysis)
    user = ensure_user(args.role, args.user)
    item = {
        'id': args.id,
        'type': args.type,
        'title': args.title,
        'content': args.content,
        'author': user['username'],
        'status': 'draft' if args.type != 'final' else 'final',
        'sensitive': args.sensitive,
        'classifications': args.classifications,
        'tags': args.tags,
        'trace_links': args.trace_links,
        'version': 1,
        'versions': [],
        'reviewers': args.reviewers,
        'guest_project_allowed': args.guest_project_allowed,
        'unresolved': False,
        'exceptions': [],
    }
    item['versions'].append({'version': 1, 'timestamp': now(), 'user': user['username'], 'content': args.content, 'status': item['status']})
    analysis['items'][args.id] = item
    record_history(analysis, 'create', user, item_id=args.id)
    save_state(state)
    print(args.id)


def cmd_edit(args):
    state = load_state()
    analysis = get_analysis(state, args.analysis)
    item = analysis['items'][args.id]
    user = ensure_user(args.role, args.user)
    if item['status'] == 'final':
        new_item = json.loads(json.dumps(item))
        new_item['id'] = f"{item['id']}-r{len(item['versions'])+1}"
        new_item['version'] = item['version'] + 1
        new_item['status'] = 'draft'
        new_item['content'] = args.content
        new_item['author'] = user['username']
        new_item['versions'].append({'version': new_item['version'], 'timestamp': now(), 'user': user['username'], 'content': args.content, 'status': 'draft'})
        analysis['items'][new_item['id']] = new_item
        record_history(analysis, 'revise-final', user, args.reason, item_id=new_item['id'])
    else:
        item['content'] = args.content
        item['version'] += 1
        item['versions'].append({'version': item['version'], 'timestamp': now(), 'user': user['username'], 'content': args.content, 'status': item['status']})
        record_history(analysis, 'edit', user, args.reason, item_id=args.id)
    save_state(state)
    print('ok')


def cmd_approve(args):
    state = load_state()
    analysis = get_analysis(state, args.analysis)
    item = analysis['items'][args.id]
    user = ensure_user(args.role, args.user)
    item['status'] = 'final'
    item['reviewed_by'] = user['username']
    item['reviewed_at'] = now()
    record_history(analysis, 'approve', user, args.reason, item_id=args.id)
    save_state(state)
    print('approved')


def cmd_view(args):
    state = load_state()
    analysis = get_analysis(state, args.analysis)
    item = analysis['items'][args.id]
    user = ensure_user(args.role, args.user)
    print(json.dumps(basic_item_view(item, user), indent=2))


def cmd_import(args):
    state = load_state()
    analysis = get_analysis(state, args.analysis)
    source = json.loads(Path(args.file).read_text())
    imported = source.get('items', [])
    for i, raw in enumerate(imported, 1):
        item_id = raw.get('id', f'imported-{i}')
        analysis['items'][item_id] = {
            'id': item_id,
            'type': raw.get('type', 'requirement'),
            'title': raw.get('title'),
            'content': raw.get('content', ''),
            'author': 'import',
            'status': 'final',
            'sensitive': raw.get('sensitive', False),
            'classifications': raw.get('classifications', []),
            'tags': raw.get('tags', []),
            'trace_links': raw.get('trace_links', []),
            'version': raw.get('version', 1),
            'versions': raw.get('versions', []),
            'reviewers': [],
            'guest_project_allowed': False,
            'unresolved': raw.get('unresolved', False),
            'exceptions': raw.get('exceptions', []),
            'import_source': args.file,
        }
    record_history(analysis, 'import', {'username': args.user, 'role': args.role}, item_id=None)
    save_state(state)
    print(f'imported {len(imported)} items')


def build_parser():
    p = argparse.ArgumentParser(prog='sprat')
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('init').set_defaults(func=cmd_init)
    a = sub.add_parser('add')
    a.add_argument('--analysis', required=True)
    a.add_argument('--id', required=True)
    a.add_argument('--type', default='requirement')
    a.add_argument('--title', required=True)
    a.add_argument('--content', default='')
    a.add_argument('--user', required=True)
    a.add_argument('--role', required=True)
    a.add_argument('--sensitive', action='store_true')
    a.add_argument('--classifications', nargs='*', default=[])
    a.add_argument('--tags', nargs='*', default=[])
    a.add_argument('--trace-links', nargs='*', default=[])
    a.add_argument('--reviewers', nargs='*', default=[])
    a.add_argument('--guest-project-allowed', action='store_true')
    a.set_defaults(func=cmd_add)
    e = sub.add_parser('edit')
    e.add_argument('--analysis', required=True)
    e.add_argument('--id', required=True)
    e.add_argument('--content', required=True)
    e.add_argument('--user', required=True)
    e.add_argument('--role', required=True)
    e.add_argument('--reason')
    e.set_defaults(func=cmd_edit)
    ap = sub.add_parser('approve')
    ap.add_argument('--analysis', required=True)
    ap.add_argument('--id', required=True)
    ap.add_argument('--user', required=True)
    ap.add_argument('--role', required=True)
    ap.add_argument('--reason')
    ap.set_defaults(func=cmd_approve)
    v = sub.add_parser('view')
    v.add_argument('--analysis', required=True)
    v.add_argument('--id', required=True)
    v.add_argument('--user', required=True)
    v.add_argument('--role', required=True)
    v.set_defaults(func=cmd_view)
    im = sub.add_parser('import')
    im.add_argument('--analysis', required=True)
    im.add_argument('--file', required=True)
    im.add_argument('--user', required=True)
    im.add_argument('--role', required=True)
    im.set_defaults(func=cmd_import)
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
