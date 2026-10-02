#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from pypdf import PdfReader, PdfWriter
except Exception as exc:  # pragma: no cover
    print("ERROR: pypdf is required. Install it with 'pip install pypdf'.", file=sys.stderr)
    raise


VERSION = "1.0"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse_page_spec(spec: str) -> List[int]:
    pages = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start = int(a)
            end = int(b)
            if start <= end:
                pages.extend(range(start, end + 1))
            else:
                pages.extend(range(start, end - 1, -1))
        else:
            pages.append(int(part))
    return pages


def natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


@dataclass
class Entry:
    source: str
    pages: Optional[List[int]] = None
    rotate: int = 0


@dataclass
class Workspace:
    entries: List[Entry]
    output: Optional[str] = None
    mode: str = "merge"

    @staticmethod
    def load(path: Path) -> "Workspace":
        data = json.loads(path.read_text(encoding='utf-8'))
        entries = [Entry(**item) for item in data.get('entries', [])]
        return Workspace(entries=entries, output=data.get('output'), mode=data.get('mode', 'merge'))

    def save(self, path: Path):
        data = {
            'entries': [asdict(e) for e in self.entries],
            'output': self.output,
            'mode': self.mode,
        }
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def read_pdf(path: Path):
    try:
        return PdfReader(str(path))
    except Exception as exc:
        raise RuntimeError(f"Failed to read '{path}': {exc}") from exc


def apply_rotation(page, rotate: int):
    if rotate % 360:
        page.rotate_clockwise(rotate % 360) if rotate > 0 else page.rotate_counter_clockwise((-rotate) % 360)


def select_pages(reader, pages: Optional[List[int]]):
    if pages is None:
        return list(range(1, len(reader.pages) + 1))
    return pages


def build_writer_from_entries(entries: List[Entry]) -> PdfWriter:
    writer = PdfWriter()
    for entry in entries:
        reader = read_pdf(Path(entry.source))
        for pageno in select_pages(reader, entry.pages):
            if pageno < 1 or pageno > len(reader.pages):
                raise RuntimeError(f"Page {pageno} out of range for '{entry.source}'")
            page = reader.pages[pageno - 1]
            page_copy = page
            apply_rotation(page_copy, entry.rotate)
            writer.add_page(page_copy)
    return writer


def write_pdf(writer: PdfWriter, output: Path, overwrite: bool):
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not overwrite:
        raise RuntimeError(f"Output file exists: {output}")
    with open(output, 'wb') as f:
        writer.write(f)


def cmd_merge(args):
    entries = [Entry(source=s) for s in args.inputs]
    writer = build_writer_from_entries(entries)
    out = Path(args.output or default_output_name(args.inputs, 'merged'))
    write_pdf(writer, out, args.overwrite)
    print(out)


def cmd_split(args):
    src = Path(args.input)
    reader = read_pdf(src)
    base = src.stem
    pages = len(reader.pages)
    boundaries = sorted(set(parse_page_spec(args.after))) if args.after else []
    groups = []
    start = 1
    for b in boundaries:
        if b < start or b >= pages:
            continue
        groups.append((start, b))
        start = b + 1
    groups.append((start, pages))
    outputs = []
    for i, (a, b) in enumerate(groups, 1):
        writer = PdfWriter()
        for p in range(a, b + 1):
            writer.add_page(reader.pages[p - 1])
        out = Path(args.output_dir) / f"{base}_split_{i:02d}_{a}-{b}.pdf"
        write_pdf(writer, out, args.overwrite)
        outputs.append(str(out))
    print("\n".join(outputs))


def cmd_extract(args):
    entry = Entry(source=args.input, pages=parse_page_spec(args.pages))
    writer = build_writer_from_entries([entry])
    out = Path(args.output or default_output_name([args.input], 'extracted'))
    write_pdf(writer, out, args.overwrite)
    print(out)


def cmd_rotate(args):
    entry = Entry(source=args.input, rotate=args.degrees)
    writer = build_writer_from_entries([entry])
    out = Path(args.output or default_output_name([args.input], 'rotated'))
    write_pdf(writer, out, args.overwrite)
    print(out)


