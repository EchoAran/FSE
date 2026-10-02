from __future__ import annotations

import argparse
from pathlib import Path

from .core import (
    alternate_pages,
    extract_pages,
    load_setup,
    merge_pdfs,
    reorder_pages,
    rotate_pages,
    save_setup,
    split_pdf,
)


def _parse_pages(value: str):
    return [int(x) for x in value.split(",") if x.strip()]


def _parse_rotations(value: str):
    result = {}
    if value.strip():
        for item in value.split(","):
            page, deg = item.split(":", 1)
            result[int(page)] = int(deg)
    return result


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pdfsplitmerge")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("split")
    s.add_argument("input")
    s.add_argument("output_dir")

    s = sub.add_parser("merge")
    s.add_argument("inputs", nargs="+")
    s.add_argument("-o", "--output", required=True)

    s = sub.add_parser("extract")
    s.add_argument("input")
    s.add_argument("-p", "--pages", required=True)
    s.add_argument("-o", "--output", required=True)

    s = sub.add_parser("rotate")
    s.add_argument("input")
    s.add_argument("-r", "--rotations", required=True)
    s.add_argument("-o", "--output", required=True)

    s = sub.add_parser("reorder")
    s.add_argument("input")
    s.add_argument("-o", "--order", required=True)
    s.add_argument("-d", "--output", required=True)

    s = sub.add_parser("alternate")
    s.add_argument("inputs", nargs="+")
    s.add_argument("-o", "--output", required=True)

    s = sub.add_parser("save-setup")
    s.add_argument("setup_json")
    s.add_argument("output")

    s = sub.add_parser("load-setup")
    s.add_argument("setup_json")

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.cmd == "split":
        split_pdf(args.input, args.output_dir)
    elif args.cmd == "merge":
        merge_pdfs(args.inputs, args.output)
    elif args.cmd == "extract":
        extract_pages(args.input, _parse_pages(args.pages), args.output)
    elif args.cmd == "rotate":
        rotate_pages(args.input, _parse_rotations(args.rotations), args.output)
    elif args.cmd == "reorder":
        reorder_pages(args.input, _parse_pages(args.order), args.output)
    elif args.cmd == "alternate":
        alternate_pages(args.inputs, args.output)
    elif args.cmd == "save-setup":
        save_setup(load_setup(args.setup_json), args.output)
    elif args.cmd == "load-setup":
        print(load_setup(args.setup_json))


if __name__ == "__main__":
    main()
