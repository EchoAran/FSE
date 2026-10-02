from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from http import cookies
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Any
import html
import json
import uuid

@dataclass
class Product:
    id: str
    name: str
    description: str
    price: float
    category: str
    availability: int
    image_url: str = ''

@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str
    contact_number: str = ''

@dataclass
class Order:
    id: str
    customer_name: str
    email: str
    address: str
    contact_number: str
    items: List[Dict[str, Any]]
    total: float
    created_at: str

PRODUCTS: Dict[str, Product] = {}
CUSTOMERS: Dict[str, Customer] = {}
ORDERS: List[Order] = []
SESSIONS: Dict[str, Dict[str, Any]] = {}

for p in [
    Product(str(uuid.uuid4()), 'Starter Widget', 'A beginner-friendly widget.', 19.99, 'Widgets', 10, 'https://via.placeholder.com/100'),
    Product(str(uuid.uuid4()), 'Premium Gadget', 'A premium gadget for daily use.', 49.5, 'Gadgets', 5, 'https://via.placeholder.com/100'),
    Product(str(uuid.uuid4()), 'Budget Widget', 'Affordable and simple.', 9.99, 'Widgets', 20, ''),
]:
    PRODUCTS[p.id] = p


def esc(s):
    return html.escape(str(s), quote=True)


def new_session():
    sid = str(uuid.uuid4())
    SESSIONS[sid] = {'cart': {}}
    return sid


def cart_for(sid):
    return SESSIONS.setdefault(sid, {'cart': {}})['cart']


def cart_items(sid):
    items = []
    for pid, qty in cart_for(sid).items():
        product = PRODUCTS.get(pid)
        if product:
            items.append({'product': product, 'qty': qty, 'subtotal': round(product.price * qty, 2)})
    return items


def cart_total(sid):
    return round(sum(i['subtotal'] for i in cart_items(sid)), 2)


def page(title, body):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{esc(title)}</title></head><body>{body}</body></html>'


def home():
    return page('GAMMA-J Web Store', '<h1>GAMMA-J Web Store</h1><p><a href="/products">Browse products</a> | <a href="/cart">Cart</a> | <a href="/account">My account</a> | <a href="/admin">Staff</a></p>')


def products_page(qs):
    q = qs.get('q', [''])[0].lower()
    category = qs.get('category', [''])[0].lower()
    min_price = qs.get('min_price', [''])[0]
    max_price = qs.get('max_price', [''])[0]
    items = list(PRODUCTS.values())
    if q:
        items = [p for p in items if q in p.name.lower()]
    if category:
        items = [p for p in items if category in p.category.lower()]
    if min_price:
        items = [p for p in items if p.price >= float(min_price)]
    if max_price:
        items = [p for p in items if p.price <= float(max_price)]
    out = ['<h1>Products</h1>']
    out.append('<form method="get">Search: <input name="q" value="{}"> Category: <input name="category" value="{}"> Min price: <input name="min_price" value="{}" size="6"> Max price: <input name="max_price" value="{}" size="6"> <button type="submit">Filter</button></form>'.format(esc(qs.get('q',[''])[0]), esc(qs.get('category',[''])[0]), esc(min_price), esc(max_price)))
    out.append('<p><a href="/">Home</a> | <a href="/cart">Cart</a></p><ul>')
    for p in items:
        img = f'<br><img src="{esc(p.image_url)}" alt="{esc(p.name)}" width="60">' if p.image_url else ''
        out.append(f'<li><strong>{esc(p.name)}</strong> - {esc(p.description)} - ${p.price:.2f} - {esc(p.category)} - Available: {p.availability}{img} <form method="post" action="/cart/add/{esc(p.id)}" style="display:inline"><button type="submit">Add to cart</button></form></li>')
    out.append('</ul>')
    return page('Products', ''.join(out))


def cart_page(sid):
    out = ['<h1>Shopping Cart</h1><p><a href="/products">Continue shopping</a> | <a href="/checkout">Checkout</a></p><ul>']
    for item in cart_items(sid):
        p = item['product']
        out.append(f'<li>{esc(p.name)} - ${p.price:.2f} x <form method="post" action="/cart/update/{esc(p.id)}" style="display:inline"><input name="qty" type="number" min="0" value="{item["qty"]}" style="width:70px"><button type="submit">Update</button></form> <form method="post" action="/cart/remove/{esc(p.id)}" style="display:inline"><button type="submit">Remove</button></form></li>')
    out.append(f'</ul><p><strong>Cart total:</strong> ${cart_total(sid):.2f}</p>')
    return page('Cart', ''.join(out))


