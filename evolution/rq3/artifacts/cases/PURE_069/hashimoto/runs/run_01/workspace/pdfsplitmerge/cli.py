import argparse
import os
from pathlib import Path
from typing import List

from pypdf import PdfReader, PdfWriter


def _parse_pages(spec: str, total_pages: int) -> List[int]:
    pages: List[int] = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start_s, end_s = part.split('-', 1)
            start = int(start_s)
            end = int(end_s)
            if start < 1 or end < start:
                raise ValueError(f'invalid page range: {part}')
            pages.extend(range(start, end + 1))
        else:
            page = int(part)
            if page < 1:
                raise ValueError(f'invalid page number: {page}')
            pages.append(page)
    for page in pages:
        if page > total_pages:
            raise ValueError(f'page {page} exceeds total pages {total_pages}')
    return pages


def split_pdf(input_path: Path, output_dir: Path, pages_per_file: int, prefix: str, overwrite: bool) -> List[Path]:
    reader = PdfReader(str(input_path))
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: List[Path] = []
    total = len(reader.pages)
    for idx, start in enumerate(range(0, total, pages_per_file), start=1):
        writer = PdfWriter()
        for page in reader.pages[start:start + pages_per_file]:
            writer.add_page(page)
        out = output_dir / f'{prefix}_{idx:03d}.pdf'
        if out.exists() and not overwrite:
            raise FileExistsError(f'{out} exists; use --overwrite')
        with open(out, 'wb') as f:
            writer.write(f)
        outputs.append(out)
    return outputs


def merge_pdfs(inputs: List[Path], output: Path, overwrite: bool) -> Path:
    writer = PdfWriter()
    for inp in inputs:
        reader = PdfReader(str(inp))
        for page in reader.pages:
            writer.add_page(page)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not overwrite:
        raise FileExistsError(f'{output} exists; use --overwrite')
    with open(output, 'wb') as f:
        writer.write(f)
    return output


def extract_pages(input_path: Path, output: Path, pages: str, overwrite: bool) -> Path:
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    selected = _parse_pages(pages, len(reader.pages))
    for p in selected:
        writer.add_page(reader.pages[p - 1])
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not overwrite:
        raise FileExistsError(f'{output} exists; use --overwrite')
    with open(output, 'wb') as f:
        writer.write(f)
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='pdfsplitmerge', description='PDF split and merge tool')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_split = sub.add_parser('split', help='Split a PDF into multiple files')
    p_split.add_argument('input')
    p_split.add_argument('--output-dir', required=True)
    p_split.add_argument('--pages-per-file', type=int, default=1)
    p_split.add_argument('--prefix', default='split')
    p_split.add_argument('--overwrite', action='store_true')

    p_merge = sub.add_parser('merge', help='Merge PDFs')
    p_merge.add_argument('inputs', nargs='+')
    p_merge.add_argument('--output', required=True)
    p_merge.add_argument('--overwrite', action='store_true')

    p_extract = sub.add_parser('extract', help='Extract selected pages')
    p_extract.add_argument('input')
    p_extract.add_argument('--pages', required=True)
    p_extract.add_argument('--output', required=True)
    p_extract.add_argument('--overwrite', action='store_true')

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.cmd == 'split':
            split_pdf(Path(args.input), Path(args.output_dir), args.pages_per_file, args.prefix, args.overwrite)
        elif args.cmd == 'merge':
            merge_pdfs([Path(p) for p in args.inputs], Path(args.output), args.overwrite)
        elif args.cmd == 'extract':
            extract_pages(Path(args.input), Path(args.output), args.pages, args.overwrite)
        return 0
    except Exception as e:
        parser.error(str(e))
        return 2
