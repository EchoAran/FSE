from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from http.cookies import SimpleCookie
import json

STATE = {
    'products': {1: {'id': 1, 'name': 'Sample Product', 'price': 19.99, 'stock': 10, 'active': True}},
    'customers': {},
    'orders': {},
    'next_customer_id': 1,
    'next_order_id': 1,
}


def html(body):
    return ('<!doctype html><html><body>' + body + '</body></html>').encode()


def parse_cookies(environ):
    cookie = SimpleCookie(environ.get('HTTP_COOKIE', ''))
    return {k: v.value for k, v in cookie.items()}


def app(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ.get('PATH_INFO', '/')
    cookies = parse_cookies(environ)
    session = json.loads(cookies.get('session', '{}') or '{}')
    length = int(environ.get('CONTENT_LENGTH') or 0)
    body = environ['wsgi.input'].read(length).decode() if length else ''
    form = {k: v[0] for k, v in parse_qs(body).items()}

    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    def set_session_cookie():
        headers.append(('Set-Cookie', f"session={json.dumps(session)}; Path=/"))

    if path == '/' and method == 'GET':
        items = ''.join(f"<li>{p['name']} - ${p['price']:.2f} - stock {p['stock']}</li>" for p in STATE['products'].values())
        out = html(f'<h1>GAMMA-J Web Store</h1><ul>{items}</ul><a href="/cart">Cart</a>')
    elif path == '/register' and method == 'POST':
        name = form.get('name', '').strip()
        email = form.get('email', '').strip().lower()
        if not name or not email or '@' not in email:
            status = '400 Bad Request'
            out = b'Invalid customer details'
        elif any(c['email'] == email for c in STATE['customers'].values()):
            status = '400 Bad Request'
            out = b'Duplicate customer'
        else:
            cid = STATE['next_customer_id']; STATE['next_customer_id'] += 1
            STATE['customers'][cid] = {'id': cid, 'name': name, 'email': email}
            session['customer_id'] = cid
            set_session_cookie()
            status = '303 See Other'
            headers.append(('Location', '/'))
            out = b''
    elif path == '/cart/add/1' and method == 'POST':
        product = STATE['products'][1]
        cart = session.get('cart', [])
        if product['stock'] < 1:
            status = '400 Bad Request'
            out = b'Not enough stock'
        else:
            if cart and cart[0]['product_id'] == 1:
                if cart[0]['quantity'] + 1 > product['stock']:
                    status = '400 Bad Request'
                    out = b'Not enough stock'
                else:
                    cart[0]['quantity'] += 1
            else:
                cart = [{'product_id': 1, 'quantity': 1}]
            session['cart'] = cart
            set_session_cookie()
            status = '303 See Other'
            headers.append(('Location', '/cart'))
            out = b''
    elif path == '/cart' and method == 'GET':
        cart = session.get('cart', [])
        items = ''.join(f"<li>{STATE['products'][i['product_id']]['name']} x {i['quantity']}</li>" for i in cart)
        out = html(f'<h1>Cart</h1><ul>{items}</ul><form method="post" action="/checkout"><button>Checkout</button></form>')
    elif path == '/checkout' and method == 'POST':
        cid = session.get('customer_id')
        cart = session.get('cart', [])
        if not cid:
            status = '400 Bad Request'
            out = b'Customer login required'
        elif not cart:
            status = '400 Bad Request'
            out = b'Cart is empty'
        else:
            for item in cart:
                product = STATE['products'].get(item['product_id'])
                if not product or not product['active'] or product['stock'] < item['quantity']:
                    status = '400 Bad Request'
                    out = b'Cart cannot be confirmed'
                    break
            else:
                for item in cart:
                    STATE['products'][item['product_id']]['stock'] -= item['quantity']
                oid = STATE['next_order_id']; STATE['next_order_id'] += 1
                STATE['orders'][oid] = {'id': oid, 'customer_id': cid, 'items': cart, 'status': 'new'}
                session['cart'] = []
                set_session_cookie()
                out = html(f'<h1>Order {oid}</h1><p>Status: new</p>')
    elif path == '/admin' and method == 'GET':
        out = html(f"<h1>Admin</h1><p>Products: {len(STATE['products'])}</p><p>Customers: {len(STATE['customers'])}</p><p>Orders: {len(STATE['orders'])}</p>")
    else:
        status = '404 Not Found'
        out = b'Not Found'

    start_response(status, headers)
    return [out]


if __name__ == '__main__':
    print('Serving on http://127.0.0.1:8000')
    make_server('0.0.0.0', 8000, app).serve_forever()
