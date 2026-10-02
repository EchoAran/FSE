import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

from pypdf import PdfReader, PdfWriter


@dataclass
class PageSpec:
    source: Optional[str]
    page: Optional[int]
    rotate: int = 0
    include: bool = True
    repeat: int = 1


@dataclass
class Workspace:
    sources: List[str]
    pages: List[PageSpec]
    operation: str = "merge"
    output: Optional[str] = None

    def to_json(self):
        return json.dumps({
            "sources": self.sources,
            "pages": [asdict(p) for p in self.pages],
            "operation": self.operation,
            "output": self.output,
        }, indent=2)

    @staticmethod
    def from_json(text: str):
        data = json.loads(text)
        return Workspace(
            sources=data.get("sources", []),
            pages=[PageSpec(**p) for p in data.get("pages", [])],
            operation=data.get("operation", "merge"),
            output=data.get("output"),
        )


def _parse_page_ranges(spec: str):
    result = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start, end = int(a), int(b)
            step = 1 if end >= start else -1
            result.extend(range(start, end + step, step))
        else:
            result.append(int(part))
    return result


def _safe_output_name(input_path: str, suffix: str):
    p = Path(input_path)
    return str(p.with_name(f"{p.stem}_{suffix}.pdf"))


def _load_reader(path: str):
    try:
        return PdfReader(path)
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF '{path}': {e}") from e


def cmd_merge(args):
    writer = PdfWriter()
    for source in args.inputs:
        reader = _load_reader(source)
        pages = range(len(reader.pages))
        if args.pages:
            pages = [p - 1 for p in _parse_page_ranges(args.pages)]
        for i in pages:
            if i < 0 or i >= len(reader.pages):
                raise SystemExit(f"Page {i+1} out of range for {source}")
            page = reader.pages[i]
            if args.rotate:
                page.rotate(args.rotate)
            writer.add_page(page)
    out = args.output or _safe_output_name(args.inputs[0], "merged")
    with open(out, "wb") as f:
        writer.write(f)
    print(out)
    return 0


def cmd_split(args):
    source = args.input
    reader = _load_reader(source)
    boundaries = sorted(set(_parse_page_ranges(args.boundaries))) if args.boundaries else []
    outdir = Path(args.output_dir or Path(source).parent)
    outdir.mkdir(parents=True, exist_ok=True)
    start = 1
    outputs = []
    all_pages = list(range(1, len(reader.pages) + 1))
    chunks = []
    if boundaries:
        for b in boundaries:
            chunks.append((start, b))
            start = b + 1
        if start <= len(reader.pages):
            chunks.append((start, len(reader.pages)))
    else:
        chunks.append((1, len(reader.pages)))
    for idx, (a, b) in enumerate(chunks, 1):
        writer = PdfWriter()
        for p in range(a - 1, b):
            writer.add_page(reader.pages[p])
        out = outdir / f"{Path(source).stem}_split_{idx:02d}_{a}-{b}.pdf"
        with open(out, "wb") as f:
            writer.write(f)
        outputs.append(str(out))
    print("\n".join(outputs))
    return 0


def cmd_preview(args):
    if args.input:
        reader = _load_reader(args.input)
        for i, page in enumerate(reader.pages, 1):
            mediabox = page.mediabox
            print(json.dumps({
                "page": i,
                "source": args.input,
                "width": float(mediabox.width),
                "height": float(mediabox.height),
            }))
        return 0
    if args.workspace:
        ws = Workspace.from_json(Path(args.workspace).read_text())
        print(ws.to_json())
        return 0
    raise SystemExit("preview requires --input or --workspace")


def cmd_workspace_save(args):
    ws = Workspace(sources=args.inputs, pages=[], operation=args.operation, output=args.output)
    Path(args.file).write_text(ws.to_json())
    print(args.file)
    return 0


def cmd_workspace_run(args):
    ws = Workspace.from_json(Path(args.file).read_text())
    if ws.operation == "merge":
        merge_args = argparse.Namespace(inputs=ws.sources, pages=None, rotate=0, output=ws.output)
        return cmd_merge(merge_args)
    raise SystemExit(f"Unsupported workspace operation: {ws.operation}")


def build_parser():
    p = argparse.ArgumentParser(prog="pdfsplitmerge", description="Local PDF split and merge tool")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("merge")
    m.add_argument("inputs", nargs="+")
    m.add_argument("--pages")
    m.add_argument("--rotate", type=int, default=0)
    m.add_argument("--output")
    m.set_defaults(func=cmd_merge)

    s = sub.add_parser("split")
    s.add_argument("input")
    s.add_argument("--boundaries", help="Page boundaries, e.g. 2,5")
    s.add_argument("--output-dir")
    s.set_defaults(func=cmd_split)

    pr = sub.add_parser("preview")
    pr.add_argument("--input")
    pr.add_argument("--workspace")
    pr.set_defaults(func=cmd_preview)

    ws = sub.add_parser("workspace-save")
    ws.add_argument("file")
    ws.add_argument("--operation", default="merge")
    ws.add_argument("--output")
    ws.add_argument("inputs", nargs="*")
    ws.set_defaults(func=cmd_workspace_save)

    wr = sub.add_parser("workspace-run")
    wr.add_argument("file")
    wr.set_defaults(func=cmd_workspace_run)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
