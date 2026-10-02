from flask import Flask, request, redirect, url_for, render_template_string, session, flash, abort
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import os
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

PRODUCTS = {}
ORDERS = {}
AUDIT_LOG = []
CATEGORIES = ['Books', 'Electronics', 'Home']


def audit(action, before=None, after=None, user='system'):
    AUDIT_LOG.append({
        'id': str(uuid.uuid4()),
        'who': user,
        'what': action,
        'when': datetime.now(timezone.utc).isoformat(),
        'before': before,
        'after': after,
    })


def seed_data():
    if PRODUCTS:
        return
    PRODUCTS['p1'] = {
        'id': 'p1',
        'name': 'Starter Book',
        'description': 'A simple product for new stores.',
        'price': Decimal('12.99'),
        'quantity': 10,
        'active': True,
        'available': True,
        'category': 'Books',
        'images': [],
    }
    PRODUCTS['p2'] = {
        'id': 'p2',
        'name': 'Widget',
        'description': 'Basic retail item.',
        'price': Decimal('5.00'),
        'quantity': 0,
        'active': True,
        'available': True,
        'category': 'Home',
        'images': [],
    }


def cart():
    session.setdefault('cart', {})
    return session['cart']


def cart_items():
    items = []
    for pid, qty in cart().items():
        p = PRODUCTS.get(pid)
        if p:
            items.append((p, qty))
    return items


def purchasable(product):
    return product['active'] and product['available'] and product['price'] is not None and product['quantity'] > 0


def price_value(product):
    return Decimal(product['price']) if not isinstance(product['price'], Decimal) else product['price']


@app.before_request
def before_request():
    seed_data()


@app.route('/')
def index():
    q = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    filtered = []
    for p in PRODUCTS.values():
        if q and q not in p['name'].lower() and q not in p['description'].lower():
            continue
        if category and p['category'] != category:
            continue
        filtered.append(p)
    template = '''
    <h1>GAMMA-J Web Store</h1>
    <a href="/cart">Cart</a> | <a href="/admin">Admin</a>
    <form method="get">
      <input name="q" placeholder="Search" value="{{request.args.get('q','')}}">
      <select name="category">
        <option value="">All</option>
        {% for c in categories %}<option value="{{c}}" {% if request.args.get('category')==c %}selected{% endif %}>{{c}}</option>{% endfor %}
      </select>
      <button>Filter</button>
    </form>
    {% for p in products %}
      <div style="border:1px solid #ccc;margin:8px;padding:8px">
        <h3>{{p.name}}</h3>
        <p>{{p.description}}</p>
        <p>Price: {{p.price}}</p>
        <p>Status: {% if purchasable(p) %}Available{% else %}Unavailable{% endif %}</p>
        <a href="/product/{{p.id}}">View</a>
      </div>
    {% endfor %}
    '''
    return render_template_string(template, products=filtered, categories=CATEGORIES, purchasable=purchasable, request=request)


@app.route('/product/<pid>')
def product(pid):
    p = PRODUCTS.get(pid) or abort(404)
    template = '''
    <h1>{{p.name}}</h1>
    <p>{{p.description}}</p>
    <p>Price: {{p.price}}</p>
    <p>Quantity: {{p.quantity}}</p>
    <p>{% if purchasable(p) %}Purchasable{% else %}Not purchasable{% endif %}</p>
    <form method="post" action="/cart/add/{{p.id}}">
      <input name="qty" type="number" min="1" value="1">
      <button {% if not purchasable(p) %}disabled{% endif %}>Add to cart</button>
    </form>
    <a href="/">Back</a>
    '''
    return render_template_string(template, p=p, purchasable=purchasable)


@app.route('/cart')
def view_cart():
    items = cart_items()
    total = sum(price_value(p) * qty for p, qty in items)
    template = '''
    <h1>Cart</h1>
    {% for p, qty in items %}
      <div>{{p.name}} x {{qty}}</div>
    {% endfor %}
    <p>Total: {{total}}</p>
    <form method="post" action="/checkout">
      <button>Checkout</button>
    </form>
    <a href="/">Continue shopping</a>
    '''
    return render_template_string(template, items=items, total=total)


