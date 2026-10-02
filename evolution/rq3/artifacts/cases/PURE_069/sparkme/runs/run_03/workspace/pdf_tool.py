#!/usr/bin/env python3
import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

from pypdf import PdfReader, PdfWriter


@dataclass
class Operation:
    kind: str
    params: dict


@dataclass
class Workspace:
    inputs: List[str]
    operations: List[Operation]
    output: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps({
            "inputs": self.inputs,
            "operations": [{"kind": op.kind, "params": op.params} for op in self.operations],
            "output": self.output,
        }, indent=2)

    @staticmethod
    def from_json(text: str) -> "Workspace":
        data = json.loads(text)
        return Workspace(
            inputs=data.get("inputs", []),
            operations=[Operation(op["kind"], op.get("params", {})) for op in data.get("operations", [])],
            output=data.get("output"),
        )


def parse_pages(spec: str, total_pages: int) -> List[int]:
    pages = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start = int(a)
            end = int(b)
            step = 1 if end >= start else -1
            for n in range(start, end + step, step):
                pages.append(n)
        else:
            pages.append(int(part))
    out = []
    for p in pages:
        if p < 1 or p > total_pages:
            raise ValueError(f"page {p} out of range 1..{total_pages}")
        out.append(p - 1)
    return out


def load_reader(path: str) -> PdfReader:
    return PdfReader(path)


def write_pdf(writer: PdfWriter, output: str) -> None:
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'wb') as f:
        writer.write(f)


def cmd_split(args):
    reader = load_reader(args.input)
    total = len(reader.pages)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for i in range(total):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        write_pdf(writer, str(output_dir / f"page_{i+1}.pdf"))


def cmd_merge(args):
    writer = PdfWriter()
    for path in args.inputs:
        reader = load_reader(path)
        for page in reader.pages:
            writer.add_page(page)
    write_pdf(writer, args.output)


def cmd_extract(args):
    reader = load_reader(args.input)
    indices = parse_pages(args.pages, len(reader.pages))
    writer = PdfWriter()
    for idx in indices:
        writer.add_page(reader.pages[idx])
    write_pdf(writer, args.output)


def cmd_rotate(args):
    reader = load_reader(args.input)
    indices = parse_pages(args.pages, len(reader.pages))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i in indices:
            if args.degrees == 90:
                page.rotate(90)
            elif args.degrees == 180:
                page.rotate(180)
            elif args.degrees == 270:
                page.rotate(270)
            else:
                raise ValueError("degrees must be 90, 180, or 270")
        writer.add_page(page)
    write_pdf(writer, args.output)


def cmd_reorder(args):
    reader = load_reader(args.input)
    indices = parse_pages(args.order, len(reader.pages))
    writer = PdfWriter()
    for idx in indices:
        writer.add_page(reader.pages[idx])
    write_pdf(writer, args.output)


def cmd_interleave(args):
    readers = [load_reader(p) for p in args.inputs]
    max_pages = max(len(r.pages) for r in readers)
    writer = PdfWriter()
    for i in range(max_pages):
        for r in readers:
            if i < len(r.pages):
                writer.add_page(r.pages[i])
    write_pdf(writer, args.output)


def cmd_workspace_save(args):
    ws = Workspace(inputs=args.inputs, operations=[], output=args.output)
    Path(args.file).write_text(ws.to_json(), encoding='utf-8')


def cmd_workspace_load(args):
    ws = Workspace.from_json(Path(args.file).read_text(encoding='utf-8'))
    print(ws.to_json())


def main(argv=None):
    parser = argparse.ArgumentParser(prog='pdf-tool')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('split')
    p.add_argument('input')
    p.add_argument('output_dir')
    p.set_defaults(func=cmd_split)

    p = sub.add_parser('merge')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser('extract')
    p.add_argument('input')
    p.add_argument('pages', help='e.g. 1-3,5')
    p.add_argument('output')
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser('rotate')
    p.add_argument('input')
    p.add_argument('pages')
    p.add_argument('degrees', type=int)
    p.add_argument('output')
    p.set_defaults(func=cmd_rotate)

    p = sub.add_parser('reorder')
    p.add_argument('input')
    p.add_argument('order')
    p.add_argument('output')
    p.set_defaults(func=cmd_reorder)

    p = sub.add_parser('interleave')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')
    p.set_defaults(func=cmd_interleave)

    p = sub.add_parser('workspace-save')
    p.add_argument('file')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')
    p.set_defaults(func=cmd_workspace_save)

    p = sub.add_parser('workspace-load')
    p.add_argument('file')
    p.set_defaults(func=cmd_workspace_load)

    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except Exception as e:
        print(f'error: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