def interleave_reads(sources: List[str], pattern: List[int], stop_at_shortest: bool):
    readers = [read_pdf(Path(s)) for s in sources]
    maxpages = max(len(r.pages) for r in readers)
    result = []
    for i in range(maxpages):
        for idx in pattern:
            r = readers[idx]
            if i < len(r.pages):
                result.append((sources[idx], i + 1, r.pages[i]))
            elif stop_at_shortest:
                return result
    return result


def cmd_interleave(args):
    pattern = [int(x) - 1 for x in args.pattern.split(',')]
    if any(i < 0 or i >= len(args.inputs) for i in pattern):
        raise RuntimeError("Pattern references invalid source index")
    items = interleave_reads(args.inputs, pattern, args.stop_at_shortest)
    writer = PdfWriter()
    for _, _, page in items:
        writer.add_page(page)
    out = Path(args.output or default_output_name(args.inputs, 'interleaved'))
    write_pdf(writer, out, args.overwrite)
    print(out)


def cmd_preview(args):
    if args.mode == 'merge':
        entries = [Entry(source=s) for s in args.inputs]
        desc = []
        for entry in entries:
            reader = read_pdf(Path(entry.source))
            desc.extend([f"{entry.source}: page {i}" for i in range(1, len(reader.pages) + 1)])
        print("\n".join(desc))
    else:
        src = Path(args.input)
        reader = read_pdf(src)
        print(f"{src} pages: 1-{len(reader.pages)}")


def default_output_name(inputs: List[str], op: str) -> str:
    stem = Path(inputs[0]).stem if inputs else 'output'
    return f"{stem}_{op}.pdf"


def cmd_workspace_save(args):
    ws = Workspace(entries=[Entry(source=s) for s in args.inputs], output=args.output, mode=args.mode)
    ws.save(Path(args.file))
    print(args.file)


def cmd_workspace_run(args):
    ws = Workspace.load(Path(args.file))
    if ws.mode == 'merge':
        writer = build_writer_from_entries(ws.entries)
    else:
        raise RuntimeError(f"Unsupported workspace mode: {ws.mode}")
    out = Path(args.output or ws.output or default_output_name([e.source for e in ws.entries], 'merged'))
    write_pdf(writer, out, args.overwrite)
    print(out)


def main(argv=None):
    parser = argparse.ArgumentParser(prog='pdfsplitmerge', description='PDF Split and Merge tool')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('merge')
    p.add_argument('inputs', nargs='+')
    p.add_argument('-o', '--output')
    p.add_argument('--overwrite', action='store_true')
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser('split')
    p.add_argument('input')
    p.add_argument('--after', help='Split after these pages, e.g. 2,5-7')
    p.add_argument('--output-dir', default='.')
    p.add_argument('--overwrite', action='store_true')
    p.set_defaults(func=cmd_split)

    p = sub.add_parser('extract')
    p.add_argument('input')
    p.add_argument('pages')
    p.add_argument('-o', '--output')
    p.add_argument('--overwrite', action='store_true')
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser('rotate')
    p.add_argument('input')
    p.add_argument('degrees', type=int, choices=[-270, -180, -90, 90, 180, 270])
    p.add_argument('-o', '--output')
    p.add_argument('--overwrite', action='store_true')
    p.set_defaults(func=cmd_rotate)

    p = sub.add_parser('interleave')
    p.add_argument('inputs', nargs='+')
    p.add_argument('--pattern', required=True)
    p.add_argument('--stop-at-shortest', action='store_true')
    p.add_argument('-o', '--output')
    p.add_argument('--overwrite', action='store_true')
    p.set_defaults(func=cmd_interleave)

    p = sub.add_parser('preview')
    p.add_argument('mode', choices=['merge', 'split'])
    p.add_argument('inputs', nargs='*')
    p.add_argument('--input')
    p.set_defaults(func=cmd_preview)

    p = sub.add_parser('workspace-save')
    p.add_argument('file')
    p.add_argument('inputs', nargs='+')
    p.add_argument('-o', '--output')
    p.add_argument('--mode', default='merge')
    p.set_defaults(func=cmd_workspace_save)

    p = sub.add_parser('workspace-run')
    p.add_argument('file')
    p.add_argument('-o', '--output')
    p.add_argument('--overwrite', action='store_true')
    p.set_defaults(func=cmd_workspace_run)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except Exception as exc:
        eprint(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
