import json
import threading
import time
from urllib import request, error

import app


def reset_state():
    app.families.clear()
    app.children.clear()
    app.classrooms.clear()
    app.enrollments.clear()
    app.waiting_list.clear()
    app.immunizations.clear()
    app.invoices.clear()


def call(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(f"http://127.0.0.1:8000{path}", data=data, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with request.urlopen(req, timeout=3) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def test_flow():
    reset_state()
    status, fam = call("POST", "/families", {"name": "Smith Family"})
    assert status == 201
    family_id = fam["id"]
    status, cls = call("POST", "/classrooms", {"name": "Toddlers", "capacity": 1})
    assert status == 201
    classroom_id = cls["id"]
    status, child = call("POST", "/children", {"family_id": family_id, "name": "Ava"})
    assert status == 201
    child_id = child["id"]
    assert call("POST", "/enrollments", {"child_id": child_id, "classroom_id": classroom_id})[0] == 201
    assert call("POST", f"/children/{child_id}/immunizations", {"vaccine": "MMR"})[0] == 201
    assert call("POST", "/invoices", {"family_id": family_id, "amount": 125.50})[0] == 201
    status, ops = call("GET", "/reports/operations")
    assert status == 200
    assert ops["families"] == 1
    assert ops["children"] == 1
    assert ops["enrolled_children"] == 1
    assert ops["immunization_records"] == 1
    assert ops["invoices"] == 1
    assert call("GET", f"/reports/customer/{family_id}")[0] == 200


def test_waitlist():
    reset_state()
    family_id = call("POST", "/families", {"name": "Jones Family"})[1]["id"]
    classroom_id = call("POST", "/classrooms", {"name": "Infants", "capacity": 0})[1]["id"]
    child_id = call("POST", "/children", {"family_id": family_id, "name": "Noah"})[1]["id"]
    status, payload = call("POST", "/enrollments", {"child_id": child_id, "classroom_id": classroom_id})
    assert status == 202 and payload["status"] == "waitlisted"
    assert call("GET", "/waiting-list")[1]["items"]


if __name__ == "__main__":
    server = threading.Thread(target=app.run_server, daemon=True)
    server.start()
    time.sleep(0.5)
    test_flow()
    test_waitlist()
    print("tests passed")
