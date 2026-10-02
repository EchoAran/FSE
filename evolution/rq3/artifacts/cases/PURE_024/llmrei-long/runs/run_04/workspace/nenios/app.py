from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

@dataclass
class AuditEntry:
    timestamp: str
    actor: str
    action: str
    entity: str
    entity_id: str
    details: str

@dataclass
class Child:
    id: str
    name: str
    age_group: str
    status: str = "waiting"
    family_id: str = ""
    health_info: str = ""
    immunizations_current: bool = False
    waiting_list_position: int | None = None
    classroom_id: str | None = None

@dataclass
class Family:
    id: str
    name: str
    contacts: list[str]
    children: list[str] = field(default_factory=list)

@dataclass
class Classroom:
    id: str
    name: str
    age_group: str
    capacity: int
    enrolled_children: list[str] = field(default_factory=list)
    @property
    def available_spots(self):
        return max(self.capacity - len(self.enrolled_children), 0)

@dataclass
class Invoice:
    id: str
    family_id: str
    child_id: str
    amount: float
    description: str
    paid: float = 0.0
    @property
    def outstanding(self):
        return round(max(self.amount - self.paid, 0.0), 2)

class DataStore:
    def __init__(self):
        self.families = {}
        self.children = {}
        self.classrooms = {}
        self.invoices = {}
        self.audit = []
    def log(self, actor, action, entity, entity_id, details):
        self.audit.append(AuditEntry(datetime.now(timezone.utc).isoformat(), actor, action, entity, entity_id, details))

def seed(store):
    store.classrooms["c1"] = Classroom("c1", "Tadpoles", "infant", 2)
    store.classrooms["c2"] = Classroom("c2", "Frogs", "toddler", 1)
    store.families["f1"] = Family("f1", "Smith", ["smith@example.com"])
    store.children["ch1"] = Child("ch1", "Alice Smith", "infant", "active", "f1", "Healthy", True, None, "c1")
    store.children["ch2"] = Child("ch2", "Bob Smith", "infant", "waiting", "f1", "Needs physical", False, 1, None)
    store.families["f1"].children = ["ch1", "ch2"]
    store.classrooms["c1"].enrolled_children = ["ch1"]
    store.invoices["i1"] = Invoice("i1", "f1", "ch1", 250.0, "Weekly tuition", 100.0)
    store.log("system", "seed", "system", "seed", "Seeded initial records")

