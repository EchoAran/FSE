from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from typing import Any, Dict, List, Optional, Tuple

ROLES = {"admin", "office", "teacher", "parent"}


def iso_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


@dataclass
class Family:
    id: int
    name: str
    contacts: List[Dict[str, Any]] = field(default_factory=list)
    children: List[int] = field(default_factory=list)


@dataclass
class Child:
    id: int
    family_id: int
    name: str
    age_group: str
    health_info: Dict[str, Any] = field(default_factory=dict)
    immunizations: Dict[str, Any] = field(default_factory=dict)
    enrollment_status: str = "pending"
    classroom: Optional[str] = None
    waiting_list_position: Optional[int] = None


@dataclass
class Classroom:
    id: str
    age_group: str
    capacity: int
    enrolled_child_ids: List[int] = field(default_factory=list)


@dataclass
class Invoice:
    id: int
    family_id: int
    child_id: int
    amount: float
    description: str
    paid: float = 0.0

    @property
    def outstanding(self) -> float:
        return round(self.amount - self.paid, 2)


families: Dict[int, Family] = {}
children: Dict[int, Child] = {}
classrooms: Dict[str, Classroom] = {}
waiting_lists: Dict[str, List[int]] = {}
invoices: Dict[int, Invoice] = {}
audit_log: List[Dict[str, Any]] = []
next_ids = {"family": 1, "child": 1, "invoice": 1}


def log_action(actor: str, action: str, details: Dict[str, Any]) -> None:
    audit_log.append({"timestamp": iso_now(), "actor": actor, "action": action, "details": details})


def reset_state() -> None:
    families.clear(); children.clear(); classrooms.clear(); waiting_lists.clear(); invoices.clear(); audit_log.clear()
    next_ids["family"] = 1; next_ids["child"] = 1; next_ids["invoice"] = 1


def response(status: int, payload: Any) -> Tuple[int, Dict[str, Any]]:
    return status, payload


def auth(headers: Dict[str, str]) -> Tuple[Optional[str], Optional[Tuple[int, Dict[str, Any]]]]:
    role = headers.get("x-role", "office")
    if role not in ROLES:
        return None, response(400, {"error": "invalid role"})
    return role, None


def allow_family(role: str, headers: Dict[str, str], family_id: int):
    if role in {"admin", "office"}:
        return None
    if role == "parent":
        try:
            allowed = int(headers.get("x-family-id", "-1"))
        except ValueError:
            allowed = -1
        if allowed != family_id:
            return response(403, {"error": "forbidden"})
    return None


def create_family(data):
    fid = next_ids["family"]; next_ids["family"] += 1
    fam = Family(id=fid, name=data["name"], contacts=data.get("contacts", []))
    families[fid] = fam
    log_action("office", "create_family", asdict(fam))
    return response(201, asdict(fam))


def create_child(data):
    family_id = int(data["family_id"])
    if family_id not in families:
        return response(404, {"error": "family not found"})
    cid = next_ids["child"]; next_ids["child"] += 1
    child = Child(id=cid, family_id=family_id, name=data["name"], age_group=data["age_group"],
                  health_info=data.get("health_info", {}), immunizations=data.get("immunizations", {}),
                  enrollment_status=data.get("enrollment_status", "pending"))
    children[cid] = child
    families[family_id].children.append(cid)
    if child.enrollment_status == "waiting":
        waiting_lists.setdefault(child.age_group, []).append(cid)
        child.waiting_list_position = len(waiting_lists[child.age_group])
    log_action("office", "create_child", asdict(child))
    return response(201, asdict(child))


def enroll_child(child_id: int):
    child = children.get(child_id)
    if not child:
        return response(404, {"error": "child not found"})
    open_classroom = next((c for c in classrooms.values() if c.age_group == child.age_group and len(c.enrolled_child_ids) < c.capacity), None)
    if not open_classroom:
        return response(409, {"error": "no capacity"})
    if child_id in waiting_lists.get(child.age_group, []):
        waiting_lists[child.age_group].remove(child_id)
        for idx, cid in enumerate(waiting_lists[child.age_group], start=1):
            children[cid].waiting_list_position = idx
    child.enrollment_status = "enrolled"; child.classroom = open_classroom.id; child.waiting_list_position = None
    open_classroom.enrolled_child_ids.append(child_id)
    log_action("office", "enroll_child", {"child_id": child_id, "classroom": open_classroom.id})
    return response(200, asdict(child))


