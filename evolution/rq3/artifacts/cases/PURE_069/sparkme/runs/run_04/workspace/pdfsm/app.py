import argparse
import os
import sys
from dataclasses import dataclass
from typing import List

from pypdf import PdfReader, PdfWriter


def parse_pages(spec: str, max_pages: int) -> List[int]:
    pages = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start = int(a)
            end = int(b)
            if start <= end:
                pages.extend(range(start, end + 1))
            else:
                pages.extend(range(start, end - 1, -1))
        else:
            pages.append(int(part))
    seen = set()
    result = []
    for p in pages:
        if p < 1 or p > max_pages:
            raise ValueError(f'page {p} out of range 1..{max_pages}')
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def safe_write(writer: PdfWriter, output: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output)) or '.', exist_ok=True)
    tmp = output + '.tmp'
    with open(tmp, 'wb') as f:
        writer.write(f)
    os.replace(tmp, output)


def cmd_split(args):
    reader = PdfReader(args.input)
    base = os.path.splitext(os.path.basename(args.input))[0]
    os.makedirs(args.output_dir, exist_ok=True)
    for i, page in enumerate(reader.pages, start=1):
        w = PdfWriter()
        w.add_page(page)
        safe_write(w, os.path.join(args.output_dir, f'{base}_page_{i}.pdf'))
    return 0


def cmd_merge(args):
    writer = PdfWriter()
    for path in args.inputs:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    safe_write(writer, args.output)
    return 0


def cmd_extract(args):
    reader = PdfReader(args.input)
    pages = parse_pages(args.pages, len(reader.pages))
    writer = PdfWriter()
    for p in pages:
        writer.add_page(reader.pages[p - 1])
    safe_write(writer, args.output)
    return 0


def cmd_rotate(args):
    reader = PdfReader(args.input)
    writer = PdfWriter()
    delta = int(args.degrees)
    if delta % 90 != 0:
        raise ValueError('rotation must be a multiple of 90')
    for idx, page in enumerate(reader.pages, start=1):
        if args.pages is None or idx in parse_pages(args.pages, len(reader.pages)):
            page.rotate(delta)
        writer.add_page(page)
    safe_write(writer, args.output)
    return 0


def cmd_reorder(args):
    reader = PdfReader(args.input)
    pages = parse_pages(args.pages, len(reader.pages))
    writer = PdfWriter()
    for p in pages:
        writer.add_page(reader.pages[p - 1])
    safe_write(writer, args.output)
    return 0


def cmd_interleave(args):
    readers = [PdfReader(p) for p in args.inputs]
    max_len = max(len(r.pages) for r in readers)
    writer = PdfWriter()
    for i in range(max_len):
        for r in readers:
            if i < len(r.pages):
                writer.add_page(r.pages[i])
    safe_write(writer, args.output)
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog='pdfsm', description='PDF Split and Merge CLI')
    sp = p.add_subparsers(dest='cmd', required=True)

    s = sp.add_parser('split')
    s.add_argument('input')
    s.add_argument('output_dir')
    s.set_defaults(func=cmd_split)

    m = sp.add_parser('merge')
    m.add_argument('output')
    m.add_argument('inputs', nargs='+')
    m.set_defaults(func=cmd_merge)

    e = sp.add_parser('extract')
    e.add_argument('input')
    e.add_argument('pages')
    e.add_argument('output')
    e.set_defaults(func=cmd_extract)

    r = sp.add_parser('rotate')
    r.add_argument('input')
    r.add_argument('degrees')
    r.add_argument('output')
    r.add_argument('--pages')
    r.set_defaults(func=cmd_rotate)

    o = sp.add_parser('reorder')
    o.add_argument('input')
    o.add_argument('pages')
    o.add_argument('output')
    o.set_defaults(func=cmd_reorder)

    i = sp.add_parser('interleave')
    i.add_argument('output')
    i.add_argument('inputs', nargs='+')
    i.set_defaults(func=cmd_interleave)

    return p


def main(argv=None):
    try:
        parser = build_parser()
        args = parser.parse_args(argv)
        return args.func(args)
    except Exception as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1
