import csv
import json
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROLE_LEVEL = {"guest": 0, "analyst": 1, "manager": 2, "admin": 3}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_db(path: Path) -> Dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text())
    return {"items": [], "next_id": 1}


def save_db(path: Path, db: Dict[str, Any]):
    path.write_text(json.dumps(db, indent=2, sort_keys=True))


def add_history(item, action, user, reason=None, details=None):
    item["history"].append({
        "timestamp": now_iso(),
        "user": user,
        "action": action,
        "reason": reason,
        "details": details or {},
    })


def parse_tags(tags: Optional[str]):
    if not tags:
        return []
    return [t.strip() for t in tags.split(",") if t.strip()]


def new_item(db, title, content, item_type, owner, role, project, sensitivity=False, status="draft", classifications=None, tags=None, trace_links=None, source=None):
    item = {
        "id": db["next_id"],
        "title": title,
        "content": content,
        "type": item_type,
        "owner": owner,
        "project": project,
        "sensitive": bool(sensitivity),
        "status": status,
        "reviewers": [],
        "approved_version": None,
        "revisions": [],
        "classifications": classifications or [],
        "tags": tags or [],
        "trace_links": trace_links or [],
        "flags": [],
        "history": [],
        "source": source,
    }
    add_history(item, "create", owner, details={"role": role, "status": status})
    item["revisions"].append({"version": 1, "title": title, "content": content, "created_at": now_iso(), "created_by": owner})
    db["items"].append(item)
    db["next_id"] += 1
    return item


def find_item(db, item_id):
    for item in db["items"]:
        if item["id"] == item_id:
            return item
    raise SystemExit(f"Item {item_id} not found")


def visible_metadata(item, role):
    data = {"id": item["id"], "title": item["title"], "type": item["type"], "status": item["status"], "owner": item["owner"]}
    if item["sensitive"] and ROLE_LEVEL[role] < ROLE_LEVEL["admin"]:
        if role in ("author", "reviewer"):
            return data
        return {"id": item["id"], "title": "[restricted]", "type": item["type"], "status": item["status"]}
    return data


def item_view(item, role, username):
    can_see_content = True
    if item["status"] in ("draft", "pending"):
        if role == "guest":
            return None
        if item["sensitive"] and username not in {item["owner"]} and role != "admin":
            can_see_content = False
        elif role == "analyst" and username != item["owner"]:
            can_see_content = False
        elif role == "manager":
            can_see_content = False
    if item["sensitive"] and role not in ("admin",) and username != item["owner"] and role != "manager":
        pass
    out = visible_metadata(item, role)
    out.update({
        "sensitive": item["sensitive"],
        "classifications": item["classifications"],
        "tags": item["tags"],
        "flags": item["flags"],
        "trace_links": item["trace_links"],
        "history": item["history"],
        "revisions": item["revisions"],
    })
    out["content"] = item["content"] if can_see_content or item["status"] == "final" or role == "admin" else "[hidden]"
    out["approved_version"] = item["approved_version"]
    return out


def cmd_add(args):
    db = load_db(Path(args.db))
    item = new_item(db, args.title, args.content, args.type, args.user, args.role, args.project, args.sensitive, args.status, args.classifications, parse_tags(args.tags), source=args.source)
    save_db(Path(args.db), db)
    print(json.dumps(item_view(item, args.role, args.user), indent=2))


def cmd_list(args):
    db = load_db(Path(args.db))
    role = args.role
    for item in db["items"]:
        v = item_view(item, role, args.user)
        if v is None:
            continue
        print(json.dumps(v, indent=2))


def cmd_edit(args):
    db = load_db(Path(args.db))
    item = find_item(db, args.id)
    if item["status"] == "final":
        item["revisions"].append({"version": len(item["revisions"]) + 1, "title": args.title or item["title"], "content": args.content or item["content"], "created_at": now_iso(), "created_by": args.user})
        item["status"] = "draft"
    if args.title:
        item["title"] = args.title
    if args.content:
        item["content"] = args.content
    add_history(item, "edit", args.user, args.reason)
    save_db(Path(args.db), db)
    print(json.dumps(item_view(item, args.role, args.user), indent=2))


def cmd_approve(args):
    db = load_db(Path(args.db))
    item = find_item(db, args.id)
    item["status"] = "final"
    item["approved_version"] = len(item["revisions"])
    if args.reviewer not in item["reviewers"]:
        item["reviewers"].append(args.reviewer)
    add_history(item, "approve", args.reviewer, args.reason)
    save_db(Path(args.db), db)
    print(json.dumps(item_view(item, args.role, args.user), indent=2))


def cmd_flag(args):
    db = load_db(Path(args.db))
    item = find_item(db, args.id)
    item["flags"].append({"type": args.flag_type, "note": args.note, "user": args.user, "timestamp": now_iso()})
    add_history(item, "flag", args.user, args.note)
    save_db(Path(args.db), db)
    print(json.dumps(item_view(item, args.role, args.user), indent=2))


def cmd_compare(args):
    db = load_db(Path(args.db))
    a = find_item(db, args.left)
    b = find_item(db, args.right)
    print(json.dumps({"left": a["id"], "right": b["id"], "title_changed": a["title"] != b["title"], "content_changed": a["content"] != b["content"], "trace_links_changed": a["trace_links"] != b["trace_links"]}, indent=2))


def import_json(db, path, user, role, project):
    data = json.loads(Path(path).read_text())
    for obj in data.get("items", data if isinstance(data, list) else []):
        new_item(db, obj.get("title", "Imported item"), obj.get("content", ""), obj.get("type", "requirement"), user, role, project, obj.get("sensitive", False), obj.get("status", "draft"), obj.get("classifications", []), obj.get("tags", []), obj.get("trace_links", []), source=path)


def import_csv(db, path, user, role, project):
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            new_item(db, row.get("title", "Imported item"), row.get("content", ""), row.get("type", "requirement"), user, role, project, row.get("sensitive", "false").lower() == "true", row.get("status", "draft"), parse_tags(row.get("classifications")), parse_tags(row.get("tags")), source=path)


def cmd_import(args):
    db = load_db(Path(args.db))
    ext = Path(args.source).suffix.lower()
    if ext in {".json"}:
        import_json(db, args.source, args.user, args.role, args.project)
    else:
        import_csv(db, args.source, args.user, args.role, args.project)
    save_db(Path(args.db), db)
    print(json.dumps({"imported": True, "count": len(db["items"])}, indent=2))
