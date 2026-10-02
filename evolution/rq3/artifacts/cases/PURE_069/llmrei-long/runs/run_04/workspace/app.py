#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional


@dataclass
class Doc:
    pages: List[str]


def read_doc(path: str) -> Doc:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Doc(pages=data['pages'])


def write_doc(doc: Doc, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(asdict(doc), f, indent=2)


def parse_pages(spec: str, total: int) -> List[int]:
    out = []
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-', 1)
            rng = range(int(a), int(b) + 1)
            out.extend(rng)
        else:
            out.append(int(part))
    dedup = []
    for p in out:
        if p < 1 or p > total:
            raise ValueError(f'page {p} out of range 1..{total}')
        if p not in dedup:
            dedup.append(p)
    return dedup


def split_pdf(input_path: str, output_dir: str, pages_per_file: int) -> None:
    doc = read_doc(input_path)
    os.makedirs(output_dir, exist_ok=True)
    if pages_per_file <= 0:
        raise ValueError('pages_per_file must be positive')
    for idx, start in enumerate(range(0, len(doc.pages), pages_per_file), start=1):
        write_doc(Doc(doc.pages[start:start + pages_per_file]), os.path.join(output_dir, f'split_{idx:03d}.json'))


def merge_pdfs(inputs: List[str], output: str) -> None:
    pages = []
    for p in inputs:
        pages.extend(read_doc(p).pages)
    write_doc(Doc(pages), output)


def extract_pages(input_path: str, output: str, pages: str) -> None:
    doc = read_doc(input_path)
    selected = parse_pages(pages, len(doc.pages))
    write_doc(Doc([doc.pages[i - 1] for i in selected]), output)


def rotate_pages(input_path: str, output: str, rotation: int, pages: Optional[str]) -> None:
    doc = read_doc(input_path)
    selected = set(parse_pages(pages, len(doc.pages))) if pages else None
    rotated = []
    for idx, page in enumerate(doc.pages, start=1):
        if selected is None or idx in selected:
            rotated.append(f'{page} [rotated {rotation}]')
        else:
            rotated.append(page)
    write_doc(Doc(rotated), output)


def reorder_pages(input_path: str, output: str, order: str) -> None:
    doc = read_doc(input_path)
    selected = parse_pages(order, len(doc.pages))
    write_doc(Doc([doc.pages[i - 1] for i in selected]), output)


def alternate_merge(inputs: List[str], output: str) -> None:
    docs = [read_doc(p) for p in inputs]
    pages = []
    max_len = max(len(d.pages) for d in docs)
    for i in range(max_len):
        for d in docs:
            if i < len(d.pages):
                pages.append(d.pages[i])
    write_doc(Doc(pages), output)


def save_workspace(path: str, name: str, steps: List[dict]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'name': name, 'steps': steps}, f, indent=2)


def load_workspace(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_workspace(workspace: dict) -> None:
    for step in workspace['steps']:
        op = step['op']
        if op == 'split':
            split_pdf(step['input'], step['output_dir'], step['pages_per_file'])
        elif op == 'merge':
            merge_pdfs(step['inputs'], step['output'])
        elif op == 'extract':
            extract_pages(step['input'], step['output'], step['pages'])
        elif op == 'rotate':
            rotate_pages(step['input'], step['output'], step['rotation'], step.get('pages'))
        elif op == 'reorder':
            reorder_pages(step['input'], step['output'], step['order'])
        elif op == 'alternate_merge':
            alternate_merge(step['inputs'], step['output'])
        else:
            raise ValueError(f'unknown workspace operation: {op}')


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='PDF Split and Merge (JSON document demo implementation)')
    sub = p.add_subparsers(dest='cmd', required=True)
    sp = sub.add_parser('split')
    sp.add_argument('input')
    sp.add_argument('output_dir')
    sp.add_argument('--pages-per-file', type=int, default=1)
    sp = sub.add_parser('merge')
    sp.add_argument('output')
    sp.add_argument('inputs', nargs='+')
    sp = sub.add_parser('extract')
    sp.add_argument('input')
    sp.add_argument('output')
    sp.add_argument('--pages', required=True)
    sp = sub.add_parser('rotate')
    sp.add_argument('input')
    sp.add_argument('output')
    sp.add_argument('--rotation', type=int, required=True)
    sp.add_argument('--pages')
    sp = sub.add_parser('reorder')
    sp.add_argument('input')
    sp.add_argument('output')
    sp.add_argument('--order', required=True)
    sp = sub.add_parser('alternate-merge')
    sp.add_argument('output')
    sp.add_argument('inputs', nargs='+')
    sp = sub.add_parser('save-workspace')
    sp.add_argument('output')
    sp.add_argument('--name', default='workspace')
    sp.add_argument('--step', action='append', required=True)
    sp = sub.add_parser('run-workspace')
    sp.add_argument('workspace_file')
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == 'split': split_pdf(args.input, args.output_dir, args.pages_per_file)
        elif args.cmd == 'merge': merge_pdfs(args.inputs, args.output)
        elif args.cmd == 'extract': extract_pages(args.input, args.output, args.pages)
        elif args.cmd == 'rotate': rotate_pages(args.input, args.output, args.rotation, args.pages)
        elif args.cmd == 'reorder': reorder_pages(args.input, args.output, args.order)
        elif args.cmd == 'alternate-merge': alternate_merge(args.inputs, args.output)
        elif args.cmd == 'save-workspace': save_workspace(args.output, args.name, [json.loads(s) for s in args.step])
        elif args.cmd == 'run-workspace': run_workspace(load_workspace(args.workspace_file))
        return 0
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
