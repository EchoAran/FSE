#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from pypdf import PdfReader, PdfWriter


@dataclass
class JobConfig:
    inputs: List[Path]
    output: str
    mode: str
    pages: List[int] | None = None
    overwrite: bool = False


def parse_pages(spec: str) -> List[int]:
    pages: list[int] = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start_s, end_s = part.split('-', 1)
            start = int(start_s)
            end = int(end_s)
            step = 1 if end >= start else -1
            pages.extend(list(range(start, end + step, step)))
        else:
            pages.append(int(part))
    # de-duplicate while preserving order
    seen = set()
    result = []
    for p in pages:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_pdf(writer: PdfWriter, output: Path, overwrite: bool) -> None:
    if output.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {output}")
    ensure_parent(output)
    with output.open('wb') as fh:
        writer.write(fh)


def split_pdf(input_path: Path, output_pattern: str, pages: List[int] | None, overwrite: bool) -> list[Path]:
    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    selected = pages if pages is not None else list(range(1, total + 1))
    outputs: list[Path] = []
    if '{page}' not in output_pattern:
        raise ValueError("Split output pattern must contain {page}")
    for page_num in selected:
        if page_num < 1 or page_num > total:
            raise ValueError(f"Page {page_num} out of range for {input_path} ({total} pages)")
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num - 1])
        out = Path(output_pattern.format(page=page_num, stem=input_path.stem))
        write_pdf(writer, out, overwrite)
        outputs.append(out)
    return outputs


def merge_pdfs(inputs: Iterable[Path], output: Path, overwrite: bool) -> Path:
    writer = PdfWriter()
    for path in inputs:
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)
    write_pdf(writer, output, overwrite)
    return output


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='PDF Split and Merge')
    sub = p.add_subparsers(dest='command', required=True)

    sp = sub.add_parser('split', help='Split a PDF into separate pages or selected pages')
    sp.add_argument('input', type=Path)
    sp.add_argument('--output-pattern', required=True, help='Output path pattern, must include {page}')
    sp.add_argument('--pages', help='Comma-separated page list/ranges, e.g. 1,3-5')
    sp.add_argument('--overwrite', action='store_true')

    mp = sub.add_parser('merge', help='Merge PDFs into one file')
    mp.add_argument('inputs', nargs='+', type=Path)
    mp.add_argument('--output', required=True, type=Path)
    mp.add_argument('--overwrite', action='store_true')

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == 'split':
            pages = parse_pages(args.pages) if args.pages else None
            outs = split_pdf(args.input, args.output_pattern, pages, args.overwrite)
            for o in outs:
                print(o)
        elif args.command == 'merge':
            out = merge_pdfs(args.inputs, args.output, args.overwrite)
            print(out)
        return 0
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
