#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_FILE = Path(os.environ.get('SPRAT_DB', '/workspace/sprat_db.json'))
ROLES = {'admin', 'manager', 'analyst', 'guest'}
VIEW_ROLES = {'admin', 'manager', 'analyst', 'guest'}
EDIT_ROLES = {'admin', 'manager', 'analyst'}
ADMIN_ROLES = {'admin'}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_db() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        return {'artifacts': [], 'next_id': 1, 'users': {}, 'history': []}
    return json.loads(DATA_FILE.read_text())


def save_db(db: Dict[str, Any]) -> None:
    DATA_FILE.write_text(json.dumps(db, indent=2, sort_keys=True))


def role_of(db: Dict[str, Any], user: str) -> str:
    return db.get('users', {}).get(user, 'guest')


def ensure_role(role: str) -> None:
    if role not in ROLES:
        raise SystemExit(f'invalid role: {role}')


def can_view(role: str) -> bool:
    return role in VIEW_ROLES


def can_edit(role: str) -> bool:
    return role in EDIT_ROLES


def can_admin(role: str) -> bool:
    return role in ADMIN_ROLES


def find_artifact(db: Dict[str, Any], artifact_id: int) -> Dict[str, Any]:
    for a in db['artifacts']:
        if a['id'] == artifact_id:
            return a
    raise SystemExit(f'artifact not found: {artifact_id}')


def snapshot(db: Dict[str, Any], action: str) -> None:
    db['history'].append({'timestamp': now(), 'action': action, 'db': deepcopy({'artifacts': db['artifacts'], 'next_id': db['next_id'], 'users': db['users']})})


def create_artifact(args: argparse.Namespace) -> None:
    db = load_db()
    role = role_of(db, args.user)
    if not can_edit(role):
        raise SystemExit('permission denied')
    snapshot(db, f'create:{args.type}')
    artifact = {
        'id': db['next_id'],
        'type': args.type,
        'title': args.title,
        'content': args.content,
        'classification': args.classification,
        'sources': [],
        'primary_source_id': None,
        'links': [],
        'created_by': args.user,
        'updated_by': args.user,
        'created_at': now(),
        'updated_at': now(),
        'version': 1,
    }
    if args.type == 'requirement' and args.sources:
        artifact['sources'] = args.sources
        artifact['primary_source_id'] = args.primary_source
    db['artifacts'].append(artifact)
    db['next_id'] += 1
    save_db(db)
    print(json.dumps(artifact, indent=2))


def link_artifacts(args: argparse.Namespace) -> None:
    db = load_db()
    role = role_of(db, args.user)
    if not can_edit(role):
        raise SystemExit('permission denied')
    src = find_artifact(db, args.source)
    dst = find_artifact(db, args.target)
    snapshot(db, f'link:{src["id"]}->{dst["id"]}')
    link = {'target': dst['id'], 'relation': args.relation}
    if link not in src['links']:
        src['links'].append(link)
    save_db(db)
    print(json.dumps({'source': src['id'], 'target': dst['id'], 'relation': args.relation}, indent=2))


def show_artifact(args: argparse.Namespace) -> None:
    db = load_db()
    role = role_of(db, args.user)
    if not can_view(role):
        raise SystemExit('permission denied')
    art = find_artifact(db, args.id)
    out = deepcopy(art)
    out['linked_artifacts'] = [find_artifact(db, l['target'])['id'] for l in art.get('links', [])]
    if art['type'] == 'requirement':
        out['source_artifacts'] = [find_artifact(db, sid)['title'] for sid in art.get('sources', []) if any(a['id'] == sid for a in db['artifacts'])]
    print(json.dumps(out, indent=2))


def compare(args: argparse.Namespace) -> None:
    db = load_db()
    role = role_of(db, args.user)
    if not can_view(role):
        raise SystemExit('permission denied')
    a = find_artifact(db, args.first)
    b = find_artifact(db, args.second)
    print(json.dumps({'first': {'id': a['id'], 'title': a['title'], 'type': a['type'], 'classification': a['classification']}, 'second': {'id': b['id'], 'title': b['title'], 'type': b['type'], 'classification': b['classification']}}, indent=2))


def set_user(args: argparse.Namespace) -> None:
    db = load_db()
    ensure_role(args.role)
    db.setdefault('users', {})[args.user] = args.role
    save_db(db)
    print(json.dumps({'user': args.user, 'role': args.role}, indent=2))


def history(args: argparse.Namespace) -> None:
    db = load_db()
    print(json.dumps(db.get('history', []), indent=2))


def undo(args: argparse.Namespace) -> None:
    db = load_db()
    role = role_of(db, args.user)
    if not can_edit(role):
        raise SystemExit('permission denied')
    if not db.get('history'):
        raise SystemExit('nothing to undo')
    last = db['history'].pop()
    restored = last['db']
    db['artifacts'] = restored['artifacts']
    db['next_id'] = restored['next_id']
    db['users'] = restored['users']
    save_db(db)
    print(json.dumps({'undone': last['action']}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='sprat')
    sub = p.add_subparsers(dest='cmd', required=True)

    u = sub.add_parser('set-user')
    u.add_argument('user')
    u.add_argument('role')
    u.set_defaults(func=set_user)

    c = sub.add_parser('create')
    c.add_argument('type', choices=['goal', 'scenario', 'requirement', 'policy'])
    c.add_argument('title')
    c.add_argument('--content', default='')
    c.add_argument('--classification', default='general')
    c.add_argument('--user', default='guest')
    c.add_argument('--sources', type=int, nargs='*', default=[])
    c.add_argument('--primary-source', type=int)
    c.set_defaults(func=create_artifact)

    l = sub.add_parser('link')
    l.add_argument('source', type=int)
    l.add_argument('target', type=int)
    l.add_argument('--relation', default='related-to')
    l.add_argument('--user', default='guest')
    l.set_defaults(func=link_artifacts)

    s = sub.add_parser('show')
    s.add_argument('id', type=int)
    s.add_argument('--user', default='guest')
    s.set_defaults(func=show_artifact)

    cmp_ = sub.add_parser('compare')
    cmp_.add_argument('first', type=int)
    cmp_.add_argument('second', type=int)
    cmp_.add_argument('--user', default='guest')
    cmp_.set_defaults(func=compare)

    h = sub.add_parser('history')
    h.set_defaults(func=history)

    un = sub.add_parser('undo')
    un.add_argument('--user', default='guest')
    un.set_defaults(func=undo)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
