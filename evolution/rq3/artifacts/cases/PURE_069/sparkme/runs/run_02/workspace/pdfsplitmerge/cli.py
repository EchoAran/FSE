from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import (
    extract_pages,
    interleave_pdfs,
    load_workspace,
    merge_pdfs,
    reorder_pages,
    result_to_dict,
    rotate_pages,
    save_workspace,
    split_pdf,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog='pdfsplitmerge')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('split')
    p.add_argument('input')
    p.add_argument('output_dir')

    p = sub.add_parser('merge')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')

    p = sub.add_parser('extract')
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('pages', nargs='+', type=int)

    p = sub.add_parser('rotate')
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('--page', action='append', default=[])

    p = sub.add_parser('reorder')
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('order', nargs='+', type=int)

    p = sub.add_parser('interleave')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')

    p = sub.add_parser('save-workspace')
    p.add_argument('path')
    p.add_argument('json_data')

    p = sub.add_parser('load-workspace')
    p.add_argument('path')

    args = parser.parse_args(argv)

    if args.cmd == 'split':
        print(json.dumps(result_to_dict(split_pdf(args.input, args.output_dir)), indent=2))
    elif args.cmd == 'merge':
        print(json.dumps(result_to_dict(merge_pdfs(args.inputs, args.output)), indent=2))
    elif args.cmd == 'extract':
        print(json.dumps(result_to_dict(extract_pages(args.input, args.pages, args.output)), indent=2))
    elif args.cmd == 'rotate':
        rotations = {}
        for item in args.page:
            page, deg = item.split(':', 1)
            rotations[int(page)] = int(deg)
        print(json.dumps(result_to_dict(rotate_pages(args.input, rotations, args.output)), indent=2))
    elif args.cmd == 'reorder':
        print(json.dumps(result_to_dict(reorder_pages(args.input, args.order, args.output)), indent=2))
    elif args.cmd == 'interleave':
        print(json.dumps(result_to_dict(interleave_pdfs(args.inputs, args.output)), indent=2))
    elif args.cmd == 'save-workspace':
        save_workspace(json.loads(args.json_data), args.path)
        print(args.path)
    elif args.cmd == 'load-workspace':
        print(json.dumps(load_workspace(args.path), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
