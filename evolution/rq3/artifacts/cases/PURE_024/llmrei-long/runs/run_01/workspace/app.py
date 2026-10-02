from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime, timezone

ROLES = {'admin', 'office_staff', 'teacher', 'parent'}
STATE = {
    'families': {}, 'children': {}, 'classrooms': {}, 'enrollments': {},
    'invoices': {}, 'payments': {}, 'audit': [],
    'next_ids': {k: 1 for k in ['family', 'child', 'classroom', 'enrollment', 'invoice', 'payment']}
}


def next_id(kind):
    i = STATE['next_ids'][kind]
    STATE['next_ids'][kind] += 1
    return i


def audit(action, entity, entity_id, role, before=None, after=None):
    STATE['audit'].append({
        'ts': datetime.now(timezone.utc).isoformat(), 'action': action, 'entity': entity,
        'entity_id': entity_id, 'role': role, 'before': before, 'after': after
    })


def json_response(handler, code, payload):
    data = json.dumps(payload).encode()
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def read_body(handler):
    length = int(handler.headers.get('Content-Length', '0'))
    if length <= 0:
        return {}
    return json.loads(handler.rfile.read(length).decode())


def role_from(handler):
    role = handler.headers.get('X-Role', 'office_staff')
    if role not in ROLES:
        raise PermissionError('invalid role')
    return role


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        try:
            role = role_from(self)
            path = urlparse(self.path).path
            if path == '/':
                return json_response(self, 200, {'service': 'Nenios Child Care Management', 'status': 'ok'})
            if path == '/enrollment/availability':
                result = []
                for c in STATE['classrooms'].values():
                    enrolled = sum(1 for e in STATE['enrollments'].values() if e['classroom_id'] == c['id'] and e['status'] == 'enrolled')
                    result.append({**c, 'available_spots': c['capacity'] - enrolled})
                return json_response(self, 200, result)
            if path == '/health/compliance':
                return json_response(self, 200, [{'child_id': c['id'], 'name': c['name'], 'immunizations_current': c.get('immunizations_current', False)} for c in STATE['children'].values()])
            if path == '/billing/summary':
                return json_response(self, 200, list(STATE['invoices'].values()))
            if path == '/reports/daily':
                enrolled = [e for e in STATE['enrollments'].values() if e['status'] == 'enrolled']
                waitlisted = [e for e in STATE['enrollments'].values() if e['status'] == 'waitlisted']
                open_spots = {c['id']: c['capacity'] - sum(1 for e in enrolled if e['classroom_id'] == c['id']) for c in STATE['classrooms'].values()}
                return json_response(self, 200, {'enrollment_count': len(enrolled), 'waitlist_count': len(waitlisted), 'open_spots': open_spots, 'unpaid_invoices': [i for i in STATE['invoices'].values() if i['balance'] > 0], 'health_reminders': [c for c in STATE['children'].values() if not c.get('immunizations_current', False)]})
            if path == '/audit':
                return json_response(self, 200, STATE['audit'])
            return json_response(self, 404, {'error': 'not found'})
        except PermissionError as e:
            return json_response(self, 403, {'error': str(e)})

    def do_POST(self):
        try:
            role = role_from(self)
            path = urlparse(self.path).path
            body = read_body(self)
            if path == '/families':
                fid = next_id('family'); STATE['families'][fid] = {'id': fid, 'name': body.get('name', ''), 'contacts': body.get('contacts', [])}; audit('create', 'family', fid, role, None, STATE['families'][fid]); return json_response(self, 200, STATE['families'][fid])
            if path == '/classrooms':
                if role not in {'admin', 'office_staff'}: return json_response(self, 403, {'error': 'not allowed'})
                cid = next_id('classroom'); STATE['classrooms'][cid] = {'id': cid, 'name': body.get('name', ''), 'age_group': body.get('age_group', ''), 'capacity': int(body.get('capacity', 0))}; audit('create', 'classroom', cid, role, None, STATE['classrooms'][cid]); return json_response(self, 200, STATE['classrooms'][cid])
            if path == '/children':
                if body.get('family_id') not in STATE['families']: return json_response(self, 404, {'error': 'family not found'})
                cid = next_id('child'); STATE['children'][cid] = {'id': cid, 'family_id': body['family_id'], 'name': body.get('name', ''), 'age_group': body.get('age_group', ''), 'health_info': body.get('health_info', {}), 'immunizations_current': bool(body.get('immunizations_current', False))}; audit('create', 'child', cid, role, None, STATE['children'][cid]); return json_response(self, 200, STATE['children'][cid])
            if path == '/enrollments':
                if body.get('child_id') not in STATE['children']: return json_response(self, 404, {'error': 'child not found'})
                if body.get('classroom_id') not in STATE['classrooms']: return json_response(self, 404, {'error': 'classroom not found'})
                classroom = STATE['classrooms'][body['classroom_id']]
                enrolled = sum(1 for e in STATE['enrollments'].values() if e['classroom_id'] == body['classroom_id'] and e['status'] == 'enrolled')
                if body.get('status', 'pending') == 'enrolled' and enrolled >= classroom['capacity']:
                    return json_response(self, 400, {'error': 'classroom full'})
                eid = next_id('enrollment'); STATE['enrollments'][eid] = {'id': eid, 'child_id': body['child_id'], 'classroom_id': body['classroom_id'], 'status': body.get('status', 'pending')}; audit('create', 'enrollment', eid, role, None, STATE['enrollments'][eid]); return json_response(self, 200, STATE['enrollments'][eid])
            if path.startswith('/enrollments/') and path.endswith('/move-next'):
                classroom_id = int(path.split('/')[2])
                if classroom_id not in STATE['classrooms']: return json_response(self, 404, {'error': 'classroom not found'})
                classroom = STATE['classrooms'][classroom_id]
                open_spots = classroom['capacity'] - sum(1 for e in STATE['enrollments'].values() if e['classroom_id'] == classroom_id and e['status'] == 'enrolled')
                if open_spots <= 0: return json_response(self, 400, {'error': 'no available spots'})
                candidates = [e for e in STATE['enrollments'].values() if e['classroom_id'] == classroom_id and e['status'] == 'waitlisted']
                if not candidates: return json_response(self, 404, {'error': 'no waitlisted child'})
                chosen = sorted(candidates, key=lambda e: e['id'])[0]
                before = chosen.copy(); chosen['status'] = 'enrolled'; audit('update', 'enrollment', chosen['id'], role, before, chosen.copy()); return json_response(self, 200, chosen)
            if path.startswith('/children/') and path.endswith('/health'):
                child_id = int(path.split('/')[2])
                if child_id not in STATE['children']: return json_response(self, 404, {'error': 'child not found'})
                before = STATE['children'][child_id].copy()
                if 'immunizations_current' in body: STATE['children'][child_id]['immunizations_current'] = bool(body['immunizations_current'])
                if 'note' in body: STATE['children'][child_id].setdefault('health_info', {})['note'] = body['note']
                audit('update', 'child', child_id, role, before, STATE['children'][child_id].copy()); return json_response(self, 200, STATE['children'][child_id])
            if path == '/invoices':
                if body.get('family_id') not in STATE['families'] or body.get('child_id') not in STATE['children']: return json_response(self, 404, {'error': 'family or child not found'})
                iid = next_id('invoice'); amount = float(body.get('amount', 0)); STATE['invoices'][iid] = {'id': iid, 'family_id': body['family_id'], 'child_id': body['child_id'], 'amount': amount, 'description': body.get('description', ''), 'paid': 0.0, 'balance': amount}; audit('create', 'invoice', iid, role, None, STATE['invoices'][iid]); return json_response(self, 200, STATE['invoices'][iid])
            if path == '/payments':
                params = parse_qs(urlparse(self.path).query)
                family_id = int(params.get('family_id', [body.get('family_id')])[0])
                invoice_id = int(params.get('invoice_id', [body.get('invoice_id')])[0])
                amount = float(params.get('amount', [body.get('amount')])[0])
                if invoice_id not in STATE['invoices']: return json_response(self, 404, {'error': 'invoice not found'})
                inv = STATE['invoices'][invoice_id]
                if inv['family_id'] != family_id: return json_response(self, 400, {'error': 'family mismatch'})
                pid = next_id('payment'); STATE['payments'][pid] = {'id': pid, 'family_id': family_id, 'invoice_id': invoice_id, 'amount': amount}; inv['paid'] += amount; inv['balance'] = max(0.0, inv['amount'] - inv['paid']); audit('create', 'payment', pid, role, None, STATE['payments'][pid]); return json_response(self, 200, STATE['payments'][pid])
            return json_response(self, 404, {'error': 'not found'})
        except PermissionError as e:
            return json_response(self, 403, {'error': str(e)})


def run(host='0.0.0.0', port=8000):
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == '__main__':
    run()
