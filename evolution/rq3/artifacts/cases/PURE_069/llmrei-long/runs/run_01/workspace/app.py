from __future__ import annotations

import argparse
import io
import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

from flask import Flask, jsonify, request
from pypdf import PdfReader, PdfWriter
from pypdf._page import PageObject


def parse_page_spec(spec: str, page_count: int) -> List[int]:
    if not spec.strip():
        return list(range(page_count))
    result: List[int] = []
    seen = set()
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start = int(a)
            end = int(b)
            if start < 1 or end < 1 or start > page_count or end > page_count:
                raise ValueError('page range out of bounds')
            step = 1 if end >= start else -1
            for i in range(start, end + step, step):
                if i not in seen:
                    result.append(i - 1)
                    seen.add(i)
        else:
            i = int(part)
            if i < 1 or i > page_count:
                raise ValueError('page number out of bounds')
            if i not in seen:
                result.append(i - 1)
                seen.add(i)
    return result


def read_pdf(path: str | Path) -> PdfReader:
    return PdfReader(str(path))


def write_pdf(writer: PdfWriter, path: str | Path) -> None:
    with open(path, 'wb') as f:
        writer.write(f)


def split_pdf(input_path: str, output_dir: str) -> List[str]:
    reader = read_pdf(input_path)
    out = []
    os.makedirs(output_dir, exist_ok=True)
    stem = Path(input_path).stem
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = str(Path(output_dir) / f'{stem}_page_{i}.pdf')
        write_pdf(writer, out_path)
        out.append(out_path)
    return out


def merge_pdfs(inputs: Sequence[str], output_path: str) -> str:
    writer = PdfWriter()
    for inp in inputs:
        reader = read_pdf(inp)
        for page in reader.pages:
            writer.add_page(page)
    write_pdf(writer, output_path)
    return output_path


def extract_pages(input_path: str, pages: str, output_path: str) -> str:
    reader = read_pdf(input_path)
    indices = parse_page_spec(pages, len(reader.pages))
    writer = PdfWriter()
    for i in indices:
        writer.add_page(reader.pages[i])
    write_pdf(writer, output_path)
    return output_path


def rotate_pages(input_path: str, output_path: str, pages: str, degrees: int) -> str:
    reader = read_pdf(input_path)
    indices = set(parse_page_spec(pages, len(reader.pages)))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        p = page
        if i in indices:
            p = p.rotate(degrees)
        writer.add_page(p)
    write_pdf(writer, output_path)
    return output_path


def reorder_pages(input_path: str, output_path: str, order: str) -> str:
    reader = read_pdf(input_path)
    indices = parse_page_spec(order, len(reader.pages))
    if len(indices) != len(reader.pages):
        missing = [i + 1 for i in range(len(reader.pages)) if i not in indices]
        indices.extend([m - 1 for m in missing])
    writer = PdfWriter()
    for i in indices:
        writer.add_page(reader.pages[i])
    write_pdf(writer, output_path)
    return output_path


def alternate_pdfs(inputs: Sequence[str], output_path: str) -> str:
    readers = [read_pdf(p) for p in inputs]
    writer = PdfWriter()
    max_pages = max((len(r.pages) for r in readers), default=0)
    for idx in range(max_pages):
        for reader in readers:
            if idx < len(reader.pages):
                writer.add_page(reader.pages[idx])
    write_pdf(writer, output_path)
    return output_path


def compose_pdfs(inputs: Sequence[str], output_path: str, pages_per_input: Optional[str] = None) -> str:
    writer = PdfWriter()
    for inp in inputs:
        reader = read_pdf(inp)
        if pages_per_input:
            indices = parse_page_spec(pages_per_input, len(reader.pages))
        else:
            indices = list(range(len(reader.pages)))
        for i in indices:
            writer.add_page(reader.pages[i])
    write_pdf(writer, output_path)
    return output_path


