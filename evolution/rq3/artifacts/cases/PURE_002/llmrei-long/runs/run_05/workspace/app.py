from flask import Flask, request, redirect, url_for, session, render_template_string, flash
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional
import itertools

app = Flask(__name__)
app.secret_key = 'gamma-j-web-store-secret'

@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    category: str
    availability: int
    image_url: str = ''

@dataclass
class Customer:
    id: int
    name: str
    email: str
    phone: str = ''
    address: str = ''

@dataclass
class Order:
    id: int
    customer_name: str
    email: str
    phone: str
    address: str
    items: List[Dict]
    total: float
    created_at: str

products: List[Product] = [
    Product(1, 'Starter Laptop', 'A simple laptop for everyday tasks', 499.99, 'Electronics', 5, 'https://via.placeholder.com/120'),
    Product(2, 'Wireless Mouse', 'Comfortable wireless mouse', 24.99, 'Electronics', 25, 'https://via.placeholder.com/120'),
    Product(3, 'Office Chair', 'Ergonomic chair for home office', 149.99, 'Furniture', 7, 'https://via.placeholder.com/120'),
]
customers: List[Customer] = [
    Customer(1, 'Alex Smith', 'alex@example.com', '555-0100', '1 Main St'),
]
orders: List[Order] = []
product_id_seq = itertools.count(len(products) + 1)
customer_id_seq = itertools.count(len(customers) + 1)
order_id_seq = itertools.count(1)


def cart():
    return session.setdefault('cart', {})


def cart_items_and_total():
    items = []
    total = 0.0
    for pid, qty in cart().items():
        product = next((p for p in products if p.id == int(pid)), None)
        if product:
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return items, total


layout = '''
<!doctype html>
<title>GAMMA-J Web Store</title>
<style>
body{font-family:Arial,sans-serif;max-width:1000px;margin:20px auto;padding:0 12px}
nav a{margin-right:10px}
.product{border:1px solid #ddd;padding:10px;margin:10px 0;display:flex;gap:10px}
img{width:80px;height:80px;object-fit:cover}
.flash{background:#eef;padding:8px;margin:8px 0}
input,select,textarea{padding:6px;margin:4px 0;width:100%;max-width:420px}
button{padding:8px 12px}
table{border-collapse:collapse;width:100%} td,th{border:1px solid #ccc;padding:6px;text-align:left}
</style>
<nav>
<a href='/'>Products</a>
<a href='/cart'>Cart</a>
<a href='/checkout'>Checkout</a>
<a href='/orders'>Order History</a>
<a href='/staff/products'>Staff Products</a>
<a href='/staff/customers'>Staff Customers</a>
<a href='/staff/reports'>Sales Report</a>
</nav>
{% with messages = get_flashed_messages() %}{% if messages %}{% for m in messages %}<div class='flash'>{{m}}</div>{% endfor %}{% endif %}{% endwith %}
{{ body|safe }}
'''

@app.route('/')
def index():
    q = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    filtered = products
    if q:
        filtered = [p for p in filtered if q in p.name.lower()]
    if category:
        filtered = [p for p in filtered if p.category == category]
    if min_price is not None:
        filtered = [p for p in filtered if p.price >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p.price <= max_price]
    cats = sorted(set(p.category for p in products))
    body = render_template_string('''
    <h1>Products</h1>
    <form method='get'>
      <input name='q' placeholder='Search by name' value='{{request.args.get("q", "")}}'>
      <select name='category'><option value=''>All categories</option>{% for c in cats %}<option value='{{c}}' {% if request.args.get('category') == c %}selected{% endif %}>{{c}}</option>{% endfor %}</select>
      <input name='min_price' type='number' step='0.01' placeholder='Min price' value='{{request.args.get("min_price", "")}}'>
      <input name='max_price' type='number' step='0.01' placeholder='Max price' value='{{request.args.get("max_price", "")}}'>
      <button type='submit'>Filter</button>
    </form>
    {% for p in products %}
      <div class='product'>
        {% if p.image_url %}<img src='{{p.image_url}}' alt='image'>{% endif %}
        <div>
          <h3>{{p.name}}</h3>
          <div>{{p.description}}</div>
          <div>Price: ${{'%.2f'|format(p.price)}} | Availability: {{p.availability}}</div>
          <form method='post' action='/cart/add/{{p.id}}'><button>Add to cart</button></form>
        </div>
      </div>
    {% endfor %}
    ''', products=filtered, cats=cats)
    return render_template_string(layout, body=body)