class AppHandler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: Any):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        role, err = auth({k.lower(): v for k, v in self.headers.items()})
        if err:
            return self._json(*err)
        if path == "/health": return self._json(200, {"status": "ok"})
        if path == "/": return self._json(200, {"name": "Nenios Child Care Management", "status": "running"})
        if path == "/enrollment/summary":
            if role not in {"admin", "office", "teacher"}: return self._json(403, {"error": "forbidden"})
            return self._json(200, {"enrolled": [asdict(c) for c in children.values() if c.enrollment_status == "enrolled"], "pending": [asdict(c) for c in children.values() if c.enrollment_status == "pending"], "waiting": [asdict(c) for c in children.values() if c.enrollment_status == "waiting"]})
        if path == "/classrooms/availability":
            if role not in {"admin", "office", "teacher"}: return self._json(403, {"error": "forbidden"})
            return self._json(200, [{"id": c.id, "age_group": c.age_group, "capacity": c.capacity, "enrolled": len(c.enrolled_child_ids), "open_spots": max(c.capacity - len(c.enrolled_child_ids), 0)} for c in classrooms.values()])
        if path == "/billing/summary":
            if role not in {"admin", "office"}: return self._json(403, {"error": "forbidden"})
            return self._json(200, [{**asdict(i), "outstanding": i.outstanding} for i in invoices.values()])
        if path.startswith("/billing/family/") and path.endswith("/statement"):
            if role not in {"admin", "office", "parent"}: return self._json(403, {"error": "forbidden"})
            family_id = int(path.split("/")[3])
            access = allow_family(role, {k.lower(): v for k, v in self.headers.items()}, family_id)
            if access: return self._json(*access)
            return self._json(200, {"family_id": family_id, "invoices": [{**asdict(i), "outstanding": i.outstanding} for i in invoices.values() if i.family_id == family_id]})
        if path == "/health/reminders":
            if role not in {"admin", "office", "teacher"}: return self._json(403, {"error": "forbidden"})
            return self._json(200, [{"child_id": c.id, "child_name": c.name, "health_current": bool(c.health_info), "immunizations_current": c.immunizations.get("current", False), "needs_attention": (not c.health_info) or (not c.immunizations.get("current", False))} for c in children.values()])
        if path == "/report/daily-snapshot":
            if role not in {"admin", "office", "teacher"}: return self._json(403, {"error": "forbidden"})
            return self._json(200, {"date": date.today().isoformat(), "enrollment_counts": {"enrolled": len([c for c in children.values() if c.enrollment_status == "enrolled"]), "pending": len([c for c in children.values() if c.enrollment_status == "pending"]), "waiting": len([c for c in children.values() if c.enrollment_status == "waiting"])}, "classroom_occupancy": [{"id": c.id, "enrolled": len(c.enrolled_child_ids), "capacity": c.capacity} for c in classrooms.values()], "waiting_list": {k: v[:] for k, v in waiting_lists.items()}, "open_spots": [{"id": c.id, "age_group": c.age_group, "open_spots": max(c.capacity - len(c.enrolled_child_ids), 0)} for c in classrooms.values()], "unpaid_invoices": [{"id": i.id, "outstanding": i.outstanding} for i in invoices.values() if i.outstanding > 0]})
        if path == "/audit":
            if role not in {"admin", "office"}: return self._json(403, {"error": "forbidden"})
            q = qs.get("q", [""])[0].lower()
            return self._json(200, [entry for entry in audit_log if q in str(entry).lower()])
        if path == "/waiting-list/toddlers/next":
            q = waiting_lists.get("toddlers", [])
            return self._json(200, {"next_child_id": q[0] if q else None, "child": asdict(children[q[0]]) if q else None})
        self._json(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        role, err = auth({k.lower(): v for k, v in self.headers.items()})
        if err:
            return self._json(*err)
        length = int(self.headers.get("Content-Length", "0"))
        data = json.loads(self.rfile.read(length) or b"{}")
        if path == "/setup/classrooms":
            if role not in {"admin", "office"}: return self._json(403, {"error": "forbidden"})
            classroom = Classroom(id=data["id"], age_group=data["age_group"], capacity=int(data["capacity"]))
            classrooms[classroom.id] = classroom; waiting_lists.setdefault(classroom.age_group, [])
            log_action(role, "upsert_classroom", asdict(classroom))
            return self._json(201, asdict(classroom))
        if path == "/families":
            if role not in {"admin", "office"}: return self._json(403, {"error": "forbidden"})
            status, payload = create_family(data); return self._json(status, payload)
        if path == "/children":
            if role not in {"admin", "office"}: return self._json(403, {"error": "forbidden"})
            status, payload = create_child(data); return self._json(status, payload)
        if path.startswith("/waiting-list/") and path.endswith("/enroll"):
            if role not in {"admin", "office"}: return self._json(403, {"error": "forbidden"})
            status, payload = enroll_child(int(path.split("/")[2])); return self._json(status, payload)
        if path == "/billing/generate":
            if role not in {"admin", "office"}: return self._json(403, {"error": "forbidden"})
            invoice_id = next_ids["invoice"]; next_ids["invoice"] += 1
            inv = Invoice(id=invoice_id, family_id=int(data["family_id"]), child_id=int(data["child_id"]), amount=float(data["amount"]), description=data.get("description", "care charge"))
            invoices[invoice_id] = inv
            log_action(role, "generate_invoice", asdict(inv))
            return self._json(201, {**asdict(inv), "outstanding": inv.outstanding})
        self._json(404, {"error": "not found"})

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), AppHandler)
    print("Nenios Child Care Management running on http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
