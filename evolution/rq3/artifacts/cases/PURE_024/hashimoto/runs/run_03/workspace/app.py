from flask import Flask, jsonify, request, render_template_string
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from typing import Dict, List, Optional
import itertools

app = Flask(__name__)


def today_iso() -> str:
    return date.today().isoformat()


@dataclass
class Family:
    id: int
    name: str
    contact_name: str
    contact_email: str
    contact_phone: str
    children: List[int] = field(default_factory=list)


@dataclass
class Child:
    id: int
    family_id: int
    name: str
    date_of_birth: str
    classroom_id: Optional[int] = None
    immunizations: List[dict] = field(default_factory=list)


@dataclass
class Classroom:
    id: int
    name: str
    capacity: int
    enrolled_child_ids: List[int] = field(default_factory=list)


@dataclass
class WaitingListEntry:
    id: int
    child_name: str
    family_id: int
    preferred_classroom_id: Optional[int]
    created_at: str
    status: str = "waiting"


@dataclass
class Invoice:
    id: int
    family_id: int
    child_id: int
    amount: float
    description: str
    issued_at: str
    paid: bool = False


class Storage:
    def __init__(self):
        self.family_ids = itertools.count(1)
        self.child_ids = itertools.count(1)
        self.classroom_ids = itertools.count(1)
        self.waiting_ids = itertools.count(1)
        self.invoice_ids = itertools.count(1)
        self.families: Dict[int, Family] = {}
        self.children: Dict[int, Child] = {}
        self.classrooms: Dict[int, Classroom] = {}
        self.waiting_list: Dict[int, WaitingListEntry] = {}
        self.invoices: Dict[int, Invoice] = {}


store = Storage()


def seed_data():
    if store.classrooms:
        return
    c1 = Classroom(id=next(store.classroom_ids), name="Infants", capacity=5)
    c2 = Classroom(id=next(store.classroom_ids), name="Toddlers", capacity=3)
    store.classrooms[c1.id] = c1
    store.classrooms[c2.id] = c2


seed_data()


@app.route("/")
def index():
    return render_template_string(
        """
        <h1>Nenios Child Care Management</h1>
        <p>Use the JSON endpoints to manage families, children, classrooms, waiting list, immunizations, invoices, and reports.</p>
        <ul>
          <li>GET /api/state</li>
          <li>POST /api/families</li>
          <li>POST /api/children</li>
          <li>POST /api/classrooms</li>
          <li>POST /api/waiting-list</li>
          <li>POST /api/immunizations</li>
          <li>POST /api/invoices</li>
          <li>GET /api/reports/operations</li>
          <li>GET /api/reports/customer/&lt;family_id&gt;</li>
        </ul>
        """
    )


@app.route("/api/state")
def state():
    return jsonify({
        "families": [asdict(f) for f in store.families.values()],
        "children": [asdict(c) for c in store.children.values()],
        "classrooms": [asdict(c) for c in store.classrooms.values()],
        "waiting_list": [asdict(w) for w in store.waiting_list.values()],
        "invoices": [asdict(i) for i in store.invoices.values()],
    })


@app.route("/api/families", methods=["POST"])
def create_family():
    data = request.get_json(force=True)
    family = Family(
        id=next(store.family_ids),
        name=data["name"],
        contact_name=data.get("contact_name", ""),
        contact_email=data.get("contact_email", ""),
        contact_phone=data.get("contact_phone", ""),
    )
    store.families[family.id] = family
    return jsonify(asdict(family)), 201


