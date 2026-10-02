from flask import Flask, jsonify, request, abort, Response
from dataclasses import dataclass, asdict, field
from datetime import datetime, date
from typing import Dict, List, Optional
import uuid

app = Flask(__name__)

ROLES = {"admin", "office", "teacher", "parent"}

USERS = {
    "admin": {"role": "admin"},
    "office": {"role": "office"},
    "teacher": {"role": "teacher"},
    "parent": {"role": "parent"},
}

@dataclass
class Family:
    id: str
    name: str
    contacts: List[str]
    children: List[str] = field(default_factory=list)

@dataclass
class Child:
    id: str
    name: str
    family_id: str
    age_group: str
    classroom_id: Optional[str] = None
    status: str = "pending"
    waiting_list_position: Optional[int] = None
    health_info: str = ""
    immunization_current: bool = False
    care_schedule: str = "full-day"

@dataclass
class Classroom:
    id: str
    name: str
    age_group: str
    capacity: int
    enrolled_children: List[str] = field(default_factory=list)

@dataclass
class Invoice:
    id: str
    family_id: str
    child_id: str
    amount: float
    status: str
    description: str

@dataclass
class AuditEntry:
    timestamp: str
    user: str
    action: str
    entity: str
    entity_id: str
    details: str

families: Dict[str, Family] = {}
children: Dict[str, Child] = {}
classrooms: Dict[str, Classroom] = {}
invoices: Dict[str, Invoice] = {}
audit_log: List[AuditEntry] = []


def log(user, action, entity, entity_id, details):
    audit_log.append(AuditEntry(datetime.utcnow().isoformat() + "Z", user, action, entity, entity_id, details))


def seed():
    c1 = Classroom(id="room-tots", name="Tots Room", age_group="2-3", capacity=2)
    c2 = Classroom(id="room-prek", name="Pre-K Room", age_group="4-5", capacity=3)
    classrooms[c1.id] = c1
    classrooms[c2.id] = c2

    f1 = Family(id="fam1", name="Doe Family", contacts=["jane@example.com", "555-1000"])
    f2 = Family(id="fam2", name="Smith Family", contacts=["sam@example.com"])
    families[f1.id] = f1
    families[f2.id] = f2

    ch1 = Child(id="child1", name="Mia Doe", family_id=f1.id, age_group="2-3", classroom_id=c1.id, status="enrolled", health_info="Asthma action plan on file", immunization_current=True)
    ch2 = Child(id="child2", name="Leo Doe", family_id=f1.id, age_group="4-5", status="waiting", waiting_list_position=1, immunization_current=False)
    ch3 = Child(id="child3", name="Ava Smith", family_id=f2.id, age_group="4-5", classroom_id=c2.id, status="enrolled", health_info="", immunization_current=False)
    for ch in (ch1, ch2, ch3):
        children[ch.id] = ch
        families[ch.family_id].children.append(ch.id)
    classrooms[c1.id].enrolled_children.append(ch1.id)
    classrooms[c2.id].enrolled_children.append(ch3.id)

    inv1 = Invoice(id="inv1", family_id=f1.id, child_id=ch1.id, amount=1200.0, status="paid", description="Monthly tuition")
    inv2 = Invoice(id="inv2", family_id=f1.id, child_id=ch2.id, amount=1200.0, status="outstanding", description="Monthly tuition")
    inv3 = Invoice(id="inv3", family_id=f2.id, child_id=ch3.id, amount=950.0, status="outstanding", description="Monthly tuition")
    for inv in (inv1, inv2, inv3):
        invoices[inv.id] = inv

seed()


def user_role():
    name = request.args.get("user", "office")
    return USERS.get(name, {"role": "office"})["role"], name


def require_role(*allowed):
    role, user = user_role()
    if role not in allowed:
        abort(403)
    return role, user

@app.get("/")
def index():
    return Response(
        """
        <h1>Nenios Child Care Management</h1>
        <ul>
          <li><a href='/dashboard'>Dashboard</a></li>
          <li><a href='/families'>Families</a></li>
          <li><a href='/enrollment'>Enrollment</a></li>
          <li><a href='/billing'>Billing</a></li>
          <li><a href='/health'>Health reminders</a></li>
          <li><a href='/reports'>Reports</a></li>
          <li><a href='/audit'>Audit trail</a></li>
        </ul>
        <p>Use ?user=admin|office|teacher|parent for role simulation.</p>
        """,
        mimetype="text/html",
    )

