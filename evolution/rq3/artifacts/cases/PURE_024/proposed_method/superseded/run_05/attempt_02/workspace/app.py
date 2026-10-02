from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import csv
import io
import json


def now_iso() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


@dataclass
class AuditEvent:
    at: str
    action: str
    actor: str
    details: dict


@dataclass
class Classroom:
    id: str
    site: str
    name: str
    capacity: int
    room_type: str = "classroom"


@dataclass
class Family:
    id: str
    name: str
    contacts: List[dict] = field(default_factory=list)
    address: str = ""
    email: str = ""
    phone: str = ""
    children_ids: List[str] = field(default_factory=list)
    billing_notes: str = ""


@dataclass
class Child:
    id: str
    family_id: str
    name: str
    dob: str
    site: str
    classroom_id: Optional[str] = None
    waiting_list: bool = False
    immunization_status: str = "missing"
    immunization_due: Optional[str] = None
    compliance_verified: bool = False
    allergies: List[str] = field(default_factory=list)
    pickup_authority: List[str] = field(default_factory=list)
    attendance: List[dict] = field(default_factory=list)
    notes: str = ""


@dataclass
class Invoice:
    id: str
    family_id: str
    child_id: Optional[str]
    amount: float
    balance: float
    status: str = "open"
    adjustments: List[dict] = field(default_factory=list)
    payments: List[dict] = field(default_factory=list)


state = {"families": {}, "children": {}, "classrooms": {}, "invoices": {}, "waiting_list": [], "audit": []}


def log(action: str, actor: str, details: dict):
    state["audit"].append(AuditEvent(at=now_iso(), action=action, actor=actor, details=details))


def serialize(obj):
    return asdict(obj)


def child_status(child: Child) -> str:
    if child.immunization_status in {"missing", "overdue", "expired", "incomplete", "noncompliant"} or not child.compliance_verified:
        return "not_compliant"
    return "compliant"


def make_response(status: int, body):
    return status, {"Content-Type": "application/json"}, json.dumps(body).encode()


