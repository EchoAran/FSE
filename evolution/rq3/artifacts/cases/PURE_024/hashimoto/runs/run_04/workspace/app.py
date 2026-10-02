from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional
import json
import itertools


def _next_id(counter=itertools.count(1)):
    return next(counter)


@dataclass
class Family:
    id: int
    name: str
    contact: str = ""
    children: List[int] = field(default_factory=list)


@dataclass
class Child:
    id: int
    family_id: int
    name: str
    classroom_id: Optional[int] = None
    immunizations: List[str] = field(default_factory=list)


@dataclass
class Classroom:
    id: int
    name: str
    capacity: int
    enrolled_children: List[int] = field(default_factory=list)


@dataclass
class Enrollment:
    id: int
    child_id: int
    classroom_id: int
    status: str
    created_at: str


@dataclass
class Invoice:
    id: int
    family_id: int
    amount: float
    description: str
    paid: bool = False


families: Dict[int, Family] = {}
children: Dict[int, Child] = {}
classrooms: Dict[int, Classroom] = {}
enrollments: Dict[int, Enrollment] = {}
waitlist: List[int] = []
invoices: Dict[int, Invoice] = {}


def reset_state():
    families.clear(); children.clear(); classrooms.clear(); enrollments.clear(); waitlist.clear(); invoices.clear()


def add_family(name: str, contact: str = "") -> Family:
    family = Family(id=_next_id(), name=name, contact=contact)
    families[family.id] = family
    return family


def add_child(family_id: int, name: str) -> Child:
    child = Child(id=_next_id(), family_id=family_id, name=name)
    children[child.id] = child
    families[family_id].children.append(child.id)
    return child


def add_classroom(name: str, capacity: int) -> Classroom:
    classroom = Classroom(id=_next_id(), name=name, capacity=capacity)
    classrooms[classroom.id] = classroom
    return classroom


def enroll_child(child_id: int, classroom_id: int) -> Enrollment:
    classroom = classrooms[classroom_id]
    if len(classroom.enrolled_children) >= classroom.capacity:
        if child_id not in waitlist:
            waitlist.append(child_id)
        status = "waitlisted"
    else:
        classroom.enrolled_children.append(child_id)
        children[child_id].classroom_id = classroom_id
        status = "enrolled"
    enrollment = Enrollment(id=_next_id(), child_id=child_id, classroom_id=classroom_id, status=status, created_at=datetime.now(timezone.utc).isoformat())
    enrollments[enrollment.id] = enrollment
    return enrollment


def add_immunization(child_id: int, record: str):
    children[child_id].immunizations.append(record)


def create_invoice(family_id: int, amount: float, description: str) -> Invoice:
    invoice = Invoice(id=_next_id(), family_id=family_id, amount=amount, description=description)
    invoices[invoice.id] = invoice
    return invoice


def operations_report():
    return {
        "family_count": len(families),
        "child_count": len(children),
        "classroom_count": len(classrooms),
        "enrollment_count": len(enrollments),
        "waitlist_count": len(waitlist),
        "invoice_count": len(invoices),
        "open_invoice_total": sum(inv.amount for inv in invoices.values() if not inv.paid),
    }


def customer_report():
    data = []
    for family in families.values():
        data.append({
            "family": asdict(family),
            "children": [asdict(children[cid]) for cid in family.children if cid in children],
            "invoices": [asdict(inv) for inv in invoices.values() if inv.family_id == family.id],
        })
    return data


HTML = """<!doctype html><html><head><title>Nenios Child Care Management</title></head><body>
<h1>Nenios Child Care Management</h1>
<form method='post' action='/families'><input name='name' placeholder='Family name' required><input name='contact' placeholder='Contact'><button>Add Family</button></form>
<form method='post' action='/children'><input name='family_id' placeholder='Family ID' required><input name='name' placeholder='Child name' required><button>Add Child</button></form>
<form method='post' action='/classrooms'><input name='name' placeholder='Classroom name' required><input name='capacity' type='number' placeholder='Capacity' required><button>Add Classroom</button></form>
<form method='post' action='/enroll'><input name='child_id' placeholder='Child ID' required><input name='classroom_id' placeholder='Classroom ID' required><button>Enroll</button></form>
<form method='post' action='/immunizations'><input name='child_id' placeholder='Child ID' required><input name='record' placeholder='Immunization record' required><button>Add Immunization</button></form>
<form method='post' action='/invoices'><input name='family_id' placeholder='Family ID' required><input name='amount' type='number' step='0.01' placeholder='Amount' required><input name='description' placeholder='Description' required><button>Create Invoice</button></form>
<ul>
<li>Families: {families}</li><li>Children: {children}</li><li>Classrooms: {classrooms}</li><li>Enrollments: {enrollments}</li><li>Waitlist: {waitlist}</li><li>Invoices: {invoices}</li>
</ul></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type="text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send(200, HTML.format(families=len(families), children=len(children), classrooms=len(classrooms), enrollments=len(enrollments), waitlist=len(waitlist), invoices=len(invoices)))
        elif parsed.path == "/reports/operations":
            self._send(200, json.dumps(operations_report()), "application/json")
        elif parsed.path == "/reports/customers":
            self._send(200, json.dumps(customer_report()), "application/json")
        else:
            self._send(404, "Not Found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = parse_qs(self.rfile.read(length).decode())
        path = urlparse(self.path).path
        if path == "/families":
            add_family(data["name"][0], data.get("contact", [""])[0])
        elif path == "/children":
            add_child(int(data["family_id"][0]), data["name"][0])
        elif path == "/classrooms":
            add_classroom(data["name"][0], int(data["capacity"][0]))
        elif path == "/enroll":
            enroll_child(int(data["child_id"][0]), int(data["classroom_id"][0]))
        elif path == "/immunizations":
            add_immunization(int(data["child_id"][0]), data["record"][0])
        elif path == "/invoices":
            create_invoice(int(data["family_id"][0]), float(data["amount"][0]), data["description"][0])
        else:
            self._send(404, "Not Found")
            return
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


def run_server(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
