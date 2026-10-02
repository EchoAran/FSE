from __future__ import annotations

import argparse
import json
from .core import SPRATApp


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sprat")
    p.add_argument("--db", default="sprat_store.json")
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add-user")
    add.add_argument("username")
    add.add_argument("role")

    create = sub.add_parser("create")
    create.add_argument("username")
    create.add_argument("kind")
    create.add_argument("title")
    create.add_argument("--content", default="")
    create.add_argument("--classifications", default="")
    create.add_argument("--sources", default="")
    create.add_argument("--primary-source", default=None)

    show = sub.add_parser("show")
    show.add_argument("username")
    show.add_argument("artifact_id")

    link = sub.add_parser("link")
    link.add_argument("username")
    link.add_argument("source_id")
    link.add_argument("target_id")

    compare = sub.add_parser("compare")
    compare.add_argument("username")
    compare.add_argument("left_id")
    compare.add_argument("right_id")

    hist = sub.add_parser("history")
    hist.add_argument("username")
    hist.add_argument("artifact_id")

    return p


def main() -> None:
    args = build_parser().parse_args()
    app = SPRATApp(args.db)
    if args.cmd == "add-user":
        app.add_user(args.username, args.role)
        print("OK")
    elif args.cmd == "create":
        art = app.create_artifact(args.username, args.kind, args.title, args.content, args.classifications.split(",") if args.classifications else [], args.sources.split(",") if args.sources else [], args.primary_source)
        print(json.dumps(art.snapshot(), indent=2))
    elif args.cmd == "show":
        print(json.dumps(app.get_artifact(args.username, args.artifact_id), indent=2))
    elif args.cmd == "link":
        app.link_artifacts(args.username, args.source_id, args.target_id)
        print("OK")
    elif args.cmd == "compare":
        print(json.dumps(app.compare_artifacts(args.username, args.left_id, args.right_id), indent=2))
    elif args.cmd == "history":
        print(json.dumps(app.history(args.username, args.artifact_id), indent=2))


if __name__ == "__main__":
    main()
