from __future__ import annotations

import copy
import datetime as dt
import json
from dataclasses import dataclass, field, asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

ROLES = {"administrator", "project_manager", "analyst", "guest"}


def now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


@dataclass
class HistoryEntry:
    timestamp: str
    user: str
    action: str
    reason: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ItemVersion:
    version: int
    data: Dict[str, Any]
    history: List[HistoryEntry]
    status: str


@dataclass
class Item:
    item_id: str
    data: Dict[str, Any]
    status: str = "draft"
    owner: str = ""
    sensitive: bool = False
    review_required: bool = True
    reviewer: Optional[str] = None
    approved_by: Optional[str] = None
    versions: List[ItemVersion] = field(default_factory=list)
    history: List[HistoryEntry] = field(default_factory=list)


class Store:
    def __init__(self) -> None:
        self.items: Dict[str, Item] = {}
        self.next_id = 1

    def create_item(self, payload: Dict[str, Any], user: str) -> Item:
        item_id = str(self.next_id)
        self.next_id += 1
        data = copy.deepcopy(payload)
        item = Item(
            item_id=item_id,
            data=data,
            owner=user,
            sensitive=bool(data.get("sensitive", False)),
            review_required=bool(data.get("review_required", True)),
        )
        item.history.append(HistoryEntry(now_iso(), user, "created"))
        self.items[item_id] = item
        return item

    def update_item(self, item: Item, payload: Dict[str, Any], user: str, reason: Optional[str]) -> Item:
        if item.status == "final":
            version = ItemVersion(len(item.versions) + 1, copy.deepcopy(item.data), copy.deepcopy(item.history), item.status)
            item.versions.append(version)
        item.data.update(copy.deepcopy(payload))
        item.sensitive = bool(item.data.get("sensitive", item.sensitive))
        item.review_required = bool(item.data.get("review_required", item.review_required))
        item.status = "draft"
        item.history.append(HistoryEntry(now_iso(), user, "updated", reason=reason))
        return item


store = Store()


def visible_item(item: Item, role: str, user: str) -> Dict[str, Any]:
    base = {
        "item_id": item.item_id,
        "status": item.status,
        "owner": item.owner,
        "sensitive": item.sensitive,
        "review_required": item.review_required,
    }
    if item.status == "draft":
        base["draft_visible"] = role in {"analyst", "project_manager", "administrator"}
        base["content"] = None
        if item.sensitive:
            if role in {"administrator", "project_manager"} or user == item.owner:
                base["metadata_only"] = True
            else:
                base = {"item_id": item.item_id, "status": item.status}
        else:
            if role in {"analyst", "project_manager", "administrator"} or user == item.owner:
                base["content_summary"] = item.data.get("title") or item.data.get("summary") or "draft item"
        return base
    base["content"] = item.data
    return base


def parse_json(handler: BaseHTTPRequestHandler) -> Dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length) if length else b"{}"
    return json.loads(raw.decode("utf-8"))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: Any) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _user(self) -> tuple[str, str]:
        role = self.headers.get("X-Role", "guest")
        user = self.headers.get("X-User", "guest")
        if role not in ROLES:
            role = "guest"
        return user, role

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        user, role = self._user()
        if parsed.path == "/health":
            return self._send(200, {"ok": True})
        if parsed.path == "/items":
            return self._send(200, {"items": [visible_item(i, role, user) for i in store.items.values()]})
        if parsed.path.startswith("/items/"):
            item = store.items.get(parsed.path.rsplit("/", 1)[-1])
            if not item:
                return self._send(404, {"error": "not found"})
            return self._send(200, visible_item(item, role, user))
        return self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        user, role = self._user()
        payload = parse_json(self)
        if parsed.path == "/items":
            if role == "guest":
                return self._send(403, {"error": "access denied"})
            item = store.create_item(payload, user)
            return self._send(201, {"item_id": item.item_id, "status": item.status})
        if parsed.path.startswith("/items/") and parsed.path.endswith("/review"):
            item_id = parsed.path.split("/")[2]
            item = store.items.get(item_id)
            if not item:
                return self._send(404, {"error": "not found"})
            if role not in {"project_manager", "administrator"}:
                return self._send(403, {"error": "review forbidden"})
            item.status = payload.get("status", "reviewed")
            item.approved_by = user
            item.history.append(HistoryEntry(now_iso(), user, "reviewed", reason=payload.get("reason")))
            return self._send(200, {"item_id": item.item_id, "status": item.status})
        if parsed.path.startswith("/items/") and parsed.path.endswith("/compare"):
            item_id = parsed.path.split("/")[2]
            item = store.items.get(item_id)
            if not item:
                return self._send(404, {"error": "not found"})
            a = int(payload.get("version_a", 1))
            b = int(payload.get("version_b", len(item.versions) + 1))
            versions = {v.version: v for v in item.versions}
            if b == len(item.versions) + 1:
                versions[b] = ItemVersion(b, item.data, item.history, item.status)
            va, vb = versions.get(a), versions.get(b)
            if not va or not vb:
                return self._send(400, {"error": "invalid version"})
            return self._send(200, {"version_a": asdict(va), "version_b": asdict(vb)})
        if parsed.path == "/import":
            if role == "guest":
                return self._send(403, {"error": "access denied"})
            imported = []
            for row in payload.get("items", []):
                imported.append(store.create_item(row, user).item_id)
            return self._send(201, {"imported": imported})
        return self._send(404, {"error": "not found"})

    def do_PUT(self) -> None:
        parsed = urlparse(self.path)
        user, role = self._user()
        payload = parse_json(self)
        if parsed.path.startswith("/items/"):
            item = store.items.get(parsed.path.rsplit("/", 1)[-1])
            if not item:
                return self._send(404, {"error": "not found"})
            if role == "guest":
                return self._send(403, {"error": "access denied"})
            store.update_item(item, payload, user, payload.get("reason"))
            return self._send(200, {"item_id": item.item_id, "status": item.status})
        return self._send(404, {"error": "not found"})

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("SPRAT listening on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