class Handler(BaseHTTPRequestHandler):
    def _json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}") if length else {}

    def _send(self, result):
        status, headers, body = result
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send(make_response(200, {"name": "Nenios Child Care Management", "status": "ok"}))
        elif parsed.path == "/families":
            self._send(make_response(200, [serialize(f) for f in state["families"].values()]))
        elif parsed.path == "/children":
            self._send(make_response(200, [{**serialize(c), "status": child_status(c)} for c in state["children"].values()]))
        elif parsed.path == "/classrooms":
            result = []
            for room in state["classrooms"].values():
                enrolled = sum(1 for c in state["children"].values() if c.classroom_id == room.id)
                result.append({**serialize(room), "enrolled": enrolled, "available": enrolled < room.capacity})
            self._send(make_response(200, result))
        elif parsed.path == "/attendance/review":
            self._send(make_response(200, {cid: c.attendance for cid, c in state["children"].items()}))
        elif parsed.path == "/reports/dashboard":
            self._send(make_response(200, {"families": len(state["families"]), "children": len(state["children"]), "classrooms": len(state["classrooms"]), "waiting_list": list(state["waiting_list"]), "invoices": {iid: serialize(inv) for iid, inv in state["invoices"].items()}, "noncompliant_children": [c.id for c in state["children"].values() if child_status(c) != "compliant"]}))
        elif parsed.path == "/export/csv":
            kind = parse_qs(parsed.query).get("kind", ["families"])[0]
            output = io.StringIO()
            writer = csv.writer(output)
            if kind == "families":
                writer.writerow(["id", "name", "email", "phone"])
                for f in state["families"].values(): writer.writerow([f.id, f.name, f.email, f.phone])
            elif kind == "children":
                writer.writerow(["id", "family_id", "name", "site", "classroom_id", "immunization_status", "status"])
                for c in state["children"].values(): writer.writerow([c.id, c.family_id, c.name, c.site, c.classroom_id or "", c.immunization_status, child_status(c)])
            else:
                self._send(make_response(400, {"error": "Unsupported export kind"})); return
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.end_headers()
            self.wfile.write(output.getvalue().encode())
        else:
            self._send(make_response(404, {"error": "Not found"}))

    def do_POST(self):
        parsed = urlparse(self.path)
        data = self._json()
        if parsed.path == "/families":
            family = Family(id=data["id"], name=data["name"], address=data.get("address", ""), email=data.get("email", ""), phone=data.get("phone", ""), contacts=data.get("contacts", []))
            state["families"][family.id] = family; log("family.create", data.get("actor", "system"), serialize(family)); self._send(make_response(201, serialize(family)))
        elif parsed.path == "/children":
            if data["family_id"] not in state["families"]: self._send(make_response(400, {"error": "Unknown family"})); return
            child = Child(id=data["id"], family_id=data["family_id"], name=data["name"], dob=data["dob"], site=data["site"], immunization_status=data.get("immunization_status", "missing"), immunization_due=data.get("immunization_due"), allergies=data.get("allergies", []), pickup_authority=data.get("pickup_authority", []))
            state["children"][child.id] = child; state["families"][child.family_id].children_ids.append(child.id); log("child.create", data.get("actor", "system"), serialize(child)); self._send(make_response(201, serialize(child)))
        elif parsed.path == "/classrooms":
            room = Classroom(id=data["id"], site=data["site"], name=data["name"], capacity=int(data["capacity"]), room_type=data.get("room_type", "classroom"))
            state["classrooms"][room.id] = room; log("classroom.create", data.get("actor", "system"), serialize(room)); self._send(make_response(201, serialize(room)))
        elif parsed.path.startswith("/children/") and parsed.path.endswith("/assign"):
            cid = parsed.path.split("/")[2]; child = state["children"].get(cid)
            if not child: self._send(make_response(404, {"error": "Unknown child"})); return
            room = state["classrooms"].get(data["classroom_id"])
            if not room: self._send(make_response(404, {"error": "Unknown classroom"})); return
            enrolled = sum(1 for c in state["children"].values() if c.classroom_id == room.id)
            if enrolled >= room.capacity and not bool(data.get("override", False)):
                child.waiting_list = True
                if cid not in state["waiting_list"]: state["waiting_list"].append(cid)
                self._send(make_response(409, {"error": "Classroom full", "waiting_list": True})); return
            child.classroom_id = room.id; child.waiting_list = False
            if cid in state["waiting_list"]: state["waiting_list"].remove(cid)
            log("child.assign", data.get("actor", "system"), {"child_id": cid, "classroom_id": room.id})
            self._send(make_response(200, serialize(child)))
        elif parsed.path.startswith("/children/") and parsed.path.endswith("/immunization"):
            cid = parsed.path.split("/")[2]; child = state["children"].get(cid)
            if not child: self._send(make_response(404, {"error": "Unknown child"})); return
            child.immunization_status = data.get("status", child.immunization_status); child.immunization_due = data.get("due", child.immunization_due); child.compliance_verified = bool(data.get("verified", False)); log("child.immunization.update", data.get("actor", "system"), serialize(child)); self._send(make_response(200, {**serialize(child), "status": child_status(child)}))
        elif parsed.path == "/attendance/checkin":
            child = state["children"].get(data["child_id"])
            if not child: self._send(make_response(404, {"error": "Unknown child"})); return
            entry = {"type": "in", "at": now_iso(), "actor": data.get("actor", "system")}; child.attendance.append(entry); log("attendance.checkin", entry["actor"], {"child_id": child.id}); self._send(make_response(201, entry))
        elif parsed.path == "/attendance/checkout":
            child = state["children"].get(data["child_id"])
            if not child: self._send(make_response(404, {"error": "Unknown child"})); return
            entry = {"type": "out", "at": now_iso(), "actor": data.get("actor", "system")}; child.attendance.append(entry); log("attendance.checkout", entry["actor"], {"child_id": child.id}); self._send(make_response(201, entry))
        elif parsed.path == "/invoices":
            invoice = Invoice(id=data["id"], family_id=data["family_id"], child_id=data.get("child_id"), amount=float(data["amount"]), balance=float(data.get("balance", data["amount"])))
            state["invoices"][invoice.id] = invoice; log("invoice.create", data.get("actor", "system"), serialize(invoice)); self._send(make_response(201, serialize(invoice)))
        elif parsed.path.startswith("/invoices/") and parsed.path.endswith("/adjustments"):
            iid = parsed.path.split("/")[2]; invoice = state["invoices"].get(iid)
            if not invoice: self._send(make_response(404, {"error": "Unknown invoice"})); return
            adjustment = {"reason": data["reason"], "amount": float(data["amount"]), "type": data.get("type", "adjustment"), "at": now_iso(), "actor": data.get("actor", "system")}; invoice.adjustments.append(adjustment); invoice.balance += adjustment["amount"]; invoice.status = "open" if invoice.balance > 0 else "paid"; log("invoice.adjustment", adjustment["actor"], {"invoice_id": iid, **adjustment}); self._send(make_response(200, serialize(invoice)))
        elif parsed.path == "/payments":
            invoice = state["invoices"].get(data["invoice_id"])
            if not invoice: self._send(make_response(404, {"error": "Unknown invoice"})); return
            amount = float(data["amount"]); payment = {"amount": amount, "method": data.get("method", "card"), "payer": data.get("payer", "authorized"), "at": now_iso(), "status": "success"}; invoice.payments.append(payment); invoice.balance = round(invoice.balance - amount, 2); invoice.status = "paid" if invoice.balance <= 0 else "partial"; invoice.balance = max(invoice.balance, 0.0); log("payment.record", data.get("actor", "system"), {"invoice_id": invoice.id, **payment}); self._send(make_response(200, serialize(invoice)))
        elif parsed.path == "/imports/csv":
            kind = parse_qs(parsed.query).get("kind", ["families"])[0]
            reader = csv.DictReader(io.StringIO(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode() if False else data if False else ""))
            self._send(make_response(400, {"error": "Use raw CSV upload not JSON in this minimal server"}))
        else:
            self._send(make_response(404, {"error": "Not found"}))


def run():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("Nenios Child Care Management listening on http://127.0.0.1:8000", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    run()
