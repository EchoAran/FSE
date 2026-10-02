import argparse
import os
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def _parse_page_specs(specs, total_pages):
    pages = []
    for spec in specs:
        if "-" in spec:
            start_s, end_s = spec.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start < 1 or end < 1 or start > end:
                raise ValueError(f"Invalid page range: {spec}")
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(spec))
    for p in pages:
        if p < 1 or p > total_pages:
            raise ValueError(f"Page out of range: {p}")
    return pages


def _ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def _write_pdf(writer: PdfWriter, output: Path, overwrite: bool):
    if output.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {output}")
    _ensure_parent(output)
    with open(output, "wb") as f:
        writer.write(f)


def cmd_split(args):
    reader = PdfReader(args.input)
    if args.pages:
        pages = _parse_page_specs(args.pages, len(reader.pages))
    else:
        pages = list(range(1, len(reader.pages) + 1))
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    created = []
    for page_num in pages:
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num - 1])
        output = outdir / f"{Path(args.input).stem}_p{page_num}.pdf"
        _write_pdf(writer, output, args.overwrite)
        created.append(str(output))
    return 0, created


def cmd_merge(args):
    writer = PdfWriter()
    for input_path in args.inputs:
        reader = PdfReader(input_path)
        for page in reader.pages:
            writer.add_page(page)
    output = Path(args.output)
    _write_pdf(writer, output, args.overwrite)
    return 0, [str(output)]


def build_parser():
    parser = argparse.ArgumentParser(prog="pdfsplitmerge", description="PDF Split and Merge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_split = sub.add_parser("split", help="Split a PDF into page files")
    p_split.add_argument("input")
    p_split.add_argument("-o", "--output-dir", required=True)
    p_split.add_argument("--pages", nargs="*", help="Pages/ranges like 1 3 5-7")
    p_split.add_argument("--overwrite", action="store_true")
    p_split.set_defaults(func=cmd_split)

    p_merge = sub.add_parser("merge", help="Merge PDF files")
    p_merge.add_argument("inputs", nargs="+")
    p_merge.add_argument("-o", "--output", required=True)
    p_merge.add_argument("--overwrite", action="store_true")
    p_merge.set_defaults(func=cmd_merge)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        code, outputs = args.func(args)
        for item in outputs:
            print(item)
        return code
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
