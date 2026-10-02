from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import uuid


ROLES = {"admin", "project_manager", "analyst", "guest"}
PERMISSIONS = {
    "admin": {"create", "read", "update", "delete", "compare", "view_history", "revert"},
    "project_manager": {"create", "read", "update", "compare", "view_history", "revert"},
    "analyst": {"create", "read", "update", "compare", "view_history", "revert"},
    "guest": {"read", "compare"},
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class VersionEntry:
    version_id: str
    timestamp: str
    user: str
    action: str
    before: Optional[Dict[str, Any]]
    after: Optional[Dict[str, Any]]


@dataclass
class Artifact:
    id: str
    kind: str
    title: str
    content: str = ""
    classifications: List[str] = field(default_factory=list)
    primary_source: Optional[str] = None
    source_ids: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)
    history: List[VersionEntry] = field(default_factory=list)

    def snapshot(self) -> Dict[str, Any]:
        data = asdict(self)
        data["history"] = [asdict(v) for v in self.history]
        return data


class SPRATApp:
    def __init__(self, db_path: str | Path = "sprat_store.json") -> None:
        self.db_path = Path(db_path)
        self.state = {"users": {}, "artifacts": {}}
        if self.db_path.exists():
            self.state = json.loads(self.db_path.read_text())

    def save(self) -> None:
        self.db_path.write_text(json.dumps(self.state, indent=2, sort_keys=True))

    def add_user(self, username: str, role: str) -> None:
        if role not in ROLES:
            raise ValueError(f"Unknown role: {role}")
        self.state["users"][username] = {"role": role}
        self.save()

    def _role(self, username: str) -> str:
        if username not in self.state["users"]:
            raise ValueError(f"Unknown user: {username}")
        return self.state["users"][username]["role"]

    def _check(self, username: str, action: str) -> None:
        if action not in PERMISSIONS[self._role(username)]:
            raise PermissionError(f"{username} cannot {action}")

    def create_artifact(self, username: str, kind: str, title: str, content: str = "", classifications: Optional[List[str]] = None, source_ids: Optional[List[str]] = None, primary_source: Optional[str] = None) -> Artifact:
        self._check(username, "create")
        aid = str(uuid.uuid4())
        artifact = Artifact(id=aid, kind=kind, title=title, content=content, classifications=classifications or [], source_ids=source_ids or [], primary_source=primary_source)
        artifact.history.append(VersionEntry(str(uuid.uuid4()), now_iso(), username, "create", None, artifact.snapshot()))
        self.state["artifacts"][aid] = artifact.snapshot()
        self.save()
        return artifact

    def get_artifact(self, username: str, artifact_id: str) -> Dict[str, Any]:
        self._check(username, "read")
        return self.state["artifacts"][artifact_id]

    def link_artifacts(self, username: str, source_id: str, target_id: str) -> None:
        self._check(username, "update")
        for left, right in [(source_id, target_id), (target_id, source_id)]:
            art = self.state["artifacts"][left]
            if right not in art["links"]:
                art["links"].append(right)
                art["updated_at"] = now_iso()
                art["history"].append(asdict(VersionEntry(str(uuid.uuid4()), now_iso(), username, "link", None, art.copy())))
        self.save()

    def update_artifact(self, username: str, artifact_id: str, **changes: Any) -> None:
        self._check(username, "update")
        art = self.state["artifacts"][artifact_id]
        before = json.loads(json.dumps(art))
        for key, value in changes.items():
            if key in art:
                art[key] = value
        art["updated_at"] = now_iso()
        art["history"].append(asdict(VersionEntry(str(uuid.uuid4()), now_iso(), username, "update", before, json.loads(json.dumps(art)))))
        self.save()

    def compare_artifacts(self, username: str, left_id: str, right_id: str) -> Dict[str, Any]:
        self._check(username, "compare")
        left = self.state["artifacts"][left_id]
        right = self.state["artifacts"][right_id]
        keys = sorted(set(left) | set(right))
        return {k: {"left": left.get(k), "right": right.get(k)} for k in keys if left.get(k) != right.get(k)}

    def history(self, username: str, artifact_id: str) -> List[Dict[str, Any]]:
        self._check(username, "view_history")
        return self.state["artifacts"][artifact_id]["history"]

    def revert(self, username: str, artifact_id: str, version_index: int) -> None:
        self._check(username, "revert")
        art = self.state["artifacts"][artifact_id]
        snap = art["history"][version_index]["after"]
        if snap is None:
            raise ValueError("Cannot revert to empty version")
        art.update(json.loads(json.dumps(snap)))
        art["updated_at"] = now_iso()
        art["history"].append(asdict(VersionEntry(str(uuid.uuid4()), now_iso(), username, "revert", None, json.loads(json.dumps(art)))))
        self.save()
