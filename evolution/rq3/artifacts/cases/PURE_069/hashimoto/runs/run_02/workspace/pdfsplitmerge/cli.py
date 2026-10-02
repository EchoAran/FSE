import argparse
import json
import sys
from pathlib import Path
from typing import List

from pypdf import PdfReader, PdfWriter


def _parse_pages(spec: str, page_count: int) -> List[int]:
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
            for p in range(start, end + step, step):
                pages.append(p)
        else:
            pages.append(int(part))
    result = []
    seen = set()
    for p in pages:
        if p < 1 or p > page_count:
            raise ValueError(f"page {p} out of range 1..{page_count}")
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def _ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def _write_pdf(writer: PdfWriter, output: Path, overwrite: bool = False):
    if output.exists() and not overwrite:
        raise FileExistsError(f"Output exists: {output}")
    _ensure_parent(output)
    with output.open('wb') as f:
        writer.write(f)


def cmd_split(args):
    reader = PdfReader(args.input)
    outdir = Path(args.output_dir or args.workspace or '.')
    outdir.mkdir(parents=True, exist_ok=True)
    stem = Path(args.input).stem
    created = []
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        target = outdir / f"{stem}_page_{i:03d}.pdf"
        _write_pdf(writer, target, overwrite=args.overwrite)
        created.append(str(target))
    return created


def cmd_extract(args):
    reader = PdfReader(args.input)
    pages = _parse_pages(args.pages, len(reader.pages))
    writer = PdfWriter()
    for p in pages:
        writer.add_page(reader.pages[p - 1])
    output = Path(args.output)
    _write_pdf(writer, output, overwrite=args.overwrite)
    return [str(output)]


def cmd_merge(args):
    writer = PdfWriter()
    for src in args.inputs:
        reader = PdfReader(src)
        for page in reader.pages:
            writer.add_page(page)
    output = Path(args.output)
    _write_pdf(writer, output, overwrite=args.overwrite)
    return [str(output)]


def cmd_rotate(args):
    reader = PdfReader(args.input)
    pages = _parse_pages(args.pages, len(reader.pages)) if args.pages else list(range(1, len(reader.pages) + 1))
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        if idx in pages:
            page.rotate(int(args.degrees))
        writer.add_page(page)
    output = Path(args.output)
    _write_pdf(writer, output, overwrite=args.overwrite)
    return [str(output)]


def cmd_reorder(args):
    reader = PdfReader(args.input)
    pages = _parse_pages(args.order, len(reader.pages))
    writer = PdfWriter()
    for p in pages:
        writer.add_page(reader.pages[p - 1])
    output = Path(args.output)
    _write_pdf(writer, output, overwrite=args.overwrite)
    return [str(output)]


def cmd_alternate(args):
    readers = [PdfReader(src) for src in args.inputs]
    max_pages = max(len(r.pages) for r in readers)
    writer = PdfWriter()
    for i in range(max_pages):
        for r in readers:
            if i < len(r.pages):
                writer.add_page(r.pages[i])
    output = Path(args.output)
    _write_pdf(writer, output, overwrite=args.overwrite)
    return [str(output)]


def cmd_workspace_init(args):
    path = Path(args.path)
    path.mkdir(parents=True, exist_ok=True)
    cfg = {"default_output_dir": args.default_output_dir}
    (path / "workspace.json").write_text(json.dumps(cfg, indent=2))
    return [str(path / "workspace.json")]


def cmd_workspace_run(args):
    cfg = json.loads(Path(args.workspace).joinpath('workspace.json').read_text())
    cmd = [args.operation]
    if args.operation in {'split', 'merge', 'extract', 'rotate', 'reorder', 'alternate'}:
        cmd.extend(args.op_args)
    return run_command(cmd, default_output_dir=cfg.get('default_output_dir'))


def run_command(argv, default_output_dir=None):
    parser = build_parser(default_output_dir)
    args = parser.parse_args(argv)
    if not hasattr(args, 'func'):
        parser.print_help()
        return 2
    try:
        outputs = args.func(args)
        for o in outputs:
            print(o)
        return 0
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


def build_parser(default_output_dir=None):
    p = argparse.ArgumentParser(prog='pdfsplitmerge', description='PDF split and merge utility')
    sub = p.add_subparsers(dest='cmd')

    sp = sub.add_parser('split')
    sp.add_argument('input')
    sp.add_argument('--output-dir', default=default_output_dir)
    sp.add_argument('--workspace')
    sp.add_argument('--overwrite', action='store_true')
    sp.set_defaults(func=cmd_split)

    sp = sub.add_parser('extract')
    sp.add_argument('input')
    sp.add_argument('--pages', required=True)
    sp.add_argument('--output', required=True)
    sp.add_argument('--overwrite', action='store_true')
    sp.set_defaults(func=cmd_extract)

    sp = sub.add_parser('merge')
    sp.add_argument('inputs', nargs='+')
    sp.add_argument('--output', required=True)
    sp.add_argument('--overwrite', action='store_true')
    sp.set_defaults(func=cmd_merge)

    sp = sub.add_parser('rotate')
    sp.add_argument('input')
    sp.add_argument('--degrees', required=True)
    sp.add_argument('--pages')
    sp.add_argument('--output', required=True)
    sp.add_argument('--overwrite', action='store_true')
    sp.set_defaults(func=cmd_rotate)

    sp = sub.add_parser('reorder')
    sp.add_argument('input')
    sp.add_argument('--order', required=True)
    sp.add_argument('--output', required=True)
    sp.add_argument('--overwrite', action='store_true')
    sp.set_defaults(func=cmd_reorder)

    sp = sub.add_parser('alternate')
    sp.add_argument('inputs', nargs='+')
    sp.add_argument('--output', required=True)
    sp.add_argument('--overwrite', action='store_true')
    sp.set_defaults(func=cmd_alternate)

    sp = sub.add_parser('workspace-init')
    sp.add_argument('path')
    sp.add_argument('--default-output-dir', default='.')
    sp.set_defaults(func=cmd_workspace_init)

    sp = sub.add_parser('workspace-run')
    sp.add_argument('workspace')
    sp.add_argument('operation')
    sp.add_argument('op_args', nargs=argparse.REMAINDER)
    sp.set_defaults(func=cmd_workspace_run)

    return p


def main():
    return run_command(sys.argv[1:])
