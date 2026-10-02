#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import List

from pypdf import PdfReader, PdfWriter


def parse_page_spec(spec: str, page_count: int) -> List[int]:
    pages: List[int] = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start_s, end_s = part.split('-', 1)
            start = int(start_s)
            end = int(end_s)
            step = 1 if end >= start else -1
            for p in range(start, end + step, step):
                if 1 <= p <= page_count:
                    pages.append(p - 1)
        else:
            p = int(part)
            if 1 <= p <= page_count:
                pages.append(p - 1)
    return pages


def write_pdf(reader: PdfReader, page_indexes: List[int], output: Path, rotate: int = 0):
    writer = PdfWriter()
    for idx in page_indexes:
        page = reader.pages[idx]
        if rotate:
            page.rotate(rotate)
        writer.add_page(page)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as f:
        writer.write(f)


def cmd_split(args):
    reader = PdfReader(args.input)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        with (outdir / f'page-{i:03d}.pdf').open('wb') as f:
            writer.write(f)


def cmd_extract(args):
    reader = PdfReader(args.input)
    pages = parse_page_spec(args.pages, len(reader.pages))
    write_pdf(reader, pages, Path(args.output))


def cmd_rotate(args):
    reader = PdfReader(args.input)
    pages = parse_page_spec(args.pages, len(reader.pages)) if args.pages else list(range(len(reader.pages)))
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages):
        if idx in pages:
            page.rotate(args.degrees)
        writer.add_page(page)
    with Path(args.output).open('wb') as f:
        writer.write(f)


def cmd_merge(args):
    writer = PdfWriter()
    for input_path in args.inputs:
        reader = PdfReader(input_path)
        if args.pages:
            pages = parse_page_spec(args.pages, len(reader.pages))
            for idx in pages:
                writer.add_page(reader.pages[idx])
        else:
            for page in reader.pages:
                writer.add_page(page)
    with Path(args.output).open('wb') as f:
        writer.write(f)


def cmd_reorder(args):
    reader = PdfReader(args.input)
    pages = parse_page_spec(args.order, len(reader.pages))
    write_pdf(reader, pages, Path(args.output))


def cmd_interleave(args):
    readers = [PdfReader(p) for p in args.inputs]
    writer = PdfWriter()
    max_pages = max(len(r.pages) for r in readers)
    for i in range(max_pages):
        for reader in readers:
            if i < len(reader.pages):
                writer.add_page(reader.pages[i])
    with Path(args.output).open('wb') as f:
        writer.write(f)


def build_parser():
    p = argparse.ArgumentParser(description='PDF split and merge tool')
    sub = p.add_subparsers(dest='cmd', required=True)

    s = sub.add_parser('split')
    s.add_argument('input')
    s.add_argument('output_dir')
    s.set_defaults(func=cmd_split)

    s = sub.add_parser('extract')
    s.add_argument('input')
    s.add_argument('pages', help='Page spec like 1-3,5')
    s.add_argument('output')
    s.set_defaults(func=cmd_extract)

    s = sub.add_parser('rotate')
    s.add_argument('input')
    s.add_argument('degrees', type=int)
    s.add_argument('output')
    s.add_argument('--pages', default='')
    s.set_defaults(func=cmd_rotate)

    s = sub.add_parser('merge')
    s.add_argument('output')
    s.add_argument('inputs', nargs='+')
    s.add_argument('--pages', default='')
    s.set_defaults(func=cmd_merge)

    s = sub.add_parser('reorder')
    s.add_argument('input')
    s.add_argument('order')
    s.add_argument('output')
    s.set_defaults(func=cmd_reorder)

    s = sub.add_parser('interleave')
    s.add_argument('output')
    s.add_argument('inputs', nargs='+')
    s.set_defaults(func=cmd_interleave)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
