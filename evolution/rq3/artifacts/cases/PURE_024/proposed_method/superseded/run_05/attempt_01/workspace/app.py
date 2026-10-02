from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from datetime import datetime
from uuid import uuid4
from urllib.parse import urlparse

state = {'families': {}, 'children': {}, 'classrooms': {}, 'waitlist': [], 'invoices': {}, 'payments': [], 'attendance': []}


def now(): return datetime.utcnow().isoformat() + 'Z'
def new_id(prefix): return f"{prefix}_{uuid4().hex[:10]}"


def reset_state():
    for k in state:
        state[k].clear() if isinstance(state[k], dict) else state[k].clear()


def json_response(handler, code, payload):
    body = json.dumps(payload).encode()
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length) or b'{}')
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/':
            return json_response(self, 200, {'service': 'Nenios Child Care Management', 'status': 'running'})
        if path == '/families': return json_response(self, 200, list(state['families'].values()))
        if path == '/children': return json_response(self, 200, list(state['children'].values()))
        if path == '/classrooms':
            return json_response(self, 200, [{**c, 'enrolled_count': len(c['children']), 'available': len(c['children']) < c['capacity']} for c in state['classrooms'].values()])
        if path == '/attendance': return json_response(self, 200, state['attendance'])
        if path == '/invoices': return json_response(self, 200, list(state['invoices'].values()))
        if path == '/reports/summary': return json_response(self, 200, {'families': len(state['families']), 'children': len(state['children']), 'classrooms': len(state['classrooms']), 'waitlist': len(state['waitlist']), 'invoices': len(state['invoices']), 'payments': len(state['payments']), 'attendance_events': len(state['attendance'])})
        self.send_error(404)
    def do_POST(self):
        path = urlparse(self.path).path
        data = self.read_json()
        if path == '/families':
            fid = new_id('fam'); state['families'][fid] = {'id': fid, 'name': data.get('name'), 'contacts': data.get('contacts', []), 'authorized_guardians': data.get('authorized_guardians', []), 'children': [], 'created_at': now(), 'updated_at': now()}; return json_response(self, 201, state['families'][fid])
        if path == '/children':
            fid = data.get('family_id')
            if fid not in state['families']: return self.send_error(404, 'family not found')
            cid = new_id('child'); child = {'id': cid, 'family_id': fid, 'name': data.get('name'), 'dob': data.get('dob'), 'classroom_id': None, 'waitlisted': False, 'immunization_status': data.get('immunization_status', 'missing'), 'allergy_alerts': data.get('allergy_alerts', []), 'pickup_authorities': data.get('pickup_authorities', []), 'notes': data.get('notes', ''), 'compliant': data.get('immunization_status', 'missing') in {'current', 'exempt'}, 'created_at': now(), 'updated_at': now()}; state['children'][cid] = child; state['families'][fid]['children'].append(cid); return json_response(self, 201, child)
        if path == '/classrooms':
            clid = new_id('cls'); state['classrooms'][clid] = {'id': clid, 'name': data.get('name'), 'site': data.get('site', 'default'), 'room_type': data.get('room_type', 'general'), 'capacity': int(data.get('capacity', 0)), 'children': []}; return json_response(self, 201, state['classrooms'][clid])
        if path == '/enroll':
            child = state['children'].get(data.get('child_id')); classroom = state['classrooms'].get(data.get('classroom_id'))
            if not child or not classroom: return self.send_error(404, 'child or classroom not found')
            if len(classroom['children']) >= classroom['capacity'] and not data.get('override', False): child['waitlisted'] = True; state['waitlist'].append({'child_id': child['id'], 'classroom_id': classroom['id'], 'created_at': now()}); return json_response(self, 409, {'status': 'waitlisted'})
            if child['classroom_id'] and child['classroom_id'] in state['classrooms'] and child['id'] in state['classrooms'][child['classroom_id']]['children']: state['classrooms'][child['classroom_id']]['children'].remove(child['id'])
            child['classroom_id'] = classroom['id']; child['waitlisted'] = False; classroom['children'].append(child['id']) if child['id'] not in classroom['children'] else None; return json_response(self, 200, {'status': 'enrolled'})
        if path == '/attendance/check-in':
            if data.get('child_id') not in state['children']: return self.send_error(404, 'child not found')
            rec = {'child_id': data.get('child_id'), 'action': 'check-in', 'time': now()}; state['attendance'].append(rec); return json_response(self, 201, rec)
        if path == '/attendance/check-out':
            if data.get('child_id') not in state['children']: return self.send_error(404, 'child not found')
            if not any(a['child_id'] == data.get('child_id') and a['action'] == 'check-in' for a in state['attendance']): return self.send_error(400, 'child has not been checked in')
            rec = {'child_id': data.get('child_id'), 'action': 'check-out', 'time': now()}; state['attendance'].append(rec); return json_response(self, 201, rec)
        if path == '/invoices':
            iid = new_id('inv'); inv = {'id': iid, 'family_id': data.get('family_id'), 'child_id': data.get('child_id'), 'amount': float(data.get('amount', 0)), 'balance': float(data.get('amount', 0)), 'status': 'open', 'adjustments': [], 'payments': []}; state['invoices'][iid] = inv; return json_response(self, 201, inv)
        if path == '/payments':
            inv = state['invoices'].get(data.get('invoice_id'))
            if not inv: return self.send_error(404, 'invoice not found')
            payment = {'id': new_id('pay'), 'invoice_id': inv['id'], 'payer': data.get('payer'), 'amount': float(data.get('amount', 0)), 'status': 'failed' if data.get('fail') else 'completed', 'time': now()}; state['payments'].append(payment)
            if payment['status'] == 'failed': return json_response(self, 402, payment)
            inv['balance'] = max(0.0, inv['balance'] - payment['amount']); inv['payments'].append(payment['id']); inv['status'] = 'paid' if inv['balance'] == 0 else 'open'; return json_response(self, 201, payment)
        self.send_error(404)


def main():
    reset_state()
    ThreadingHTTPServer(('0.0.0.0', 8000), Handler).serve_forever()


if __name__ == '__main__': main()
