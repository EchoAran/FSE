from flask import Flask, jsonify, request, abort, Response
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from datetime import datetime, timezone
import json
import uuid

app = Flask(__name__)

ROLES = {"admin", "project_manager", "analyst", "guest"}
ROLE_ORDER = {"guest": 0, "analyst": 1, "project_manager": 2, "admin": 3}

@dataclass
class TraceLink:
    target_id: str
    relation: str
    policy_ref: Optional[str] = None
    policy_excerpt: Optional[str] = None
    rationale: Optional[str] = None
    created_by: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Item:
    id: str
    project_id: str
    type: str
    title: str
    description: str = ""
    classifications: List[str] = field(default_factory=list)
    trace_links: List[TraceLink] = field(default_factory=list)
    audit: List[dict] = field(default_factory=list)
    sensitive: bool = False
    approved: bool = True
    active: bool = True

@dataclass
class Project:
    id: str
    name: str
    sensitivity: str = "low"
    items: Dict[str, Item] = field(default_factory=dict)

DATA = {
    "projects": {},
    "users": {
        "admin": {"role": "admin"},
        "pm": {"role": "project_manager"},
        "analyst": {"role": "analyst"},
        "guest": {"role": "guest"},
    },
}


def now():
    return datetime.now(timezone.utc).isoformat()


def require_role(min_role: str):
    user = request.headers.get("X-User", "guest")
    role = DATA["users"].get(user, {"role": "guest"})["role"]
    if ROLE_ORDER[role] < ROLE_ORDER[min_role]:
        abort(403)
    return user, role


def get_project(pid):
    project = DATA["projects"].get(pid)
    if not project:
        abort(404)
    return project


def item_to_dict(item: Item, role: str):
    d = asdict(item)
    d["trace_links"] = [asdict(t) for t in item.trace_links]
    if role == "guest":
        d.pop("description", None)
        for t in d["trace_links"]:
            t.pop("policy_excerpt", None)
            t.pop("rationale", None)
    return d

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/projects")
def create_project():
    require_role("project_manager")
    payload = request.get_json(force=True)
    pid = payload.get("id") or str(uuid.uuid4())
    project = Project(id=pid, name=payload["name"], sensitivity=payload.get("sensitivity", "low"))
    DATA["projects"][pid] = project
    return jsonify({"id": pid, "name": project.name, "sensitivity": project.sensitivity})

@app.get("/projects/<pid>")
def get_project_api(pid):
    _, role = require_role("guest")
    project = get_project(pid)
    return jsonify({"id": project.id, "name": project.name, "sensitivity": project.sensitivity, "items": [item_to_dict(i, role) for i in project.items.values()]})

@app.post("/projects/<pid>/items")
def create_item(pid):
    require_role("analyst")
    project = get_project(pid)
    payload = request.get_json(force=True)
    iid = payload.get("id") or str(uuid.uuid4())
    item = Item(
        id=iid,
        project_id=pid,
        type=payload["type"],
        title=payload["title"],
        description=payload.get("description", ""),
        classifications=payload.get("classifications", []),
        sensitive=payload.get("sensitive", False),
        approved=payload.get("approved", True),
    )
    item.audit.append({"action": "create", "by": request.headers.get("X-User", "guest"), "when": now(), "details": payload})
    project.items[iid] = item
    return jsonify(item_to_dict(item, "admin"))

@app.post("/projects/<pid>/items/<iid>/trace")
def add_trace(pid, iid):
    user, role = require_role("analyst")
    project = get_project(pid)
    item = project.items[iid]
    payload = request.get_json(force=True)
    target_id = payload["target_id"]
    if target_id not in project.items:
        abort(404)
    if item.type == "requirement" and not payload.get("policy_ref"):
        abort(400)
    if project.sensitivity == "high" and role == "analyst" and not payload.get("approved_override"):
        abort(403)
    link = TraceLink(target_id=target_id, relation=payload.get("relation", "derived-from"), policy_ref=payload.get("policy_ref"), policy_excerpt=payload.get("policy_excerpt"), rationale=payload.get("rationale"), created_by=user)
    item.trace_links.append(link)
    item.audit.append({"action": "trace", "by": user, "when": now(), "details": asdict(link)})
    return jsonify({"status": "ok", "trace": asdict(link)})

@app.get("/compare/<pid>/<a>/<b>")
def compare(pid, a, b):
    _, role = require_role("guest")
    project = get_project(pid)
    ia, ib = project.items[a], project.items[b]
    def proj(item):
        return {"type": item.type, "title": item.title, "classifications": item.classifications}
    return jsonify({"left": proj(ia), "right": proj(ib), "same_type": ia.type == ib.type, "same_title": ia.title == ib.title, "role_view": role})

@app.get("/export/<pid>")
def export_project(pid):
    _, role = require_role("project_manager")
    project = get_project(pid)
    fmt = request.args.get("format", "json")
    payload = {"project": {"id": project.id, "name": project.name}, "items": [item_to_dict(i, role) for i in project.items.values()]}
    if fmt == "csv":
        rows = ["id,type,title"] + [f'{i.id},{i.type},{json.dumps(i.title)}' for i in project.items.values()]
        return Response("\n".join(rows), mimetype="text/csv")
    return Response(json.dumps(payload, indent=2), mimetype="application/json")

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "bad request"}), 400

@app.errorhandler(403)
def forbidden(e):
    return jsonify({"error": "forbidden"}), 403

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
