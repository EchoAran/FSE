from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from flask import Flask, abort, g, redirect, render_template, request, url_for

DATA_FILE = Path(os.environ.get('NENIOS_DATA_FILE', '/workspace/nenios_data.json'))

ROLES = {"admin", "office", "teacher", "parent"}


@dataclass
class Family:
    id: int
    name: str
    contacts: List[str]
    children: List[int] = field(default_factory=list)


@dataclass
class Child:
    id: int
    family_id: int
    name: str
    age_group: str
    status: str
    waiting_position: Optional[int] = None
    health_info: str = ""
    immunization_status: str = "missing"
    care_schedule: str = "full-day"


@dataclass
class Classroom:
    id: int
    name: str
    age_group: str
    capacity: int
    enrolled_child_ids: List[int] = field(default_factory=list)


@dataclass
class Invoice:
    id: int
    family_id: int
    child_id: int
    amount: float
    paid: float
    description: str
    created_at: str


@dataclass
class AuditEntry:
    timestamp: str
    user_role: str
    action: str
    target: str
    details: str


class Storage:
    def __init__(self, path: Path):
        self.path = path
        self.state = self._default_state()
        self.load()

    def _default_state(self) -> Dict[str, Any]:
        return {
            "families": [
                asdict(Family(id=1, name="Rivera Family", contacts=["parent1@example.com"], children=[1, 2])),
                asdict(Family(id=2, name="Nguyen Family", contacts=["parent2@example.com"], children=[3])),
            ],
            "children": [
                asdict(Child(id=1, family_id=1, name="Ava Rivera", age_group="toddler", status="enrolled", health_info="Up to date", immunization_status="current")),
                asdict(Child(id=2, family_id=1, name="Milo Rivera", age_group="toddler", status="waiting", waiting_position=1, health_info="Missing physical form", immunization_status="due")),
                asdict(Child(id=3, family_id=2, name="Linh Nguyen", age_group="preschool", status="pending", waiting_position=1, health_info="Up to date", immunization_status="current")),
            ],
            "classrooms": [
                asdict(Classroom(id=1, name="Toddler Room", age_group="toddler", capacity=1, enrolled_child_ids=[1])),
                asdict(Classroom(id=2, name="Preschool Room", age_group="preschool", capacity=2, enrolled_child_ids=[])),
            ],
            "invoices": [
                asdict(Invoice(id=1, family_id=1, child_id=1, amount=500.0, paid=250.0, description="Monthly tuition", created_at=date.today().isoformat())),
                asdict(Invoice(id=2, family_id=1, child_id=2, amount=500.0, paid=0.0, description="Monthly tuition", created_at=date.today().isoformat())),
                asdict(Invoice(id=3, family_id=2, child_id=3, amount=450.0, paid=450.0, description="Monthly tuition", created_at=date.today().isoformat())),
            ],
            "audit": [],
            "next_ids": {"family": 3, "child": 4, "classroom": 3, "invoice": 4},
        }

    def load(self) -> None:
        if self.path.exists():
            self.state = json.loads(self.path.read_text())
        else:
            self.save()

    def save(self) -> None:
        self.path.write_text(json.dumps(self.state, indent=2))

    def audit(self, role: str, action: str, target: str, details: str) -> None:
        self.state.setdefault("audit", []).append(asdict(AuditEntry(timestamp=datetime.utcnow().isoformat(), user_role=role, action=action, target=target, details=details)))
        self.save()

    def find_family(self, family_id: int) -> Dict[str, Any]:
        for fam in self.state["families"]:
            if fam["id"] == family_id:
                return fam
        abort(404)

    def find_child(self, child_id: int) -> Dict[str, Any]:
        for child in self.state["children"]:
            if child["id"] == child_id:
                return child
        abort(404)

    def find_classroom(self, classroom_id: int) -> Dict[str, Any]:
        for room in self.state["classrooms"]:
            if room["id"] == classroom_id:
                return room
        abort(404)


def create_app() -> Flask:
    app = Flask(__name__)
    storage = Storage(DATA_FILE)

    def current_role() -> str:
        role = request.args.get("role", "office")
        if role not in ROLES:
            abort(403)
        return role

    @app.before_request
    def load_user():
        g.role = current_role()

    def require_roles(*roles: str):
        if g.role not in roles:
            abort(403)

    def capacity_summary() -> List[Dict[str, Any]]:
        summary = []
        for room in storage.state["classrooms"]:
            summary.append({
                **room,
                "enrolled_count": len(room["enrolled_child_ids"]),
                "available_spots": room["capacity"] - len(room["enrolled_child_ids"]),
            })
        return summary

    def next_waiting_child(age_group: str) -> Optional[Dict[str, Any]]:
        waiting = [c for c in storage.state["children"] if c["status"] in {"waiting", "pending"} and c["age_group"] == age_group]
        waiting.sort(key=lambda c: (c.get("waiting_position") or 9999, c["id"]))
        return waiting[0] if waiting else None

    @app.route("/")
    def dashboard():
        return render_template(
            "dashboard.html",
            role=g.role,
            families=storage.state["families"],
            children=storage.state["children"],
            classrooms=capacity_summary(),
            invoices=storage.state["invoices"],
            audit=storage.state["audit"][-10:],
            next_waiting=next_waiting_child("toddler"),
        )

    @app.route("/families")
    def families():
        return render_template("families.html", role=g.role, families=storage.state["families"], children=storage.state["children"])

    @app.route("/enrollment")
    def enrollment():
        children = storage.state["children"]
        return render_template("enrollment.html", role=g.role, children=children, classrooms=capacity_summary())

    @app.route("/health")
    def health():
        reminders = [c for c in storage.state["children"] if c["immunization_status"] != "current" or not c["health_info"]]
        return render_template("health.html", role=g.role, reminders=reminders)

    @app.route("/billing")
    def billing():
        summaries = []
        for fam in storage.state["families"]:
            fam_invoices = [i for i in storage.state["invoices"] if i["family_id"] == fam["id"]]
            billed = sum(i["amount"] for i in fam_invoices)
            paid = sum(i["paid"] for i in fam_invoices)
            summaries.append({"family": fam, "billed": billed, "paid": paid, "outstanding": billed - paid, "invoices": fam_invoices})
        return render_template("billing.html", role=g.role, summaries=summaries)

    @app.route("/promote/<int:child_id>", methods=["POST"])
    def promote(child_id: int):
        require_roles("admin", "office")
        child = storage.find_child(child_id)
        room = next((r for r in storage.state["classrooms"] if r["age_group"] == child["age_group"]), None)
        if not room:
            abort(400)
        if len(room["enrolled_child_ids"]) >= room["capacity"]:
            abort(409, description="Classroom is full")
        room["enrolled_child_ids"].append(child_id)
        child["status"] = "enrolled"
        child["waiting_position"] = None
        storage.audit(g.role, "promote", f"child:{child_id}", f"Moved to {room['name']}")
        storage.save()
        return redirect(url_for("enrollment", role=g.role))

    @app.route("/audit")
    def audit():
        require_roles("admin", "office")
        q = request.args.get("q", "").lower()
        entries = storage.state["audit"]
        if q:
            entries = [e for e in entries if q in json.dumps(e).lower()]
        return render_template("audit.html", role=g.role, audit=entries)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
