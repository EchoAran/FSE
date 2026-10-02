from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import datetime
from uuid import uuid4
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'gamma-j-store-secret')

PRODUCTS = [
    {
        'id': 'p1',
        'name': 'Starter Mug',
        'description': 'Simple branded mug for new shops.',
        'price': 9.99,
        'category': 'Accessories',
        'availability': 'In stock',
        'image': 'https://via.placeholder.com/200?text=Starter+Mug',
    },
    {
        'id': 'p2',
        'name': 'Launch T-Shirt',
        'description': 'Comfortable shirt for your team or customers.',
        'price': 19.99,
        'category': 'Apparel',
        'availability': 'In stock',
        'image': 'https://via.placeholder.com/200?text=Launch+T-Shirt',
    },
    {
        'id': 'p3',
        'name': 'Desk Sticker Pack',
        'description': 'Pack of assorted shop stickers.',
        'price': 4.5,
        'category': 'Accessories',
        'availability': 'Limited',
        'image': '',
    },
]
CUSTOMERS = {
    'customer@example.com': {
        'name': 'Sample Customer',
        'email': 'customer@example.com',
        'phone': '',
        'address': '123 Main St',
    }
}
ORDERS = []


def cart():
    return session.setdefault('cart', {})


def get_product(pid):
    return next((p for p in PRODUCTS if p['id'] == pid), None)


def cart_items_and_total():
    items = []
    total = 0.0
    for pid, qty in cart().items():
        product = get_product(pid)
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return items, total


@app.route('/')
def index():
    q = request.args.get('q', '').strip().lower()
    category = request.args.get('category', '').strip()
    min_price = request.args.get('min_price', '').strip()
    max_price = request.args.get('max_price', '').strip()
    products = PRODUCTS
    if q:
        products = [p for p in products if q in p['name'].lower()]
    if category:
        products = [p for p in products if p['category'] == category]
    try:
        if min_price:
            mp = float(min_price)
            products = [p for p in products if p['price'] >= mp]
        if max_price:
            xp = float(max_price)
            products = [p for p in products if p['price'] <= xp]
    except ValueError:
        flash('Invalid price filter ignored.')
    categories = sorted(set(p['category'] for p in PRODUCTS))
    return render_template('index.html', products=products, categories=categories, filters=request.args)


@app.route('/cart')
def view_cart():
    items, total = cart_items_and_total()
    return render_template('cart.html', items=items, total=total)


@app.route('/cart/add/<pid>', methods=['POST'])
def add_cart(pid):
    c = cart()
    c[pid] = c.get(pid, 0) + 1
    session['cart'] = c
    flash('Item added to cart.')
    return redirect(url_for('view_cart'))


@app.route('/cart/update/<pid>', methods=['POST'])
def update_cart(pid):
    qty = int(request.form.get('qty', '1'))
    c = cart()
    if qty <= 0:
        c.pop(pid, None)
    else:
        c[pid] = qty
    session['cart'] = c
    return redirect(url_for('view_cart'))


@app.route('/cart/remove/<pid>', methods=['POST'])
def remove_cart(pid):
    c = cart()
    c.pop(pid, None)
    session['cart'] = c
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    items, total = cart_items_and_total()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        if not name or not email or not address:
            flash('Name, contact email, and delivery address are required.')
            return render_template('checkout.html', items=items, total=total)
        order = {
            'id': str(uuid4())[:8],
            'created_at': datetime.utcnow().isoformat(timespec='seconds') + 'Z',
            'customer': {'name': name, 'email': email, 'address': address, 'phone': phone},
            'items': [{'name': i['product']['name'], 'qty': i['qty'], 'price': i['product']['price']} for i in items],
            'total': total,
        }
        ORDERS.append(order)
        CUSTOMERS[email] = {'name': name, 'email': email, 'phone': phone, 'address': address}
        session['last_order'] = order
        session['cart'] = {}
        flash('Order placed successfully.')
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html', items=items, total=total)


@app.route('/order/confirmation')
def order_confirmation():
    order = session.get('last_order')
    return render_template('order_confirmation.html', order=order)


@app.route('/account', methods=['GET', 'POST'])
def account():
    email = request.args.get('email', 'customer@example.com')
    customer = CUSTOMERS.get(email, CUSTOMERS['customer@example.com']).copy()
    if request.method == 'POST':
        customer['name'] = request.form.get('name', '').strip()
        customer['email'] = request.form.get('email', '').strip()
        customer['phone'] = request.form.get('phone', '').strip()
        customer['address'] = request.form.get('address', '').strip()
        CUSTOMERS[customer['email']] = customer
        flash('Account updated.')
        return redirect(url_for('account', email=customer['email']))
    return render_template('account.html', customer=customer)


@app.route('/orders')
def orders():
    email = request.args.get('email', 'customer@example.com')
    history = [o for o in ORDERS if o['customer']['email'] == email]
    return render_template('orders.html', orders=history, email=email)


@app.route('/staff/products', methods=['GET', 'POST'])
def staff_products():
    if request.method == 'POST':
        pid = request.form.get('id') or str(uuid4())[:8]
        product = {
            'id': pid,
            'name': request.form['name'],
            'description': request.form['description'],
            'price': float(request.form['price']),
            'category': request.form['category'],
            'availability': request.form['availability'],
            'image': request.form.get('image', ''),
        }
        existing = next((i for i, p in enumerate(PRODUCTS) if p['id'] == pid), None)
        if existing is None:
            PRODUCTS.append(product)
        else:
            PRODUCTS[existing] = product
        flash('Product saved.')
        return redirect(url_for('staff_products'))
    return render_template('staff_products.html', products=PRODUCTS)


@app.route('/staff/customers', methods=['GET', 'POST'])
def staff_customers():
    if request.method == 'POST':
        customer = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),
        }
        CUSTOMERS[customer['email']] = customer
        flash('Customer saved.')
        return redirect(url_for('staff_customers'))
    return render_template('staff_customers.html', customers=list(CUSTOMERS.values()))


@app.route('/staff/reports')
def staff_reports():
    sales_total = sum(o['total'] for o in ORDERS)
    return render_template('staff_reports.html', orders=ORDERS, sales_total=sales_total)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '8000')), debug=True)
