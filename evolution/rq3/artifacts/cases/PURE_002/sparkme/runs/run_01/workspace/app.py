from flask import Flask, render_template, request, redirect, url_for, session, flash
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

app = Flask(__name__)
app.secret_key = 'gamma-j-demo-secret'

STATE = {
    'store': {'name': '', 'currency': 'USD'},
    'setup_complete': False,
    'categories': ['General'],
    'products': [
        {'id': 'p1', 'name': 'Starter Tee', 'sku': 'TEE-001', 'price': 19.99, 'stock': 12, 'category': 'General', 'available': True, 'description': 'A simple starter product.'},
        {'id': 'p2', 'name': 'Coffee Mug', 'sku': 'MUG-001', 'price': 9.5, 'stock': 0, 'category': 'General', 'available': False, 'description': 'Out of stock example.'},
    ],
    'customers': [
        {'id': 'c1', 'name': 'Alex Customer', 'email': 'alex@example.com', 'orders': []},
    ],
    'cart': [],
    'orders': [],
    'logs': [],
    'notifications': [],
    'import_state': None,
}


def log(event, detail, actor='system'):
    STATE['logs'].insert(0, {
        'time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'actor': actor,
        'event': event,
        'detail': detail,
    })


def notify(level, title, message):
    STATE['notifications'].insert(0, {
        'time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'level': level,
        'title': title,
        'message': message,
    })


def current_cart_total():
    return round(sum(item['price'] * item['qty'] for item in STATE['cart']), 2)


@app.route('/')
def home():
    return render_template('home.html', state=STATE, cart_total=current_cart_total())


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    step = int(request.values.get('step', 1))
    errors = []
    if request.method == 'POST':
        if step == 1:
            name = request.form.get('name', '').strip()
            if not name:
                errors.append('Store name is required.')
            else:
                STATE['store']['name'] = name
                log('setup', f'Store name set to {name}')
                return redirect(url_for('setup', step=2))
        elif step == 2:
            category = request.form.get('category', '').strip()
            if not category:
                errors.append('Please add one category to continue.')
            else:
                if category not in STATE['categories']:
                    STATE['categories'].append(category)
                log('setup', f'Category added: {category}')
                return redirect(url_for('setup', step=3))
        elif step == 3:
            STATE['setup_complete'] = True
            log('setup', 'Setup completed')
            flash('Setup complete. You can start selling now.')
            return redirect(url_for('home'))
    return render_template('setup.html', step=step, errors=errors, state=STATE)


@app.route('/products')
def products():
    return render_template('products.html', products=STATE['products'], categories=STATE['categories'])


@app.route('/product/<pid>/toggle', methods=['POST'])
def toggle_product(pid):
    for p in STATE['products']:
        if p['id'] == pid:
            p['available'] = not p['available']
            p['stock'] = max(0, p['stock'])
            log('product', f"Availability changed for {p['name']} to {p['available']}", actor='staff')
            notify('info', 'Product updated', f"{p['name']} availability changed.")
            break
    return redirect(url_for('products'))


@app.route('/cart/add/<pid>', methods=['POST'])
def add_cart(pid):
    prod = next((p for p in STATE['products'] if p['id'] == pid), None)
    if prod:
        item = next((i for i in STATE['cart'] if i['id'] == pid), None)
        if item:
            item['qty'] += 1
        else:
            STATE['cart'].append({'id': prod['id'], 'name': prod['name'], 'price': prod['price'], 'qty': 1})
        log('cart', f"Added {prod['name']} to cart")
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    return render_template('cart.html', cart=STATE['cart'], total=current_cart_total())


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    errors = []
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        payment = request.form.get('payment', '').strip()
        if not all([name, email, address, payment]):
            errors.append('Please fill in customer, shipping, and payment information.')
        if '@' not in email:
            errors.append('Please enter a valid email address.')
        if not payment.replace(' ', '').isdigit():
            errors.append('Payment information looks incomplete.')
        if errors:
            return render_template('checkout.html', errors=errors, cart=STATE['cart'], total=current_cart_total())
        order = {
            'id': 'o' + uuid.uuid4().hex[:8],
            'customer': name,
            'email': email,
            'address': address,
            'payment_status': 'paid',
            'shipping_status': 'pending',
            'items': list(STATE['cart']),
            'total': current_cart_total(),
            'time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        }
        STATE['orders'].insert(0, order)
        STATE['cart'].clear()
        log('order', f"Order {order['id']} placed for {name}")
        notify('success', 'Order placed', f"Order {order['id']} was created successfully.")
        return redirect(url_for('orders'))
    return render_template('checkout.html', errors=errors, cart=STATE['cart'], total=current_cart_total())


@app.route('/orders')
def orders():
    return render_template('orders.html', orders=STATE['orders'])


@app.route('/import', methods=['GET', 'POST'])
def import_products():
    if request.method == 'POST':
        sample = request.form.get('sample', 'Widget A,SKU1,12.00,5,General').strip()
        rows = []
        for line in sample.splitlines():
            parts = [p.strip() for p in line.split(',')]
            if len(parts) != 5:
                continue
            name, sku, price, stock, category = parts
            issues = []
            suggestions = []
            if not name:
                issues.append('Missing product name')
            if not sku:
                issues.append('Missing SKU')
            try:
                price_val = float(price)
                if price_val <= 0:
                    issues.append('Missing or invalid price')
            except Exception:
                issues.append('Price is not a number')
                price_val = 0.0
            try:
                stock_val = int(stock)
            except Exception:
                issues.append('Stock quantity is unclear')
                stock_val = 0
            if category not in STATE['categories']:
                suggestions.append(f'Category suggestion: {STATE["categories"][0]}')
            duplicate = any(p['sku'] == sku or p['name'].lower() == name.lower() for p in STATE['products'])
            if duplicate:
                suggestions.append('Possible duplicate record')
            rows.append({'name': name, 'sku': sku, 'price': price_val, 'stock': stock_val, 'category': category, 'issues': issues, 'suggestions': suggestions})
        STATE['import_state'] = rows
        log('import', 'Import review generated')
        return redirect(url_for('import_review'))
    return render_template('import.html')


@app.route('/import/review')
def import_review():
    rows = STATE.get('import_state') or []
    ready = sum(1 for r in rows if not r['issues'])
    need = len(rows) - ready
    return render_template('import_review.html', rows=rows, ready=ready, need=need)


@app.route('/logs')
def logs():
    return render_template('logs.html', logs=STATE['logs'])


@app.route('/notifications')
def notifications():
    return render_template('notifications.html', notifications=STATE['notifications'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