@dataclass
class Setup:
    operation: str
    parameters: dict


def save_setup(path: str, setup: Setup) -> str:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(asdict(setup), f, indent=2)
    return path


def load_setup(path: str) -> Setup:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Setup(operation=data['operation'], parameters=data['parameters'])


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='PDF Split and Merge')
    sub = p.add_subparsers(dest='cmd', required=True)

    s = sub.add_parser('split')
    s.add_argument('input')
    s.add_argument('output_dir')

    s = sub.add_parser('merge')
    s.add_argument('inputs', nargs='+')
    s.add_argument('-o', '--output', required=True)

    s = sub.add_parser('extract')
    s.add_argument('input')
    s.add_argument('-p', '--pages', required=True)
    s.add_argument('-o', '--output', required=True)

    s = sub.add_parser('rotate')
    s.add_argument('input')
    s.add_argument('-p', '--pages', required=True)
    s.add_argument('-d', '--degrees', type=int, required=True)
    s.add_argument('-o', '--output', required=True)

    s = sub.add_parser('reorder')
    s.add_argument('input')
    s.add_argument('-o', '--output', required=True)
    s.add_argument('--order', required=True)

    s = sub.add_parser('alternate')
    s.add_argument('inputs', nargs='+')
    s.add_argument('-o', '--output', required=True)

    s = sub.add_parser('compose')
    s.add_argument('inputs', nargs='+')
    s.add_argument('-o', '--output', required=True)
    s.add_argument('--pages-per-input')

    s = sub.add_parser('save-setup')
    s.add_argument('file')
    s.add_argument('--operation', required=True)
    s.add_argument('--parameters', default='{}')

    s = sub.add_parser('load-setup')
    s.add_argument('file')

    s = sub.add_parser('serve')
    s.add_argument('--host', default='127.0.0.1')
    s.add_argument('--port', type=int, default=8000)

    return p


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get('/')
    def index():
        return '''<html><body><h1>PDF Split and Merge</h1><p>Use the CLI or POST JSON to /api/merge, /api/extract, /api/rotate, /api/reorder, /api/alternate, /api/compose.</p></body></html>'''

    @app.post('/api/<op>')
    def api(op: str):
        data = request.get_json(force=True)
        out = data['output']
        if op == 'merge':
            result = merge_pdfs(data['inputs'], out)
        elif op == 'extract':
            result = extract_pages(data['input'], data['pages'], out)
        elif op == 'rotate':
            result = rotate_pages(data['input'], out, data['pages'], int(data['degrees']))
        elif op == 'reorder':
            result = reorder_pages(data['input'], out, data['order'])
        elif op == 'alternate':
            result = alternate_pdfs(data['inputs'], out)
        elif op == 'compose':
            result = compose_pdfs(data['inputs'], out, data.get('pages_per_input'))
        else:
            return jsonify({'error': 'unknown operation'}), 404
        return jsonify({'output': result})

    return app


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == 'split':
        split_pdf(args.input, args.output_dir)
    elif args.cmd == 'merge':
        merge_pdfs(args.inputs, args.output)
    elif args.cmd == 'extract':
        extract_pages(args.input, args.pages, args.output)
    elif args.cmd == 'rotate':
        rotate_pages(args.input, args.output, args.pages, args.degrees)
    elif args.cmd == 'reorder':
        reorder_pages(args.input, args.output, args.order)
    elif args.cmd == 'alternate':
        alternate_pdfs(args.inputs, args.output)
    elif args.cmd == 'compose':
        compose_pdfs(args.inputs, args.output, args.pages_per_input)
    elif args.cmd == 'save-setup':
        save_setup(args.file, Setup(args.operation, json.loads(args.parameters)))
    elif args.cmd == 'load-setup':
        print(json.dumps(asdict(load_setup(args.file)), indent=2))
    elif args.cmd == 'serve':
        create_app().run(host=args.host, port=args.port)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