@app.post('/cart/add/<int:pid>')
def add_to_cart(pid):
    c = cart()
    c[str(pid)] = c.get(str(pid), 0) + 1
    session['cart'] = c
    flash('Item added to cart')
    return redirect(url_for('index'))

@app.route('/cart', methods=['GET', 'POST'])
def view_cart():
    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('qty_'):
                pid = key.split('_', 1)[1]
                qty = max(0, int(value))
                if qty == 0:
                    cart().pop(pid, None)
                else:
                    cart()[pid] = qty
        session['cart'] = cart()
        flash('Cart updated')
        return redirect(url_for('view_cart'))
    items, total = cart_items_and_total()
    body = render_template_string('''
    <h1>Shopping Cart</h1>
    <form method='post'>
    <table>
      <tr><th>Product</th><th>Qty</th><th>Price</th><th>Subtotal</th></tr>
      {% for row in items %}
      <tr>
        <td>{{row.product.name}}</td>
        <td><input type='number' min='0' name='qty_{{row.product.id}}' value='{{row.qty}}'></td>
        <td>${{'%.2f'|format(row.product.price)}}</td>
        <td>${{'%.2f'|format(row.subtotal)}}</td>
      </tr>
      {% endfor %}
    </table>
    <p>Total: ${{'%.2f'|format(total)}}</p>
    <button type='submit'>Update quantities</button>
    </form>
    <p><a href='/checkout'>Proceed to checkout</a></p>
    ''', items=items, total=total)
    return render_template_string(layout, body=body)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    items, total = cart_items_and_total()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        if not name or not email or not address:
            flash('Name, email, and delivery address are required')
        elif not items:
            flash('Cart is empty')
        else:
            order = Order(next(order_id_seq), name, email, phone, address, [
                {'product_id': r['product'].id, 'name': r['product'].name, 'qty': r['qty'], 'price': r['product'].price}
                for r in items
            ], total, datetime.utcnow().isoformat())
            orders.append(order)
            session['cart'] = {}
            flash(f'Order #{order.id} confirmed successfully')
            return redirect(url_for('order_confirmation', oid=order.id))
    body = render_template_string('''
    <h1>Checkout</h1>
    <p>Total before checkout: ${{'%.2f'|format(total)}}</p>
    <form method='post'>
      <input name='name' placeholder='Name' required>
      <input name='email' placeholder='Contact email' required>
      <input name='phone' placeholder='Contact number (optional)'>
      <textarea name='address' placeholder='Delivery address' required></textarea>
      <button type='submit'>Submit order</button>
    </form>
    ''', total=total)
    return render_template_string(layout, body=body)

@app.route('/order/<int:oid>')
def order_confirmation(oid):
    order = next((o for o in orders if o.id == oid), None)
    if not order:
        return 'Order not found', 404
    body = render_template_string('''
    <h1>Order Confirmation</h1>
    <p>Your purchase was successful. Order #{{order.id}}.</p>
    <p>Name: {{order.customer_name}}</p>
    <p>Email: {{order.email}}</p>
    <p>Address: {{order.address}}</p>
    <p>Total: ${{'%.2f'|format(order.total)}}</p>
    ''', order=order)
    return render_template_string(layout, body=body)

@app.route('/orders')
def order_history():
    body = render_template_string('''
    <h1>Order History</h1>
    {% for o in orders %}
      <div class='product'>Order #{{o.id}} - {{o.created_at}} - ${{'%.2f'|format(o.total)}}</div>
    {% endfor %}
    ''', orders=orders)
    return render_template_string(layout, body=body)

