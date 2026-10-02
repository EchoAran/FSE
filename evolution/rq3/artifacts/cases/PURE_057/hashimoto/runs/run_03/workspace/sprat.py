#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import sys
import uuid
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent / ".sprat"
DB_PATH = APP_DIR / "db.json"

ROLES = ["administrator", "project_manager", "analyst", "guest"]
STATE_DRAFT = "draft"
STATE_PENDING = "pending"
STATE_REVIEWED = "reviewed"
STATE_FINAL = "final"
STATE_REJECTED = "rejected"


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_db():
    if not DB_PATH.exists():
        return {"users": {}, "projects": {}, "items": {}, "next_id": 1}
    with DB_PATH.open() as f:
        return json.load(f)


def save_db(db):
    APP_DIR.mkdir(exist_ok=True)
    with DB_PATH.open("w") as f:
        json.dump(db, f, indent=2, sort_keys=True)


def add_history(item, user, action, reason=None, details=None):
    item.setdefault("history", []).append({
        "timestamp": now(),
        "user": user["username"],
        "role": user["role"],
        "action": action,
        "reason": reason or "",
        "details": details or {},
    })


def require_role(user, allowed):
    if user["role"] not in allowed:
        raise SystemExit(f"access denied for role {user['role']}; requires one of {allowed}")


def make_user(username, role):
    if role not in ROLES:
        raise SystemExit(f"invalid role: {role}")
    return {"username": username, "role": role}


def get_user(db, username):
    user = db["users"].get(username)
    if not user:
        raise SystemExit(f"unknown user: {username}")
    return user


def visible_basic(item):
    return {k: item[k] for k in ["id", "type", "title", "state", "owner", "project", "sensitive"] if k in item}


def can_see_metadata(user, item):
    if item.get("sensitive"):
        return user["role"] in ["administrator"] or user["username"] in [item.get("owner"), *item.get("reviewers", [])]
    if item.get("type") == "draft" and user["role"] == "guest":
        return False
    return True


def visible_item(user, item):
    if not can_see_metadata(user, item):
        return {"id": item["id"], "hidden": True, "reason": "restricted"}
    out = visible_basic(item)
    if item.get("state") in [STATE_DRAFT, STATE_PENDING] and (item.get("sensitive") or user["role"] == "guest"):
        out["content"] = "<hidden>"
    else:
        out["content"] = item.get("content", "")
    out["links"] = item.get("links", [])
    out["classifications"] = item.get("classifications", [])
    out["version"] = item.get("version", 1)
    out["history"] = item.get("history", [])
    out["conflict"] = item.get("conflict", False)
    out["gap"] = item.get("gap", False)
    out["unresolved"] = item.get("unresolved", False)
    return out


def cmd_init(args):
    db = {"users": {}, "projects": {}, "items": {}, "next_id": 1}
    save_db(db)
    print("initialized")


def cmd_add_user(args):
    db = load_db()
    db["users"][args.username] = {"username": args.username, "role": args.role}
    save_db(db)
    print(json.dumps(db["users"][args.username]))


def cmd_add_project(args):
    db = load_db()
    db["projects"][args.project_id] = {"project_id": args.project_id, "allow_guest_drafts": bool(args.allow_guest_drafts)}
    save_db(db)
    print(json.dumps(db["projects"][args.project_id]))


def new_item_id(db):
    item_id = f"I{db['next_id']:05d}"
    db["next_id"] += 1
    return item_id


def cmd_create(args):
    db = load_db()
    user = get_user(db, args.user)
    require_role(user, ["administrator", "project_manager", "analyst"])
    if args.project not in db["projects"]:
        raise SystemExit("unknown project")
    item_id = new_item_id(db)
    item = {
        "id": item_id,
        "type": args.type,
        "title": args.title,
        "content": args.content or "",
        "owner": user["username"],
        "project": args.project,
        "state": STATE_DRAFT,
        "version": 1,
        "reviewers": [],
        "sensitive": args.sensitive,
        "classifications": args.classification or [],
        "links": [],
        "gap": False,
        "unresolved": False,
        "conflict": False,
        "history": [],
        "versions": [{"version": 1, "content": args.content or "", "timestamp": now(), "approved": False}],
    }
    add_history(item, user, "create")
    db["items"][item_id] = item
    save_db(db)
    print(item_id)


def cmd_edit(args):
    db = load_db()
    user = get_user(db, args.user)
    item = db["items"][args.item_id]
    if user["username"] != item["owner"] and user["role"] != "administrator":
        raise SystemExit("only owner/admin can edit")
    item["content"] = args.content
    item["version"] += 1
    item["state"] = STATE_DRAFT
    item["versions"].append({"version": item["version"], "content": args.content, "timestamp": now(), "approved": False})
    add_history(item, user, "edit", args.reason)
    save_db(db)
    print("edited")


def cmd_submit(args):
    db = load_db()
    user = get_user(db, args.user)
    item = db["items"][args.item_id]
    if user["username"] != item["owner"] and user["role"] != "administrator":
        raise SystemExit("only owner/admin can submit")
    item["state"] = STATE_PENDING
    item["reviewers"] = args.reviewers or []
    add_history(item, user, "submit_for_review", args.reason, {"reviewers": item["reviewers"]})
    save_db(db)
    print("submitted")


