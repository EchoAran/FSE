from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Sequence

from pypdf import PdfReader, PdfWriter


@dataclass
class OperationResult:
    output_files: List[str]
    warnings: List[str]


def _reader(path: str) -> PdfReader:
    return PdfReader(path)


def split_pdf(input_path: str, output_dir: str) -> OperationResult:
    reader = _reader(input_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    output_files = []
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = out / f"{Path(input_path).stem}_page_{i}.pdf"
        with open(out_path, 'wb') as f:
            writer.write(f)
        output_files.append(str(out_path))
    return OperationResult(output_files, [])


def extract_pages(input_path: str, pages: Sequence[int], output_path: str) -> OperationResult:
    reader = _reader(input_path)
    writer = PdfWriter()
    warnings = []
    for p in pages:
        idx = p - 1
        if idx < 0 or idx >= len(reader.pages):
            warnings.append(f"Skipped invalid page {p}")
            continue
        writer.add_page(reader.pages[idx])
    with open(output_path, 'wb') as f:
        writer.write(f)
    return OperationResult([output_path], warnings)


def merge_pdfs(inputs: Sequence[str], output_path: str) -> OperationResult:
    writer = PdfWriter()
    warnings = []
    for path in inputs:
        try:
            reader = _reader(path)
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            warnings.append(f"Skipped {path}: {e}")
    with open(output_path, 'wb') as f:
        writer.write(f)
    return OperationResult([output_path], warnings)


def rotate_pages(input_path: str, rotations: dict[int, int], output_path: str) -> OperationResult:
    reader = _reader(input_path)
    writer = PdfWriter()
    for i, page in enumerate(reader.pages, start=1):
        if i in rotations:
            page.rotate(rotations[i])
        writer.add_page(page)
    with open(output_path, 'wb') as f:
        writer.write(f)
    return OperationResult([output_path], [])


def reorder_pages(input_path: str, order: Sequence[int], output_path: str) -> OperationResult:
    reader = _reader(input_path)
    writer = PdfWriter()
    warnings = []
    for p in order:
        idx = p - 1
        if 0 <= idx < len(reader.pages):
            writer.add_page(reader.pages[idx])
        else:
            warnings.append(f"Skipped invalid page {p}")
    with open(output_path, 'wb') as f:
        writer.write(f)
    return OperationResult([output_path], warnings)


def interleave_pdfs(inputs: Sequence[str], output_path: str) -> OperationResult:
    readers = []
    for p in inputs:
        readers.append(_reader(p))
    writer = PdfWriter()
    max_len = max((len(r.pages) for r in readers), default=0)
    for i in range(max_len):
        for r in readers:
            if i < len(r.pages):
                writer.add_page(r.pages[i])
    with open(output_path, 'wb') as f:
        writer.write(f)
    return OperationResult([output_path], [])


def save_workspace(data: dict, path: str) -> None:
    Path(path).write_text(json.dumps(data, indent=2), encoding='utf-8')


def load_workspace(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def result_to_dict(result: OperationResult) -> dict:
    return asdict(result)
