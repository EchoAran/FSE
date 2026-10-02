from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import csv
import io
import os

STATE = {
    'store': {'name': 'GAMMA-J Demo Store', 'currency': 'USD', 'setup_complete': False},
    'categories': ['General'],
    'products': [
        {'id': 1, 'name': 'Demo Tea', 'sku': 'TEA-001', 'barcode': '1001', 'category': 'General', 'price': 9.99, 'stock': 10, 'available': True, 'description': 'A simple starter product.', 'brand': 'Gamma', 'unit': 'box', 'variation': 'Standard'},
        {'id': 2, 'name': 'Demo Mug', 'sku': 'MUG-001', 'barcode': '1002', 'category': 'General', 'price': 12.5, 'stock': 5, 'available': True, 'description': 'A plain mug.', 'brand': 'Gamma', 'unit': 'each', 'variation': 'Large'},
    ],
    'customers': [{'id': 1, 'name': 'Alex Customer', 'email': 'alex@example.com', 'address': '1 Main St', 'consent': True}],
    'cart': [],
    'orders': [],
    'logs': [],
    'notifications': [],
    'issues': [],
    'imports': [],
    'manual_actions': [],
}

def now(): return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
def add_log(entity, action, who='system', reason=''): STATE['logs'].append({'time': now(), 'entity': entity, 'action': action, 'who': who, 'reason': reason})
def notify(kind, message, severity='info'): STATE['notifications'].append({'time': now(), 'kind': kind, 'message': message, 'severity': severity})
def issue(title, detail, priority='medium'): STATE['issues'].append({'time': now(), 'title': title, 'detail': detail, 'priority': priority, 'resolved': False})
def find_product(pid): return next((p for p in STATE['products'] if p['id'] == pid), None)
def next_id(items): return max([i['id'] for i in items], default=0) + 1

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))