def cmd_review(args):
    db = load_db()
    user = get_user(db, args.user)
    item = db["items"][args.item_id]
    if user["role"] not in ["administrator", "project_manager", "analyst"]:
        raise SystemExit("insufficient role for review")
    item["state"] = STATE_REVIEWED if args.approve else STATE_REJECTED
    if args.approve and item["versions"]:
        item["versions"][-1]["approved"] = True
        if args.finalize:
            item["state"] = STATE_FINAL
    add_history(item, user, "review", args.reason, {"approved": args.approve, "finalize": args.finalize})
    save_db(db)
    print(item["state"])


def cmd_link(args):
    db = load_db()
    user = get_user(db, args.user)
    item = db["items"][args.item_id]
    require_role(user, ["administrator", "project_manager", "analyst"])
    item.setdefault("links", []).append({"target": args.target, "kind": args.kind})
    add_history(item, user, "link", args.reason, {"target": args.target, "kind": args.kind})
    save_db(db)
    print("linked")


def cmd_flag_gap(args):
    db = load_db()
    user = get_user(db, args.user)
    item = db["items"][args.item_id]
    item["gap"] = True
    item["unresolved"] = True
    add_history(item, user, "flag_gap", args.reason, {"assumptions": args.assumptions})
    save_db(db)
    print("gap-flagged")


def cmd_flag_conflict(args):
    db = load_db()
    user = get_user(db, args.user)
    item = db["items"][args.item_id]
    item["conflict"] = True
    add_history(item, user, "flag_conflict", args.reason)
    save_db(db)
    print("conflict-flagged")


def cmd_show(args):
    db = load_db()
    user = get_user(db, args.user)
    item = db["items"][args.item_id]
    print(json.dumps(visible_item(user, item), indent=2, sort_keys=True))


def cmd_list(args):
    db = load_db()
    user = get_user(db, args.user)
    for item in db["items"].values():
        if can_see_metadata(user, item):
            print(json.dumps(visible_basic(item), sort_keys=True))


def cmd_export(args):
    db = load_db()
    with open(args.path, "w") as f:
        json.dump(db, f, indent=2, sort_keys=True)
    print(args.path)


def cmd_import(args):
    db = load_db()
    with open(args.path) as f:
        incoming = json.load(f)
    db["items"].update(incoming.get("items", {}))
    db["projects"].update(incoming.get("projects", {}))
    db["users"].update(incoming.get("users", {}))
    db["next_id"] = max(db.get("next_id", 1), incoming.get("next_id", 1))
    save_db(db)
    print("imported")


def main():
    p = argparse.ArgumentParser(prog="sprat")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(func=cmd_init)
    ap = sub.add_parser("add-user"); ap.add_argument("username"); ap.add_argument("role"); ap.set_defaults(func=cmd_add_user)
    ap = sub.add_parser("add-project"); ap.add_argument("project_id"); ap.add_argument("--allow-guest-drafts", action="store_true"); ap.set_defaults(func=cmd_add_project)
    ap = sub.add_parser("create"); ap.add_argument("--user", required=True); ap.add_argument("--project", required=True); ap.add_argument("--type", required=True); ap.add_argument("--title", required=True); ap.add_argument("--content"); ap.add_argument("--classification", action="append"); ap.add_argument("--sensitive", action="store_true"); ap.set_defaults(func=cmd_create)
    ap = sub.add_parser("edit"); ap.add_argument("--user", required=True); ap.add_argument("item_id"); ap.add_argument("--content", required=True); ap.add_argument("--reason"); ap.set_defaults(func=cmd_edit)
    ap = sub.add_parser("submit"); ap.add_argument("--user", required=True); ap.add_argument("item_id"); ap.add_argument("--reviewers", nargs="*"); ap.add_argument("--reason"); ap.set_defaults(func=cmd_submit)
    ap = sub.add_parser("review"); ap.add_argument("--user", required=True); ap.add_argument("item_id"); ap.add_argument("--approve", action="store_true"); ap.add_argument("--finalize", action="store_true"); ap.add_argument("--reason"); ap.set_defaults(func=cmd_review)
    ap = sub.add_parser("link"); ap.add_argument("--user", required=True); ap.add_argument("item_id"); ap.add_argument("--target", required=True); ap.add_argument("--kind", required=True); ap.add_argument("--reason"); ap.set_defaults(func=cmd_link)
    ap = sub.add_parser("flag-gap"); ap.add_argument("--user", required=True); ap.add_argument("item_id"); ap.add_argument("--assumptions", default=""); ap.add_argument("--reason"); ap.set_defaults(func=cmd_flag_gap)
    ap = sub.add_parser("flag-conflict"); ap.add_argument("--user", required=True); ap.add_argument("item_id"); ap.add_argument("--reason"); ap.set_defaults(func=cmd_flag_conflict)
    ap = sub.add_parser("show"); ap.add_argument("--user", required=True); ap.add_argument("item_id"); ap.set_defaults(func=cmd_show)
    ap = sub.add_parser("list"); ap.add_argument("--user", required=True); ap.set_defaults(func=cmd_list)
    ap = sub.add_parser("export"); ap.add_argument("path"); ap.set_defaults(func=cmd_export)
    ap = sub.add_parser("import"); ap.add_argument("path"); ap.set_defaults(func=cmd_import)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
