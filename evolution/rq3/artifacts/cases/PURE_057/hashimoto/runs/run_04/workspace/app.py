from flask import Flask, jsonify, request
from datetime import datetime, timezone
from copy import deepcopy
from uuid import uuid4

app = Flask(__name__)

DATA = {
    "users": {
        "admin": {"role": "administrator"},
        "pm": {"role": "project_manager"},
        "analyst": {"role": "analyst"},
        "guest": {"role": "guest"},
    },
    "projects": {}
}

ROLE_ORDER = {"guest": 0, "analyst": 1, "project_manager": 2, "administrator": 3}


def now():
    return datetime.now(timezone.utc).isoformat()


def get_user():
    username = request.headers.get("X-User", "guest")
    user = DATA["users"].get(username)
    if not user:
        username = "guest"
        user = DATA["users"]["guest"]
    return username, user


def ensure_project(project_id):
    project = DATA["projects"].get(project_id)
    if not project:
        project = {"id": project_id, "items": {}, "allow_guest_drafts": False}
        DATA["projects"][project_id] = project
    return project


def visible_metadata(item, username, role, project):
    sensitive = item.get("sensitive", False)
    status = item.get("status", "draft")
    own = item.get("author") == username
    allowed_reviewer = username in item.get("reviewers", [])
    is_admin = role == "administrator"
    is_pm = role == "project_manager"

    if sensitive and not (own or allowed_reviewer or is_admin):
        return {"id": item["id"], "hidden": True, "reason": "sensitive"}

    meta = {
        "id": item["id"],
        "type": item.get("type"),
        "title": item.get("title"),
        "status": status,
        "author": item.get("author"),
        "updated_at": item.get("updated_at"),
        "version": item.get("version", 1),
    }
    if status == "draft":
        if role == "guest" and not project.get("allow_guest_drafts"):
            return {"id": item["id"], "hidden": True, "reason": "guest_not_allowed"}
        meta["draft_visible"] = True
        if role in ("administrator", "project_manager") or own or allowed_reviewer:
            meta["reviewers"] = item.get("reviewers", [])
            meta["summary"] = item.get("summary")
        elif role == "analyst":
            meta["summary"] = item.get("summary")
    if status in ("reviewed", "final"):
        meta["summary"] = item.get("summary")
    if is_pm or is_admin or own or allowed_reviewer:
        meta["traceability"] = item.get("traceability", [])
    return meta


def visible_content(item, username, role):
    sensitive = item.get("sensitive", False)
    status = item.get("status", "draft")
    own = item.get("author") == username
    allowed_reviewer = username in item.get("reviewers", [])
    is_admin = role == "administrator"
    is_pm = role == "project_manager"
    if sensitive and not (own or allowed_reviewer or is_admin):
        return None
    if status == "draft" and not (own or allowed_reviewer or is_pm or is_admin):
        return None
    if status == "draft" and role == "analyst":
        return {"summary": item.get("summary")}
    return item


@app.post("/projects/<project_id>/items")
def create_item(project_id):
    username, user = get_user()
    if user["role"] == "guest":
        return jsonify({"error": "forbidden"}), 403
    project = ensure_project(project_id)
    payload = request.get_json(force=True)
    item_id = str(uuid4())
    item = {
        "id": item_id,
        "project_id": project_id,
        "type": payload.get("type", "requirement"),
        "title": payload.get("title", "Untitled"),
        "content": payload.get("content", {}),
        "summary": payload.get("summary", ""),
        "traceability": payload.get("traceability", []),
        "classifications": payload.get("classifications", []),
        "tags": payload.get("tags", []),
        "status": "draft",
        "author": username,
        "created_at": now(),
        "updated_at": now(),
        "history": [],
        "version": 1,
        "reviewers": payload.get("reviewers", []),
        "sensitive": bool(payload.get("sensitive", False)),
        "unresolved": bool(payload.get("unresolved", False)),
        "assumptions": payload.get("assumptions", []),
        "conflicts": payload.get("conflicts", []),
        "exceptions": payload.get("exceptions", []),
    }
    item["history"].append({"action": "create", "user": username, "timestamp": now(), "reason": payload.get("reason")})
    project["items"][item_id] = item
    return jsonify({"item": visible_metadata(item, username, user["role"], project)}), 201


