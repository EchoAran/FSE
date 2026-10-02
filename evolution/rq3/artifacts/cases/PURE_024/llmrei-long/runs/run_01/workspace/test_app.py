import json
import threading
import time
from http.client import HTTPConnection
from app import run

PORT = 8765

server_thread = threading.Thread(target=run, kwargs={'host': '127.0.0.1', 'port': PORT}, daemon=True)
server_thread.start()
time.sleep(0.2)

def request(method, path, body=None):
    conn = HTTPConnection('127.0.0.1', PORT)
    headers = {'X-Role': 'office_staff', 'Content-Type': 'application/json'}
    payload = json.dumps(body).encode() if body is not None else None
    conn.request(method, path, body=payload, headers=headers)
    resp = conn.getresponse()
    data = resp.read().decode()
    return resp.status, json.loads(data) if data else None


def test_workflow():
    status, fam = request('POST', '/families', {'name': 'Smith', 'contacts': ['555-1111']})
    assert status == 200
    status, cls = request('POST', '/classrooms', {'name': 'Sunflowers', 'age_group': 'toddler', 'capacity': 1})
    assert status == 200
    status, child1 = request('POST', '/children', {'family_id': fam['id'], 'name': 'Ava', 'age_group': 'toddler', 'immunizations_current': False})
    assert status == 200
    status, child2 = request('POST', '/children', {'family_id': fam['id'], 'name': 'Ben', 'age_group': 'toddler', 'immunizations_current': True})
    assert status == 200
    status, e1 = request('POST', '/enrollments', {'child_id': child1['id'], 'classroom_id': cls['id'], 'status': 'enrolled'})
    assert status == 200
    status, e2 = request('POST', '/enrollments', {'child_id': child2['id'], 'classroom_id': cls['id'], 'status': 'waitlisted'})
    assert status == 200
    status, avail = request('GET', '/enrollment/availability')
    assert status == 200 and avail[0]['available_spots'] == 0
    status, moved = request('POST', f'/enrollments/{cls["id"]}/move-next')
    assert status == 400
    status, health = request('GET', '/health/compliance')
    assert status == 200 and any(not x['immunizations_current'] for x in health)
    status, inv = request('POST', '/invoices', {'family_id': fam['id'], 'child_id': child1['id'], 'amount': 100, 'description': 'Tuition'})
    assert status == 200
    status, pay = request('POST', f'/payments?family_id={fam["id"]}&invoice_id={inv["id"]}&amount=40')
    assert status == 200
    status, summary = request('GET', '/billing/summary')
    assert status == 200 and summary[0]['balance'] == 60
    status, report = request('GET', '/reports/daily')
    assert status == 200 and report['enrollment_count'] == 1
    status, audit = request('GET', '/audit')
    assert status == 200 and len(audit) >= 7
