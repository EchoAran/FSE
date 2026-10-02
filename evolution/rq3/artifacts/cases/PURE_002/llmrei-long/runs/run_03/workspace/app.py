from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import html
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path('/workspace/data.json')

DEFAULT_DATA = {
    'products': [
        {
            'id': 1,
            'name': 'Starter Coffee Mug',
            'description': 'A simple mug for new stores and new customers.',
            'price': 12.5,
            'category': 'Home',
            'availability': 25,
            'image': '',
        },
        {
            'id': 2,
            'name': 'Welcome Notebook',
            'description': 'A basic notebook for everyday notes.',
            'price': 8.0,
            'category': 'Office',
            'availability': 40,
            'image': '',
        },
        {
            'id': 3,
            'name': 'Eco Water Bottle',
            'description': 'Reusable bottle for daily use.',
            'price': 15.0,
            'category': 'Outdoors',
            'availability': 15,
            'image': '',
        },
    ],
    'customers': [
        {
            'id': 1,
            'name': 'Demo Customer',
            'email': 'customer@example.com',
            'phone': '',
            'address': '1 Demo Street',
        }
    ],
    'orders': [],
    'staff': {'product_updates': 0, 'customer_updates': 0, 'orders_seen': 0},
}


def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    save_data(DEFAULT_DATA)
    return json.loads(json.dumps(DEFAULT_DATA))


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


def money(v):
    return f"${v:.2f}"


def esc(v):
    return html.escape(str(v), quote=True)


def layout(title, body, nav=''):
    return f"""<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>{esc(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f7f7fb; color: #222; }}
    header {{ background: #243447; color: white; padding: 16px; }}
    nav a {{ color: white; margin-right: 12px; text-decoration: none; }}
    main {{ padding: 18px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 14px; }}
    .card {{ background: white; border-radius: 10px; padding: 14px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }}
    .muted {{ color: #666; }}
    .success {{ background: #e6ffed; padding: 12px; border: 1px solid #9ae6b4; border-radius: 8px; }}
    input, select, textarea {{ width: 100%; padding: 8px; margin: 6px 0 10px; box-sizing: border-box; }}
    button {{ padding: 8px 12px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
  </style>
</head>
<body>
<header>
  <div><strong>GAMMA-J Web Store</strong></div>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
</body>
</html>"""


def get_cart(handler):
    cookie = handler.headers.get('Cookie', '')
    cart = {}
    for part in cookie.split(';'):
        if part.strip().startswith('cart='):
            value = part.strip()[5:]
            try:
                cart = json.loads(value)
            except Exception:
                cart = {}
    return cart


def set_cart(handler, cart):
    handler.send_header('Set-Cookie', f"cart={json.dumps(cart)}; Path=/")


def find_customer(data):
    return data['customers'][0]


def render_products(data, query):
    name = query.get('name', [''])[0].lower()
    category = query.get('category', [''])[0]
    min_price = query.get('min_price', [''])[0]
    max_price = query.get('max_price', [''])[0]
    items = []
    for p in data['products']:
        if name and name not in p['name'].lower():
            continue
        if category and category != p['category']:
            continue
        if min_price:
            try:
                if p['price'] < float(min_price):
                    continue
            except ValueError:
                pass
        if max_price:
            try:
                if p['price'] > float(max_price):
                    continue
            except ValueError:
                pass
        img = f"<img src='{esc(p['image'])}' alt='' style='max-width:100%;max-height:150px;'>" if p['image'] else ''
        items.append(f"<div class='card'><h3>{esc(p['name'])}</h3>{img}<p>{esc(p['description'])}</p><p>Price: {money(p['price'])}</p><p>Category: {esc(p['category'])}</p><p>Availability: {p['availability']}</p><form method='post' action='/cart/add'><input type='hidden' name='product_id' value='{p['id']}'><button>Add to cart</button></form></div>")
    return items


