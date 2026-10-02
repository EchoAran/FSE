from flask import Flask, request, redirect, url_for, render_template_string, session, abort
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any
import uuid

app = Flask(__name__)
app.secret_key = 'gamma-j-secret-key'

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

# seed data
for p in [
    Product(str(uuid.uuid4()), 'Starter Widget', 'A beginner-friendly widget.', 19.99, 'Widgets', 10, 'https://via.placeholder.com/100'),
    Product(str(uuid.uuid4()), 'Premium Gadget', 'A premium gadget for daily use.', 49.5, 'Gadgets', 5, 'https://via.placeholder.com/100'),
    Product(str(uuid.uuid4()), 'Budget Widget', 'Affordable and simple.', 9.99, 'Widgets', 20, ''),
]:
    PRODUCTS[p.id] = p


def cart():
    return session.setdefault('cart', {})


def cart_items():
    items = []
    for pid, qty in cart().items():
        product = PRODUCTS.get(pid)
        if product:
            items.append({'product': product, 'qty': qty, 'subtotal': round(product.price * qty, 2)})
    return items


def cart_total():
    return round(sum(i['subtotal'] for i in cart_items()), 2)


HOME = '''
<h1>GAMMA-J Web Store</h1>
<p><a href="/products">Browse products</a> | <a href="/cart">Cart</a> | <a href="/account">My account</a> | <a href="/admin">Staff</a></p>
<p>Simple storefront for browsing, cart management, checkout, and staff product/customer management.</p>
'''

PRODUCTS_TMPL = '''
<h1>Products</h1>
<form method="get">
  Search: <input name="q" value="{{q}}">
  Category: <input name="category" value="{{category}}">
  Min price: <input name="min_price" value="{{min_price}}" size="6">
  Max price: <input name="max_price" value="{{max_price}}" size="6">
  <button type="submit">Filter</button>
</form>
<p><a href="/">Home</a> | <a href="/cart">Cart</a></p>
<ul>
{% for p in products %}
<li>
  <strong>{{p.name}}</strong> - {{p.description}} - ${{'%.2f'|format(p.price)}} - {{p.category}} - Available: {{p.availability}}
  {% if p.image_url %}<br><img src="{{p.image_url}}" alt="{{p.name}}" width="60">{% endif %}
  <form method="post" action="/cart/add/{{p.id}}" style="display:inline">
    <button type="submit">Add to cart</button>
  </form>
</li>
{% endfor %}
</ul>
'''

CART_TMPL = '''
<h1>Shopping Cart</h1>
<p><a href="/products">Continue shopping</a> | <a href="/checkout">Checkout</a></p>
<ul>
{% for item in items %}
<li>
  {{item.product.name}} - ${{'%.2f'|format(item.product.price)}} x
  <form method="post" action="/cart/update/{{item.product.id}}" style="display:inline">
    <input name="qty" type="number" min="0" value="{{item.qty}}" style="width:70px">
    <button type="submit">Update</button>
  </form>
  <form method="post" action="/cart/remove/{{item.product.id}}" style="display:inline">
    <button type="submit">Remove</button>
  </form>
</li>
{% endfor %}
</ul>
<p><strong>Cart total:</strong> ${{'%.2f'|format(total)}}</p>
'''

CHECKOUT_TMPL = '''
<h1>Checkout</h1>
<p>Cart total: ${{'%.2f'|format(total)}}</p>
<form method="post">
  Name: <input name="name" required><br>
  Email: <input name="email" type="email" required><br>
  Address: <input name="address" required><br>
  Contact number: <input name="contact_number"><br>
  <button type="submit">Place order</button>
</form>
'''

ACCOUNT_TMPL = '''
<h1>My account</h1>
<form method="post">
  Name: <input name="name" value="{{customer.name}}" required><br>
  Email: <input name="email" value="{{customer.email}}" type="email" required><br>
  Address: <input name="address" value="{{customer.address}}" required><br>
  Contact number: <input name="contact_number" value="{{customer.contact_number}}"><br>
  <button type="submit">Update</button>
</form>
<h2>Order history</h2>
<ul>
{% for o in orders %}
<li>{{o.id}} - {{o.created_at}} - ${{'%.2f'|format(o.total)}}</li>
{% endfor %}
</ul>
'''

ADMIN_TMPL = '''
<h1>Staff dashboard</h1>
<p><a href="/admin/products">Manage products</a> | <a href="/admin/customers">Manage customers</a> | <a href="/admin/reports">Sales report</a></p>
<h2>New orders</h2>
<ul>
{% for o in orders %}
<li>{{o.id}} - {{o.customer_name}} - ${{'%.2f'|format(o.total)}} - {{o.created_at}}</li>
{% endfor %}
</ul>
'''

@app.route('/')
def home():
    return HOME

