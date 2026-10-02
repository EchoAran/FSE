from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json
from uuid import uuid4
from datetime import datetime

families = {}
children = {}
classrooms = {}
invoices = {}


def new_id(prefix):
    return f"{prefix}_{uuid4().hex[:8]}"


def read_json(handler):
    length = int(handler.headers.get('Content-Length', 0))
    raw = handler.rfile.read(length) if length else b'{}'
    try:
        return json.loads(raw.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return {}


def send(handler, status, payload):
    data = json.dumps(payload).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


class NeniosHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/':
            return send(self, 200, {
                'service': 'Nenios Child Care Management',
                'status': 'running',
                'routes': ['/families', '/children', '/classrooms', '/enrollments', '/waiting-list', '/immunizations', '/invoices', '/reports/summary'],
            })
        if path == '/families':
            return send(self, 200, list(families.values()))
        if path == '/children':
            return send(self, 200, list(children.values()))
        if path == '/classrooms':
            return send(self, 200, list(classrooms.values()))
        if path == '/invoices':
            return send(self, 200, list(invoices.values()))
        if path == '/reports/summary':
            enrolled = sum(1 for child in children.values() if child['status'] == 'enrolled')
            waiting = sum(1 for child in children.values() if child['status'] == 'waiting')
            paid = sum(1 for invoice in invoices.values() if invoice['status'] == 'paid')
            unpaid = sum(1 for invoice in invoices.values() if invoice['status'] != 'paid')
            return send(self, 200, {
                'families': len(families),
                'children': len(children),
                'classrooms': len(classrooms),
                'enrolled_children': enrolled,
                'waiting_children': waiting,
                'invoices': len(invoices),
                'paid_invoices': paid,
                'unpaid_invoices': unpaid,
            })
        if path.startswith('/reports/customer/'):
            family_id = path.rsplit('/', 1)[-1]
            if family_id not in families:
                return send(self, 404, {'error': 'family not found'})
            fam = families[family_id]
            fam_children = [children[cid] for cid in fam['children'] if cid in children]
            fam_invoices = [inv for inv in invoices.values() if inv['family_id'] == family_id]
            return send(self, 200, {'family': fam, 'children': fam_children, 'invoices': fam_invoices})
        return send(self, 404, {'error': 'not found'})

    def do_POST(self):
        path = urlparse(self.path).path
        data = read_json(self)
        if path == '/families':
            name = data.get('name')
            if not name:
                return send(self, 400, {'error': 'family name is required'})
            family_id = new_id('fam')
            family = {'id': family_id, 'name': name, 'contact': data.get('contact', {}), 'children': []}
            families[family_id] = family
            return send(self, 201, family)
        if path == '/children':
            family_id = data.get('family_id')
            name = data.get('name')
            if not family_id or family_id not in families:
                return send(self, 400, {'error': 'valid family_id is required'})
            if not name:
                return send(self, 400, {'error': 'child name is required'})
            child_id = new_id('chi')
            child = {'id': child_id, 'family_id': family_id, 'name': name, 'classroom_id': None, 'immunizations': [], 'status': 'unenrolled'}
            children[child_id] = child
            families[family_id]['children'].append(child_id)
            return send(self, 201, child)
        if path == '/classrooms':
            name = data.get('name')
            capacity = data.get('capacity')
            if not name or capacity is None:
                return send(self, 400, {'error': 'name and capacity are required'})
            try:
                capacity = int(capacity)
            except (TypeError, ValueError):
                return send(self, 400, {'error': 'capacity must be an integer'})
            classroom_id = new_id('cls')
            classroom = {'id': classroom_id, 'name': name, 'capacity': capacity, 'enrolled_children': []}
            classrooms[classroom_id] = classroom
            return send(self, 201, classroom)
        if path == '/enrollments':
            child_id = data.get('child_id')
            classroom_id = data.get('classroom_id')
            if child_id not in children:
                return send(self, 400, {'error': 'valid child_id is required'})
            if classroom_id not in classrooms:
                return send(self, 400, {'error': 'valid classroom_id is required'})
            child = children[child_id]
            classroom = classrooms[classroom_id]
            if len(classroom['enrolled_children']) >= classroom['capacity']:
                child['status'] = 'waiting'
                child['classroom_id'] = None
                return send(self, 202, {'message': 'classroom full; child added to waiting list', 'child': child})
            if child['classroom_id'] and child['classroom_id'] in classrooms:
                old = classrooms[child['classroom_id']]
                if child_id in old['enrolled_children']:
                    old['enrolled_children'].remove(child_id)
            classroom['enrolled_children'].append(child_id)
            child['classroom_id'] = classroom_id
            child['status'] = 'enrolled'
            return send(self, 200, child)
        if path == '/waiting-list':
            child_id = data.get('child_id')
            if child_id not in children:
                return send(self, 400, {'error': 'valid child_id is required'})
            child = children[child_id]
            child['status'] = 'waiting'
            child['classroom_id'] = None
            return send(self, 200, child)
        if path == '/immunizations':
            child_id = data.get('child_id')
            if child_id not in children:
                return send(self, 400, {'error': 'valid child_id is required'})
            record = {'vaccine': data.get('vaccine', 'unknown'), 'date': data.get('date', datetime.utcnow().date().isoformat()), 'status': data.get('status', 'recorded')}
            children[child_id]['immunizations'].append(record)
            return send(self, 201, record)
        if path == '/invoices':
            family_id = data.get('family_id')
            amount = data.get('amount')
            description = data.get('description', 'Tuition and care services')
            if family_id not in families:
                return send(self, 400, {'error': 'valid family_id is required'})
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                return send(self, 400, {'error': 'amount must be numeric'})
            invoice_id = new_id('inv')
            invoice = {'id': invoice_id, 'family_id': family_id, 'amount': round(amount, 2), 'description': description, 'status': 'unpaid'}
            invoices[invoice_id] = invoice
            return send(self, 201, invoice)
        return send(self, 404, {'error': 'not found'})

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(('0.0.0.0', 8000), NeniosHandler)
    print('Nenios Child Care Management listening on http://127.0.0.1:8000')
    server.serve_forever()


if __name__ == '__main__':
    main()
