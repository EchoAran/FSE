from __future__ import annotations

import argparse
from pathlib import Path

from .core import (
    PDFSMError,
    Project,
    PageRef,
    extract_pages,
    interleave_pdfs,
    load_project,
    merge_pdfs,
    normalize_rotation,
    parse_page_ranges,
    save_project,
    split_pdf,
    rotate_pages,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pdfsplitmerge", description="PDF split and merge tool")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("split")
    sp.add_argument("input")
    sp.add_argument("--ranges", required=True, help="e.g. 1-2,5-7")
    sp.add_argument("--output-dir")
    sp.add_argument("--overwrite", action="store_true")

    mp = sub.add_parser("merge")
    mp.add_argument("inputs", nargs='+')
    mp.add_argument("-o", "--output", required=True)
    mp.add_argument("--overwrite", action="store_true")

    ep = sub.add_parser("extract")
    ep.add_argument("input")
    ep.add_argument("--pages", required=True)
    ep.add_argument("-o", "--output", required=True)
    ep.add_argument("--overwrite", action="store_true")

    rp = sub.add_parser("rotate")
    rp.add_argument("input")
    rp.add_argument("--pages", required=True)
    rp.add_argument("--direction", choices=["left", "right"], required=True)
    rp.add_argument("-o", "--output", required=True)
    rp.add_argument("--overwrite", action="store_true")

    ip = sub.add_parser("interleave")
    ip.add_argument("inputs", nargs='+')
    ip.add_argument("-o", "--output", required=True)
    ip.add_argument("--overwrite", action="store_true")

    pp = sub.add_parser("project-save")
    pp.add_argument("path")
    pp.add_argument("inputs", nargs='+')
    pp.add_argument("--output-dir")
    pp.add_argument("--output-name")

    lp = sub.add_parser("project-load")
    lp.add_argument("path")
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.cmd == "split":
            ranges = []
            for r in args.ranges.split(','):
                a, b = r.split('-', 1)
                ranges.append((int(a), int(b)))
            outs = split_pdf(Path(args.input), ranges, Path(args.output_dir) if args.output_dir else None, args.overwrite)
            print("\n".join(map(str, outs)))
        elif args.cmd == "merge":
            merge_pdfs([Path(x) for x in args.inputs], Path(args.output), args.overwrite)
            print(args.output)
        elif args.cmd == "extract":
            extract_pages(Path(args.input), parse_page_ranges(args.pages), Path(args.output), args.overwrite)
            print(args.output)
        elif args.cmd == "rotate":
            rotate_pages(Path(args.input), parse_page_ranges(args.pages), args.direction, Path(args.output), args.overwrite)
            print(args.output)
        elif args.cmd == "interleave":
            interleave_pdfs([Path(x) for x in args.inputs], Path(args.output), args.overwrite)
            print(args.output)
        elif args.cmd == "project-save":
            save_project(Project(inputs=args.inputs, pages=[PageRef(source=i, page_number=1) for i in args.inputs], output_dir=args.output_dir, output_name=args.output_name), Path(args.path))
            print(args.path)
        elif args.cmd == "project-load":
            print(load_project(Path(args.path)))
        return 0
    except PDFSMError as e:
        parser.exit(2, f"error: {e}\n")


if __name__ == "__main__":
    raise SystemExit(main())