def checkout_page(sid, error=''):
    body = [f'<h1>Checkout</h1><p>Cart total: ${cart_total(sid):.2f}</p>']
    if error:
        body.append(f'<p style="color:red">{esc(error)}</p>')
    body.append('<form method="post">Name: <input name="name" required><br>Email: <input name="email" type="email" required><br>Address: <input name="address" required><br>Contact number: <input name="contact_number"><br><button type="submit">Place order</button></form>')
    return page('Checkout', ''.join(body))


def account_page(customer, orders):
    body = [f'<h1>My account</h1><form method="post">Name: <input name="name" value="{esc(customer.name)}" required><br>Email: <input name="email" value="{esc(customer.email)}" type="email" required><br>Address: <input name="address" value="{esc(customer.address)}" required><br>Contact number: <input name="contact_number" value="{esc(customer.contact_number)}"><br><button type="submit">Update</button></form><h2>Order history</h2><ul>']
    for o in orders:
        body.append(f'<li>{esc(o.id)} - {esc(o.created_at)} - ${o.total:.2f}</li>')
    body.append('</ul>')
    return page('Account', ''.join(body))


def admin_page():
    body = ['<h1>Staff dashboard</h1><p><a href="/admin/products">Manage products</a> | <a href="/admin/customers">Manage customers</a> | <a href="/admin/reports">Sales report</a></p><h2>New orders</h2><ul>']
    for o in ORDERS:
        body.append(f'<li>{esc(o.id)} - {esc(o.customer_name)} - ${o.total:.2f} - {esc(o.created_at)}</li>')
    body.append('</ul>')
    return page('Admin', ''.join(body))