@app.get("/projects/<project_id>/items/<item_id>")
def get_item(project_id, item_id):
    username, user = get_user()
    project = DATA["projects"].get(project_id)
    if not project or item_id not in project["items"]:
        return jsonify({"error": "not_found"}), 404
    item = project["items"][item_id]
    meta = visible_metadata(item, username, user["role"], project)
    content = visible_content(item, username, user["role"])
    return jsonify({"metadata": meta, "content": content, "history": item["history"]})


@app.put("/projects/<project_id>/items/<item_id>")
def edit_item(project_id, item_id):
    username, user = get_user()
    project = DATA["projects"].get(project_id)
    if not project or item_id not in project["items"]:
        return jsonify({"error": "not_found"}), 404
    item = project["items"][item_id]
    if user["role"] == "guest":
        return jsonify({"error": "forbidden"}), 403
    payload = request.get_json(force=True)
    item["version"] += 1
    item["updated_at"] = now()
    for field in ["title", "content", "summary", "traceability", "classifications", "tags", "sensitive", "unresolved", "assumptions", "conflicts", "exceptions"]:
        if field in payload:
            item[field] = payload[field]
    item["status"] = "draft" if item.get("status") == "final" else payload.get("status", item.get("status", "draft"))
    item["history"].append({"action": "edit", "user": username, "timestamp": now(), "reason": payload.get("reason")})
    return jsonify({"item": visible_metadata(item, username, user["role"], project)})


@app.post("/projects/<project_id>/items/<item_id>/review")
def review_item(project_id, item_id):
    username, user = get_user()
    project = DATA["projects"].get(project_id)
    if not project or item_id not in project["items"]:
        return jsonify({"error": "not_found"}), 404
    item = project["items"][item_id]
    if user["role"] not in ("project_manager", "administrator") and username not in item.get("reviewers", []):
        return jsonify({"error": "forbidden"}), 403
    payload = request.get_json(force=True)
    approved = bool(payload.get("approved", True))
    item["status"] = "final" if approved else "reviewed"
    item["history"].append({"action": "review", "user": username, "timestamp": now(), "approved": approved, "reason": payload.get("reason")})
    return jsonify({"item": visible_metadata(item, username, user["role"], project)})


@app.get("/projects/<project_id>/compare")
def compare_items(project_id):
    project = DATA["projects"].get(project_id)
    if not project:
        return jsonify({"error": "not_found"}), 404
    a = request.args.get("a")
    b = request.args.get("b")
    ia = project["items"].get(a)
    ib = project["items"].get(b)
    if not ia or not ib:
        return jsonify({"error": "not_found"}), 404
    return jsonify({"a": {"id": ia["id"], "title": ia["title"], "status": ia["status"], "traceability": ia["traceability"]}, "b": {"id": ib["id"], "title": ib["title"], "status": ib["status"], "traceability": ib["traceability"]}})


@app.post("/projects/<project_id>/import")
def import_items(project_id):
    username, user = get_user()
    if user["role"] == "guest":
        return jsonify({"error": "forbidden"}), 403
    project = ensure_project(project_id)
    payload = request.get_json(force=True)
    imported = []
    for raw in payload.get("items", []):
        item = {
            "id": str(uuid4()),
            "project_id": project_id,
            "type": raw.get("type", "requirement"),
            "title": raw.get("title", "Imported item"),
            "content": raw.get("content", {}),
            "summary": raw.get("summary", ""),
            "traceability": raw.get("traceability", []),
            "classifications": raw.get("classifications", []),
            "tags": raw.get("tags", []),
            "status": raw.get("status", "draft"),
            "author": username,
            "created_at": now(),
            "updated_at": now(),
            "history": [{"action": "import", "user": username, "timestamp": now()}],
            "version": raw.get("version", 1),
            "reviewers": raw.get("reviewers", []),
            "sensitive": bool(raw.get("sensitive", False)),
            "unresolved": bool(raw.get("unresolved", False)),
            "assumptions": raw.get("assumptions", []),
            "conflicts": raw.get("conflicts", []),
            "exceptions": raw.get("exceptions", []),
        }
        project["items"][item["id"]] = item
        imported.append(item["id"])
    return jsonify({"imported": imported}), 201


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
