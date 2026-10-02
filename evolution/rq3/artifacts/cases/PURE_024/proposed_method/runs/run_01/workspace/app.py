from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json

@dataclass
class Family:
    id: int
    name: str
    contacts: dict = field(default_factory=dict)

@dataclass
class Child:
    id: int
    family_id: int
    name: str
    site: str
    classroom: str | None = None
    immunization_status: str = "missing"
    allergy_alert: str = ""
    pickup_authority: list = field(default_factory=list)

@dataclass
class Classroom:
    id: int
    name: str
    site: str
    max_capacity: int
    enrolled_count: int = 0

@dataclass
class Invoice:
    id: int
    family_id: int
    amount_due: float
    balance: float
    status: str = "open"
    payments: list = field(default_factory=list)

STATE = {"families": {}, "children": {}, "classrooms": {}, "waiting_list": [], "invoices": {}, "audit": [], "next": {"family": 1, "child": 1, "classroom": 1, "invoice": 1}}


def nid(kind):
    i = STATE["next"][kind]
    STATE["next"][kind] += 1
    return i


def log(action, payload):
    STATE["audit"].append({"ts": datetime.utcnow().isoformat() + "Z", "action": action, "payload": payload})


def seed():
    if STATE["families"]:
        return
    f = Family(nid("family"), "Smith Family", {"phone": "555-0101", "email": "smith@example.com"})
    STATE["families"][f.id] = f
    c = Classroom(nid("classroom"), "Preschool", "Main", 2)
    STATE["classrooms"][c.id] = c
    ch = Child(nid("child"), f.id, "Ava Smith", "Main", c.name, "current", pickup_authority=["Parent"])
    STATE["children"][ch.id] = ch
    c.enrolled_count = 1
    inv = Invoice(nid("invoice"), f.id, 200.0, 125.0, payments=[{"amount": 75.0, "status": "successful"}])
    STATE["invoices"][inv.id] = inv
    log("seed_loaded", {})


def json_response(handler, code, payload):
    body = json.dumps(payload).encode()
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def text_response(handler, code, text, content_type="text/plain; charset=utf-8"):
    body = text.encode()
    handler.send_response(code)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        seed()
        p = urlparse(self.path).path
        if p == "/":
            html = "<html><body><h1>Nenios Child Care Management</h1></body></html>"
            return text_response(self, 200, html, "text/html; charset=utf-8")
        if p == "/api/dashboard":
            return json_response(self, 200, {
                "families": [asdict(x) for x in STATE["families"].values()],
                "children": [asdict(x) for x in STATE["children"].values()],
                "classrooms": [{**asdict(x), "status": "Full" if x.enrolled_count >= x.max_capacity else "Available"} for x in STATE["classrooms"].values()],
                "invoices": [asdict(x) for x in STATE["invoices"].values()],
                "waiting_list": STATE["waiting_list"],
                "audit": STATE["audit"],
            })
        if p == "/api/export/csv":
            lines = ["type,id,name,extra"]
            for f in STATE["families"].values():
                lines.append(f"family,{f.id},{f.name},phone={f.contacts.get('phone','')}")
            for c in STATE["children"].values():
                lines.append(f"child,{c.id},{c.name},classroom={c.classroom or 'waiting'}")
            return text_response(self, 200, "\n".join(lines), "text/csv; charset=utf-8")
        return text_response(self, 404, "Not found")

    def do_POST(self):
        seed()
        p = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0"))
        data = json.loads(self.rfile.read(length) or b"{}")
        if p == "/api/families":
            f = Family(nid("family"), data["name"], data.get("contacts", {}))
            STATE["families"][f.id] = f
            return json_response(self, 201, asdict(f))
        if p == "/api/children":
            fam_id = data["family_id"]
            if fam_id not in STATE["families"]:
                return text_response(self, 400, "Unknown family")
            classroom_name = data.get("classroom")
            classroom = next((x for x in STATE["classrooms"].values() if x.name == classroom_name), None) if classroom_name else None
            if classroom and classroom.enrolled_count >= classroom.max_capacity:
                STATE["waiting_list"].append({"child_name": data["name"], "classroom": classroom.name, "family_id": fam_id})
                return json_response(self, 202, {"status": "waiting_list", "message": "Classroom full; child added to waiting list"})
            if classroom:
                classroom.enrolled_count += 1
            ch = Child(nid("child"), fam_id, data["name"], data.get("site", "Main"), classroom.name if classroom else None, data.get("immunization_status", "missing"), data.get("allergy_alert", ""), data.get("pickup_authority", []))
            STATE["children"][ch.id] = ch
            return json_response(self, 201, asdict(ch))
        if p.endswith("/checkin") or p.endswith("/checkout"):
            return json_response(self, 200, {"status": "checked_in" if p.endswith("checkin") else "checked_out"})
        if p == "/api/invoices":
            fam_id = data["family_id"]
            inv = Invoice(nid("invoice"), fam_id, float(data["amount_due"]), float(data["amount_due"]))
            STATE["invoices"][inv.id] = inv
            return json_response(self, 201, asdict(inv))
        if p.startswith("/api/invoices/") and p.endswith("/pay"):
            inv_id = int(p.split("/")[3])
            inv = STATE["invoices"].get(inv_id)
            if not inv:
                return text_response(self, 404, "Not found")
            amount = float(data["amount"])
            inv.balance = round(max(0.0, inv.balance - amount), 2)
            inv.status = "paid" if inv.balance == 0 else "open"
            inv.payments.append({"amount": amount, "method": data.get("method", "card")})
            return json_response(self, 200, asdict(inv))
        return text_response(self, 404, "Not found")


def run(host="0.0.0.0", port=8000):
    seed()
    ThreadingHTTPServer((host, port), Handler).serve_forever()

if __name__ == "__main__":
    run()
