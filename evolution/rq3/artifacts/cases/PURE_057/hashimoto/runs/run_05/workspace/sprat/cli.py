import argparse
from pathlib import Path
from .app import cmd_add, cmd_list, cmd_edit, cmd_approve, cmd_flag, cmd_compare, cmd_import


def build_parser():
    p = argparse.ArgumentParser(prog='sprat')
    p.add_argument('--db', default='sprat_db.json')
    sub = p.add_subparsers(dest='cmd', required=True)

    def common(sp):
        sp.add_argument('--user', required=True)
        sp.add_argument('--role', choices=['guest','analyst','manager','admin'], required=True)
        sp.add_argument('--project', default='default')

    sp = sub.add_parser('add')
    common(sp)
    sp.add_argument('--title', required=True)
    sp.add_argument('--content', default='')
    sp.add_argument('--type', default='requirement')
    sp.add_argument('--status', default='draft')
    sp.add_argument('--classifications', nargs='*', default=[])
    sp.add_argument('--tags', default='')
    sp.add_argument('--sensitive', action='store_true')
    sp.add_argument('--source', default='manual')
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser('list')
    common(sp)
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser('edit')
    common(sp)
    sp.add_argument('--id', type=int, required=True)
    sp.add_argument('--title')
    sp.add_argument('--content')
    sp.add_argument('--reason')
    sp.set_defaults(func=cmd_edit)

    sp = sub.add_parser('approve')
    common(sp)
    sp.add_argument('--id', type=int, required=True)
    sp.add_argument('--reviewer', required=True)
    sp.add_argument('--reason')
    sp.set_defaults(func=cmd_approve)

    sp = sub.add_parser('flag')
    common(sp)
    sp.add_argument('--id', type=int, required=True)
    sp.add_argument('--flag-type', required=True)
    sp.add_argument('--note', default='')
    sp.set_defaults(func=cmd_flag)

    sp = sub.add_parser('compare')
    common(sp)
    sp.add_argument('--left', type=int, required=True)
    sp.add_argument('--right', type=int, required=True)
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser('import')
    common(sp)
    sp.add_argument('--source', required=True)
    sp.set_defaults(func=cmd_import)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0
