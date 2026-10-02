from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .core import alternate_merge, extract_pages, merge_pdfs, reorder_pages, rotate_pages, split_pdf


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='pdfsplitmerge')
    sub = p.add_subparsers(dest='cmd', required=True)

    sp = sub.add_parser('split')
    sp.add_argument('source', type=Path)
    sp.add_argument('--output-dir', type=Path, required=True)
    sp.add_argument('--prefix', default='page')

    ep = sub.add_parser('extract')
    ep.add_argument('source', type=Path)
    ep.add_argument('--pages', required=True)
    ep.add_argument('--output', type=Path, required=True)

    rp = sub.add_parser('rotate')
    rp.add_argument('source', type=Path)
    rp.add_argument('--degrees', type=int, required=True)
    rp.add_argument('--pages')
    rp.add_argument('--output', type=Path, required=True)

    op = sub.add_parser('reorder')
    op.add_argument('source', type=Path)
    op.add_argument('--order', required=True)
    op.add_argument('--output', type=Path, required=True)

    mp = sub.add_parser('merge')
    mp.add_argument('inputs', nargs='+', type=Path)
    mp.add_argument('--output', type=Path, required=True)

    ap = sub.add_parser('alternate-merge')
    ap.add_argument('inputs', nargs='+', type=Path)
    ap.add_argument('--output', type=Path, required=True)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == 'split':
        split_pdf(args.source, args.output_dir, args.prefix)
    elif args.cmd == 'extract':
        extract_pages(args.source, args.output, args.pages)
    elif args.cmd == 'rotate':
        rotate_pages(args.source, args.output, args.degrees, args.pages)
    elif args.cmd == 'reorder':
        reorder_pages(args.source, args.output, args.order)
    elif args.cmd == 'merge':
        merge_pdfs(args.inputs, args.output)
    elif args.cmd == 'alternate-merge':
        alternate_merge(args.inputs, args.output)
    else:
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
