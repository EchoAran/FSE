from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json, uuid
from datetime import date

STATE = {'families': {}, 'children': {}, 'classrooms': {}, 'invoices': {}, 'payments': {}, 'waiting_list': []}

def j(x): return json.dumps(x).encode()
def nid(p): return f"{p}_{uuid.uuid4().hex[:8]}"
def today(): return date.today().isoformat()

def recalc():
    for c in STATE['classrooms'].values(): c['enrolled_count'] = 0
    for ch in STATE['children'].values():
        cid = ch.get('classroom_id')
        if cid in STATE['classrooms']: STATE['classrooms'][cid]['enrolled_count'] += 1

class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        data = j(obj)
        self.send_response(code); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)
    def _read(self):
        l = int(self.headers.get('Content-Length', '0'))
        return json.loads(self.rfile.read(l) or b'{}')
    def do_GET(self):
        p = urlparse(self.path).path
        if p == '/health': return self._send(200, {'ok': True})
        if p == '/dashboard': recalc(); return self._send(200, {'classrooms': list(STATE['classrooms'].values()), 'waiting_list': STATE['waiting_list']})
        self._send(404, {'error': 'not found'})
    def do_POST(self):
        p = urlparse(self.path).path; d = self._read()
        if p == '/families':
            i = nid('fam'); STATE['families'][i] = {'id': i, 'name': d['name'], 'contact': d.get('contact', {})}; return self._send(201, STATE['families'][i])
        if p == '/children':
            if d['family_id'] not in STATE['families']: return self._send(404, {'error': 'family not found'})
            i = nid('child'); STATE['children'][i] = {'id': i, 'family_id': d['family_id'], 'name': d['name'], 'classroom_id': None, 'attendance': [], 'immunization_status': d.get('immunization_status', 'missing')}; return self._send(201, STATE['children'][i])
        if p == '/classrooms':
            i = nid('cls'); STATE['classrooms'][i] = {'id': i, 'name': d['name'], 'capacity': int(d['capacity']), 'enrolled_count': 0}; return self._send(201, STATE['classrooms'][i])
        if p.endswith('/assign'):
            cid = p.split('/')[2]; ch = STATE['children'].get(cid); cl = STATE['classrooms'].get(d['classroom_id'])
            if not ch or not cl: return self._send(404, {'error': 'not found'})
            recalc()
            if cl['enrolled_count'] >= cl['capacity'] and not d.get('override'): return self._send(409, {'error': 'classroom full'})
            ch['classroom_id'] = cl['id']; recalc(); return self._send(200, ch)
        if p.endswith('/checkin'):
            cid = p.split('/')[2]; ch = STATE['children'].get(cid)
            if not ch: return self._send(404, {'error': 'not found'})
            ch['attendance'].append({'date': today(), 'check_in': True}); return self._send(200, {'status': 'checked_in'})
        if p.endswith('/checkout'):
            cid = p.split('/')[2]; ch = STATE['children'].get(cid)
            if not ch: return self._send(404, {'error': 'not found'})
            ch['attendance'].append({'date': today(), 'check_out': True}); return self._send(200, {'status': 'checked_out'})
        if p == '/invoices':
            i = nid('inv'); STATE['invoices'][i] = {'id': i, 'family_id': d['family_id'], 'amount': float(d['amount']), 'balance': float(d['amount']), 'status': 'open'}; return self._send(201, STATE['invoices'][i])
        if p == '/payments':
            inv = STATE['invoices'].get(d['invoice_id'])
            if not inv: return self._send(404, {'error': 'invoice not found'})
            amt = float(d['amount'])
            if amt > inv['balance']: return self._send(400, {'error': 'payment exceeds balance'})
            inv['balance'] -= amt
            if inv['balance'] == 0: inv['status'] = 'paid'
            return self._send(200, {'invoice': inv, 'payment': {'amount': amt}})
        if p == '/waiting-list':
            i = nid('wait'); e = {'id': i, 'family_id': d['family_id'], 'child_name': d['child_name']}; STATE['waiting_list'].append(e); return self._send(201, e)
        self._send(404, {'error': 'not found'})

def run(host='0.0.0.0', port=8000):
    ThreadingHTTPServer((host, port), H).serve_forever()

if __name__ == '__main__':
    run()
