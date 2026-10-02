#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

MAGIC = 'PDFTOOL1'


@dataclass
class Document:
    pages: List[dict]


def load_doc(path: str) -> Document:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if data.get('magic') != MAGIC:
        raise ValueError(f'{path} is not a supported document')
    return Document(pages=data['pages'])


def save_doc(doc: Document, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'magic': MAGIC, 'pages': doc.pages}, f, indent=2)


def make_blank_doc(page_count: int) -> Document:
    return Document(pages=[{'rotation': 0, 'content': f'page-{i+1}'} for i in range(page_count)])


def parse_page_spec(spec: str, total_pages: Optional[int] = None) -> List[int]:
    pages: List[int] = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start_s, end_s = part.split('-', 1)
            start = int(start_s)
            end = int(end_s)
            step = 1 if end >= start else -1
            pages.extend(list(range(start, end + step, step)))
        else:
            pages.append(int(part))
    if total_pages is not None:
        for p in pages:
            if p < 1 or p > total_pages:
                raise ValueError(f'Page {p} out of range 1..{total_pages}')
    return pages


def cmd_split(args: argparse.Namespace) -> None:
    doc = load_doc(args.input)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc.pages, start=1):
        save_doc(Document([page.copy()]), str(outdir / f"{Path(args.input).stem}_page_{i}.pdf"))


def cmd_extract(args: argparse.Namespace) -> None:
    doc = load_doc(args.input)
    pages = parse_page_spec(args.pages, len(doc.pages))
    save_doc(Document([doc.pages[p - 1].copy() for p in pages]), args.output)


def cmd_rotate(args: argparse.Namespace) -> None:
    doc = load_doc(args.input)
    pages = parse_page_spec(args.pages, len(doc.pages)) if args.pages else list(range(1, len(doc.pages) + 1))
    rotate_set = set(pages)
    new_pages = []
    for i, page in enumerate(doc.pages, start=1):
        p = page.copy()
        if i in rotate_set:
            p['rotation'] = (p.get('rotation', 0) + args.degrees) % 360
        new_pages.append(p)
    save_doc(Document(new_pages), args.output)


def cmd_merge(args: argparse.Namespace) -> None:
    merged: List[dict] = []
    for item in args.inputs:
        path, _, spec = item.partition(':')
        doc = load_doc(path)
        if spec:
            pages = parse_page_spec(spec, len(doc.pages))
            merged.extend(doc.pages[p - 1].copy() for p in pages)
        else:
            merged.extend(page.copy() for page in doc.pages)
    save_doc(Document(merged), args.output)


def cmd_reorder(args: argparse.Namespace) -> None:
    doc = load_doc(args.input)
    pages = parse_page_spec(args.order, len(doc.pages))
    save_doc(Document([doc.pages[p - 1].copy() for p in pages]), args.output)


def cmd_alternate(args: argparse.Namespace) -> None:
    docs = [load_doc(p) for p in args.inputs]
    max_len = max(len(d.pages) for d in docs)
    result: List[dict] = []
    for i in range(max_len):
        for d in docs:
            if i < len(d.pages):
                result.append(d.pages[i].copy())
    save_doc(Document(result), args.output)


def cmd_save_setup(args: argparse.Namespace) -> None:
    setup = {'description': args.description, 'operations': [op.__dict__ for op in args.operations]}
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(setup, f, indent=2)


def run_operation(op: dict, current_input: str, output: str) -> None:
    kind = op['kind']
    params = op.get('params', {})
    if kind == 'extract':
        cmd_extract(argparse.Namespace(input=current_input, pages=params['pages'], output=output))
    elif kind == 'rotate':
        cmd_rotate(argparse.Namespace(input=current_input, pages=params.get('pages'), degrees=params['degrees'], output=output))
    elif kind == 'reorder':
        cmd_reorder(argparse.Namespace(input=current_input, order=params['order'], output=output))
    else:
        raise ValueError(f'Unsupported setup operation: {kind}')


def cmd_run_setup(args: argparse.Namespace) -> None:
    with open(args.setup, 'r', encoding='utf-8') as f:
        setup = json.load(f)
    current = args.input
    operations = setup.get('operations', [])
    for idx, op in enumerate(operations):
        out = args.output if idx == len(operations) - 1 else f'{args.output}.tmp{idx}.pdf'
        run_operation(op, current, out)
        current = out


def parse_operation(text: str):
    kind, _, payload = text.partition('=')
    params = json.loads(payload) if payload else {}
    return type('Op', (), {'__dict__': {'kind': kind, 'params': params}})()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='PDF Split and Merge tool')
    sub = parser.add_subparsers(dest='command', required=True)

    p = sub.add_parser('split')
    p.add_argument('input')
    p.add_argument('output_dir')
    p.set_defaults(func=cmd_split)

    p = sub.add_parser('extract')
    p.add_argument('input')
    p.add_argument('pages')
    p.add_argument('output')
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser('rotate')
    p.add_argument('input')
    p.add_argument('degrees', type=int)
    p.add_argument('output')
    p.add_argument('--pages')
    p.set_defaults(func=cmd_rotate)

    p = sub.add_parser('merge')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser('reorder')
    p.add_argument('input')
    p.add_argument('order')
    p.add_argument('output')
    p.set_defaults(func=cmd_reorder)

    p = sub.add_parser('alternate')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')
    p.set_defaults(func=cmd_alternate)

    p = sub.add_parser('save-setup')
    p.add_argument('output')
    p.add_argument('--description', default='')
    p.add_argument('--operation', action='append', dest='operations', type=parse_operation, required=True)
    p.set_defaults(func=cmd_save_setup)

    p = sub.add_parser('run-setup')
    p.add_argument('setup')
    p.add_argument('input')
    p.add_argument('output')
    p.set_defaults(func=cmd_run_setup)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.func(args)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
