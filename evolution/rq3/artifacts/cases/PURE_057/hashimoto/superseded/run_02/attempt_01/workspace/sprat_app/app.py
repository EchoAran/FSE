from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse
from uuid import uuid4

DATA_PATH = Path(os.environ.get("SPRAT_DATA_PATH", "/workspace/sprat_state.json"))

ROLES = {"administrator", "project_manager", "analyst", "guest"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Store:
    def __init__(self, path: Path):
        self.path = path
        self.state = self._load()

    def _default(self) -> Dict[str, Any]:
        return {"users": [], "items": [], "imports": []}

    def _load(self) -> Dict[str, Any]:
        if self.path.exists():
            return json.loads(self.path.read_text())
        return self._default()

    def save(self) -> None:
        self.path.write_text(json.dumps(self.state, indent=2, sort_keys=True))

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return next((u for u in self.state["users"] if u["id"] == user_id), None)

    def add_user(self, name: str, role: str) -> Dict[str, Any]:
        if role not in ROLES:
            raise ValueError("invalid role")
        user = {"id": str(uuid4()), "name": name, "role": role}
        self.state["users"].append(user)
        self.save()
        return user

    def _record_revision(self, item: Dict[str, Any], user: Dict[str, Any], action: str, reason: Optional[str] = None) -> None:
        snapshot = {k: item.get(k) for k in ["type", "title", "content", "metadata", "classifications", "tags", "trace_links", "policy_links", "status", "sensitive"]}
        item["revisions"].append({"timestamp": now_iso(), "user_id": user["id"], "action": action, "reason": reason, "snapshot": snapshot})
        item["history"].append({"timestamp": now_iso(), "user_id": user["id"], "action": action, "reason": reason})
        item["updated_at"] = now_iso()

    def add_item(self, payload: Dict[str, Any], creator: Dict[str, Any]) -> Dict[str, Any]:
        item = {
            "id": str(uuid4()),
            "type": payload.get("type", "requirement"),
            "title": payload.get("title", ""),
            "content": payload.get("content", ""),
            "metadata": payload.get("metadata", {}),
            "classifications": payload.get("classifications", []),
            "tags": payload.get("tags", []),
            "trace_links": payload.get("trace_links", []),
            "policy_links": payload.get("policy_links", []),
            "status": payload.get("status", "draft"),
            "sensitive": bool(payload.get("sensitive", False)),
            "owner_id": creator["id"],
            "created_by": creator["id"],
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "revisions": [],
            "history": [],
            "reviewers": payload.get("reviewers", []),
            "review_notes": [],
            "unresolved": False,
            "gap": None,
            "conflicts": [],
            "partial_analysis": False,
        }
        self._record_revision(item, creator, "created")
        self.state["items"].append(item)
        self.save()
        return item


def create_app(bind_host: str = "127.0.0.1", bind_port: int = 0):
    store = Store(DATA_PATH)

    def auth_user(headers: Dict[str, str]) -> Dict[str, Any]:
        user_id = headers.get("X-User-Id")
        if not user_id:
            raise PermissionError("missing user")
        user = store.get_user(user_id)
        if not user:
            raise PermissionError("unknown user")
        return user

    def can_view(user: Dict[str, Any], item: Dict[str, Any]) -> bool:
        if user["role"] == "administrator":
            return True
        if item["sensitive"]:
            return user["id"] == item["owner_id"] or user["role"] == "project_manager"
        if item["status"] in {"draft", "pending"}:
            return user["role"] in {"analyst", "project_manager", "administrator", "guest"}
        return True

    def visible_item(user: Dict[str, Any], item: Dict[str, Any]) -> Dict[str, Any]:
        base = {k: item[k] for k in ["id", "type", "title", "status", "sensitive", "owner_id", "created_by", "created_at", "updated_at", "classifications", "tags", "reviewers", "unresolved", "partial_analysis"]}
        if item["status"] in {"draft", "pending"} and not can_view(user, item):
            return base
        if item["sensitive"] and user["role"] not in {"administrator", "project_manager"} and user["id"] != item["owner_id"]:
            return base
        base.update({"content": item["content"], "trace_links": item["trace_links"], "policy_links": item["policy_links"], "history": item["history"], "revisions": item["revisions"], "review_notes": item["review_notes"], "gap": item["gap"], "conflicts": item["conflicts"]})
        return base

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, payload: Any):
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode())

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
            try:
                if self.path == "/users":
                    user = store.add_user(data["name"], data["role"])
                    return self._send(201, user)
                user = auth_user(self.headers)
                if self.path == "/items":
                    if user["role"] not in {"analyst", "project_manager", "administrator"}:
                        return self._send(403, {"error": "forbidden"})
                    item = store.add_item(data, user)
                    return self._send(201, visible_item(user, item))
                if self.path == "/import":
                    if user["role"] not in {"analyst", "project_manager", "administrator"}:
                        return self._send(403, {"error": "forbidden"})
                    imported = []
                    for raw in data.get("items", []):
                        item = store.add_item(raw, user)
                        if not raw.get("trace_links") or not raw.get("policy_links"):
                            item["partial_analysis"] = True
                            item["unresolved"] = True
                            item["gap"] = raw.get("gap", "Traceability incomplete")
                            item["history"].append({"timestamp": now_iso(), "user_id": user["id"], "action": "exception", "reason": "documented exception"})
                        imported.append(visible_item(user, item))
                    store.save()
                    return self._send(201, {"imported": imported})
                parts = self.path.strip("/").split("/")
                item = next((i for i in store.state["items"] if i["id"] == parts[1]), None)
                if not item:
                    return self._send(404, {"error": "not found"})
                if parts[2] == "submit":
                    if user["id"] != item["owner_id"]:
                        return self._send(403, {"error": "forbidden"})
                    item["status"] = "pending"
                    store._record_revision(item, user, "submitted")
                    store.save()
                    return self._send(200, {"status": item["status"]})
                if parts[2] == "review":
                    if user["role"] not in {"project_manager", "administrator"} and user["id"] not in item.get("reviewers", []):
                        return self._send(403, {"error": "forbidden"})
                    item["status"] = data.get("status", "reviewed")
                    item["review_notes"].append({"user_id": user["id"], "timestamp": now_iso(), "note": data.get("note", "")})
                    store._record_revision(item, user, "reviewed", data.get("note"))
                    if item["status"] == "final":
                        store._record_revision(item, user, "finalized", data.get("note"))
                    store.save()
                    return self._send(200, visible_item(user, item))
                if parts[2] == "compare":
                    rev_a, rev_b = parts[3], parts[4]
                    a = next((r for r in item["revisions"] if r["timestamp"] == rev_a), None)
                    b = next((r for r in item["revisions"] if r["timestamp"] == rev_b), None)
                    if not a or not b:
                        return self._send(404, {"error": "not found"})
                    return self._send(200, {"from": a, "to": b})
            except PermissionError as e:
                return self._send(401, {"error": str(e)})
            except Exception as e:
                return self._send(400, {"error": str(e)})
            return self._send(404, {"error": "not found"})

        def do_GET(self):
            try:
                user = auth_user(self.headers)
            except PermissionError as e:
                return self._send(401, {"error": str(e)})
            if self.path == "/items":
                return self._send(200, [visible_item(user, i) for i in store.state["items"] if can_view(user, i) or i["status"] == "final"])
            parts = self.path.strip("/").split("/")
            if len(parts) == 2 and parts[0] == "items":
                item = next((i for i in store.state["items"] if i["id"] == parts[1]), None)
                if not item:
                    return self._send(404, {"error": "not found"})
                if not can_view(user, item) and item["status"] != "final":
                    return self._send(403, {"error": "forbidden"})
                return self._send(200, visible_item(user, item))
            return self._send(404, {"error": "not found"})

    return ThreadingHTTPServer((bind_host, bind_port), Handler)


if __name__ == "__main__":
    server = create_app("127.0.0.1", int(os.environ.get("PORT", "8000")))
    server.serve_forever()
