from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Tuple

from pypdf import PdfReader, PdfWriter


class PDFSMError(Exception):
    pass


@dataclass
class PageRef:
    source: str
    page_number: int  # 1-based
    rotate: int = 0


@dataclass
class Project:
    inputs: List[str]
    pages: List[PageRef]
    output_dir: Optional[str] = None
    output_name: Optional[str] = None


def parse_page_ranges(spec: str) -> List[int]:
    pages: List[int] = []
    if not spec:
        raise PDFSMError("empty page range")
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start, end = int(a), int(b)
            if start <= 0 or end <= 0 or end < start:
                raise PDFSMError(f"invalid range: {part}")
            pages.extend(range(start, end + 1))
        else:
            p = int(part)
            if p <= 0:
                raise PDFSMError(f"invalid page: {part}")
            pages.append(p)
    if not pages:
        raise PDFSMError("no pages parsed")
    return pages


def normalize_rotation(rot: int) -> int:
    if rot % 90 != 0:
        raise PDFSMError("rotation must be a multiple of 90")
    return rot % 360


def safe_default_name(input_path: Path, operation: str) -> str:
    stem = input_path.stem
    return f"{stem}_{operation}.pdf"


def ensure_output_path(output: Optional[str], input_path: Path, operation: str) -> Path:
    if output:
        return Path(output)
    return input_path.with_name(safe_default_name(input_path, operation))


def read_pdf(path: Path) -> PdfReader:
    try:
        return PdfReader(str(path))
    except Exception as e:
        raise PDFSMError(f"failed to read '{path}': {e}") from e


def write_pdf(writer: PdfWriter, output: Path, overwrite: bool = False) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not overwrite:
        raise PDFSMError(f"output already exists: {output}")
    tmp = output.with_suffix(output.suffix + ".tmp")
    try:
        with open(tmp, "wb") as f:
            writer.write(f)
        os.replace(tmp, output)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def split_pdf(input_path: Path, ranges: List[Tuple[int, int]], output_dir: Optional[Path] = None, overwrite: bool = False) -> List[Path]:
    reader = read_pdf(input_path)
    outdir = output_dir or input_path.parent
    outputs: List[Path] = []
    for idx, (start, end) in enumerate(ranges, 1):
        writer = PdfWriter()
        for p in range(start, end + 1):
            if p < 1 or p > len(reader.pages):
                raise PDFSMError(f"page {p} out of range for {input_path} ({len(reader.pages)} pages)")
            writer.add_page(reader.pages[p - 1])
        out = outdir / f"{input_path.stem}_split_{idx}_{start}-{end}.pdf"
        write_pdf(writer, out, overwrite=overwrite)
        outputs.append(out)
    return outputs


def merge_pdfs(inputs: List[Path], output: Path, overwrite: bool = False) -> Path:
    writer = PdfWriter()
    for p in inputs:
        reader = read_pdf(p)
        for page in reader.pages:
            writer.add_page(page)
    write_pdf(writer, output, overwrite=overwrite)
    return output


def extract_pages(input_path: Path, pages: List[int], output: Path, overwrite: bool = False) -> Path:
    reader = read_pdf(input_path)
    writer = PdfWriter()
    for p in pages:
        if p < 1 or p > len(reader.pages):
            raise PDFSMError(f"page {p} out of range for {input_path} ({len(reader.pages)} pages)")
        writer.add_page(reader.pages[p - 1])
    write_pdf(writer, output, overwrite=overwrite)
    return output


def rotate_pages(input_path: Path, pages: List[int], direction: str, output: Path, overwrite: bool = False) -> Path:
    reader = read_pdf(input_path)
    writer = PdfWriter()
    delta = 90 if direction == "right" else -90
    for i, page in enumerate(reader.pages, 1):
        if i in pages:
            page.rotate(delta)
        writer.add_page(page)
    write_pdf(writer, output, overwrite=overwrite)
    return output


def interleave_pdfs(inputs: List[Path], output: Path, overwrite: bool = False) -> Path:
    readers = [read_pdf(p) for p in inputs]
    max_pages = max(len(r.pages) for r in readers)
    writer = PdfWriter()
    for i in range(max_pages):
        for r in readers:
            if i < len(r.pages):
                writer.add_page(r.pages[i])
    write_pdf(writer, output, overwrite=overwrite)
    return output


def save_project(project: Project, path: Path) -> Path:
    data = {
        "inputs": project.inputs,
        "pages": [asdict(p) for p in project.pages],
        "output_dir": project.output_dir,
        "output_name": project.output_name,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_project(path: Path) -> Project:
    data = json.loads(path.read_text(encoding="utf-8"))
    pages = [PageRef(**p) for p in data.get("pages", [])]
    return Project(inputs=data.get("inputs", []), pages=pages, output_dir=data.get("output_dir"), output_name=data.get("output_name"))
