import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from pypdf import PdfReader, PdfWriter


@dataclass
class PageRef:
    source: Path
    page_number: int  # 1-based


def eprint(*args):
    print(*args, file=sys.stderr)


def parse_range_spec(spec: str) -> List[int]:
    pages: List[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            start = int(a)
            end = int(b)
            step = 1 if end >= start else -1
            pages.extend(list(range(start, end + step, step)))
        else:
            pages.append(int(part))
    return pages


def normalize_pages(pages: Sequence[int], total: int) -> List[int]:
    out = []
    for p in pages:
        if p < 1 or p > total:
            raise ValueError(f"page {p} out of range 1..{total}")
        out.append(p)
    return out


def default_output_name(input_path: Path, suffix: str) -> Path:
    return input_path.with_name(f"{input_path.stem}_{suffix}.pdf")


def read_pdf(path: Path) -> PdfReader:
    if not path.exists():
        raise FileNotFoundError(f"source file not found: {path}")
    return PdfReader(str(path))


def write_pdf(writer: PdfWriter, out: Path, overwrite: bool) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and not overwrite:
        raise FileExistsError(f"output exists: {out} (use --overwrite)")
    with open(out, "wb") as f:
        writer.write(f)


def cmd_split(args) -> int:
    src = Path(args.input)
    reader = read_pdf(src)
    total = len(reader.pages)
    ranges = []
    if args.ranges:
        for spec in args.ranges:
            ranges.extend(parse_range_spec(spec))
    else:
        # default: split into individual pages
        ranges = list(range(1, total + 1))

    pages = normalize_pages(ranges, total)
    if args.output:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = src.parent

    for idx, p in enumerate(pages, start=1):
        writer = PdfWriter()
        writer.add_page(reader.pages[p - 1])
        if args.output:
            out = out_dir / f"{src.stem}_split_{idx:03d}_p{p}.pdf"
        else:
            out = default_output_name(src, f"split_{idx:03d}_p{p}")
        write_pdf(writer, out, args.overwrite)
    return 0


def collect_pages(inputs: Sequence[str], ranges: Optional[Sequence[str]]) -> List[PageRef]:
    result: List[PageRef] = []
    if ranges and len(ranges) != len(inputs):
        raise ValueError("--ranges must be provided once per --input file")
    for i, inp in enumerate(inputs):
        path = Path(inp)
        reader = read_pdf(path)
        if ranges:
            pages = normalize_pages(parse_range_spec(ranges[i]), len(reader.pages))
        else:
            pages = list(range(1, len(reader.pages) + 1))
        for p in pages:
            result.append(PageRef(path, p))
    return result


def apply_rotations(writer: PdfWriter, rotations: Sequence[str], count: int) -> None:
    rot_map = {}
    for rot in rotations:
        page_s, deg_s = rot.split(":", 1)
        page = int(page_s)
        deg = int(deg_s)
        if deg not in (-90, 90, 180, 270, -270):
            raise ValueError("rotation must be one of -90, 90, 180, 270, -270")
        rot_map[page] = deg
    for i, page in enumerate(writer.pages, start=1):
        if i in rot_map:
            page.rotate(rot_map[i])


def cmd_merge(args) -> int:
    writer = PdfWriter()
    pages = collect_pages(args.inputs, args.ranges)
    for pref in pages:
        reader = read_pdf(pref.source)
        writer.add_page(reader.pages[pref.page_number - 1])
    if getattr(args, "rotate", None):
        apply_rotations(writer, args.rotate, len(writer.pages))
    out = Path(args.output)
    write_pdf(writer, out, args.overwrite)
    return 0


def cmd_extract(args) -> int:
    return cmd_merge(args)


def cmd_interleave(args) -> int:
    inputs = [Path(p) for p in args.inputs]
    readers = [read_pdf(p) for p in inputs]
    counts = [len(r.pages) for r in readers]
    if args.ranges:
        ranges = [parse_range_spec(r) for r in args.ranges]
        if len(ranges) != len(inputs):
            raise ValueError("--ranges must be provided once per --input file")
    else:
        ranges = [list(range(1, c + 1)) for c in counts]
    maxlen = max(len(r) for r in ranges)
    writer = PdfWriter()
    for i in range(maxlen):
        for src_idx, path in enumerate(inputs):
            if i < len(ranges[src_idx]):
                p = ranges[src_idx][i]
                if p < 1 or p > counts[src_idx]:
                    raise ValueError(f"page {p} out of range for {path}")
                writer.add_page(readers[src_idx].pages[p - 1])
            elif not args.stop_when_exhausted:
                continue
    write_pdf(writer, Path(args.output), args.overwrite)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pdfsplitmerge", description="Local PDF split and merge tool")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("split", help="split a PDF into page files")
    p.add_argument("input")
    p.add_argument("--ranges", nargs="*", help="page ranges, e.g. 1-3 5 7-9")
    p.add_argument("--output", help="output directory for split files")
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(func=cmd_split)

    p = sub.add_parser("merge", help="merge PDFs or selected page ranges")
    p.add_argument("--inputs", nargs="+", required=True)
    p.add_argument("--ranges", nargs="*")
    p.add_argument("--rotate", nargs="*", default=[])
    p.add_argument("--output", required=True)
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser("extract", help="extract pages from a PDF")
    p.add_argument("--inputs", nargs="+", required=True)
    p.add_argument("--ranges", nargs="*")
    p.add_argument("--output", required=True)
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("interleave", help="alternate pages from multiple PDFs")
    p.add_argument("--inputs", nargs="+", required=True)
    p.add_argument("--ranges", nargs="*")
    p.add_argument("--output", required=True)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--stop-when-exhausted", action="store_true", default=False)
    p.set_defaults(func=cmd_interleave)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        eprint(f"error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
