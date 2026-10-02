from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from datetime import datetime
from collections import defaultdict
import json
import uuid

families = {}
children = {}
classrooms = {}
enrollments = {}
waiting_list = []
immunizations = defaultdict(list)
invoices = {}


def new_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def json_response(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            json_response(self, 200, {
                "service": "Nenios Child Care Management",
                "features": [
                    "family registration",
                    "enrollment management",
                    "classroom capacity management",
                    "waiting list management",
                    "immunization tracking",
                    "invoicing",
                    "reporting"
                ]
            })
            return
        if path == "/waiting-list":
            json_response(self, 200, {"items": waiting_list})
            return
        if path == "/reports/operations":
            enrolled_children = sum(len(c["enrolled_child_ids"]) for c in classrooms.values())
            json_response(self, 200, {
                "families": len(families),
                "children": len(children),
                "classrooms": len(classrooms),
                "enrolled_children": enrolled_children,
                "waiting_list_entries": len(waiting_list),
                "immunization_records": sum(len(v) for v in immunizations.values()),
                "invoices": len(invoices),
                "total_invoice_amount": round(sum(i["amount"] for i in invoices.values()), 2)
            })
            return
        if path.startswith("/reports/customer/"):
            family_id = path.split("/", 3)[3]
            if family_id not in families:
                json_response(self, 400, {"error": "Valid family_id is required"})
                return
            family_children = [children[cid] for cid in families[family_id]["children"] if cid in children]
            family_invoices = [inv for inv in invoices.values() if inv["family_id"] == family_id]
            family_immunizations = {cid: immunizations[cid] for cid in families[family_id]["children"] if cid in immunizations}
            json_response(self, 200, {"family": families[family_id], "children": family_children, "immunizations": family_immunizations, "invoices": family_invoices})
            return
        json_response(self, 404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        data = self.read_json()
        if path == "/families":
            name = data.get("name")
            if not name:
                json_response(self, 400, {"error": "Family name is required"})
                return
            family_id = new_id("fam")
            families[family_id] = {"id": family_id, "name": name, "contact": data.get("contact", {}), "children": []}
            json_response(self, 201, families[family_id])
            return
        if path == "/classrooms":
            name = data.get("name")
            capacity = data.get("capacity")
            if not name:
                json_response(self, 400, {"error": "Classroom name is required"})
                return
            if not isinstance(capacity, int) or capacity < 0:
                json_response(self, 400, {"error": "Classroom capacity must be a non-negative integer"})
                return
            classroom_id = new_id("cls")
            classrooms[classroom_id] = {"id": classroom_id, "name": name, "capacity": capacity, "enrolled_child_ids": []}
            json_response(self, 201, classrooms[classroom_id])
            return
        if path == "/children":
            family_id = data.get("family_id")
            name = data.get("name")
            if not family_id or family_id not in families:
                json_response(self, 400, {"error": "Valid family_id is required"})
                return
            if not name:
                json_response(self, 400, {"error": "Child name is required"})
                return
            child_id = new_id("child")
            children[child_id] = {"id": child_id, "family_id": family_id, "name": name, "dob": data.get("dob")}
            families[family_id]["children"].append(child_id)
            json_response(self, 201, children[child_id])
            return
        if path == "/enrollments":
            child_id = data.get("child_id")
            classroom_id = data.get("classroom_id")
            if child_id not in children:
                json_response(self, 400, {"error": "Valid child_id is required"})
                return
            if classroom_id not in classrooms:
                json_response(self, 400, {"error": "Valid classroom_id is required"})
                return
            classroom = classrooms[classroom_id]
            if len(classroom["enrolled_child_ids"]) >= classroom["capacity"]:
                waiting_list.append({"child_id": child_id, "classroom_id": classroom_id, "requested_at": datetime.utcnow().isoformat() + "Z"})
                json_response(self, 202, {"status": "waitlisted", "child_id": child_id, "classroom_id": classroom_id})
                return
            enrollment_id = new_id("enr")
            enrollments[enrollment_id] = {"id": enrollment_id, "child_id": child_id, "classroom_id": classroom_id, "status": "enrolled"}
            classroom["enrolled_child_ids"].append(child_id)
            json_response(self, 201, enrollments[enrollment_id])
            return
        if path.startswith("/children/") and path.endswith("/immunizations"):
            child_id = path.split("/")[2]
            if child_id not in children:
                json_response(self, 400, {"error": "Valid child_id is required"})
                return
            vaccine = data.get("vaccine")
            if not vaccine:
                json_response(self, 400, {"error": "Vaccine name is required"})
                return
            record = {"vaccine": vaccine, "date": data.get("date", datetime.utcnow().date().isoformat())}
            immunizations[child_id].append(record)
            json_response(self, 201, {"child_id": child_id, "immunizations": immunizations[child_id]})
            return
        if path == "/invoices":
            family_id = data.get("family_id")
            amount = data.get("amount")
            if family_id not in families:
                json_response(self, 400, {"error": "Valid family_id is required"})
                return
            if not isinstance(amount, (int, float)) or amount < 0:
                json_response(self, 400, {"error": "Amount must be a non-negative number"})
                return
            invoice_id = new_id("inv")
            invoices[invoice_id] = {"id": invoice_id, "family_id": family_id, "amount": float(amount), "status": data.get("status", "open"), "created_at": datetime.utcnow().isoformat() + "Z"}
            json_response(self, 201, invoices[invoice_id])
            return
        json_response(self, 404, {"error": "Not found"})


def run_server(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