def page(title, body):
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>{esc(title)}</title>
    <style>
    body {{ font-family: Arial,sans-serif; margin:20px; line-height:1.4; }} nav a {{ margin-right:12px; }}
    .card {{ border:1px solid #ccc; padding:12px; margin:12px 0; border-radius:8px; }}
    .small {{ color:#666; font-size:0.92em; }} table {{ border-collapse:collapse; width:100%; }}
    td,th {{ border:1px solid #ddd; padding:8px; vertical-align:top; }} .bad {{ background:#ffe0e0; }} .ok {{ background:#e8ffe8; }}
    input,textarea {{ width:100%; padding:8px; margin:4px 0 10px; box-sizing:border-box; }} .btn {{ display:inline-block; padding:8px 12px; background:#2d6cdf; color:#fff; text-decoration:none; border:none; border-radius:6px; cursor:pointer; }}
    .secondary {{ background:#666; }} .warn {{ background:#b26a00; }} .mono {{ font-family:monospace; }}
    </style></head><body><nav><a href='/'>Home</a><a href='/setup'>Setup</a><a href='/browse'>Browse</a><a href='/cart'>Cart</a><a href='/checkout'>Checkout</a><a href='/staff'>Staff</a><a href='/import'>Import</a><a href='/logs'>Logs</a><a href='/notifications'>Notifications</a></nav>{body}</body></html>"""

def checkout_form(msg=''):
    return f"<div class='card'><p><strong>Validation happens before submission.</strong></p>{('<div class=\'bad card\'>'+esc(msg)+'</div>') if msg else ''}<form method='post'><label>Name</label><input name='name'><label>Email</label><input name='email'><label>Address</label><input name='address'><label>Payment method</label><input name='payment' placeholder='card'><label>Shipping method</label><input name='shipping' placeholder='standard'><button class='btn' type='submit'>Place order</button></form></div>"

class Handler(BaseHTTPRequestHandler):
    def send_html(self, body, code=200):
        data = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def parse_post(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode('utf-8')
        return {k: v[0] for k, v in parse_qs(raw).items()}

    def do_GET(self):
        p = urlparse(self.path)
        path = p.path
        if path == '/':
            counts = {'products': len(STATE['products']), 'customers': len(STATE['customers']), 'orders': len(STATE['orders']), 'issues': sum(1 for i in STATE['issues'] if not i['resolved'])}
            body = f"<h1>GAMMA-J Web Store</h1><div class='grid'><div class='card'><strong>Store</strong><p>{esc(STATE['store']['name'])}</p><p>Setup complete: {'Yes' if STATE['store']['setup_complete'] else 'No'}</p></div><div class='card'><strong>Summary</strong><p>Products: {counts['products']}</p><p>Customers: {counts['customers']}</p><p>Orders: {counts['orders']}</p><p>Unresolved issues: {counts['issues']}</p></div></div><div class='card'><strong>Plain-language tips</strong><p>Use Setup to add store details. Use Import for CSV product uploads. Use Staff to manage products and orders.</p></div>"
            return self.send_html(page('Home', body))
        if path == '/setup':
            body = f"<h1>Guided setup</h1><div class='card'><p><strong>Step 1:</strong> Enter basic store information.</p><p><strong>Step 2:</strong> Add categories, products, and customer account settings.</p><p><strong>Step 3:</strong> Review clear examples and prompts before you begin selling.</p><form method='post'><label>Store name</label><input name='name' value='{esc(STATE['store']['name'])}'><label>Currency</label><input name='currency' value='{esc(STATE['store']['currency'])}'><label>Categories separated by commas</label><input name='categories' placeholder='Shoes, Accessories'><button class='btn' type='submit'>Save setup</button></form></div>"
            return self.send_html(page('Setup', body))
        if path == '/browse':
            rows = ''.join(f"<tr><td>{esc(p['name'])}</td><td>{esc(p['category'])}</td><td>{p['price']}</td><td>{p['stock']}</td><td><a class='btn' href='/cart/add/{p['id']}'>Add to cart</a></td></tr>" for p in STATE['products'])
            return self.send_html(page('Browse', f"<h1>Browse products</h1><table><tr><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th></th></tr>{rows}</table>"))
        if path == '/cart':
            total = 0; rows = ''
            for item in STATE['cart']:
                p = find_product(item['product_id'])
                subtotal = item['qty'] * p['price']; total += subtotal
                rows += f"<tr><td>{esc(p['name'])}</td><td>{item['qty']}</td><td>{subtotal:.2f}</td><td><a class='btn secondary' href='/cart/remove/{p['id']}'>Remove</a></td></tr>"
            return self.send_html(page('Cart', f"<h1>Shopping cart</h1><table><tr><th>Product</th><th>Qty</th><th>Subtotal</th><th></th></tr>{rows}</table><p><strong>Total:</strong> {total:.2f}</p>"))
        if path == '/checkout': return self.send_html(page('Checkout', "<h1>Checkout</h1>" + checkout_form()))
        if path == '/staff':
            issues = ''.join(f"<li>{esc(i['priority'])} - {esc(i['title'])}: {esc(i['detail'])}</li>" for i in [x for x in STATE['issues'] if not x['resolved']]) or '<li>No unresolved issues.</li>'
            products = ''.join(f"<tr><td>{p['id']}</td><td>{esc(p['name'])}</td><td>{p['available']}</td><td>{p['stock']}</td><td><a class='btn secondary' href='/staff/toggle/{p['id']}'>Toggle availability</a></td></tr>" for p in STATE['products'])
            orders = ''.join(f"<tr><td>{o['id']}</td><td>{esc(o['customer'])}</td><td>{o['payment_status']}</td><td>{o['shipping_status']}</td><td><a class='btn' href='/staff/pay/{o['id']}'>Retry payment</a> <a class='btn warn' href='/staff/ship/{o['id']}'>Retry shipping</a></td></tr>" for o in STATE['orders'])
            return self.send_html(page('Staff', f"<h1>Staff dashboard</h1><p>Payment failures are highest priority.</p><div class='card'><strong>Unresolved issues</strong><ul>{issues}</ul></div><table><tr><th>ID</th><th>Product</th><th>Available</th><th>Stock</th><th></th></tr>{products}</table><h2>Orders</h2><table><tr><th>ID</th><th>Customer</th><th>Payment</th><th>Shipping</th><th></th></tr>{orders}</table>"))
        if path == '/import': return self.send_html(page('Import', "<h1>Product import</h1><div class='card'><p>Paste CSV data below.</p><p class='small'>Required columns: name, sku, barcode, category, price, stock.</p><form method='post'><textarea name='csvdata' rows='12'></textarea><button class='btn' type='submit'>Import CSV</button></form></div>"))
        if path == '/logs':
            items = ''.join(f"<li><span class='mono'>{esc(l['time'])}</span> | {esc(l['entity'])} | {esc(l['action'])} | {esc(l['who'])} {('(' + esc(l['reason']) + ')') if l['reason'] else ''}</li>" for l in reversed(STATE['logs'])) or '<li>No logs yet.</li>'
            return self.send_html(page('Logs', f"<h1>Change log</h1><ul>{items}</ul>"))
        if path == '/notifications':
            items = ''.join(f"<li><strong>{esc(n['severity'])}</strong> [{esc(n['kind'])}] {esc(n['message'])} - {esc(n['time'])}</li>" for n in reversed(STATE['notifications'])) or '<li>No notifications yet.</li>'
            return self.send_html(page('Notifications', f"<h1>Notifications</h1><ul>{items}</ul>"))
        if path.startswith('/cart/add/'):
            pid = int(path.rsplit('/', 1)[-1]); found = next((x for x in STATE['cart'] if x['product_id'] == pid), None)
            (found.update({'qty': found['qty'] + 1}) if found else STATE['cart'].append({'product_id': pid, 'qty': 1})); add_log('cart', f'add product {pid}'); return self.redirect('/cart')
        if path.startswith('/cart/remove/'):
            pid = int(path.rsplit('/', 1)[-1]); STATE['cart'] = [x for x in STATE['cart'] if x['product_id'] != pid]; add_log('cart', f'remove product {pid}'); return self.redirect('/cart')
        if path.startswith('/staff/toggle/'):
            pid = int(path.rsplit('/', 1)[-1]); p = find_product(pid)
            if p: p['available'] = not p['available']; add_log('product', f'toggle availability {pid}', who='staff'); notify('stock', f'Product {p["name"]} availability changed.', 'info')
            return self.redirect('/staff')
        if path.startswith('/staff/pay/'):
            oid = int(path.rsplit('/', 1)[-1]); o = next((x for x in STATE['orders'] if x['id'] == oid), None)
            if o: o['payment_status'] = 'paid'; add_log('order', f'payment resolved {oid}', who='staff', reason='manual retry'); STATE['manual_actions'].append({'time': now(), 'staff': 'staff', 'reason': 'manual retry', 'original_error': 'payment failure', 'action': 'payment retry', 'order_id': oid})
            return self.redirect('/staff')
        if path.startswith('/staff/ship/'):
            oid = int(path.rsplit('/', 1)[-1]); o = next((x for x in STATE['orders'] if x['id'] == oid), None)
            if o: o['shipping_status'] = 'shipped'; add_log('order', f'shipping resolved {oid}', who='staff', reason='manual retry')
            return self.redirect('/staff')
        self.send_html(page('Not found', '<h1>Not found</h1>'), 404)

    def do_POST(self):
        path = urlparse(self.path).path
        data = self.parse_post()
        if path == '/setup':
            name = data.get('name', '').strip(); currency = data.get('currency', 'USD').strip().upper(); cats = [c.strip() for c in data.get('categories', '').split(',') if c.strip()]
            if name:
                STATE['store'].update({'name': name, 'currency': currency, 'setup_complete': True})
                if cats: STATE['categories'] = sorted(set(STATE['categories'] + cats))
                add_log('store', 'setup updated'); notify('setup', 'Store setup saved.', 'info'); return self.redirect('/')
            return self.send_html(page('Setup', '<p>Please enter a store name.</p>'))
        if path == '/checkout':
            errors = []
            name = data.get('name', '').strip(); email = data.get('email', '').strip(); address = data.get('address', '').strip(); payment = data.get('payment', '').strip(); shipping = data.get('shipping', '').strip()
            if not name: errors.append('Customer name is required.')
            if not email or '@' not in email: errors.append('Please enter a valid email address.')
            if not address: errors.append('Shipping address is required.')
            if payment.lower() not in ['card', 'paypal', 'gateway']: errors.append('Payment details look incomplete or invalid.')
            if not shipping: errors.append('Shipping method is required.')
            if errors: return self.send_html(page('Checkout', '<h1>Checkout</h1>' + checkout_form('<br>'.join(errors))))
            if not STATE['cart']: return self.send_html(page('Checkout', '<h1>Checkout</h1><p>Your cart is empty.</p>'))
            order = {'id': next_id(STATE['orders']), 'customer': name, 'email': email, 'address': address, 'payment_status': 'unpaid', 'shipping_status': 'pending', 'items': list(STATE['cart']), 'created': now()}
            STATE['orders'].append(order); STATE['cart'] = []; issue('Payment failure possible', f'Order {order["id"]} awaiting payment confirmation', 'high'); notify('order', f'Order {order["id"]} placed. Payment may need attention.', 'warning'); add_log('order', f'create order {order["id"]}', who=name)
            return self.send_html(page('Checkout', f"<h1>Order placed</h1><p>Order #{order['id']} saved. Payment status: unpaid for staff visibility.</p>"))
        if path == '/import':
            reader = csv.DictReader(io.StringIO(data.get('csvdata', '').strip()))
            imported = skipped = issues_count = 0
            for row in reader:
                name = (row.get('name') or '').strip(); sku = (row.get('sku') or '').strip(); barcode = (row.get('barcode') or '').strip(); price = row.get('price', '').strip(); category = (row.get('category') or 'General').strip() or 'General'
                duplicate = any((sku and p['sku'] == sku) or (barcode and p['barcode'] == barcode) or (name and p['name'].lower() == name.lower()) for p in STATE['products'])
                issue_text = []
                if not name: issue_text.append('Missing product name')
                if not price or not str(price).replace('.', '', 1).isdigit(): issue_text.append('Missing or invalid price')
                if duplicate: issue_text.append('Possible duplicate')
                if issue_text: issues_count += 1; skipped += 1
                else:
                    STATE['products'].append({'id': next_id(STATE['products']), 'name': name, 'sku': sku or f'SKU-{next_id(STATE["products"])}', 'barcode': barcode or '', 'category': category, 'price': float(price), 'stock': int(row.get('stock', 0) or 0), 'available': True, 'description': row.get('description', ''), 'brand': row.get('brand', ''), 'unit': row.get('unit', ''), 'variation': row.get('variation', '')}); imported += 1
            STATE['imports'].append({'time': now(), 'imported': imported, 'skipped': skipped, 'issues': issues_count})
            return self.send_html(page('Import', f"<div class='card ok'><strong>Import complete</strong><p>Succeeded: {imported}</p><p>Skipped: {skipped}</p><p>Needs attention: {issues_count}</p></div><h1>Product import</h1><div class='card'><p>Paste CSV data below.</p><form method='post'><textarea name='csvdata' rows='12'></textarea><button class='btn' type='submit'>Import CSV</button></form></div>"))
        self.send_html(page('Not found', '<h1>Not found</h1>'), 404)

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', int(os.environ.get('PORT', '8000'))), Handler).serve_forever()
