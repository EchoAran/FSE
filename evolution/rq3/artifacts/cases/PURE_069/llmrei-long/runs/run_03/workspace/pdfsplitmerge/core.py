from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Sequence

from pypdf import PdfReader, PdfWriter


def _reader(path: str | Path) -> PdfReader:
    return PdfReader(str(path))


def _writer_from_pages(pages) -> PdfWriter:
    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)
    return writer


def split_pdf(input_path: str | Path, output_dir: str | Path) -> list[str]:
    reader = _reader(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    stem = Path(input_path).stem
    for idx, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out = output_dir / f"{stem}_page_{idx}.pdf"
        with out.open("wb") as f:
            writer.write(f)
        outputs.append(str(out))
    return outputs


def merge_pdfs(input_paths: Sequence[str | Path], output_path: str | Path) -> str:
    writer = PdfWriter()
    for path in input_paths:
        reader = _reader(path)
        for page in reader.pages:
            writer.add_page(page)
    with Path(output_path).open("wb") as f:
        writer.write(f)
    return str(output_path)


def extract_pages(input_path: str | Path, pages: Sequence[int], output_path: str | Path) -> str:
    reader = _reader(input_path)
    writer = PdfWriter()
    for p in pages:
        writer.add_page(reader.pages[p - 1])
    with Path(output_path).open("wb") as f:
        writer.write(f)
    return str(output_path)


def rotate_pages(input_path: str | Path, rotations: dict[int, int], output_path: str | Path) -> str:
    reader = _reader(input_path)
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        if idx in rotations:
            page.rotate(rotations[idx])
        writer.add_page(page)
    with Path(output_path).open("wb") as f:
        writer.write(f)
    return str(output_path)


def reorder_pages(input_path: str | Path, order: Sequence[int], output_path: str | Path) -> str:
    reader = _reader(input_path)
    writer = PdfWriter()
    for p in order:
        writer.add_page(reader.pages[p - 1])
    with Path(output_path).open("wb") as f:
        writer.write(f)
    return str(output_path)


def alternate_pages(inputs: Sequence[str | Path], output_path: str | Path) -> str:
    readers = [_reader(path) for path in inputs]
    max_len = max((len(r.pages) for r in readers), default=0)
    writer = PdfWriter()
    for i in range(max_len):
        for reader in readers:
            if i < len(reader.pages):
                writer.add_page(reader.pages[i])
    with Path(output_path).open("wb") as f:
        writer.write(f)
    return str(output_path)


def save_setup(setup: dict, output_path: str | Path) -> str:
    with Path(output_path).open("w", encoding="utf-8") as f:
        json.dump(setup, f, indent=2, sort_keys=True)
    return str(output_path)


def load_setup(input_path: str | Path) -> dict:
    with Path(input_path).open("r", encoding="utf-8") as f:
        return json.load(f)
