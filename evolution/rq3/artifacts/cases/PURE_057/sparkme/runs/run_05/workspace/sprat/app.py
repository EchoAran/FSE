from __future__ import annotations

import json
import itertools
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Version:
    id: int
    timestamp: str
    data: dict
    reason: str = "initial"


@dataclass
class Artifact:
    id: int
    project: str
    kind: str
    title: str
    content: str = ""
    status: str = "draft"
    archived: bool = False
    source: str = ""
    rationale: str = ""
    source_notes: str = ""
    assumptions: str = ""
    owner: str = ""
    links: list = field(default_factory=list)
    comments: list = field(default_factory=list)
    versions: list = field(default_factory=list)

    def snapshot(self) -> dict:
        d = asdict(self)
        d["versions"] = [asdict(v) for v in self.versions]
        return d


class Store:
    def __init__(self) -> None:
        self.projects = {}
        self.artifacts = {}
        self.glossary = {
            "policy": {"definition": "An approved rule or source policy.", "examples": ["security policy"]},
            "requirement": {"definition": "A captured need or constraint.", "examples": ["access control requirement"]},
        }
        self._artifact_ids = itertools.count(1)
        self.conflicts = []
        self.import_queue = []

    def create_project(self, name: str, owner: str = "system") -> dict:
        self.projects[name] = {"name": name, "owner": owner, "created_at": now_iso(), "items": []}
        return self.projects[name]

    def create_artifact(self, payload: dict) -> Artifact:
        art = Artifact(
            id=next(self._artifact_ids),
            project=payload.get("project", "default"),
            kind=payload.get("kind", "requirement"),
            title=payload.get("title", "Untitled"),
            content=payload.get("content", ""),
            status=payload.get("status", "draft"),
            source=payload.get("source", ""),
            rationale=payload.get("rationale", ""),
            source_notes=payload.get("source_notes", ""),
            assumptions=payload.get("assumptions", ""),
            owner=payload.get("owner", "analyst"),
        )
        art.versions.append(Version(id=1, timestamp=now_iso(), data=art.snapshot(), reason="created"))
        self.artifacts[art.id] = art
        self.projects.setdefault(art.project, {"name": art.project, "owner": "system", "created_at": now_iso(), "items": []})["items"].append(art.id)
        return art


store = Store()
store.create_project("default")


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict | list):
    body = json.dumps(payload).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class SpratHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if parsed.path == "/health":
            return json_response(self, 200, {"status": "ok"})
        if parsed.path == "/dashboard":
            return json_response(self, 200, {"current_project": qs.get("project", ["default"])[0], "recent_items": [a.snapshot() for a in list(store.artifacts.values())[-5:]], "unresolved_conflicts": store.conflicts, "review_tasks": store.import_queue})
        if parsed.path == "/artifacts":
            q = qs.get("q", [""])[0].lower()
            items = [a.snapshot() for a in store.artifacts.values() if not q or q in a.title.lower() or q in a.content.lower() or q in a.project.lower()]
            return json_response(self, 200, items)
        if parsed.path == "/search":
            q = qs.get("q", [""])[0].lower()
            result = []
            for art in store.artifacts.values():
                if q in art.title.lower() or q in art.content.lower() or q in art.project.lower():
                    result.append({"id": art.id, "title": art.title, "project": art.project, "status": art.status, "archived": art.archived})
            return json_response(self, 200, {"query": q, "results": result})
        if parsed.path.startswith("/artifacts/"):
            try:
                artifact_id = int(parsed.path.split("/")[2])
            except Exception:
                return json_response(self, 400, {"error": "bad request"})
            art = store.artifacts.get(artifact_id)
            if not art:
                return json_response(self, 404, {"error": "not found"})
            return json_response(self, 200, art.snapshot())
        return json_response(self, 404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length) or b"{}")
        if parsed.path == "/projects":
            return json_response(self, 200, store.create_project(data["name"], data.get("owner", "system")))
        if parsed.path == "/artifacts":
            warnings = []
            term = data.get("title", "").strip().lower()
            if term and term in store.glossary:
                warnings.append({"type": "exact_match", "term": term, "definition": store.glossary[term]["definition"]})
            elif term:
                for g in store.glossary:
                    if term != g and (term in g or g in term):
                        warnings.append({"type": "near_match", "term": term, "suggested": g, "definition": store.glossary[g]["definition"]})
            art = store.create_artifact(data)
            return json_response(self, 201, {"artifact": art.snapshot(), "warnings": warnings})
        if parsed.path.startswith("/artifacts/") and parsed.path.endswith("/comments"):
            artifact_id = int(parsed.path.split("/")[2])
            art = store.artifacts.get(artifact_id)
            if not art:
                return json_response(self, 404, {"error": "not found"})
            comment = {"author": data.get("author", "guest"), "text": data.get("text", ""), "timestamp": now_iso()}
            art.comments.append(comment)
            return json_response(self, 201, comment)
        if parsed.path.startswith("/artifacts/") and parsed.path.endswith("/conflict"):
            artifact_id = int(parsed.path.split("/")[2])
            art = store.artifacts.get(artifact_id)
            if not art:
                return json_response(self, 404, {"error": "not found"})
            conflict = {"artifact_id": artifact_id, "left": data.get("left", {}), "right": data.get("right", {}), "status": "needs review", "created_at": now_iso()}
            store.conflicts.append(conflict)
            return json_response(self, 201, conflict)
        if parsed.path == "/imports":
            staged = []
            for item in data.get("items", []):
                staged.append({"source_value": item, "suggested_mapping": item.get("suggested_mapping"), "status": "review queue" if item.get("ambiguous") else "staged", "reason": item.get("reason", "")})
            store.import_queue.extend(staged)
            return json_response(self, 202, {"staged": staged, "published": False})
        return json_response(self, 404, {"error": "not found"})


def run(host: str = "0.0.0.0", port: int = 8000):
    server = ThreadingHTTPServer((host, port), SpratHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