@app.route("/api/children", methods=["POST"])
def create_child():
    data = request.get_json(force=True)
    family_id = int(data["family_id"])
    if family_id not in store.families:
        return jsonify({"error": "family not found"}), 404
    child = Child(
        id=next(store.child_ids),
        family_id=family_id,
        name=data["name"],
        date_of_birth=data["date_of_birth"],
    )
    classroom_id = data.get("classroom_id")
    if classroom_id is not None:
        classroom = store.classrooms.get(int(classroom_id))
        if not classroom:
            return jsonify({"error": "classroom not found"}), 404
        if len(classroom.enrolled_child_ids) >= classroom.capacity:
            return jsonify({"error": "classroom full"}), 409
        classroom.enrolled_child_ids.append(child.id)
        child.classroom_id = classroom.id
    store.children[child.id] = child
    store.families[family_id].children.append(child.id)
    return jsonify(asdict(child)), 201


@app.route("/api/classrooms", methods=["POST"])
def create_classroom():
    data = request.get_json(force=True)
    classroom = Classroom(
        id=next(store.classroom_ids),
        name=data["name"],
        capacity=int(data["capacity"]),
    )
    store.classrooms[classroom.id] = classroom
    return jsonify(asdict(classroom)), 201


@app.route("/api/waiting-list", methods=["POST"])
def add_waiting_list():
    data = request.get_json(force=True)
    family_id = int(data["family_id"])
    if family_id not in store.families:
        return jsonify({"error": "family not found"}), 404
    preferred_classroom_id = data.get("preferred_classroom_id")
    if preferred_classroom_id is not None:
        preferred_classroom_id = int(preferred_classroom_id)
        if preferred_classroom_id not in store.classrooms:
            return jsonify({"error": "classroom not found"}), 404
    entry = WaitingListEntry(
        id=next(store.waiting_ids),
        child_name=data["child_name"],
        family_id=family_id,
        preferred_classroom_id=preferred_classroom_id,
        created_at=today_iso(),
    )
    store.waiting_list[entry.id] = entry
    return jsonify(asdict(entry)), 201


@app.route("/api/immunizations", methods=["POST"])
def add_immunization():
    data = request.get_json(force=True)
    child_id = int(data["child_id"])
    child = store.children.get(child_id)
    if not child:
        return jsonify({"error": "child not found"}), 404
    record = {
        "name": data["name"],
        "date": data.get("date", today_iso()),
        "notes": data.get("notes", ""),
    }
    child.immunizations.append(record)
    return jsonify(asdict(child)), 200


@app.route("/api/invoices", methods=["POST"])
def create_invoice():
    data = request.get_json(force=True)
    family_id = int(data["family_id"])
    child_id = int(data["child_id"])
    if family_id not in store.families:
        return jsonify({"error": "family not found"}), 404
    if child_id not in store.children:
        return jsonify({"error": "child not found"}), 404
    invoice = Invoice(
        id=next(store.invoice_ids),
        family_id=family_id,
        child_id=child_id,
        amount=float(data["amount"]),
        description=data.get("description", "Child care services"),
        issued_at=today_iso(),
    )
    store.invoices[invoice.id] = invoice
    return jsonify(asdict(invoice)), 201


@app.route("/api/reports/operations")
def operations_report():
    enrolled = sum(1 for c in store.children.values() if c.classroom_id is not None)
    capacity = sum(c.capacity for c in store.classrooms.values())
    return jsonify({
        "families": len(store.families),
        "children": len(store.children),
        "classrooms": len(store.classrooms),
        "enrolled_children": enrolled,
        "remaining_capacity": capacity - enrolled,
        "waiting_list": len(store.waiting_list),
        "unpaid_invoices": sum(1 for i in store.invoices.values() if not i.paid),
        "immunization_records": sum(len(c.immunizations) for c in store.children.values()),
    })


@app.route("/api/reports/customer/<int:family_id>")
def customer_report(family_id: int):
    family = store.families.get(family_id)
    if not family:
        return jsonify({"error": "family not found"}), 404
    family_children = [store.children[cid] for cid in family.children if cid in store.children]
    family_invoices = [i for i in store.invoices.values() if i.family_id == family_id]
    return jsonify({
        "family": asdict(family),
        "children": [asdict(c) for c in family_children],
        "invoices": [asdict(i) for i in family_invoices],
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