@app.route('/staff/products', methods=['GET', 'POST'])
def staff_products():
    if request.method == 'POST':
        pid = request.form.get('id')
        if pid:
            p = next((x for x in products if x.id == int(pid)), None)
        else:
            p = None
        if p is None:
            p = Product(next(product_id_seq), '', '', 0.0, '', 0, '')
            products.append(p)
        p.name = request.form['name']
        p.description = request.form['description']
        p.price = float(request.form['price'])
        p.category = request.form['category']
        p.availability = int(request.form['availability'])
        p.image_url = request.form.get('image_url', '')
        flash('Product saved')
        return redirect(url_for('staff_products'))
    body = render_template_string('''
    <h1>Staff Products</h1>
    <form method='post'>
      <input name='id' placeholder='Existing product id to update'>
      <input name='name' placeholder='Name' required>
      <input name='description' placeholder='Short description' required>
      <input name='price' type='number' step='0.01' placeholder='Price' required>
      <input name='category' placeholder='Category' required>
      <input name='availability' type='number' placeholder='Availability' required>
      <input name='image_url' placeholder='Image URL'>
      <button type='submit'>Save</button>
    </form>
    <ul>{% for p in products %}<li>#{{p.id}} {{p.name}} - ${{'%.2f'|format(p.price)}} - {{p.category}} - {{p.availability}}</li>{% endfor %}</ul>
    ''', products=products)
    return render_template_string(layout, body=body)

@app.route('/staff/customers', methods=['GET', 'POST'])
def staff_customers():
    if request.method == 'POST':
        cid = request.form.get('id')
        c = next((x for x in customers if x.id == int(cid)), None) if cid else None
        if c is None:
            c = Customer(next(customer_id_seq), '', '')
            customers.append(c)
        c.name = request.form['name']
        c.email = request.form['email']
        c.phone = request.form.get('phone', '')
        c.address = request.form.get('address', '')
        flash('Customer saved')
        return redirect(url_for('staff_customers'))
    body = render_template_string('''
    <h1>Staff Customers</h1>
    <form method='post'>
      <input name='id' placeholder='Existing customer id to update'>
      <input name='name' placeholder='Name' required>
      <input name='email' placeholder='Email' required>
      <input name='phone' placeholder='Phone'>
      <input name='address' placeholder='Address'>
      <button type='submit'>Save</button>
    </form>
    <ul>{% for c in customers %}<li>#{{c.id}} {{c.name}} - {{c.email}} - {{c.phone}} - {{c.address}}</li>{% endfor %}</ul>
    ''', customers=customers)
    return render_template_string(layout, body=body)

@app.route('/staff/reports')
def staff_reports():
    total_sales = sum(o.total for o in orders)
    body = render_template_string('''
    <h1>Sales Report</h1>
    <p>Orders placed: {{orders|length}}</p>
    <p>Total sales: ${{'%.2f'|format(total_sales)}}</p>
    <ul>{% for o in orders %}<li>Order #{{o.id}} - ${{'%.2f'|format(o.total)}} - {{o.customer_name}}</li>{% endfor %}</ul>
    ''', orders=orders, total_sales=total_sales)
    return render_template_string(layout, body=body)

@app.route('/account', methods=['GET', 'POST'])
def account():
    customer = customers[0]
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form.get('phone', '')
        customer.address = request.form.get('address', '')
        flash('Your details were updated')
        return redirect(url_for('account'))
    body = render_template_string('''
    <h1>Your Account</h1>
    <form method='post'>
      <input name='name' value='{{customer.name}}' required>
      <input name='email' value='{{customer.email}}' required>
      <input name='phone' value='{{customer.phone}}'>
      <input name='address' value='{{customer.address}}'>
      <button type='submit'>Update</button>
    </form>
    ''', customer=customer)
    return render_template_string(layout, body=body)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
