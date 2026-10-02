#!/usr/bin/env python3
"""PDF Split and Merge CLI tool."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

from pypdf import PdfReader, PdfWriter


@dataclass
class Workspace:
    name: str
    steps: List[dict]


def _parse_pages(spec: str, total_pages: int) -> List[int]:
    pages: List[int] = []
    if not spec:
        return pages
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start < 1 or end < start:
                raise ValueError(f"Invalid page range: {part}")
            pages.extend(range(start, min(end, total_pages) + 1))
        else:
            page = int(part)
            if page < 1 or page > total_pages:
                raise ValueError(f"Invalid page number: {part}")
            pages.append(page)
    seen = set()
    result = []
    for p in pages:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def split_pdf(input_path: Path, output_dir: Path) -> None:
    reader = PdfReader(str(input_path))
    output_dir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out = output_dir / f"{input_path.stem}_page_{i}.pdf"
        with out.open("wb") as f:
            writer.write(f)


def merge_pdfs(inputs: List[Path], output_path: Path) -> None:
    writer = PdfWriter()
    for item in inputs:
        reader = PdfReader(str(item))
        for page in reader.pages:
            writer.add_page(page)
    with output_path.open("wb") as f:
        writer.write(f)


def extract_pages(input_path: Path, output_path: Path, pages_spec: str) -> None:
    reader = PdfReader(str(input_path))
    pages = _parse_pages(pages_spec, len(reader.pages))
    writer = PdfWriter()
    for page_num in pages:
        writer.add_page(reader.pages[page_num - 1])
    with output_path.open("wb") as f:
        writer.write(f)


def rotate_pages(input_path: Path, output_path: Path, degrees: int, pages_spec: str | None) -> None:
    reader = PdfReader(str(input_path))
    pages = set(_parse_pages(pages_spec, len(reader.pages))) if pages_spec else None
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        if pages is None or idx in pages:
            page.rotate(degrees)
        writer.add_page(page)
    with output_path.open("wb") as f:
        writer.write(f)


def reorder_pages(input_path: Path, output_path: Path, order_spec: str) -> None:
    reader = PdfReader(str(input_path))
    order = _parse_pages(order_spec, len(reader.pages))
    writer = PdfWriter()
    for page_num in order:
        writer.add_page(reader.pages[page_num - 1])
    with output_path.open("wb") as f:
        writer.write(f)


def alternate_pdfs(inputs: List[Path], output_path: Path) -> None:
    readers = [PdfReader(str(p)) for p in inputs]
    max_pages = max(len(r.pages) for r in readers)
    writer = PdfWriter()
    for i in range(max_pages):
        for reader in readers:
            if i < len(reader.pages):
                writer.add_page(reader.pages[i])
    with output_path.open("wb") as f:
        writer.write(f)


def save_workspace(path: Path, name: str, steps: List[dict]) -> None:
    ws = Workspace(name=name, steps=steps)
    path.write_text(json.dumps(asdict(ws), indent=2), encoding="utf-8")


def load_workspace(path: Path) -> Workspace:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Workspace(name=data["name"], steps=data["steps"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PDF Split and Merge")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("split")
    p.add_argument("input")
    p.add_argument("output_dir")

    p = sub.add_parser("merge")
    p.add_argument("inputs", nargs="+")
    p.add_argument("output")

    p = sub.add_parser("extract")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--pages", required=True)

    p = sub.add_parser("rotate")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--degrees", type=int, default=90)
    p.add_argument("--pages")

    p = sub.add_parser("reorder")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--order", required=True)

    p = sub.add_parser("alternate")
    p.add_argument("inputs", nargs="+")
    p.add_argument("output")

    p = sub.add_parser("workspace-save")
    p.add_argument("path")
    p.add_argument("--name", default="workspace")
    p.add_argument("--steps", default="[]")

    p = sub.add_parser("workspace-load")
    p.add_argument("path")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "split":
        split_pdf(Path(args.input), Path(args.output_dir))
    elif args.command == "merge":
        merge_pdfs([Path(p) for p in args.inputs], Path(args.output))
    elif args.command == "extract":
        extract_pages(Path(args.input), Path(args.output), args.pages)
    elif args.command == "rotate":
        rotate_pages(Path(args.input), Path(args.output), args.degrees, args.pages)
    elif args.command == "reorder":
        reorder_pages(Path(args.input), Path(args.output), args.order)
    elif args.command == "alternate":
        alternate_pdfs([Path(p) for p in args.inputs], Path(args.output))
    elif args.command == "workspace-save":
        save_workspace(Path(args.path), args.name, json.loads(args.steps))
    elif args.command == "workspace-load":
        ws = load_workspace(Path(args.path))
        print(json.dumps(asdict(ws), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
