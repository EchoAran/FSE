#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


class PDFToolError(Exception):
    pass


def load_pdf(path: Path) -> PdfReader:
    if not path.exists():
        raise PDFToolError(f"Input file not found: {path}")
    try:
        return PdfReader(str(path))
    except Exception as e:
        raise PDFToolError(f"Failed to read PDF '{path}': {e}") from e


def save_writer(writer: PdfWriter, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as f:
        writer.write(f)


def split_pdf(input_path: Path, output_dir: Path, pages_per_file: int) -> list[str]:
    reader = load_pdf(input_path)
    outputs = []
    total = len(reader.pages)
    for start in range(0, total, pages_per_file):
        writer = PdfWriter()
        for i in range(start, min(start + pages_per_file, total)):
            writer.add_page(reader.pages[i])
        out = output_dir / f"{input_path.stem}_part_{start+1:03d}-{min(start+pages_per_file,total):03d}.pdf"
        save_writer(writer, out)
        outputs.append(str(out))
    return outputs


def merge_pdfs(inputs: list[Path], output: Path) -> None:
    writer = PdfWriter()
    for p in inputs:
        reader = load_pdf(p)
        for page in reader.pages:
            writer.add_page(page)
    save_writer(writer, output)


def extract_pages(input_path: Path, output: Path, pages: list[int]) -> None:
    reader = load_pdf(input_path)
    writer = PdfWriter()
    for page_num in pages:
        if page_num < 1 or page_num > len(reader.pages):
            raise PDFToolError(f"Page out of range: {page_num}")
        writer.add_page(reader.pages[page_num - 1])
    save_writer(writer, output)


def rotate_pages(input_path: Path, output: Path, pages: list[int], degrees: int) -> None:
    if degrees % 90 != 0:
        raise PDFToolError("Rotation must be a multiple of 90")
    reader = load_pdf(input_path)
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        if not pages or idx in pages:
            if degrees > 0:
                page.rotate(degrees)
            else:
                page.rotate(degrees)
        writer.add_page(page)
    save_writer(writer, output)


def reorder_pages(input_path: Path, output: Path, order: list[int]) -> None:
    reader = load_pdf(input_path)
    if sorted(order) != list(range(1, len(reader.pages) + 1)):
        raise PDFToolError("Order must include each page number exactly once")
    writer = PdfWriter()
    for page_num in order:
        writer.add_page(reader.pages[page_num - 1])
    save_writer(writer, output)


def parse_pages(spec: str) -> list[int]:
    pages = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='PDF split and merge tool')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('split')
    p.add_argument('input')
    p.add_argument('-o', '--output-dir', required=True)
    p.add_argument('--pages-per-file', type=int, default=1)

    p = sub.add_parser('merge')
    p.add_argument('inputs', nargs='+')
    p.add_argument('-o', '--output', required=True)

    p = sub.add_parser('extract')
    p.add_argument('input')
    p.add_argument('-o', '--output', required=True)
    p.add_argument('--pages', required=True, help='Comma-separated list or ranges, e.g. 1,3-5')

    p = sub.add_parser('rotate')
    p.add_argument('input')
    p.add_argument('-o', '--output', required=True)
    p.add_argument('--pages', default='', help='Pages to rotate, empty means all pages')
    p.add_argument('--degrees', type=int, required=True)

    p = sub.add_parser('reorder')
    p.add_argument('input')
    p.add_argument('-o', '--output', required=True)
    p.add_argument('--order', required=True, help='Comma-separated page order, e.g. 2,1,3')

    p = sub.add_parser('manifest')
    p.add_argument('-o', '--output', required=True)
    p.add_argument('files', nargs='*')

    args = parser.parse_args(argv)

    try:
        if args.cmd == 'split':
            out = split_pdf(Path(args.input), Path(args.output_dir), args.pages_per_file)
            print(json.dumps(out, indent=2))
        elif args.cmd == 'merge':
            merge_pdfs([Path(x) for x in args.inputs], Path(args.output))
        elif args.cmd == 'extract':
            extract_pages(Path(args.input), Path(args.output), parse_pages(args.pages))
        elif args.cmd == 'rotate':
            rotate_pages(Path(args.input), Path(args.output), parse_pages(args.pages) if args.pages else [], args.degrees)
        elif args.cmd == 'reorder':
            reorder_pages(Path(args.input), Path(args.output), parse_pages(args.order))
        elif args.cmd == 'manifest':
            Path(args.output).write_text(json.dumps({'files': args.files}, indent=2))
        return 0
    except PDFToolError as e:
        print(f'Error: {e}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
