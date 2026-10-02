from __future__ import annotations

import copy
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from uuid import uuid4

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

ROLE_PERMISSIONS = {
    "admin": {"create", "read", "update", "delete", "compare", "history", "link", "audit"},
    "project_manager": {"create", "read", "update", "compare", "history", "link", "audit"},
    "analyst": {"create", "read", "update", "compare", "history", "link", "audit"},
    "guest": {"read", "compare", "history"},
}

ARTIFACT_TYPES = {"goal", "scenario", "requirement", "policy", "compliance_note", "classification"}

@dataclass
class ArtifactVersion:
    version: int
    timestamp: str
    actor: str
    action: str
    data: Dict[str, Any]

@dataclass
class Artifact:
    id: str
    type: str
    title: str
    description: str = ""
    sources: List[str] = field(default_factory=list)
    primary_source: Optional[str] = None
    links: List[str] = field(default_factory=list)
    classification: Optional[str] = None
    created_by: str = "system"
    created_at: str = ""
    updated_at: str = ""
    version: int = 1
    history: List[ArtifactVersion] = field(default_factory=list)

store: Dict[str, Artifact] = {}
audit_log: List[Dict[str, Any]] = []


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def actor_role() -> str:
    return request.headers.get("X-Role", "guest")


def actor_name() -> str:
    return request.headers.get("X-User", "anonymous")


def require_permission(permission: str):
    role = actor_role()
    if permission not in ROLE_PERMISSIONS.get(role, set()):
        abort(403, description=f"role '{role}' lacks permission '{permission}'")


def artifact_to_dict(a: Artifact) -> Dict[str, Any]:
    return {
        "id": a.id,
        "type": a.type,
        "title": a.title,
        "description": a.description,
        "sources": a.sources,
        "primary_source": a.primary_source,
        "links": a.links,
        "classification": a.classification,
        "created_by": a.created_by,
        "created_at": a.created_at,
        "updated_at": a.updated_at,
        "version": a.version,
    }


def log_action(action: str, artifact_id: Optional[str], before: Optional[dict], after: Optional[dict]):
    audit_log.append({
        "timestamp": now_iso(),
        "actor": actor_name(),
        "role": actor_role(),
        "action": action,
        "artifact_id": artifact_id,
        "before": before,
        "after": after,
    })


def snapshot_version(artifact: Artifact, action: str):
    artifact.history.append(ArtifactVersion(
        version=artifact.version,
        timestamp=now_iso(),
        actor=actor_name(),
        action=action,
        data=copy.deepcopy(artifact_to_dict(artifact)),
    ))


def get_artifact_or_404(artifact_id: str) -> Artifact:
    artifact = store.get(artifact_id)
    if not artifact:
        abort(404, description="artifact not found")
    return artifact


@app.get("/")
def index():
    return jsonify({
        "name": "SPRAT",
        "description": "Security and Privacy Requirements Analysis Tool",
        "endpoints": ["/artifacts", "/compare", "/audit"],
    })


@app.get("/artifacts")
def list_artifacts():
    require_permission("read")
    artifact_type = request.args.get("type")
    items = [artifact_to_dict(a) for a in store.values() if not artifact_type or a.type == artifact_type]
    return jsonify(items)


@app.post("/artifacts")
def create_artifact():
    require_permission("create")
    payload = request.get_json(force=True, silent=False) or {}
    a_type = payload.get("type")
    title = payload.get("title")
    if a_type not in ARTIFACT_TYPES:
        abort(400, description="invalid or missing artifact type")
    if not title:
        abort(400, description="title is required")
    artifact_id = str(uuid4())
    artifact = Artifact(
        id=artifact_id,
        type=a_type,
        title=title,
        description=payload.get("description", ""),
        sources=list(payload.get("sources", [])),
        primary_source=payload.get("primary_source"),
        links=list(payload.get("links", [])),
        classification=payload.get("classification"),
        created_by=actor_name(),
        created_at=now_iso(),
        updated_at=now_iso(),
    )
    if artifact.primary_source and artifact.primary_source not in artifact.sources:
        artifact.sources.append(artifact.primary_source)
    snapshot_version(artifact, "create")
    store[artifact_id] = artifact
    log_action("create", artifact_id, None, artifact_to_dict(artifact))
    return jsonify(artifact_to_dict(artifact)), 201


@app.get("/artifacts/<artifact_id>")
def get_artifact(artifact_id: str):
    require_permission("read")
    return jsonify(artifact_to_dict(get_artifact_or_404(artifact_id)))


