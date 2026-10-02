from flask import Flask, jsonify, request
from datetime import datetime, date
import json
import os
from pathlib import Path

Path = Path

DATA_FILE = Path('/workspace/data.json')

def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {
        'families': [], 'children': [], 'classrooms': [], 'attendance': [],
        'invoices': [], 'payments': [], 'requests': [], 'audit_log': []
    }

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, default=str))

app = Flask(__name__)

def next_id(items):
    return (max([x['id'] for x in items], default=0) + 1)

def find(items, item_id):
    return next((x for x in items if x['id'] == item_id), None)

def child_status(child):
    status = child.get('immunization_status', 'missing')
    return status

@app.get('/')
def index():
    return jsonify({'service': 'Nenios Child Care Management', 'status': 'ok'})

@app.get('/families')
def list_families():
    return jsonify(load_data()['families'])

@app.post('/families')
def add_family():
    data = load_data()
    payload = request.get_json(force=True)
    family = {
        'id': next_id(data['families']),
        'name': payload['name'],
        'contacts': payload.get('contacts', []),
        'billing_email': payload.get('billing_email', ''),
        'children_ids': []
    }
    data['families'].append(family)
    save_data(data)
    return jsonify(family), 201

@app.post('/children')
def add_child():
    data = load_data()
    payload = request.get_json(force=True)
    family = find(data['families'], payload['family_id'])
    if not family:
        return jsonify({'error': 'family not found'}), 404
    classrooms = data['classrooms']
    classroom = find(classrooms, payload.get('classroom_id')) if payload.get('classroom_id') else None
    child = {
        'id': next_id(data['children']),
        'family_id': payload['family_id'],
        'name': payload['name'],
        'dob': payload.get('dob', ''),
        'classroom_id': classroom['id'] if classroom else None,
        'immunization_status': payload.get('immunization_status', 'missing'),
        'allergy_alerts': payload.get('allergy_alerts', []),
        'pickup_authority': payload.get('pickup_authority', []),
        'compliant': payload.get('immunization_status', 'missing') == 'current',
    }
    if classroom:
        enrolled = sum(1 for c in data['children'] if c.get('classroom_id') == classroom['id'])
        if enrolled >= classroom.get('capacity', 0):
            return jsonify({'error': 'classroom full'}), 409
    data['children'].append(child)
    family['children_ids'].append(child['id'])
    save_data(data)
    return jsonify(child), 201

@app.post('/classrooms')
def add_classroom():
    data = load_data()
    payload = request.get_json(force=True)
    classroom = {
        'id': next_id(data['classrooms']),
        'name': payload['name'],
        'capacity': int(payload['capacity']),
        'room_type': payload.get('room_type', 'general')
    }
    data['classrooms'].append(classroom)
    save_data(data)
    return jsonify(classroom), 201

@app.get('/classrooms')
def classrooms():
    data = load_data()
    result = []
    for c in data['classrooms']:
        count = sum(1 for child in data['children'] if child.get('classroom_id') == c['id'])
        result.append({**c, 'enrolled_count': count, 'available': count < c['capacity']})
    return jsonify(result)

@app.post('/attendance/checkin')
def checkin():
    data = load_data()
    payload = request.get_json(force=True)
    entry = {'id': next_id(data['attendance']), 'child_id': payload['child_id'], 'type': 'in', 'timestamp': datetime.utcnow().isoformat()}
    data['attendance'].append(entry)
    save_data(data)
    return jsonify(entry), 201

@app.post('/attendance/checkout')
def checkout():
    data = load_data()
    payload = request.get_json(force=True)
    entry = {'id': next_id(data['attendance']), 'child_id': payload['child_id'], 'type': 'out', 'timestamp': datetime.utcnow().isoformat()}
    data['attendance'].append(entry)
    save_data(data)
    return jsonify(entry), 201

@app.get('/attendance')
def attendance():
    return jsonify(load_data()['attendance'])

@app.get('/children/<int:child_id>')
def get_child(child_id):
    data = load_data()
    child = find(data['children'], child_id)
    if not child:
        return jsonify({'error': 'not found'}), 404
    classroom = find(data['classrooms'], child.get('classroom_id')) if child.get('classroom_id') else None
    family = find(data['families'], child['family_id'])
    return jsonify({
        **child,
        'classroom': classroom,
        'family_contacts': family.get('contacts', []) if family else []
    })

@app.post('/invoices')
def add_invoice():
    data = load_data()
    payload = request.get_json(force=True)
    invoice = {
        'id': next_id(data['invoices']),
        'family_id': payload['family_id'],
        'amount': float(payload['amount']),
        'balance': float(payload['amount']),
        'status': 'open',
        'items': payload.get('items', []),
    }
    data['invoices'].append(invoice)
    save_data(data)
    return jsonify(invoice), 201

@app.get('/invoices')
def invoices():
    return jsonify(load_data()['invoices'])

@app.post('/payments')
def add_payment():
    data = load_data()
    payload = request.get_json(force=True)
    invoice = find(data['invoices'], payload['invoice_id'])
    if not invoice:
        return jsonify({'error': 'invoice not found'}), 404
    amount = float(payload['amount'])
    payment = {'id': next_id(data['payments']), 'invoice_id': invoice['id'], 'amount': amount, 'payer': payload.get('payer', 'authorized'), 'status': 'posted', 'timestamp': datetime.utcnow().isoformat()}
    invoice['balance'] = round(invoice['balance'] - amount, 2)
    if invoice['balance'] <= 0:
        invoice['status'] = 'paid'
        invoice['balance'] = 0.0
    data['payments'].append(payment)
    save_data(data)
    return jsonify(payment), 201

@app.get('/children/<int:child_id>/immunization')
def immunization(child_id):
    data = load_data()
    child = find(data['children'], child_id)
    if not child:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'child_id': child_id, 'status': child_status(child), 'compliant': child.get('compliant', False)})

@app.post('/children/<int:child_id>/immunization')
def update_immunization(child_id):
    data = load_data()
    child = find(data['children'], child_id)
    if not child:
        return jsonify({'error': 'not found'}), 404
    payload = request.get_json(force=True)
    child['immunization_status'] = payload['status']
    child['compliant'] = payload['status'] == 'current'
    save_data(data)
    return jsonify({'child_id': child_id, 'status': child['immunization_status'], 'compliant': child['compliant']})

@app.post('/requests')
def add_request():
    data = load_data()
    payload = request.get_json(force=True)
    req = {'id': next_id(data['requests']), 'type': payload['type'], 'details': payload.get('details', {}), 'status': 'pending'}
    data['requests'].append(req)
    save_data(data)
    return jsonify(req), 201

@app.get('/requests')
def list_requests():
    return jsonify(load_data()['requests'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=True)
