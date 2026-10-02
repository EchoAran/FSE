from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

from pypdf import PdfReader, PdfWriter


@dataclass(frozen=True)
class OperationResult:
    outputs: List[Path]


def _parse_pages(spec: str, page_count: int) -> List[int]:
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
            pages.extend(range(start - 1, min(end, page_count)))
        else:
            page = int(part)
            if page < 1 or page > page_count:
                raise ValueError(f'page out of range: {page}')
            pages.append(page - 1)
    if not pages:
        raise ValueError('no pages selected')
    return pages


def split_pdf(source: Path, output_dir: Path, prefix: str = 'page') -> OperationResult:
    reader = PdfReader(str(source))
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: List[Path] = []
    for idx, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out = output_dir / f'{prefix}_{idx:03d}.pdf'
        with out.open('wb') as f:
            writer.write(f)
        outputs.append(out)
    return OperationResult(outputs)


def extract_pages(source: Path, output: Path, pages: str) -> OperationResult:
    reader = PdfReader(str(source))
    writer = PdfWriter()
    for i in _parse_pages(pages, len(reader.pages)):
        writer.add_page(reader.pages[i])
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as f:
        writer.write(f)
    return OperationResult([output])


def rotate_pages(source: Path, output: Path, rotation: int, pages: str | None = None) -> OperationResult:
    if rotation % 90 != 0:
        raise ValueError('rotation must be a multiple of 90')
    reader = PdfReader(str(source))
    writer = PdfWriter()
    selected = set(range(len(reader.pages))) if pages is None else set(_parse_pages(pages, len(reader.pages)))
    for idx, page in enumerate(reader.pages):
        if idx in selected:
            page = page.rotate(rotation)
        writer.add_page(page)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as f:
        writer.write(f)
    return OperationResult([output])


def reorder_pages(source: Path, output: Path, order: str) -> OperationResult:
    reader = PdfReader(str(source))
    writer = PdfWriter()
    for idx in _parse_pages(order, len(reader.pages)):
        writer.add_page(reader.pages[idx])
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as f:
        writer.write(f)
    return OperationResult([output])


def merge_pdfs(inputs: Sequence[Path], output: Path) -> OperationResult:
    writer = PdfWriter()
    for src in inputs:
        reader = PdfReader(str(src))
        for page in reader.pages:
            writer.add_page(page)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as f:
        writer.write(f)
    return OperationResult([output])


def alternate_merge(inputs: Sequence[Path], output: Path) -> OperationResult:
    readers = [PdfReader(str(p)) for p in inputs]
    max_pages = max((len(r.pages) for r in readers), default=0)
    writer = PdfWriter()
    for page_idx in range(max_pages):
        for reader in readers:
            if page_idx < len(reader.pages):
                writer.add_page(reader.pages[page_idx])
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as f:
        writer.write(f)
    return OperationResult([output])
