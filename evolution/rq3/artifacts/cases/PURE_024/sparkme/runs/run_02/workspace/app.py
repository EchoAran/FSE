from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from datetime import datetime
import json
import threading

state = {
    'users': {
        'admin': {'password': 'admin', 'roles': ['administrator']},
        'teacher': {'password': 'teacher', 'roles': ['teacher']},
        'office': {'password': 'office', 'roles': ['front-desk', 'billing']},
    },
    'sessions': {},
    'families': {},
    'children': {},
    'invoices': {},
    'imports': {},
    'audit': [],
    'counters': {'family': 1, 'child': 1, 'invoice': 1, 'import': 1},
    'record_locks': {},
}
lock = threading.Lock()


def now(): return datetime.utcnow().isoformat() + 'Z'

def log(action, user, target, details=None):
    state['audit'].append({'time': now(), 'action': action, 'user': user, 'target': target, 'details': details or {}})

def next_id(kind):
    val = state['counters'][kind]
    state['counters'][kind] += 1
    return str(val)

def json_response(handler, code, payload):
    body = json.dumps(payload).encode()
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

def read_json(handler):
    length = int(handler.headers.get('Content-Length', 0))
    return json.loads(handler.rfile.read(length) or b'{}')

def session_user(handler):
    token = handler.headers.get('X-Session-Token')
    return state['sessions'].get(token)

def require_role(handler, *roles):
    user = session_user(handler)
    if not user: return None, (401, {'error': 'authentication required'})
    if not set(user['roles']).intersection(roles): return None, (403, {'error': 'forbidden'})
    return user, None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/': return json_response(self, 200, {'service': 'Nenios Child Care Management', 'status': 'running'})
        if path == '/audit':
            user, err = require_role(self, 'administrator')
            if err: return json_response(self, err[0], err[1])
            return json_response(self, 200, state['audit'])
        if path.startswith('/records/'):
            user = session_user(self)
            if not user: return json_response(self, 401, {'error': 'authentication required'})
            _, kind, rid = path.split('/', 3)[1:]
            rec = {'family': state['families'], 'child': state['children'], 'invoice': state['invoices']}.get(kind, {}).get(rid)
            if not rec: return json_response(self, 404, {'error': 'not found'})
            owner = state['record_locks'].get(f'{kind}:{rid}')
            if owner and owner != user['username']: return json_response(self, 200, {'record': rec, 'warning': f'being edited by {owner}', 'read_only': True})
            state['record_locks'][f'{kind}:{rid}'] = user['username']
            log('view_record', user['username'], f'{kind}:{rid}')
            return json_response(self, 200, rec)
        return json_response(self, 404, {'error': 'not found'})

    def do_POST(self):
        path = urlparse(self.path).path
        data = read_json(self) if self.headers.get('Content-Length') else {}
        if path == '/login':
            user = state['users'].get(data.get('username'))
            if not user or user['password'] != data.get('password'): return json_response(self, 401, {'error': 'invalid credentials'})
            token = f"t{len(state['sessions'])+1}"
            state['sessions'][token] = {'username': data['username'], 'roles': user['roles']}
            log('login', data['username'], 'session')
            return json_response(self, 200, {'token': token, 'roles': user['roles']})
        if path == '/families':
            user, err = require_role(self, 'administrator', 'front-desk', 'billing')
            if err: return json_response(self, err[0], err[1])
            fid = next_id('family'); state['families'][fid] = {'id': fid, 'name': data.get('name'), 'contact': data.get('contact', {}), 'archived': False, 'children': []}; log('create_family', user['username'], f'family:{fid}'); return json_response(self, 201, state['families'][fid])
        if path == '/children':
            user, err = require_role(self, 'administrator', 'front-desk')
            if err: return json_response(self, err[0], err[1])
            cid = next_id('child'); state['children'][cid] = {'id': cid, 'family_id': data.get('family_id'), 'name': data.get('name'), 'allergies': data.get('allergies', []), 'immunizations': data.get('immunizations', []), 'status': 'active', 'draft': False, 'updated_at': now()};
            if data.get('family_id') in state['families']: state['families'][data.get('family_id')]['children'].append(cid)
            log('create_child', user['username'], f'child:{cid}'); return json_response(self, 201, state['children'][cid])
        if path.endswith('/archive') and path.startswith('/children/'):
            user, err = require_role(self, 'administrator')
            if err: return json_response(self, err[0], err[1])
            cid = path.split('/')[2]; child = state['children'].get(cid)
            if not child: return json_response(self, 404, {'error': 'not found'})
            child['status'] = 'archived'; child['archived_at'] = now(); log('archive_child', user['username'], f'child:{cid}'); return json_response(self, 200, child)
        if path == '/invoices':
            user, err = require_role(self, 'administrator', 'billing', 'front-desk')
            if err: return json_response(self, err[0], err[1])
            iid = next_id('invoice'); state['invoices'][iid] = {'id': iid, 'family_id': data.get('family_id'), 'amount': float(data.get('amount', 0)), 'paid_amount': 0.0, 'status': 'draft' if data.get('draft', True) else 'submitted', 'payments': [], 'updated_at': now()}; log('create_invoice', user['username'], f'invoice:{iid}'); return json_response(self, 201, state['invoices'][iid])
        if path.startswith('/invoices/') and path.endswith('/submit'):
            user, err = require_role(self, 'administrator', 'billing')
            if err: return json_response(self, err[0], err[1])
            iid = path.split('/')[2]; inv = state['invoices'].get(iid)
            if not inv: return json_response(self, 404, {'error': 'not found'})
            inv['status'] = 'submitted'; inv['updated_at'] = now(); log('submit_invoice', user['username'], f'invoice:{iid}'); return json_response(self, 200, inv)
        if path.startswith('/invoices/') and path.endswith('/pay'):
            user, err = require_role(self, 'administrator', 'billing')
            if err: return json_response(self, err[0], err[1])
            iid = path.split('/')[2]; inv = state['invoices'].get(iid)
            if not inv: return json_response(self, 404, {'error': 'not found'})
            amt = float(data.get('amount', 0)); inv['paid_amount'] += amt; inv['payments'].append({'date': now(), 'amount': amt, 'type': 'payment'}); inv['status'] = 'paid' if inv['paid_amount'] >= inv['amount'] else 'partial'; inv['updated_at'] = now(); log('pay_invoice', user['username'], f'invoice:{iid}', {'amount': amt}); return json_response(self, 200, inv)
        if path == '/imports/preview':
            user, err = require_role(self, 'administrator')
            if err: return json_response(self, err[0], err[1])
            iid = next_id('import'); records = data.get('records', []); flagged = [r for r in records if any(v in (None, '', 'UNKNOWN') for v in r.values())]; state['imports'][iid] = {'id': iid, 'records': records, 'flagged': flagged, 'status': 'preview'}; log('import_preview', user['username'], f'import:{iid}'); return json_response(self, 200, state['imports'][iid])
        if path.startswith('/imports/') and path.endswith('/finalize'):
            user, err = require_role(self, 'administrator')
            if err: return json_response(self, err[0], err[1])
            iid = path.split('/')[2]; imp = state['imports'].get(iid)
            if not imp: return json_response(self, 404, {'error': 'not found'})
            imp['status'] = 'finalized'; log('import_finalize', user['username'], f'import:{iid}'); return json_response(self, 200, imp)
        return json_response(self, 404, {'error': 'not found'})

    def log_message(self, *args):
        pass


def main():
    server = ThreadingHTTPServer(('0.0.0.0', 8000), Handler)
    server.serve_forever()

if __name__ == '__main__':
    main()
