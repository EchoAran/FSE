from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from dataclasses import dataclass, asdict, field
from typing import List, Optional
from datetime import datetime, timezone
import json
import itertools
import os

PRODUCTS = {}
ORDERS = {}
AUDIT_LOG = []
COUNTERS = {'product': itertools.count(1), 'order': itertools.count(1001)}

@dataclass
class Product:
    id: int
    name: str
    description: str
    price: Optional[float]
    quantity: int
    category: str = 'General'
    active: bool = True
    stock_control: bool = True
    min_qty: int = 1
    max_qty: int = 10
    images: List[str] = field(default_factory=list)

    def purchasable(self):
        if not self.active:
            return False, 'Product is inactive.'
        if self.price is None or self.price <= 0:
            return False, 'Product price is missing or invalid.'
        if self.stock_control and self.quantity <= 0:
            return False, 'Product is out of stock.'
        return True, ''

@dataclass
class Order:
    id: int
    items: List[dict]
    total: float
    status: str = 'pending'
    payment_status: str = 'unpaid'
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def now():
    return datetime.now(timezone.utc).isoformat()


def log_action(actor, action, before=None, after=None):
    AUDIT_LOG.append({'who': actor, 'what': action, 'when': now(), 'before': before, 'after': after})


def json_response(handler, code, payload):
    data = json.dumps(payload).encode()
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def html_response(handler, code, body):
    data = body.encode()
    handler.send_response(code)
    handler.send_header('Content-Type', 'text/html; charset=utf-8')
    handler.send_header('Content-Length', str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def redirect(handler, location):
    handler.send_response(303)
    handler.send_header('Location', location)
    handler.end_headers()


def parse_body(handler):
    length = int(handler.headers.get('Content-Length', '0'))
    body = handler.rfile.read(length).decode() if length else ''
    ctype = handler.headers.get('Content-Type', '')
    if 'application/json' in ctype:
        return json.loads(body or '{}')
    return {k: v[0] for k, v in parse_qs(body).items()}


def cart_items(cart):
    items = []
    for pid_str, qty in cart.items():
        p = PRODUCTS.get(int(pid_str))
        if p:
            items.append((p, qty))
    return items


def cart_validation(cart):
    issues = []
    for product, qty in cart_items(cart):
        ok, msg = product.purchasable()
        if not ok:
            issues.append(f'{product.name}: {msg}')
        if qty < product.min_qty or qty > product.max_qty:
            issues.append(f'{product.name}: quantity must be between {product.min_qty} and {product.max_qty}.')
        if product.stock_control and qty > product.quantity:
            issues.append(f'{product.name}: insufficient stock.')
    return issues


class Handler(BaseHTTPRequestHandler):
    server_version = 'GAMMAJ/1.0'

    def _cart(self):
        if not hasattr(self.server, 'cart'):
            self.server.cart = {}
        return self.server.cart

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/health':
            return json_response(self, 200, {'ok': True})
        if path == '/':
            return html_response(self, 200, '<h1>GAMMA-J Web Store</h1><p><a href="/store">Storefront</a> | <a href="/cart">Cart</a> | <a href="/admin">Admin</a> | <a href="/orders">Orders</a></p>')
        if path == '/store':
            parts = ['<h2>Storefront</h2>']
            for p in PRODUCTS.values():
                ok, msg = p.purchasable()
                parts.append(f'<div><strong>{p.name}</strong> - ${p.price or 0:.2f}<div>{p.description}</div><div>Category: {p.category} | Stock: {p.quantity}</div>')
                if ok:
                    parts.append(f'<form method="post" action="/cart/add/{p.id}"><button>Add to cart</button></form>')
                else:
                    parts.append(f'<p>Unavailable: {msg}</p>')
                parts.append('</div><hr>')
            return html_response(self, 200, ''.join(parts))
        if path == '/cart':
            cart = self._cart()
            lines = [f'{p.name} x {qty} = ${p.price * qty:.2f}' for p, qty in cart_items(cart)]
            return json_response(self, 200, {'cart': lines, 'issues': cart_validation(cart)})
        if path == '/admin':
            return json_response(self, 200, {'products': [asdict(p) for p in PRODUCTS.values()], 'orders': [asdict(o) for o in ORDERS.values()], 'audit_log': AUDIT_LOG})
        if path == '/orders':
            return json_response(self, 200, [asdict(o) for o in ORDERS.values()])
        if path.startswith('/orders/'):
            oid = int(path.split('/')[-1])
            order = ORDERS.get(oid)
            if not order:
                return json_response(self, 404, {'error': 'Not found'})
            return json_response(self, 200, asdict(order))
        return json_response(self, 404, {'error': 'Not found'})

    def do_POST(self):
        path = urlparse(self.path).path
        if path.startswith('/cart/add/'):
            pid = int(path.split('/')[-1])
            product = PRODUCTS.get(pid)
            if not product:
                return json_response(self, 404, {'error': 'Product not found'})
            ok, msg = product.purchasable()
            if not ok:
                return json_response(self, 400, {'error': msg})
            data = parse_body(self)
            qty = int(data.get('qty', 1) or 1)
            cart = self._cart()
            new_qty = cart.get(str(pid), 0) + qty
            if new_qty > product.max_qty:
                return json_response(self, 400, {'error': f'{product.name}: quantity exceeds maximum of {product.max_qty}'})
            cart[str(pid)] = new_qty
            return redirect(self, '/cart')
        if path == '/admin/products':
            data = parse_body(self)
            try:
                price = data.get('price')
                price = None if price in (None, '', 'null') else float(price)
                quantity = int(data.get('quantity', 0))
                product = Product(id=next(COUNTERS['product']), name=data['name'], description=data.get('description', ''), price=price, quantity=quantity, category=data.get('category', 'General'), active=str(data.get('active', 'true')).lower() != 'false', stock_control=str(data.get('stock_control', 'true')).lower() != 'false')
            except Exception as e:
                return json_response(self, 400, {'error': f'Invalid product data: {e}'})
            PRODUCTS[product.id] = product
            log_action('staff', 'add_product', None, asdict(product))
            return json_response(self, 201, asdict(product))
        if path == '/checkout':
            cart = self._cart()
            issues = cart_validation(cart)
            if issues:
                return json_response(self, 400, {'error': 'Cart has issues', 'issues': issues})
            items = []
            total = 0.0
            for product, qty in cart_items(cart):
                items.append({'product_id': product.id, 'name': product.name, 'qty': qty, 'price': product.price})
                total += product.price * qty
            order = Order(id=next(COUNTERS['order']), items=items, total=total, payment_status='paid', status='confirmed')
            ORDERS[order.id] = order
            for product, qty in cart_items(cart):
                if product.stock_control:
                    product.quantity -= qty
            self.server.cart = {}
            return json_response(self, 200, {'order_number': order.id, 'items': items, 'total': total, 'payment_status': order.payment_status, 'status': order.status})
        return json_response(self, 404, {'error': 'Not found'})

    def log_message(self, format, *args):
        return


def main():
    port = int(os.environ.get('PORT', '8000'))
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'GAMMA-J Web Store listening on http://127.0.0.1:{port}')
    server.serve_forever()


if __name__ == '__main__':
    main()