@app.route('/products')
def products():
    q = request.args.get('q', '').lower()
    category = request.args.get('category', '').lower()
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    items = list(PRODUCTS.values())
    if q:
        items = [p for p in items if q in p.name.lower()]
    if category:
        items = [p for p in items if category in p.category.lower()]
    if min_price:
        items = [p for p in items if p.price >= float(min_price)]
    if max_price:
        items = [p for p in items if p.price <= float(max_price)]
    return render_template_string(PRODUCTS_TMPL, products=items, q=request.args.get('q', ''), category=request.args.get('category', ''), min_price=min_price, max_price=max_price)

@app.route('/cart')
def view_cart():
    return render_template_string(CART_TMPL, items=cart_items(), total=cart_total())

@app.post('/cart/add/<pid>')
def add_cart(pid):
    if pid not in PRODUCTS:
        abort(404)
    c = cart()
    c[pid] = c.get(pid, 0) + 1
    session['cart'] = c
    return redirect(url_for('view_cart'))

@app.post('/cart/update/<pid>')
def update_cart(pid):
    qty = max(0, int(request.form.get('qty', 0)))
    c = cart()
    if qty == 0:
        c.pop(pid, None)
    else:
        c[pid] = qty
    session['cart'] = c
    return redirect(url_for('view_cart'))

@app.post('/cart/remove/<pid>')
def remove_cart(pid):
    c = cart()
    c.pop(pid, None)
    session['cart'] = c
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        if not name or not email or not address:
            return 'Missing required fields', 400
        if not cart_items():
            return 'Cart is empty', 400
        order = Order(str(uuid.uuid4()), name, email, address, contact_number, [
            {'product_id': i['product'].id, 'name': i['product'].name, 'qty': i['qty'], 'price': i['product'].price}
            for i in cart_items()
        ], cart_total(), datetime.utcnow().isoformat())
        ORDERS.append(order)
        session['cart'] = {}
        return f'Order placed successfully. Confirmation: {order.id}'
    return render_template_string(CHECKOUT_TMPL, total=cart_total())

@app.route('/account', methods=['GET', 'POST'])
def account():
    if not CUSTOMERS:
        customer = Customer('default', '', '', '')
        CUSTOMERS[customer.id] = customer
    customer = next(iter(CUSTOMERS.values()))
    if request.method == 'POST':
        customer.name = request.form.get('name', '').strip()
        customer.email = request.form.get('email', '').strip()
        customer.address = request.form.get('address', '').strip()
        customer.contact_number = request.form.get('contact_number', '').strip()
    orders = [o for o in ORDERS if o.email == customer.email]
    return render_template_string(ACCOUNT_TMPL, customer=customer, orders=orders)

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_TMPL, orders=ORDERS)

@app.route('/admin/products', methods=['GET', 'POST'])
def admin_products():
    if request.method == 'POST':
        pid = request.form.get('id') or str(uuid.uuid4())
        PRODUCTS[pid] = Product(
            pid,
            request.form.get('name', '').strip(),
            request.form.get('description', '').strip(),
            float(request.form.get('price', 0)),
            request.form.get('category', '').strip(),
            int(request.form.get('availability', 0)),
            request.form.get('image_url', '').strip(),
        )
        return redirect(url_for('admin_products'))
    items = list(PRODUCTS.values())
    form = '''<h1>Manage products</h1><form method="post">
    ID (optional for new): <input name="id"><br>
    Name: <input name="name" required><br>
    Description: <input name="description" required><br>
    Price: <input name="price" required><br>
    Category: <input name="category" required><br>
    Availability: <input name="availability" required><br>
    Image URL: <input name="image_url"><br>
    <button type="submit">Save</button></form><ul>{% for p in items %}<li>{{p.id}} {{p.name}} ${{'%.2f'|format(p.price)}}</li>{% endfor %}</ul>'''
    return render_template_string(form, items=items)

@app.route('/admin/customers', methods=['GET', 'POST'])
def admin_customers():
    if request.method == 'POST':
        cid = request.form.get('id') or str(uuid.uuid4())
        CUSTOMERS[cid] = Customer(cid, request.form.get('name', '').strip(), request.form.get('email', '').strip(), request.form.get('address', '').strip(), request.form.get('contact_number', '').strip())
        return redirect(url_for('admin_customers'))
    form = '''<h1>Manage customers</h1><form method="post">
    ID (optional for new): <input name="id"><br>
    Name: <input name="name" required><br>
    Email: <input name="email" required><br>
    Address: <input name="address" required><br>
    Contact number: <input name="contact_number"><br>
    <button type="submit">Save</button></form><ul>{% for c in items %}<li>{{c.id}} {{c.name}} {{c.email}}</li>{% endfor %}</ul>'''
    return render_template_string(form, items=list(CUSTOMERS.values()))

@app.route('/admin/reports')
def reports():
    total_sales = round(sum(o.total for o in ORDERS), 2)
    return f'<h1>Sales report</h1><p>Orders: {len(ORDERS)}</p><p>Total sales: ${total_sales:.2f}</p>'

@app.route('/orders')
def orders():
    return {'orders': [asdict(o) for o in ORDERS]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