class NeniosApp:
    def __init__(self):
        self.store = DataStore()
        seed(self.store)

    def role_allowed(self, headers, required):
        actor_role = headers.get("X-Role", "guest")
        allowed = {"admin": {"admin", "office"}, "office": {"office"}, "teacher": {"teacher"}, "parent": {"parent"}}
        return required in allowed.get(actor_role, set())

    def dashboard_html(self):
        families = ''.join(f'<li>{f.id} - {f.name}</li>' for f in self.store.families.values())
        children = ''.join(f'<li>{c.id} - {c.name} - {c.status}</li>' for c in self.store.children.values())
        classrooms = ''.join(f'<li>{c.name}: {c.available_spots} available</li>' for c in self.store.classrooms.values())
        invoices = ''.join(f'<li>{i.id} - outstanding {i.outstanding}</li>' for i in self.store.invoices.values())
        audit = ''.join(f'<li>{a.timestamp} {a.actor} {a.action} {a.entity} {a.entity_id} {a.details}</li>' for a in self.store.audit[-10:])
        return f"<html><body><h1>Nenios Child Care Management</h1><ul>{families}</ul><ul>{children}</ul><ul>{classrooms}</ul><ul>{invoices}</ul><ul>{audit}</ul></body></html>"

    def json_response(self, obj):
        return json.dumps(obj).encode()

    def dashboard_api(self):
        return {
            "daily_snapshot": {"enrolled_children": sum(1 for c in self.store.children.values() if c.status == "active"), "classroom_occupancy": {cid: {"name": c.name, "age_group": c.age_group, "available_spots": c.available_spots, "enrolled": len(c.enrolled_children)} for cid, c in self.store.classrooms.items()}},
            "waiting_list": [{"id": c.id, "name": c.name, "age_group": c.age_group, "position": c.waiting_list_position} for c in sorted(self.store.children.values(), key=lambda x: (x.waiting_list_position or 9999, x.name)) if c.status == "waiting"],
            "billing_summary": [{"id": i.id, "family_id": i.family_id, "child_id": i.child_id, "amount": i.amount, "paid": i.paid, "outstanding": i.outstanding} for i in self.store.invoices.values()],
            "health_reminders": [{"id": c.id, "name": c.name, "immunizations_current": c.immunizations_current, "health_info": c.health_info} for c in self.store.children.values() if not c.immunizations_current or not c.health_info],
        }

    def handle(self, method, path, headers, body):
        parsed = urlparse(path)
        parts = parsed.path.strip('/').split('/') if parsed.path != '/' else []
        if parsed.path == '/':
            return 200, 'text/html', self.dashboard_html().encode()
        if parsed.path == '/api/dashboard':
            return 200, 'application/json', self.json_response(self.dashboard_api())
        if parsed.path == '/api/classrooms':
            return 200, 'application/json', self.json_response([{"id": c.id, "name": c.name, "age_group": c.age_group, "capacity": c.capacity, "enrolled": len(c.enrolled_children), "available_spots": c.available_spots} for c in self.store.classrooms.values()])
        if parsed.path == '/api/reports/billing':
            return 200, 'application/json', self.json_response([{"id": i.id, "family_id": i.family_id, "child_id": i.child_id, "amount": i.amount, "paid": i.paid, "outstanding": i.outstanding} for i in self.store.invoices.values() if i.outstanding > 0])
        if parsed.path == '/api/reports/health':
            return 200, 'application/json', self.json_response([{"id": c.id, "name": c.name, "health_info": c.health_info, "immunizations_current": c.immunizations_current} for c in self.store.children.values() if not c.immunizations_current or not c.health_info])
        if parsed.path.startswith('/api/audit'):
            q = parse_qs(parsed.query).get('q', [''])[0].lower()
            entries = [asdict(e) for e in self.store.audit if q in (e.actor + e.action + e.entity + e.entity_id + e.details).lower()]
            return 200, 'application/json', self.json_response(entries)
        if method == 'POST' and parsed.path.startswith('/api/enroll/'):
            if not self.role_allowed(headers, 'office'):
                return 403, 'text/plain', b'Forbidden'
            child_id = parts[-1]
            child = self.store.children[child_id]
            classroom = next((c for c in self.store.classrooms.values() if c.age_group == child.age_group and c.available_spots > 0), None)
            if not classroom:
                return 409, 'text/plain', b'No available spot for matching age group'
            classroom.enrolled_children.append(child.id)
            child.status = 'active'; child.classroom_id = classroom.id; child.waiting_list_position = None
            self.store.log(headers.get('X-User', 'unknown'), 'enroll', 'child', child.id, f'Moved to {classroom.id}')
            return 200, 'application/json', self.json_response(asdict(child))
        if method == 'POST' and parsed.path == '/api/families':
            if not self.role_allowed(headers, 'office'):
                return 403, 'text/plain', b'Forbidden'
            data = json.loads(body or b'{}')
            fam = Family(data['id'], data['name'], data.get('contacts', []), data.get('children', []))
            self.store.families[fam.id] = fam
            self.store.log(headers.get('X-User', 'unknown'), 'create', 'family', fam.id, fam.name)
            return 201, 'application/json', self.json_response(asdict(fam))
        if method == 'PATCH' and parsed.path.startswith('/api/children/') and parsed.path.endswith('/health'):
            if not self.role_allowed(headers, 'office'):
                return 403, 'text/plain', b'Forbidden'
            child_id = parts[1]
            data = json.loads(body or b'{}')
            child = self.store.children[child_id]
            child.health_info = data.get('health_info', child.health_info)
            child.immunizations_current = data.get('immunizations_current', child.immunizations_current)
            self.store.log(headers.get('X-User', 'unknown'), 'update', 'child', child.id, 'Updated health/immunization')
            return 200, 'application/json', self.json_response(asdict(child))
        return 404, 'text/plain', b'Not Found'

app = NeniosApp()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.respond()
    def do_POST(self): self.respond()
    def do_PATCH(self): self.respond()
    def respond(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length else b''
        code, ctype, data = app.handle(self.command, self.path, self.headers, body)
        self.send_response(code); self.send_header('Content-Type', ctype); self.end_headers(); self.wfile.write(data)

def run(host='0.0.0.0', port=8000):
    HTTPServer((host, port), RequestHandler).serve_forever()

if __name__ == '__main__':
    run()
