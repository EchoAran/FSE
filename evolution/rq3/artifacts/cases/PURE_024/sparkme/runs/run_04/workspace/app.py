from flask import Flask, request, jsonify, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

DB = {
    'users': {
        'admin': {'password': 'admin', 'roles': ['administrator']},
        'teacher': {'password': 'teacher', 'roles': ['teacher']},
        'office': {'password': 'office', 'roles': ['office']},
    },
    'families': {},
    'children': {},
    'invoices': {},
    'audit': [],
    'imports': [],
}

COUNTERS = {'family': 1, 'child': 1, 'invoice': 1, 'import': 1}


def now():
    return datetime.utcnow().isoformat() + 'Z'


def audit(action, entity_type=None, entity_id=None, extra=None):
    DB['audit'].append({
        'time': now(), 'user': session.get('user'), 'action': action,
        'entity_type': entity_type, 'entity_id': entity_id, 'extra': extra or {}
    })


def login_required():
    if 'user' not in session:
        return jsonify({'error': 'authentication required'}), 401


def current_roles():
    user = session.get('user')
    if not user:
        return []
    return DB['users'][user]['roles']


def require_role(*roles):
    if not set(current_roles()).intersection(roles):
        return jsonify({'error': 'forbidden'}), 403


def entity_visible(entity):
    return True if entity else False


def next_id(kind):
    val = COUNTERS[kind]
    COUNTERS[kind] += 1
    return str(val)


@app.post('/login')
def login():
    data = request.get_json(force=True)
    user = data.get('username')
    password = data.get('password')
    if user in DB['users'] and DB['users'][user]['password'] == password:
        session['user'] = user
        audit('login')
        return jsonify({'ok': True, 'user': user, 'roles': DB['users'][user]['roles']})
    return jsonify({'error': 'invalid credentials'}), 401


@app.post('/logout')
def logout():
    audit('logout')
    session.clear()
    return jsonify({'ok': True})


@app.get('/me')
def me():
    if 'user' not in session:
        return jsonify({'authenticated': False})
    return jsonify({'authenticated': True, 'user': session['user'], 'roles': current_roles()})


@app.get('/families')
def families_list():
    if login_required():
        return login_required()
    q = request.args.get('q', '').lower()
    archived = request.args.get('archived') == '1'
    items = []
    for fam in DB['families'].values():
        if not archived and fam.get('archived'):
            continue
        if q and q not in fam['name'].lower() and q not in fam.get('contact', '').lower():
            continue
        items.append(fam)
    return jsonify(items)


@app.post('/families')
def create_family():
    if login_required():
        return login_required()
    if not set(current_roles()).intersection({'administrator', 'office'}):
        return jsonify({'error': 'forbidden'}), 403
    data = request.get_json(force=True)
    fid = next_id('family')
    family = {'id': fid, 'name': data.get('name', ''), 'contact': data.get('contact', ''), 'billing': data.get('billing', {}), 'archived': False, 'history': []}
    DB['families'][fid] = family
    audit('create', 'family', fid)
    return jsonify(family), 201


@app.get('/children')
def children_list():
    if login_required():
        return login_required()
    archived = request.args.get('archived') == '1'
    items = [c for c in DB['children'].values() if archived or not c.get('archived')]
    return jsonify(items)


@app.post('/children')
def create_child():
    if login_required():
        return login_required()
    if not set(current_roles()).intersection({'administrator', 'office'}):
        return jsonify({'error': 'forbidden'}), 403
    data = request.get_json(force=True)
    cid = next_id('child')
    child = {'id': cid, 'family_id': data.get('family_id'), 'name': data.get('name', ''), 'allergies': data.get('allergies', []), 'immunizations': data.get('immunizations', []), 'classroom': data.get('classroom'), 'archived': False, 'notes': []}
    DB['children'][cid] = child
    audit('create', 'child', cid)
    return jsonify(child), 201


@app.post('/children/<cid>/archive')
def archive_child(cid):
    if login_required():
        return login_required()
    if not set(current_roles()).intersection({'administrator', 'office'}):
        return jsonify({'error': 'forbidden'}), 403
    child = DB['children'].get(cid)
    if not child:
        return jsonify({'error': 'not found'}), 404
    child['archived'] = True
    audit('archive', 'child', cid)
    return jsonify(child)


@app.get('/invoices')
def invoices_list():
    if login_required():
        return login_required()
    return jsonify(list(DB['invoices'].values()))


@app.post('/invoices')
def create_invoice():
    if login_required():
        return login_required()
    if not set(current_roles()).intersection({'administrator', 'office'}):
        return jsonify({'error': 'forbidden'}), 403
    data = request.get_json(force=True)
    iid = next_id('invoice')
    inv = {'id': iid, 'family_id': data.get('family_id'), 'amount': float(data.get('amount', 0)), 'status': 'unpaid', 'payments': [], 'draft': bool(data.get('draft', False)), 'history': [{'time': now(), 'status': 'draft' if data.get('draft', False) else 'submitted'}]}
    DB['invoices'][iid] = inv
    audit('create', 'invoice', iid)
    return jsonify(inv), 201


@app.post('/invoices/<iid>/pay')
def pay_invoice(iid):
    if login_required():
        return login_required()
    if not set(current_roles()).intersection({'administrator', 'office'}):
        return jsonify({'error': 'forbidden'}), 403
    inv = DB['invoices'].get(iid)
    if not inv:
        return jsonify({'error': 'not found'}), 404
    data = request.get_json(force=True)
    amount = float(data.get('amount', 0))
    inv['payments'].append({'time': now(), 'amount': amount, 'type': 'payment'})
    paid = sum(p['amount'] for p in inv['payments'])
    if paid >= inv['amount']:
        inv['status'] = 'paid'
    elif paid > 0:
        inv['status'] = 'partial'
    audit('payment', 'invoice', iid, {'amount': amount})
    return jsonify(inv)


@app.get('/audit')
def audit_log():
    if login_required():
        return login_required()
    return jsonify(DB['audit'])


@app.post('/import')
def import_data():
    if login_required():
        return login_required()
    if not set(current_roles()).intersection({'administrator', 'office'}):
        return jsonify({'error': 'forbidden'}), 403
    data = request.get_json(force=True)
    report = {'id': next_id('import'), 'received_at': now(), 'warnings': [], 'created': {'families': 0, 'children': 0, 'invoices': 0}}
    for fam in data.get('families', []):
        fid = next_id('family')
        DB['families'][fid] = {'id': fid, 'name': fam.get('name', ''), 'contact': fam.get('contact', ''), 'billing': fam.get('billing', {}), 'archived': False}
        report['created']['families'] += 1
    for child in data.get('children', []):
        if not child.get('family_id'):
            report['warnings'].append('child missing family_id')
            continue
        cid = next_id('child')
        DB['children'][cid] = {'id': cid, 'family_id': child['family_id'], 'name': child.get('name', ''), 'allergies': child.get('allergies', []), 'immunizations': child.get('immunizations', []), 'classroom': child.get('classroom'), 'archived': False}
        report['created']['children'] += 1
    DB['imports'].append(report)
    audit('import', extra=report)
    return jsonify(report), 201


@app.get('/')
def index():
    return jsonify({'service': 'Nenios Child Care Management', 'authenticated': 'user' in session, 'endpoints': ['/login', '/families', '/children', '/invoices', '/import', '/audit']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '8000')), debug=False)