class App(BaseHTTPRequestHandler):
    def do_GET(self):
        data = load_data()
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        nav = "<a href='/'>Products</a><a href='/cart'>Cart</a><a href='/checkout'>Checkout</a><a href='/orders'>Order History</a><a href='/account'>My Account</a><a href='/staff'>Staff</a>"
        if parsed.path == '/' or parsed.path == '/products':
            cats = sorted({p['category'] for p in data['products']})
            filters = f"""<form method='get'>
              <input name='name' placeholder='Search by name' value='{esc(query.get('name', [''])[0])}'>
              <select name='category'><option value=''>All categories</option>{''.join(f"<option value='{esc(c)}' {'selected' if query.get('category', [''])[0]==c else ''}>{esc(c)}</option>" for c in cats)}</select>
              <input name='min_price' placeholder='Min price' value='{esc(query.get('min_price', [''])[0])}'>
              <input name='max_price' placeholder='Max price' value='{esc(query.get('max_price', [''])[0])}'>
              <button>Filter</button>
            </form>"""
            body = f"<h1>Products</h1>{filters}<div class='grid'>{''.join(render_products(data, query))}</div>"
            self.respond(layout('Products', body, nav))
        elif parsed.path == '/cart':
            cart = get_cart(self)
            rows = []
            total = 0.0
            for pid_s, qty in cart.items():
                product = next((p for p in data['products'] if p['id'] == int(pid_s)), None)
                if not product:
                    continue
                subtotal = product['price'] * qty
                total += subtotal
                rows.append(f"<tr><td>{esc(product['name'])}</td><td>{money(product['price'])}</td><td><form method='post' action='/cart/update'><input type='hidden' name='product_id' value='{product['id']}'><input name='qty' type='number' min='0' value='{qty}'><button>Update</button></form></td><td>{money(subtotal)}</td><td><form method='post' action='/cart/remove'><input type='hidden' name='product_id' value='{product['id']}'><button>Remove</button></form></td></tr>")
            body = f"<h1>Shopping Cart</h1><table><tr><th>Product</th><th>Price</th><th>Quantity</th><th>Subtotal</th><th></th></tr>{''.join(rows) or '<tr><td colspan=5>No items in cart.</td></tr>'}</table><p><strong>Cart total: {money(total)}</strong></p>"
            self.respond(layout('Cart', body, nav))
        elif parsed.path == '/checkout':
            cart = get_cart(self)
            total = sum((next((p['price'] for p in data['products'] if p['id'] == int(pid)), 0) * qty) for pid, qty in cart.items())
            body = f"""<h1>Checkout</h1><p>Cart total before checkout: <strong>{money(total)}</strong></p>
            <form method='post' action='/checkout'>
              <label>Name*</label><input name='name' required>
              <label>Email*</label><input name='email' type='email' required>
              <label>Phone</label><input name='phone'>
              <label>Delivery address*</label><textarea name='address' required></textarea>
              <button type='submit'>Submit order</button>
            </form>"""
            self.respond(layout('Checkout', body, nav))
        elif parsed.path == '/orders':
            customer = find_customer(data)
            orders = [o for o in data['orders'] if o['customer_email'] == customer['email']]
            rows = ''.join(f"<tr><td>{esc(o['id'])}</td><td>{esc(o['created_at'])}</td><td>{money(o['total'])}</td><td>{esc(o['status'])}</td></tr>" for o in orders)
            self.respond(layout('Orders', f"<h1>Order History</h1><table><tr><th>ID</th><th>Date</th><th>Total</th><th>Status</th></tr>{rows or '<tr><td colspan=4>No orders yet.</td></tr>'}</table>", nav))
        elif parsed.path == '/account':
            customer = find_customer(data)
            body = f"""<h1>My Account</h1>
            <form method='post' action='/account'>
              <label>Name</label><input name='name' value='{esc(customer['name'])}' required>
              <label>Email</label><input name='email' type='email' value='{esc(customer['email'])}' required>
              <label>Phone</label><input name='phone' value='{esc(customer['phone'])}'>
              <label>Address</label><textarea name='address' required>{esc(customer['address'])}</textarea>
              <button>Update details</button>
            </form>"""
            self.respond(layout('Account', body, nav))
        elif parsed.path == '/staff':
            body = f"""<h1>Staff Area</h1>
            <p>New orders placed: {len(data['orders'])}</p>
            <p>Product updates: {data['staff']['product_updates']}</p>
            <p>Customer updates: {data['staff']['customer_updates']}</p>
            <p>Orders seen: {data['staff']['orders_seen']}</p>
            <h2>Basic Sales Report</h2>
            <p>Total orders: {len(data['orders'])}</p>
            <p>Total sales: {money(sum(o['total'] for o in data['orders']))}</p>
            <h2>Create / Update Product</h2>
            <form method='post' action='/staff/product'>
              <input name='id' placeholder='Existing ID for update (optional)'>
              <input name='name' placeholder='Name' required>
              <input name='description' placeholder='Short description' required>
              <input name='price' placeholder='Price' required>
              <input name='category' placeholder='Category' required>
              <input name='availability' placeholder='Availability' required>
              <input name='image' placeholder='Image URL'>
              <button>Save product</button>
            </form>
            <h2>Create / Update Customer</h2>
            <form method='post' action='/staff/customer'>
              <input name='id' placeholder='Existing ID for update (optional)'>
              <input name='name' placeholder='Name' required>
              <input name='email' type='email' placeholder='Email' required>
              <input name='phone' placeholder='Phone'>
              <input name='address' placeholder='Address' required>
              <button>Save customer</button>
            </form>"""
            self.respond(layout('Staff', body, nav))
        else:
            self.send_error(404)

    def do_POST(self):
        data = load_data()
        length = int(self.headers.get('Content-Length', 0))
        form = parse_qs(self.rfile.read(length).decode())
        parsed = urlparse(self.path)
        if parsed.path == '/cart/add':
            cart = get_cart(self)
            pid = form.get('product_id', [''])[0]
            cart[pid] = cart.get(pid, 0) + 1
            self.redirect('/cart', cart)
        elif parsed.path == '/cart/update':
            cart = get_cart(self)
            pid = form.get('product_id', [''])[0]
            qty = max(0, int(form.get('qty', ['0'])[0]))
            if qty == 0:
                cart.pop(pid, None)
            else:
                cart[pid] = qty
            self.redirect('/cart', cart)
        elif parsed.path == '/cart/remove':
            cart = get_cart(self)
            cart.pop(form.get('product_id', [''])[0], None)
            self.redirect('/cart', cart)
        elif parsed.path == '/checkout':
            cart = get_cart(self)
            if not cart:
                self.respond(layout('Checkout', '<h1>Checkout</h1><p>Your cart is empty.</p>', "<a href='/'>Products</a>"))
                return
            customer = find_customer(data)
            name = form.get('name', [''])[0].strip()
            email = form.get('email', [''])[0].strip()
            address = form.get('address', [''])[0].strip()
            if not (name and email and address):
                self.respond(layout('Checkout', '<p>Missing required checkout details.</p>'))
                return
            items = []
            total = 0.0
            for pid_s, qty in cart.items():
                product = next((p for p in data['products'] if p['id'] == int(pid_s)), None)
                if product:
                    items.append({'product_id': product['id'], 'name': product['name'], 'qty': qty, 'price': product['price']})
                    total += product['price'] * qty
            order = {'id': len(data['orders']) + 1, 'customer_email': email, 'customer_name': name, 'address': address, 'phone': form.get('phone', [''])[0].strip(), 'items': items, 'total': total, 'status': 'Confirmed', 'created_at': datetime.utcnow().isoformat(timespec='seconds') + 'Z'}
            data['orders'].append(order)
            data['staff']['orders_seen'] += 1
            customer.update({'name': name, 'email': email, 'address': address, 'phone': form.get('phone', [''])[0].strip()})
            save_data(data)
            self.respond(layout('Order Confirmed', f"<div class='success'><h1>Order confirmed</h1><p>Your purchase was successful.</p><p>Order ID: {order['id']}</p><p>Total: {money(total)}</p></div><p><a href='/orders'>View order history</a></p>", "<a href='/'>Products</a><a href='/orders'>Order History</a>"), cart_clear=True)
        elif parsed.path == '/account':
            customer = find_customer(data)
            customer.update({'name': form.get('name', [''])[0].strip(), 'email': form.get('email', [''])[0].strip(), 'phone': form.get('phone', [''])[0].strip(), 'address': form.get('address', [''])[0].strip()})
            data['staff']['customer_updates'] += 1
            save_data(data)
            self.respond(layout('Account Updated', "<div class='success'><h1>Account updated</h1></div>", "<a href='/account'>Back</a>"))
        elif parsed.path == '/staff/product':
            pid = form.get('id', [''])[0].strip()
            new = {'name': form.get('name', [''])[0].strip(), 'description': form.get('description', [''])[0].strip(), 'price': float(form.get('price', ['0'])[0]), 'category': form.get('category', [''])[0].strip(), 'availability': int(form.get('availability', ['0'])[0]), 'image': form.get('image', [''])[0].strip()}
            if pid:
                for p in data['products']:
                    if p['id'] == int(pid):
                        p.update(new)
                        break
                else:
                    new['id'] = int(pid)
                    data['products'].append(new)
            else:
                new['id'] = max([p['id'] for p in data['products']] + [0]) + 1
                data['products'].append(new)
            data['staff']['product_updates'] += 1
            save_data(data)
            self.respond(layout('Product Saved', "<div class='success'><h1>Product saved</h1></div>", "<a href='/staff'>Back to staff</a>"))
        elif parsed.path == '/staff/customer':
            cid = form.get('id', [''])[0].strip()
            new = {'name': form.get('name', [''])[0].strip(), 'email': form.get('email', [''])[0].strip(), 'phone': form.get('phone', [''])[0].strip(), 'address': form.get('address', [''])[0].strip()}
            if cid:
                for c in data['customers']:
                    if c['id'] == int(cid):
                        c.update(new)
                        break
                else:
                    new['id'] = int(cid)
                    data['customers'].append(new)
            else:
                new['id'] = max([c['id'] for c in data['customers']] + [0]) + 1
                data['customers'].append(new)
            data['staff']['customer_updates'] += 1
            save_data(data)
            self.respond(layout('Customer Saved', "<div class='success'><h1>Customer saved</h1></div>", "<a href='/staff'>Back to staff</a>"))
        else:
            self.send_error(404)

    def respond(self, body, cart_clear=False):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        if cart_clear:
            self.send_header('Set-Cookie', 'cart={}; Path=/')
        self.end_headers()
        self.wfile.write(body.encode())

    def redirect(self, location, cart=None):
        self.send_response(302)
        self.send_header('Location', location)
        if cart is not None:
            self.send_header('Set-Cookie', f"cart={json.dumps(cart)}; Path=/")
        self.end_headers()


if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', 8000), App)
    print('Serving on http://127.0.0.1:8000')
    server.serve_forever()