class Handler(BaseHTTPRequestHandler):
    def _sid(self):
        c = cookies.SimpleCookie(self.headers.get('Cookie'))
        sid = c.get('sid')
        if sid and sid.value in SESSIONS:
            return sid.value, False
        return new_session(), True

    def _send(self, code, body, content_type='text/html; charset=utf-8', set_sid=None):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        if set_sid:
            self.send_header('Set-Cookie', f'sid={set_sid}; Path=/')
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def do_GET(self):
        sid, new = self._sid()
        parsed = urlparse(self.path)
        if parsed.path == '/':
            self._send(200, home(), set_sid=sid if new else None)
        elif parsed.path == '/products':
            self._send(200, products_page(parse_qs(parsed.query)), set_sid=sid if new else None)
        elif parsed.path == '/cart':
            self._send(200, cart_page(sid), set_sid=sid if new else None)
        elif parsed.path == '/checkout':
            self._send(200, checkout_page(sid), set_sid=sid if new else None)
        elif parsed.path == '/account':
            if not CUSTOMERS:
                CUSTOMERS['default'] = Customer('default', '', '', '')
            customer = next(iter(CUSTOMERS.values()))
            orders = [o for o in ORDERS if o.email == customer.email]
            self._send(200, account_page(customer, orders), set_sid=sid if new else None)
        elif parsed.path == '/admin':
            self._send(200, admin_page(), set_sid=sid if new else None)
        elif parsed.path == '/admin/products':
            rows = ''.join(f'<li>{esc(p.id)} {esc(p.name)} ${p.price:.2f}</li>' for p in PRODUCTS.values())
            form = '<h1>Manage products</h1><form method="post">ID (optional for new): <input name="id"><br>Name: <input name="name" required><br>Description: <input name="description" required><br>Price: <input name="price" required><br>Category: <input name="category" required><br>Availability: <input name="availability" required><br>Image URL: <input name="image_url"><br><button type="submit">Save</button></form><ul>' + rows + '</ul>'
            self._send(200, page('Manage products', form), set_sid=sid if new else None)
        elif parsed.path == '/admin/customers':
            rows = ''.join(f'<li>{esc(c.id)} {esc(c.name)} {esc(c.email)}</li>' for c in CUSTOMERS.values())
            form = '<h1>Manage customers</h1><form method="post">ID (optional for new): <input name="id"><br>Name: <input name="name" required><br>Email: <input name="email" required><br>Address: <input name="address" required><br>Contact number: <input name="contact_number"><br><button type="submit">Save</button></form><ul>' + rows + '</ul>'
            self._send(200, page('Manage customers', form), set_sid=sid if new else None)
        elif parsed.path == '/admin/reports':
            total_sales = round(sum(o.total for o in ORDERS), 2)
            self._send(200, page('Sales report', f'<h1>Sales report</h1><p>Orders: {len(ORDERS)}</p><p>Total sales: ${total_sales:.2f}</p>'), set_sid=sid if new else None)
        elif parsed.path == '/orders':
            self._send(200, json.dumps({'orders': [asdict(o) for o in ORDERS]}), 'application/json')
        else:
            self._send(404, 'Not found', set_sid=sid if new else None)

    def do_POST(self):
        sid, new = self._sid()
        parsed = urlparse(self.path)
        length = int(self.headers.get('Content-Length', 0))
        data = parse_qs(self.rfile.read(length).decode())
        if parsed.path.startswith('/cart/add/'):
            pid = parsed.path.rsplit('/', 1)[-1]
            if pid in PRODUCTS:
                cart = cart_for(sid)
                cart[pid] = cart.get(pid, 0) + 1
                self._send(302, '', set_sid=sid if new else None)
                self.send_header('Location', '/cart')
                self.end_headers()
                return
        elif parsed.path.startswith('/cart/update/'):
            pid = parsed.path.rsplit('/', 1)[-1]
            qty = max(0, int(data.get('qty', ['0'])[0]))
            cart = cart_for(sid)
            if qty == 0:
                cart.pop(pid, None)
            else:
                cart[pid] = qty
            self._send(302, '', set_sid=sid if new else None)
            self.send_header('Location', '/cart')
            self.end_headers()
            return
        elif parsed.path.startswith('/cart/remove/'):
            pid = parsed.path.rsplit('/', 1)[-1]
            cart_for(sid).pop(pid, None)
            self._send(302, '', set_sid=sid if new else None)
            self.send_header('Location', '/cart')
            self.end_headers()
            return
        elif parsed.path == '/checkout':
            name = data.get('name', [''])[0].strip()
            email = data.get('email', [''])[0].strip()
            address = data.get('address', [''])[0].strip()
            contact = data.get('contact_number', [''])[0].strip()
            if not name or not email or not address:
                self._send(400, 'Missing required fields', set_sid=sid if new else None)
                return
            items = cart_items(sid)
            if not items:
                self._send(400, 'Cart is empty', set_sid=sid if new else None)
                return
            order = Order(str(uuid.uuid4()), name, email, address, contact, [{'product_id': i['product'].id, 'name': i['product'].name, 'qty': i['qty'], 'price': i['product'].price} for i in items], cart_total(sid), datetime.utcnow().isoformat())
            ORDERS.append(order)
            SESSIONS[sid]['cart'] = {}
            self._send(200, f'Order placed successfully. Confirmation: {order.id}', set_sid=sid if new else None)
            return
        elif parsed.path == '/account':
            if not CUSTOMERS:
                CUSTOMERS['default'] = Customer('default', '', '', '')
            customer = next(iter(CUSTOMERS.values()))
            customer.name = data.get('name', [''])[0].strip()
            customer.email = data.get('email', [''])[0].strip()
            customer.address = data.get('address', [''])[0].strip()
            customer.contact_number = data.get('contact_number', [''])[0].strip()
            self._send(302, '', set_sid=sid if new else None)
            self.send_header('Location', '/account')
            self.end_headers()
            return
        elif parsed.path == '/admin/products':
            pid = data.get('id', [''])[0] or str(uuid.uuid4())
            PRODUCTS[pid] = Product(pid, data.get('name', [''])[0].strip(), data.get('description', [''])[0].strip(), float(data.get('price', ['0'])[0]), data.get('category', [''])[0].strip(), int(data.get('availability', ['0'])[0]), data.get('image_url', [''])[0].strip())
            self._send(302, '', set_sid=sid if new else None)
            self.send_header('Location', '/admin/products')
            self.end_headers()
            return
        elif parsed.path == '/admin/customers':
            cid = data.get('id', [''])[0] or str(uuid.uuid4())
            CUSTOMERS[cid] = Customer(cid, data.get('name', [''])[0].strip(), data.get('email', [''])[0].strip(), data.get('address', [''])[0].strip(), data.get('contact_number', [''])[0].strip())
            self._send(302, '', set_sid=sid if new else None)
            self.send_header('Location', '/admin/customers')
            self.end_headers()
            return
        self._send(404, 'Not found', set_sid=sid if new else None)


def run():
    server = ThreadingHTTPServer(('0.0.0.0', 8000), Handler)
    server.serve_forever()

if __name__ == '__main__':
    run()
