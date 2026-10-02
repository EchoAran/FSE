#!/usr/bin/env python3
import argparse
import copy
import json
import os
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

DB_FILE = os.environ.get("SPRAT_DB", os.path.join(os.path.dirname(__file__), "sprat_db.json"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class VersionEntry:
    timestamp: str
    action: str
    user: str
    before: Any
    after: Any


@dataclass
class Artifact:
    id: str
    type: str
    title: str
    content: str = ""
    owner: str = "system"
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)
    classifications: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    primary_source: Optional[str] = None
    version: int = 1
    history: List[VersionEntry] = field(default_factory=list)


class Store:
    def __init__(self, path: str):
        self.path = path
        self.data = {"artifacts": {}, "counter": 1}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.data = raw

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, sort_keys=True)

    def new_id(self) -> str:
        i = self.data["counter"]
        self.data["counter"] += 1
        return f"A{i:04d}"

    def get(self, artifact_id: str) -> Artifact:
        raw = self.data["artifacts"][artifact_id]
        raw = copy.deepcopy(raw)
        raw["history"] = [VersionEntry(**v) for v in raw.get("history", [])]
        return Artifact(**raw)

    def put(self, artifact: Artifact, action: str, user: str, before: Any):
        artifact.version += 1
        artifact.updated_at = now_iso()
        artifact.history.append(VersionEntry(timestamp=now_iso(), action=action, user=user, before=before, after=asdict(artifact)))
        self.data["artifacts"][artifact.id] = json.loads(json.dumps(asdict(artifact), default=str))
        self.save()

    def create(self, type_: str, title: str, content: str, owner: str, classifications: List[str]):
        artifact = Artifact(id=self.new_id(), type=type_, title=title, content=content, owner=owner, classifications=classifications)
        artifact.history.append(VersionEntry(timestamp=now_iso(), action="create", user=owner, before=None, after=asdict(artifact)))
        self.data["artifacts"][artifact.id] = json.loads(json.dumps(asdict(artifact), default=str))
        self.save()
        return artifact.id


def role_can(role: str, action: str) -> bool:
    perms = {
        "admin": {"create", "edit", "view", "link", "compare", "rollback"},
        "manager": {"create", "edit", "view", "link", "compare"},
        "analyst": {"create", "edit", "view", "link", "compare"},
        "guest": {"view", "compare"},
    }
    return action in perms.get(role, {"view"})


def require(role: str, action: str):
    if not role_can(role, action):
        raise SystemExit(f"role '{role}' cannot perform '{action}'")


def parse_common(args):
    return args.user, args.role


def cmd_add(args):
    user, role = parse_common(args)
    require(role, "create")
    store = Store(args.db)
    cid = store.create(args.type, args.title, args.content or "", user, args.classify or [])
    print(cid)


def cmd_view(args):
    _, role = parse_common(args)
    require(role, "view")
    store = Store(args.db)
    art = store.get(args.id)
    print(json.dumps(asdict(art), indent=2))


def update_artifact(store: Store, art: Artifact, action: str, user: str, before: Any):
    store.put(art, action=action, user=user, before=before)


def cmd_link(args):
    user, role = parse_common(args)
    require(role, "link")
    store = Store(args.db)
    a = store.get(args.from_id)
    b = store.get(args.to_id)
    before_a, before_b = asdict(a), asdict(b)
    if args.to_id not in a.links:
        a.links.append(args.to_id)
    if args.from_id not in b.links:
        b.links.append(args.from_id)
    update_artifact(store, a, "link", user, before_a)
    update_artifact(store, b, "link", user, before_b)
    print("linked")


def cmd_add_source(args):
    user, role = parse_common(args)
    require(role, "edit")
    store = Store(args.db)
    art = store.get(args.requirement_id)
    before = asdict(art)
    if args.source_id not in art.sources:
        art.sources.append(args.source_id)
    if args.primary:
        art.primary_source = args.source_id
    update_artifact(store, art, "add_source", user, before)
    print("source-added")


def cmd_compare(args):
    _, role = parse_common(args)
    require(role, "compare")
    store = Store(args.db)
    a = store.get(args.first)
    b = store.get(args.second)
    diff = {
        "first": {"id": a.id, "title": a.title, "type": a.type, "version": a.version, "classifications": a.classifications, "links": a.links, "sources": a.sources},
        "second": {"id": b.id, "title": b.title, "type": b.type, "version": b.version, "classifications": b.classifications, "links": b.links, "sources": b.sources},
    }
    print(json.dumps(diff, indent=2))


def cmd_history(args):
    _, role = parse_common(args)
    require(role, "view")
    store = Store(args.db)
    art = store.get(args.id)
    print(json.dumps([asdict(h) for h in art.history], indent=2))


def cmd_rollback(args):
    user, role = parse_common(args)
    require(role, "rollback")
    store = Store(args.db)
    art = store.get(args.id)
    if args.version < 1 or args.version > len(art.history):
        raise SystemExit("invalid version")
    snapshot = art.history[args.version - 1].after
    before = asdict(art)
    restored = Artifact(**{k: snapshot[k] for k in Artifact.__dataclass_fields__.keys() if k in snapshot and k != "history"})
    restored.history = art.history[:]
    update_artifact(store, restored, "rollback", user, before)
    print("rolled-back")


def build_parser():
    p = argparse.ArgumentParser(prog="sprat")
    p.add_argument("--db", default=DB_FILE)
    p.add_argument("--user", default="system")
    p.add_argument("--role", default="admin")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("add")
    sp.add_argument("type")
    sp.add_argument("title")
    sp.add_argument("--content")
    sp.add_argument("--classify", nargs="*")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("view")
    sp.add_argument("id")
    sp.set_defaults(func=cmd_view)

    sp = sub.add_parser("link")
    sp.add_argument("from_id")
    sp.add_argument("to_id")
    sp.set_defaults(func=cmd_link)

    sp = sub.add_parser("add-source")
    sp.add_argument("requirement_id")
    sp.add_argument("source_id")
    sp.add_argument("--primary", action="store_true")
    sp.set_defaults(func=cmd_add_source)

    sp = sub.add_parser("compare")
    sp.add_argument("first")
    sp.add_argument("second")
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("history")
    sp.add_argument("id")
    sp.set_defaults(func=cmd_history)

    sp = sub.add_parser("rollback")
    sp.add_argument("id")
    sp.add_argument("version", type=int)
    sp.set_defaults(func=cmd_rollback)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
