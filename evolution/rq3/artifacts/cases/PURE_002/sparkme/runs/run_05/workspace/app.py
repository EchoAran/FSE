from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import csv
import io
from datetime import datetime, timezone

STORE = {
    'info': {},
    'products': [],
    'customers': [],
    'orders': [],
    'logs': [],
    'notifications': [],
    'issues': [],
}


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def add_log(entity, action, detail):
    STORE['logs'].append({'time': now(), 'entity': entity, 'action': action, 'detail': detail})


def add_notification(kind, message):
    STORE['notifications'].append({'time': now(), 'kind': kind, 'message': message})


def html_escape(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))


def render_page(title, body):
    nav = '<nav>' + ' | '.join([
        '<a href="/">Home</a>', '<a href="/setup">Setup</a>', '<a href="/products">Products</a>',
        '<a href="/customers">Customers</a>', '<a href="/orders">Orders</a>', '<a href="/import">Import</a>',
        '<a href="/logs">Logs</a>', '<a href="/notifications">Notifications</a>',
    ]) + '</nav>'
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{html_escape(title)}</title></head><body>{nav}{body}</body></html>'.encode()


def list_items(items, formatter):
    return '<ul>' + ''.join(f'<li>{formatter(item)}</li>' for item in items) + '</ul>'


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, content, content_type='text/html; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def _form(self):
        length = int(self.headers.get('Content-Length', '0'))
        return parse_qs(self.rfile.read(length).decode())

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/':
            body = f"<h1>GAMMA-J Web Store</h1><p>Store: {html_escape(STORE['info'].get('name', 'Not set up yet'))}</p><p>Products: {len(STORE['products'])} | Customers: {len(STORE['customers'])} | Orders: {len(STORE['orders'])}</p>"
            self._send(200, render_page('GAMMA-J Web Store', body))
        elif path == '/setup':
            body = '<h1>Guided Setup</h1><form method="post"><label>Store name <input name="name"></label><br><label>Contact email <input name="email"></label><br><button type="submit">Save setup</button></form>'
            self._send(200, render_page('Setup', body))
        elif path == '/products':
            items = list_items(STORE['products'], lambda p: f"{html_escape(p['name'])} / {html_escape(p['sku'])} / {html_escape(p['price'])} / {html_escape(p['category'])} / {html_escape(p['availability'])}")
            body = '<h1>Products</h1><form method="post"><input name="name" placeholder="Name"><input name="sku" placeholder="SKU"><input name="price" placeholder="Price"><input name="category" placeholder="Category"><button type="submit">Save</button></form>' + items
            self._send(200, render_page('Products', body))
        elif path == '/customers':
            items = list_items(STORE['customers'], lambda c: f"{html_escape(c['name'])} / {html_escape(c['email'])}")
            body = '<h1>Customers</h1><form method="post"><input name="name" placeholder="Name"><input name="email" placeholder="Email"><button type="submit">Save</button></form>' + items
            self._send(200, render_page('Customers', body))
        elif path == '/orders':
            items = list_items(STORE['orders'], lambda o: f"{html_escape(o['customer'])} / {html_escape(o['status'])} / {html_escape(o['product'])}")
            body = '<h1>Orders</h1><form method="post"><input name="customer" placeholder="Customer"><input name="shipping" placeholder="Shipping address"><input name="payment" placeholder="Payment info (type fail to simulate failure)"><input name="product" placeholder="Product"><button type="submit">Submit order</button></form>' + items
            self._send(200, render_page('Orders', body))
        elif path == '/import':
            body = '<h1>CSV Import</h1><form method="post" enctype="application/x-www-form-urlencoded"><textarea name="csv" rows="8" cols="60"></textarea><br><button type="submit">Upload</button></form>'
            self._send(200, render_page('Import', body))
        elif path == '/logs':
            items = list_items(STORE['logs'], lambda l: f"{l['time']} - {html_escape(l['entity'])} - {html_escape(l['action'])} - {html_escape(l['detail'])}")
            self._send(200, render_page('Logs', '<h1>Change Log</h1>' + items))
        elif path == '/notifications':
            items = list_items(STORE['notifications'], lambda n: f"{n['time']} - {html_escape(n['kind'])} - {html_escape(n['message'])}")
            issues = list_items(STORE['issues'], lambda i: f"{i['priority']} - {html_escape(i['type'])} - {html_escape(i['message'])}")
            self._send(200, render_page('Notifications', '<h1>Notifications</h1>' + items + '<h2>Open issues</h2>' + issues))
        else:
            self._send(404, b'Not found', 'text/plain; charset=utf-8')

    def do_POST(self):
        path = urlparse(self.path).path
        form = self._form()
        get = lambda k: form.get(k, [''])[0].strip()
        if path == '/setup':
            name = get('name')
            if not name:
                self._send(400, b'Store name is required', 'text/plain; charset=utf-8')
                return
            STORE['info'] = {'name': name, 'email': get('email')}
            add_log('store', 'setup', name)
            self._redirect('/')
        elif path == '/products':
            name, sku, price, category = get('name'), get('sku'), get('price'), get('category')
            if not (name and sku and price):
                self._send(400, b'Name, SKU, and price are required', 'text/plain; charset=utf-8')
                return
            existing = next((p for p in STORE['products'] if p['sku'].lower() == sku.lower()), None)
            payload = {'name': name, 'sku': sku, 'price': price, 'category': category, 'availability': 'available'}
            if existing:
                existing.update(payload)
                add_log('product', 'update', sku)
            else:
                STORE['products'].append(payload)
                add_log('product', 'add', sku)
            self._redirect('/products')
        elif path == '/customers':
            name, email = get('name'), get('email')
            if not (name and email):
                self._send(400, b'Customer name and email are required', 'text/plain; charset=utf-8')
                return
            STORE['customers'].append({'name': name, 'email': email})
            add_log('customer', 'add', email)
            self._redirect('/customers')
        elif path == '/orders':
            customer, shipping, payment, product = get('customer'), get('shipping'), get('payment'), get('product')
            if not customer or not shipping or not payment:
                self._send(400, b'Customer, shipping, and payment are required', 'text/plain; charset=utf-8')
                return
            status = 'unpaid' if payment.lower() == 'fail' else 'paid'
            STORE['orders'].append({'customer': customer, 'shipping': shipping, 'payment': payment, 'product': product, 'status': status})
            if status == 'unpaid':
                STORE['issues'].append({'type': 'payment', 'priority': 1, 'message': 'Payment failed', 'order': customer})
                add_notification('payment', 'Payment failure needs attention')
            add_log('order', 'create', customer)
            self._redirect('/orders')
        elif path == '/import':
            data = get('csv')
            reader = csv.DictReader(io.StringIO(data))
            imported = skipped = 0
            for row in reader:
                if not row.get('name') or not row.get('sku'):
                    skipped += 1
                    continue
                candidate = {'name': row.get('name', '').strip(), 'sku': row.get('sku', '').strip(), 'price': row.get('price', '').strip(), 'category': row.get('category', '').strip(), 'availability': 'available'}
                existing = next((p for p in STORE['products'] if p['sku'].lower() == candidate['sku'].lower()), None)
                if existing:
                    existing.update(candidate)
                else:
                    STORE['products'].append(candidate)
                imported += 1
            add_log('import', 'csv', f'{imported} imported, {skipped} skipped')
            self._redirect('/import')
        else:
            self._send(404, b'Not found', 'text/plain; charset=utf-8')


def run(server_class=ThreadingHTTPServer, handler_class=Handler, port=8000):
    server = server_class(('0.0.0.0', port), handler_class)
    server.serve_forever()


if __name__ == '__main__':
    run()
