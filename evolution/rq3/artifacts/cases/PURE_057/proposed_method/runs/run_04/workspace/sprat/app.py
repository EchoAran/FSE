from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AuditEvent:
    timestamp: str
    actor: str
    action: str
    item_type: str
    item_id: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Item:
    id: str
    type: str
    title: str
    description: str = ""
    classifications: List[str] = field(default_factory=list)
    status: str = "draft"
    source_policy_ref: Optional[str] = None
    source_policy_excerpt: Optional[str] = None
    rationale: Optional[str] = None
    actor: Optional[str] = None
    trigger: Optional[str] = None
    outcome: Optional[str] = None
    derived_from: List[str] = field(default_factory=list)
    links: List[Dict[str, Any]] = field(default_factory=list)
    history: List[Dict[str, Any]] = field(default_factory=list)
    sensitive_notes: Optional[str] = None
    evidence: Optional[str] = None


class SpratStore:
    def __init__(self):
        self.items: Dict[str, Item] = {}
        self.audit: List[AuditEvent] = []
        self.counter = 1

    def create_item(self, actor: str, payload: Dict[str, Any]) -> Item:
        item_id = f"I{self.counter:04d}"
        self.counter += 1
        item = Item(id=item_id, type=payload["type"], title=payload["title"], description=payload.get("description", ""))
        for field_name in ["classifications", "status", "source_policy_ref", "source_policy_excerpt", "rationale", "actor", "trigger", "outcome", "derived_from", "links", "sensitive_notes", "evidence"]:
            if field_name in payload and payload[field_name] is not None:
                setattr(item, field_name, payload[field_name])
        self.items[item_id] = item
        self._audit(actor, "create", item.type, item.id, {"title": item.title})
        return item

    def update_item(self, actor: str, item_id: str, payload: Dict[str, Any]) -> Item:
        item = self.items[item_id]
        before = asdict(item)
        for k, v in payload.items():
            if hasattr(item, k) and v is not None:
                setattr(item, k, v)
        item.history.append({"changed_at": now(), "changed_by": actor, "before": before, "after": asdict(item)})
        self._audit(actor, "update", item.type, item.id, {"changed_fields": list(payload.keys())})
        return item

    def link(self, actor: str, source_id: str, target_id: str, relation: str, primary: bool = False) -> None:
        src = self.items[source_id]
        tgt = self.items[target_id]
        link = {"from": source_id, "to": target_id, "relation": relation, "primary": primary, "at": now(), "by": actor}
        src.links.append(link)
        tgt.links.append(link)
        self._audit(actor, "link", src.type, src.id, link)

    def compare(self, left_id: str, right_id: str) -> Dict[str, Any]:
        l = self.items[left_id]
        r = self.items[right_id]
        return {
            "left": asdict(l),
            "right": asdict(r),
            "matches": {"type": l.type == r.type, "classifications": sorted(set(l.classifications) & set(r.classifications))},
            "differences": {
                "title": l.title != r.title,
                "description": l.description != r.description,
                "links_only_left": [x for x in l.links if x not in r.links],
                "links_only_right": [x for x in r.links if x not in l.links],
            },
        }

    def export_json(self) -> Dict[str, Any]:
        return {"items": [asdict(i) for i in self.items.values()], "audit": [asdict(a) for a in self.audit]}

    def _audit(self, actor: str, action: str, item_type: str, item_id: str, details: Dict[str, Any]) -> None:
        self.audit.append(AuditEvent(timestamp=now(), actor=actor, action=action, item_type=item_type, item_id=item_id, details=details))


STORE = SpratStore()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: Any, content_type: str = "application/json"):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            return self._send(200, {"ok": True})
        if parsed.path == "/items":
            return self._send(200, [asdict(i) for i in STORE.items.values()])
        if parsed.path.startswith("/items/"):
            item_id = parsed.path.split("/")[-1]
            if item_id in STORE.items:
                return self._send(200, asdict(STORE.items[item_id]))
            return self._send(404, {"error": "not found"})
        if parsed.path == "/export":
            return self._send(200, STORE.export_json())
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        actor = payload.get("actor", "system")
        if parsed.path == "/items":
            return self._send(201, asdict(STORE.create_item(actor, payload)))
        if parsed.path == "/compare":
            return self._send(200, STORE.compare(payload["left_id"], payload["right_id"]))
        if parsed.path == "/link":
            STORE.link(actor, payload["source_id"], payload["target_id"], payload.get("relation", "derived-from"), payload.get("primary", False))
            return self._send(200, {"ok": True})
        return self._send(404, {"error": "not found"})

    def do_PUT(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        actor = payload.get("actor", "system")
        if parsed.path.startswith("/items/"):
            item_id = parsed.path.split("/")[-1]
            if item_id in STORE.items:
                return self._send(200, asdict(STORE.update_item(actor, item_id, payload)))
            return self._send(404, {"error": "not found"})
        return self._send(404, {"error": "not found"})


def main():
    host = os.environ.get("SPRAT_HOST", "127.0.0.1")
    port = int(os.environ.get("SPRAT_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"SPRAT running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
