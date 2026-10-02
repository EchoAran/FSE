#!/usr/bin/env python3
import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from pypdf import PdfReader, PdfWriter


@dataclass
class PageSpec:
    source: str
    pages: Optional[List[int]] = None
    rotate: int = 0


def parse_pages(spec: str) -> List[int]:
    pages: List[int] = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start, end = int(a), int(b)
            step = 1 if end >= start else -1
            pages.extend(list(range(start, end + step, step)))
        else:
            pages.append(int(part))
    return pages


def load_reader(path: str) -> PdfReader:
    return PdfReader(path)


def ensure_output_path(path: str):
    out = Path(path)
    if out.exists() and out.is_dir():
        raise SystemExit(f'Output path is a directory: {path}')
    out.parent.mkdir(parents=True, exist_ok=True)


def copy_pages(writer: PdfWriter, source: str, pages: Optional[List[int]] = None, rotate: int = 0):
    reader = load_reader(source)
    total = len(reader.pages)
    indices = pages if pages is not None else list(range(1, total + 1))
    for p in indices:
        if p < 1 or p > total:
            raise SystemExit(f'Page {p} out of range for {source} with {total} pages')
        page = reader.pages[p - 1]
        if rotate:
            page.rotate(rotate)
        writer.add_page(page)


def cmd_split(args):
    reader = load_reader(args.input)
    base = Path(args.output_dir)
    base.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out = base / f'page_{i}.pdf'
        with out.open('wb') as f:
            writer.write(f)


def cmd_extract(args):
    writer = PdfWriter()
    copy_pages(writer, args.input, parse_pages(args.pages))
    ensure_output_path(args.output)
    with open(args.output, 'wb') as f:
        writer.write(f)


def cmd_merge(args):
    writer = PdfWriter()
    for source in args.inputs:
        copy_pages(writer, source)
    ensure_output_path(args.output)
    with open(args.output, 'wb') as f:
        writer.write(f)


def cmd_rotate(args):
    writer = PdfWriter()
    reader = load_reader(args.input)
    pages = parse_pages(args.pages) if args.pages else list(range(1, len(reader.pages) + 1))
    for i, page in enumerate(reader.pages, start=1):
        if i in pages:
            page.rotate(args.degrees)
        writer.add_page(page)
    ensure_output_path(args.output)
    with open(args.output, 'wb') as f:
        writer.write(f)


def cmd_reorder(args):
    writer = PdfWriter()
    copy_pages(writer, args.input, parse_pages(args.pages))
    ensure_output_path(args.output)
    with open(args.output, 'wb') as f:
        writer.write(f)


def cmd_alternate(args):
    readers = [load_reader(p) for p in args.inputs]
    max_pages = max(len(r.pages) for r in readers)
    writer = PdfWriter()
    for i in range(max_pages):
        for r in readers:
            if i < len(r.pages):
                writer.add_page(r.pages[i])
    ensure_output_path(args.output)
    with open(args.output, 'wb') as f:
        writer.write(f)


def cmd_save_setup(args):
    data = {
        'command': args.setup_command,
        'description': args.description,
    }
    ensure_output_path(args.output)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def cmd_run_setup(args):
    with open(args.setup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cmd = data.get('command')
    if not cmd:
        raise SystemExit('Setup file does not contain a command')
    rc = os.system(cmd)
    if rc != 0:
        raise SystemExit(rc)


def build_parser():
    p = argparse.ArgumentParser(prog='pdf-tool', description='PDF split and merge utility')
    sub = p.add_subparsers(dest='cmd', required=True)

    sp = sub.add_parser('split', help='Split each page into a separate file')
    sp.add_argument('input')
    sp.add_argument('output_dir')
    sp.set_defaults(func=cmd_split)

    sp = sub.add_parser('extract', help='Extract selected pages')
    sp.add_argument('input')
    sp.add_argument('pages', help='Pages like 1,3-5')
    sp.add_argument('output')
    sp.set_defaults(func=cmd_extract)

    sp = sub.add_parser('merge', help='Merge PDF files')
    sp.add_argument('output')
    sp.add_argument('inputs', nargs='+')
    sp.set_defaults(func=cmd_merge)

    sp = sub.add_parser('rotate', help='Rotate pages')
    sp.add_argument('input')
    sp.add_argument('degrees', type=int)
    sp.add_argument('output')
    sp.add_argument('--pages', default='')
    sp.set_defaults(func=cmd_rotate)

    sp = sub.add_parser('reorder', help='Reorder pages')
    sp.add_argument('input')
    sp.add_argument('pages', help='New page order like 3,1,2')
    sp.add_argument('output')
    sp.set_defaults(func=cmd_reorder)

    sp = sub.add_parser('alternate', help='Alternate pages from input files')
    sp.add_argument('output')
    sp.add_argument('inputs', nargs='+')
    sp.set_defaults(func=cmd_alternate)

    sp = sub.add_parser('save-setup', help='Save reusable setup')
    sp.add_argument('output')
    sp.add_argument('--setup-command', required=True)
    sp.add_argument('--description', default='')
    sp.set_defaults(func=cmd_save_setup)

    sp = sub.add_parser('run-setup', help='Run reusable setup')
    sp.add_argument('setup_file')
    sp.set_defaults(func=cmd_run_setup)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    main()
