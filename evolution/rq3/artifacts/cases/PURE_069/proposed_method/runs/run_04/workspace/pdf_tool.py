#!/usr/bin/env python3
import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from pypdf import PdfReader, PdfWriter


@dataclass
class PageSpec:
    source_index: int
    page_index: int


def parse_page_ranges(spec: str, total_pages: int) -> List[int]:
    if not spec:
        return list(range(total_pages))
    result = []
    seen = set()
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            left, right = part.split('-', 1)
            start = int(left) if left else 1
            end = int(right) if right else total_pages
            if start < 1 or end < 1 or start > end:
                raise ValueError(f'invalid range: {part}')
            for n in range(start, end + 1):
                idx = n - 1
                if idx not in seen:
                    seen.add(idx)
                    result.append(idx)
        else:
            n = int(part)
            if n < 1:
                raise ValueError(f'invalid page number: {part}')
            idx = n - 1
            if idx not in seen:
                seen.add(idx)
                result.append(idx)
    return result


def load_reader(path: Path) -> PdfReader:
    try:
        return PdfReader(str(path))
    except Exception as e:
        raise RuntimeError(f'cannot read {path}: {e}') from e


def rotate_page(page, degrees: int):
    if degrees % 90 != 0:
        raise ValueError('rotation must be in 90-degree steps')
    if degrees:
        page.rotate(degrees)


def build_writer_from_inputs(inputs: List[Path], mode: str, pages: str, rotate: int, interleave: bool) -> PdfWriter:
    readers = [load_reader(p) for p in inputs]
    writer = PdfWriter()

    if interleave:
        page_lists = [list(range(len(r.pages))) for r in readers]
        max_len = max((len(x) for x in page_lists), default=0)
        for i in range(max_len):
            for ridx, reader in enumerate(readers):
                if i < len(reader.pages):
                    page = reader.pages[i]
                    rotate_page(page, rotate)
                    writer.add_page(page)
    else:
        for reader in readers:
            selected = parse_page_ranges(pages, len(reader.pages)) if pages else list(range(len(reader.pages)))
            for idx in selected:
                page = reader.pages[idx]
                rotate_page(page, rotate)
                writer.add_page(page)
    return writer


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def cmd_split(args):
    reader = load_reader(Path(args.input))
    total = len(reader.pages)
    ranges = []
    if args.ranges:
        for chunk in args.ranges.split(';'):
            ranges.append(parse_page_ranges(chunk.strip(), total))
    else:
        step = int(args.chunk_size)
        for start in range(0, total, step):
            ranges.append(list(range(start, min(start + step, total))))

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    base = Path(args.input).stem
    outputs = []
    for i, page_idxs in enumerate(ranges, start=1):
        writer = PdfWriter()
        for idx in page_idxs:
            page = reader.pages[idx]
            rotate_page(page, args.rotate)
            writer.add_page(page)
        out = outdir / f"{base}_split_{i:03d}.pdf"
        with open(out, 'wb') as f:
            writer.write(f)
        outputs.append(str(out))
    print(json.dumps({'outputs': outputs}))


def cmd_merge(args):
    inputs = [Path(p) for p in args.inputs]
    writer = build_writer_from_inputs(inputs, 'merge', args.pages, args.rotate, args.interleave)
    out = Path(args.output)
    ensure_parent(out)
    with open(out, 'wb') as f:
        writer.write(f)
    print(json.dumps({'output': str(out)}))


def cmd_extract(args):
    reader = load_reader(Path(args.input))
    writer = PdfWriter()
    selected = parse_page_ranges(args.pages, len(reader.pages))
    for idx in selected:
        page = reader.pages[idx]
        rotate_page(page, args.rotate)
        writer.add_page(page)
    out = Path(args.output)
    ensure_parent(out)
    with open(out, 'wb') as f:
        writer.write(f)
    print(json.dumps({'output': str(out)}))


def main(argv=None):
    parser = argparse.ArgumentParser(prog='pdf-tool')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_split = sub.add_parser('split')
    p_split.add_argument('input')
    p_split.add_argument('-o', '--output-dir', required=True)
    p_split.add_argument('--chunk-size', default=1)
    p_split.add_argument('--ranges', help='Semicolon-separated page ranges for each output, e.g. 1-2;3-5')
    p_split.add_argument('--rotate', type=int, default=0)
    p_split.set_defaults(func=cmd_split)

    p_merge = sub.add_parser('merge')
    p_merge.add_argument('inputs', nargs='+')
    p_merge.add_argument('-o', '--output', required=True)
    p_merge.add_argument('--pages', help='Page ranges applied to each source, e.g. 1-3')
    p_merge.add_argument('--rotate', type=int, default=0)
    p_merge.add_argument('--interleave', action='store_true')
    p_merge.set_defaults(func=cmd_merge)

    p_extract = sub.add_parser('extract')
    p_extract.add_argument('input')
    p_extract.add_argument('--pages', required=True)
    p_extract.add_argument('-o', '--output', required=True)
    p_extract.add_argument('--rotate', type=int, default=0)
    p_extract.set_defaults(func=cmd_extract)

    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