@app.get("/dashboard")
def dashboard():
    require_role("admin", "office", "teacher")
    enrolled = sum(1 for c in children.values() if c.status == "enrolled")
    waiting = sum(1 for c in children.values() if c.status == "waiting")
    open_spots = {cid: cls.capacity - len(cls.enrolled_children) for cid, cls in classrooms.items()}
    return jsonify({"enrolled": enrolled, "waiting": waiting, "open_spots": open_spots})

@app.get("/families")
def list_families():
    require_role("admin", "office")
    return jsonify([asdict(f) for f in families.values()])

@app.post("/families")
def create_family():
    require_role("admin", "office")
    payload = request.get_json(force=True)
    fid = payload.get("id") or str(uuid.uuid4())
    fam = Family(id=fid, name=payload["name"], contacts=payload.get("contacts", []))
    families[fid] = fam
    log(user_role()[1], "create", "family", fid, fam.name)
    return jsonify(asdict(fam)), 201

@app.get("/enrollment")
def enrollment():
    require_role("admin", "office", "teacher")
    return jsonify({
        "enrolled": [asdict(c) for c in children.values() if c.status == "enrolled"],
        "waiting": sorted([asdict(c) for c in children.values() if c.status == "waiting"], key=lambda x: x["waiting_list_position"] or 999),
    })

@app.post("/enrollment/move_next/<classroom_id>")
def move_next(classroom_id):
    require_role("admin", "office")
    cls = classrooms.get(classroom_id)
    if not cls:
        abort(404)
    waiting = [c for c in children.values() if c.status == "waiting" and c.age_group == cls.age_group]
    waiting.sort(key=lambda c: c.waiting_list_position or 999)
    if not waiting:
        return jsonify({"message": "No matching child on the waiting list"}), 200
    if len(cls.enrolled_children) >= cls.capacity:
        return jsonify({"message": "Classroom is full"}), 409
    child = waiting[0]
    child.status = "enrolled"
    child.classroom_id = cls.id
    child.waiting_list_position = None
    cls.enrolled_children.append(child.id)
    log(user_role()[1], "move", "child", child.id, f"Moved to {cls.id}")
    return jsonify(asdict(child))

@app.get("/classrooms")
def classroom_overview():
    require_role("admin", "office", "teacher")
    return jsonify([
        {"id": c.id, "name": c.name, "age_group": c.age_group, "capacity": c.capacity, "available_spots": c.capacity - len(c.enrolled_children), "enrolled_children": c.enrolled_children}
        for c in classrooms.values()
    ])

@app.get("/health")
def health():
    require_role("admin", "office", "teacher")
    return jsonify({
        "current": [asdict(c) for c in children.values() if c.immunization_current],
        "missing_or_due": [asdict(c) for c in children.values() if not c.immunization_current],
    })

@app.get("/billing")
def billing():
    require_role("admin", "office")
    return jsonify({
        "billed": [asdict(i) for i in invoices.values()],
        "paid": [asdict(i) for i in invoices.values() if i.status == "paid"],
        "outstanding": [asdict(i) for i in invoices.values() if i.status != "paid"],
    })

@app.get("/billing/statement/<family_id>")
def statement(family_id):
    require_role("admin", "office", "parent")
    fam_invoices = [asdict(i) for i in invoices.values() if i.family_id == family_id]
    return jsonify({"family": asdict(families[family_id]), "invoices": fam_invoices})

@app.get("/reports")
def reports():
    require_role("admin", "office")
    return jsonify({
        "daily_snapshot": {"enrollment_count": sum(1 for c in children.values() if c.status == "enrolled"), "classroom_occupancy": {c.name: len(c.enrolled_children) for c in classrooms.values()}},
        "waiting_list": [asdict(c) for c in sorted([c for c in children.values() if c.status == "waiting"], key=lambda c: c.waiting_list_position or 999)],
        "billing_summary": [asdict(i) for i in invoices.values() if i.status != "paid"],
        "health_reminders": [asdict(c) for c in children.values() if not c.immunization_current],
    })

@app.get("/audit")
def audit():
    require_role("admin", "office")
    q = request.args.get("q", "").lower()
    entries = [asdict(e) for e in audit_log if q in " ".join([e.timestamp, e.user, e.action, e.entity, e.entity_id, e.details]).lower()]
    return jsonify(entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