@app.route('/cart/add/<pid>', methods=['POST'])
def add_cart(pid):
    p = PRODUCTS.get(pid)
    if not p:
        abort(404)
    if not purchasable(p):
        return ('Product is unavailable and cannot be added to the cart.', 400)
    try:
        qty = int(request.form.get('qty', 1))
    except ValueError:
        qty = 1
    if qty < 1:
        qty = 1
    c = cart()
    c[pid] = c.get(pid, 0) + qty
    session['cart'] = c
    session.modified = True
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    items = cart_items()
    if request.method == 'POST':
        if not items:
            flash('Your cart is empty.')
            return redirect(url_for('view_cart'))
        for p, qty in items:
            if not purchasable(p) or p['quantity'] < qty:
                flash(f'{p["name"]} is not available in the requested quantity.')
                return redirect(url_for('view_cart'))
        order_id = str(uuid.uuid4())[:8]
        total = sum(price_value(p) * qty for p, qty in items)
        ORDERS[order_id] = {
            'id': order_id,
            'items': [{'product_id': p['id'], 'name': p['name'], 'qty': qty, 'price': str(price_value(p))} for p, qty in items],
            'total': str(total),
            'status': 'pending',
            'payment_status': 'unpaid',
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        session['last_order_id'] = order_id
        return redirect(url_for('order', oid=order_id))
    return render_template_string('''
        <h1>Checkout</h1>
        <form method="post">
          <button>Place order</button>
        </form>
    ''')


@app.route('/order/<oid>')
def order(oid):
    order = ORDERS.get(oid) or abort(404)
    return render_template_string('''
      <h1>Order {{order.id}}</h1>
      <p>Status: {{order.status}}</p>
      <p>Payment: {{order.payment_status}}</p>
      <ul>{% for item in order['items'] %}<li>{{item.name}} x {{item.qty}}</li>{% endfor %}</ul>
      <p>Total: {{order.total}}</p>
      <form method="post" action="/order/{{order.id}}/pay">
        <button>Simulate payment success</button>
      </form>
      <a href="/">Home</a>
    ''', order=order)


@app.route('/order/<oid>/pay', methods=['POST'])
def pay(oid):
    order = ORDERS.get(oid) or abort(404)
    order['payment_status'] = 'paid'
    order['status'] = 'confirmed'
    for item in order['items']:
        PRODUCTS[item['product_id']]['quantity'] -= item['qty']
    session['cart'] = {}
    session.modified = True
    return redirect(url_for('order', oid=oid))


@app.route('/admin')
def admin():
    template = '''
    <h1>Admin</h1>
    <h2>Products</h2>
    <a href="/admin/product/new">Add product</a>
    {% for p in products %}<div>{{p.id}} - {{p.name}} - {{p.price}} - {{p.quantity}}</div>{% endfor %}
    <h2>Orders</h2>
    {% for o in orders %}<div><a href="/order/{{o.id}}">{{o.id}}</a> - {{o.status}} - {{o.payment_status}}</div>{% endfor %}
    <h2>Audit log</h2>
    {% for a in audit_log %}<div>{{a.when}} {{a.who}} {{a.what}}</div>{% endfor %}
    <a href="/">Home</a>
    '''
    return render_template_string(template, products=PRODUCTS.values(), orders=ORDERS.values(), audit_log=AUDIT_LOG)


@app.route('/admin/product/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        pid = str(uuid.uuid4())[:8]
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price_text = request.form.get('price', '').strip()
        qty_text = request.form.get('quantity', '0').strip()
        if not name:
            return 'Name required', 400
        try:
            price = Decimal(price_text)
        except InvalidOperation:
            return 'Invalid price', 400
        try:
            quantity = int(qty_text)
        except ValueError:
            return 'Invalid quantity', 400
        before = None
        PRODUCTS[pid] = {'id': pid, 'name': name, 'description': description, 'price': price, 'quantity': quantity, 'active': True, 'available': True, 'category': request.form.get('category', 'Books'), 'images': []}
        audit('create_product', before=before, after=PRODUCTS[pid])
        return redirect(url_for('admin'))
    return render_template_string('''
      <h1>New product</h1>
      <form method="post">
        <input name="name" placeholder="Name"><br>
        <input name="description" placeholder="Description"><br>
        <input name="price" placeholder="Price"><br>
        <input name="quantity" placeholder="Quantity" value="0"><br>
        <select name="category">{% for c in categories %}<option value="{{c}}">{{c}}</option>{% endfor %}</select><br>
        <button>Create</button>
      </form>
    ''', categories=CATEGORIES)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=True)
