from flask import Flask, jsonify, request
from datetime import datetime, date, timezone
import uuid

app = Flask(__name__)

state = {
    'families': {},
    'children': {},
    'classrooms': {},
    'invoices': {},
    'payments': {},
    'attendance': [],
    'waiting_list': [],
}


def new_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def parse_iso_date(value):
    if not value:
        return None
    return date.fromisoformat(value)


@app.get('/health')
def health():
    return jsonify({'status': 'ok'})


@app.post('/families')
def create_family():
    data = request.get_json(force=True)
    family_id = new_id('fam')
    state['families'][family_id] = {
        'id': family_id,
        'name': data['name'],
        'contacts': data.get('contacts', []),
        'address': data.get('address', ''),
        'children': [],
    }
    return jsonify(state['families'][family_id]), 201


@app.post('/classrooms')
def create_classroom():
    data = request.get_json(force=True)
    classroom_id = new_id('cls')
    state['classrooms'][classroom_id] = {
        'id': classroom_id,
        'name': data['name'],
        'capacity': int(data['capacity']),
        'enrolled_children': [],
    }
    return jsonify(state['classrooms'][classroom_id]), 201


@app.post('/children')
def register_child():
    data = request.get_json(force=True)
    family_id = data['family_id']
    classroom_id = data.get('classroom_id')
    if family_id not in state['families']:
        return jsonify({'error': 'family not found'}), 404
    child_id = new_id('chi')
    child = {
        'id': child_id,
        'family_id': family_id,
        'name': data['name'],
        'dob': data.get('dob'),
        'immunization_status': data.get('immunization_status', 'missing'),
        'allergies': data.get('allergies', []),
        'pickup_authority': data.get('pickup_authority', []),
        'classroom_id': None,
        'waiting_list': False,
    }
    if classroom_id:
        classroom = state['classrooms'].get(classroom_id)
        if not classroom:
            return jsonify({'error': 'classroom not found'}), 404
        if len(classroom['enrolled_children']) >= classroom['capacity']:
            child['waiting_list'] = True
            state['waiting_list'].append(child_id)
        else:
            classroom['enrolled_children'].append(child_id)
            child['classroom_id'] = classroom_id
    state['children'][child_id] = child
    state['families'][family_id]['children'].append(child_id)
    return jsonify(child), 201


@app.get('/children/<child_id>')
def get_child(child_id):
    child = state['children'].get(child_id)
    if not child:
        return jsonify({'error': 'not found'}), 404
    return jsonify(child)


@app.post('/attendance/checkin')
def checkin():
    data = request.get_json(force=True)
    child_id = data['child_id']
    if child_id not in state['children']:
        return jsonify({'error': 'child not found'}), 404
    record = {'child_id': child_id, 'type': 'in', 'time': datetime.now(timezone.utc).isoformat()}
    state['attendance'].append(record)
    return jsonify(record), 201


@app.post('/attendance/checkout')
def checkout():
    data = request.get_json(force=True)
    child_id = data['child_id']
    if child_id not in state['children']:
        return jsonify({'error': 'child not found'}), 404
    record = {'child_id': child_id, 'type': 'out', 'time': datetime.now(timezone.utc).isoformat()}
    state['attendance'].append(record)
    return jsonify(record), 201


@app.get('/attendance')
def attendance():
    return jsonify(state['attendance'])


@app.post('/invoices')
def create_invoice():
    data = request.get_json(force=True)
    invoice_id = new_id('inv')
    state['invoices'][invoice_id] = {
        'id': invoice_id,
        'family_id': data['family_id'],
        'amount': float(data['amount']),
        'balance': float(data['amount']),
        'status': 'open',
        'payments': [],
    }
    return jsonify(state['invoices'][invoice_id]), 201


@app.post('/payments')
def make_payment():
    data = request.get_json(force=True)
    invoice = state['invoices'].get(data['invoice_id'])
    if not invoice:
        return jsonify({'error': 'invoice not found'}), 404
    amount = float(data['amount'])
    payment_id = new_id('pay')
    payment = {
        'id': payment_id,
        'invoice_id': data['invoice_id'],
        'amount': amount,
        'payer': data.get('payer', 'account_holder'),
        'status': 'completed',
        'time': datetime.now(timezone.utc).isoformat(),
    }
    invoice['balance'] = round(invoice['balance'] - amount, 2)
    invoice['payments'].append(payment_id)
    if invoice['balance'] <= 0:
        invoice['status'] = 'paid'
        invoice['balance'] = 0.0
    state['payments'][payment_id] = payment
    return jsonify(payment), 201


@app.get('/waiting-list')
def waiting_list():
    return jsonify(state['waiting_list'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
