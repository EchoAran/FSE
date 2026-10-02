from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json
from itertools import count

family_ids = count(1)
child_ids = count(1)
classroom_ids = count(1)
enrollment_ids = count(1)
invoice_ids = count(1)
immunization_ids = count(1)
waitlist_ids = count(1)

families = {}
children = {}
classrooms = {}
enrollments = {}
waitlist = {}
invoices = {}
immunizations = {}


def json_response(handler, status, payload):
    data = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def read_json(handler):
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    return json.loads(raw.decode("utf-8"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return json_response(self, 200, {"status": "ok"})
        if path == "/":
            return json_response(self, 200, {"message": "Nenios Child Care Management API"})
        if path == "/families":
            return json_response(self, 200, list(families.values()))
        if path == "/classrooms":
            return json_response(self, 200, list(classrooms.values()))
        if path == "/waitlist":
            return json_response(self, 200, list(waitlist.values()))
        if path == "/immunizations":
            return json_response(self, 200, list(immunizations.values()))
        if path == "/invoices":
            return json_response(self, 200, list(invoices.values()))
        if path == "/reports/summary":
            return json_response(self, 200, {
                "families": len(families),
                "children": len(children),
                "classrooms": len(classrooms),
                "enrollments": len(enrollments),
                "waitlist": len(waitlist),
                "open_invoices": sum(1 for inv in invoices.values() if inv["status"] == "open"),
                "immunizations": len(immunizations),
            })
        return json_response(self, 404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = read_json(self)
        except Exception:
            return json_response(self, 400, {"error": "invalid JSON"})

        if path == "/families":
            name = data.get("name")
            if not name:
                return json_response(self, 400, {"error": "name is required"})
            family_id = next(family_ids)
            family = {"id": family_id, "name": name, "contacts": data.get("contacts", [])}
            families[family_id] = family
            return json_response(self, 201, family)

        if path == "/classrooms":
            name = data.get("name")
            capacity = data.get("capacity")
            if not name:
                return json_response(self, 400, {"error": "name is required"})
            if capacity is None or int(capacity) < 0:
                return json_response(self, 400, {"error": "capacity must be a non-negative integer"})
            classroom_id = next(classroom_ids)
            classroom = {"id": classroom_id, "name": name, "capacity": int(capacity), "enrolled_count": 0}
            classrooms[classroom_id] = classroom
            return json_response(self, 201, classroom)

        if path == "/children":
            name = data.get("name")
            family_id = data.get("family_id")
            if not name or not family_id:
                return json_response(self, 400, {"error": "name and family_id are required"})
            family_id = int(family_id)
            if family_id not in families:
                return json_response(self, 404, {"error": "family not found"})
            child_id = next(child_ids)
            child = {"id": child_id, "name": name, "family_id": family_id}
            children[child_id] = child
            return json_response(self, 201, child)

        if path == "/enrollments":
            child_id = data.get("child_id")
            classroom_id = data.get("classroom_id")
            if not child_id or not classroom_id:
                return json_response(self, 400, {"error": "child_id and classroom_id are required"})
            child_id = int(child_id)
            classroom_id = int(classroom_id)
            child = children.get(child_id)
            classroom = classrooms.get(classroom_id)
            if not child:
                return json_response(self, 404, {"error": "child not found"})
            if not classroom:
                return json_response(self, 404, {"error": "classroom not found"})
            if classroom["enrolled_count"] >= classroom["capacity"]:
                return json_response(self, 409, {"error": "classroom is full"})
            enrollment_id = next(enrollment_ids)
            enrollment = {"id": enrollment_id, "child_id": child_id, "classroom_id": classroom_id, "status": "enrolled"}
            enrollments[enrollment_id] = enrollment
            classroom["enrolled_count"] += 1
            return json_response(self, 201, enrollment)

        if path == "/waitlist":
            child_id = data.get("child_id")
            desired_classroom_id = data.get("desired_classroom_id")
            if not child_id or not desired_classroom_id:
                return json_response(self, 400, {"error": "child_id and desired_classroom_id are required"})
            child_id = int(child_id)
            desired_classroom_id = int(desired_classroom_id)
            if child_id not in children:
                return json_response(self, 404, {"error": "child not found"})
            if desired_classroom_id not in classrooms:
                return json_response(self, 404, {"error": "classroom not found"})
            waitlist_id = next(waitlist_ids)
            entry = {"id": waitlist_id, "child_id": child_id, "desired_classroom_id": desired_classroom_id, "status": "waiting"}
            waitlist[waitlist_id] = entry
            return json_response(self, 201, entry)

        if path == "/immunizations":
            child_id = data.get("child_id")
            vaccine = data.get("vaccine")
            if not child_id or not vaccine:
                return json_response(self, 400, {"error": "child_id and vaccine are required"})
            child_id = int(child_id)
            if child_id not in children:
                return json_response(self, 404, {"error": "child not found"})
            immunization_id = next(immunization_ids)
            record = {"id": immunization_id, "child_id": child_id, "vaccine": vaccine, "date": data.get("date")}
            immunizations[immunization_id] = record
            return json_response(self, 201, record)

        if path == "/invoices":
            family_id = data.get("family_id")
            amount = data.get("amount")
            if not family_id or amount is None:
                return json_response(self, 400, {"error": "family_id and amount are required"})
            family_id = int(family_id)
            if family_id not in families:
                return json_response(self, 404, {"error": "family not found"})
            invoice_id = next(invoice_ids)
            invoice = {"id": invoice_id, "family_id": family_id, "amount": float(amount), "description": data.get("description", ""), "status": "open"}
            invoices[invoice_id] = invoice
            return json_response(self, 201, invoice)

        return json_response(self, 404, {"error": "not found"})

    def log_message(self, format, *args):
        return


def run(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    run()