@app.patch("/artifacts/<artifact_id>")
def update_artifact(artifact_id: str):
    require_permission("update")
    artifact = get_artifact_or_404(artifact_id)
    before = artifact_to_dict(artifact)
    payload = request.get_json(force=True, silent=False) or {}
    for field_name in ["title", "description", "classification", "primary_source"]:
        if field_name in payload:
            setattr(artifact, field_name, payload[field_name])
    if "sources" in payload:
        artifact.sources = list(payload["sources"])
    if artifact.primary_source and artifact.primary_source not in artifact.sources:
        artifact.sources.append(artifact.primary_source)
    if "links" in payload:
        artifact.links = list(payload["links"])
    artifact.version += 1
    artifact.updated_at = now_iso()
    snapshot_version(artifact, "update")
    log_action("update", artifact_id, before, artifact_to_dict(artifact))
    return jsonify(artifact_to_dict(artifact))


@app.post("/artifacts/<artifact_id>/link")
def link_artifacts(artifact_id: str):
    require_permission("link")
    artifact = get_artifact_or_404(artifact_id)
    payload = request.get_json(force=True, silent=False) or {}
    target_id = payload.get("target_id")
    if not target_id or target_id not in store:
        abort(400, description="valid target_id required")
    if target_id not in artifact.links:
        artifact.links.append(target_id)
        artifact.version += 1
        artifact.updated_at = now_iso()
        snapshot_version(artifact, "link")
        log_action("link", artifact_id, None, artifact_to_dict(artifact))
    return jsonify(artifact_to_dict(artifact))


@app.get("/artifacts/<artifact_id>/trace")
def trace_artifact(artifact_id: str):
    require_permission("read")
    artifact = get_artifact_or_404(artifact_id)
    source_artifacts = [artifact_to_dict(store[s]) for s in artifact.sources if s in store]
    related_requirements = []
    if artifact.type in {"policy", "compliance_note", "classification"}:
        related_requirements = [artifact_to_dict(a) for a in store.values() if artifact.id in a.sources]
    return jsonify({"artifact": artifact_to_dict(artifact), "sources": source_artifacts, "requirements": related_requirements})


@app.get("/artifacts/<artifact_id>/history")
def artifact_history(artifact_id: str):
    require_permission("history")
    artifact = get_artifact_or_404(artifact_id)
    return jsonify([
        {"version": v.version, "timestamp": v.timestamp, "actor": v.actor, "action": v.action, "data": v.data}
        for v in artifact.history
    ])


@app.post("/artifacts/<artifact_id>/restore/<int:version>")
def restore_version(artifact_id: str, version: int):
    require_permission("update")
    artifact = get_artifact_or_404(artifact_id)
    match = next((v for v in artifact.history if v.version == version), None)
    if not match:
        abort(404, description="version not found")
    before = artifact_to_dict(artifact)
    data = match.data
    artifact.title = data["title"]
    artifact.description = data["description"]
    artifact.sources = list(data["sources"])
    artifact.primary_source = data["primary_source"]
    artifact.links = list(data["links"])
    artifact.classification = data["classification"]
    artifact.version += 1
    artifact.updated_at = now_iso()
    snapshot_version(artifact, "restore")
    log_action("restore", artifact_id, before, artifact_to_dict(artifact))
    return jsonify(artifact_to_dict(artifact))


@app.get("/compare")
def compare_artifacts():
    require_permission("compare")
    left = request.args.get("left")
    right = request.args.get("right")
    if not left or not right:
        abort(400, description="left and right parameters required")
    a = get_artifact_or_404(left)
    b = get_artifact_or_404(right)
    return jsonify({
        "left": artifact_to_dict(a),
        "right": artifact_to_dict(b),
        "differences": {
            key: {"left": artifact_to_dict(a)[key], "right": artifact_to_dict(b)[key]}
            for key in artifact_to_dict(a).keys()
            if artifact_to_dict(a)[key] != artifact_to_dict(b)[key]
        },
    })


@app.get("/audit")
def audit():
    require_permission("audit")
    return jsonify(audit_log)


@app.get("/seed")
def seed():
    if store:
        return jsonify({"seeded": False, "count": len(store)})
    role = actor_role()
    if role not in {"admin", "project_manager", "analyst"}:
        abort(403)
    sample = [
        {"type": "policy", "title": "Privacy Policy", "description": "Sample source policy"},
        {"type": "requirement", "title": "Encrypt data at rest", "sources": []},
        {"type": "goal", "title": "Protect user data"},
    ]
    created = []
    for item in sample:
        with app.test_request_context(headers={"X-Role": role, "X-User": actor_name()}, json=item):
            created.append(create_artifact().json)
    req = created[1]["id"]
    pol = created[0]["id"]
    store[req].sources = [pol]
    store[req].primary_source = pol
    store[req].version += 1
    store[req].updated_at = now_iso()
    snapshot_version(store[req], "seed-link")
    return jsonify({"seeded": True, "artifacts": created})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
