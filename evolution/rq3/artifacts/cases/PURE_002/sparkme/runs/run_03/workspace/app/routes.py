from flask import Blueprint, current_app, redirect, render_template, request, url_for
from .state import now

bp = Blueprint('main', __name__)


def s():
    return current_app.config['STORE']


def log(actor, entity, action, reason=''):
    s().logs.insert(0, {'time': now(), 'actor': actor, 'entity': entity, 'action': action, 'reason': reason})


def add_notification(priority, typ, message):
    s().notifications.insert(0, {'priority': priority, 'type': typ, 'message': message})


@bp.route('/')
def home():
    return render_template('home.html', store=s())


@bp.route('/setup', methods=['GET', 'POST'])
def setup():
    store = s()
    msg = ''
    errors = []
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        currency = request.form.get('currency', '').strip() or 'USD'
        if not name:
            errors.append('Store name is required.')
        if errors:
            msg = 'Please fix the highlighted issue before continuing.'
        else:
            store.store_info.update({'name': name, 'currency': currency})
            log('owner', 'store', 'updated', 'Completed guided setup step for store information')
            msg = 'Store information saved.'
    return render_template('setup.html', store=store, msg=msg, errors=errors)


@bp.route('/products', methods=['GET', 'POST'])
def products():
    store = s()
    msg = ''
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        sku = request.form.get('sku', '').strip()
        price = request.form.get('price', '').strip()
        if name and sku and price:
            product = {'id': len(store.products) + 1, 'name': name, 'sku': sku, 'price': float(price), 'stock': int(request.form.get('stock', 0) or 0), 'category': request.form.get('category', ''), 'available': True, 'description': request.form.get('description', '')}
            store.products.append(product)
            log('staff', 'product', 'added', f"Added product {name}")
            msg = 'Product added.'
        else:
            msg = 'Name, SKU, and price are required.'
    return render_template('products.html', store=store, msg=msg)


@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    store = s()
    if request.method == 'POST':
        pid = int(request.form['product_id'])
        qty = max(1, int(request.form.get('qty', 1)))
        product = next((p for p in store.products if p['id'] == pid), None)
        if product:
            store.cart.append({'product_id': pid, 'name': product['name'], 'qty': qty, 'price': product['price']})
            log('customer', 'cart', 'updated', f"Added {product['name']} to cart")
    return render_template('cart.html', store=store)


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    store = s()
    feedback = []
    if request.method == 'POST':
        name = request.form.get('customer_name', '').strip()
        address = request.form.get('address', '').strip()
        payment = request.form.get('payment', '').strip()
        if not name or not address or len(payment) < 4:
            feedback.append('Please enter customer name, shipping address, and a valid payment reference.')
            return render_template('checkout.html', store=store, feedback=feedback)
        total = sum(i['qty'] * i['price'] for i in store.cart)
        status = 'paid' if 'fail' not in payment.lower() else 'unpaid'
        order = {'id': len(store.orders) + 1, 'customer': name, 'total': total, 'status': status, 'payment': 'success' if status == 'paid' else 'failed', 'shipping': 'pending', 'items': list(store.cart), 'created_at': now()}
        store.orders.append(order)
        store.cart.clear()
        if status == 'unpaid':
            add_notification('high', 'payment', f'Order #{order["id"]} payment failed. Customer may retry payment.')
        log('customer', 'order', 'submitted', f"Order #{order['id']} submitted")
        return render_template('checkout.html', store=store, feedback=['Order submitted. ' + ('Payment failed, order remains unpaid.' if status == 'unpaid' else 'Payment received.')])
    return render_template('checkout.html', store=store, feedback=feedback)


@bp.route('/orders')
def orders():
    return render_template('orders.html', store=s())


@bp.route('/logs')
def logs():
    return render_template('logs.html', store=s())


@bp.route('/notifications')
def notifications():
    return render_template('notifications.html', store=s())


@bp.route('/import', methods=['GET', 'POST'])
def import_products():
    store = s()
    result = None
    if request.method == 'POST':
        raw = request.form.get('csv', '').strip().splitlines()
        rows = [r.split(',') for r in raw if r.strip()]
        imported = 0
        issues = []
        for idx, row in enumerate(rows, 1):
            if len(row) < 4:
                issues.append(f'Row {idx}: missing fields.')
                continue
            name, sku, price, stock = [c.strip() for c in row[:4]]
            if not name or not sku or not price:
                issues.append(f'Row {idx}: name, SKU, and price are required.')
                continue
            dup = next((p for p in store.products if p['name'].lower() == name.lower() or p['sku'].lower() == sku.lower()), None)
            if dup:
                issues.append(f'Row {idx}: possible duplicate found for {name}.')
                continue
            store.products.append({'id': len(store.products) + 1, 'name': name, 'sku': sku, 'price': float(price), 'stock': int(stock or 0), 'category': request.form.get('category', ''), 'available': True, 'description': ''})
            imported += 1
        result = {'imported': imported, 'issues': issues, 'ready': imported, 'needs_attention': len(issues)}
        store.import_result = result
        log('staff', 'import', 'completed', f"Imported {imported} rows")
    return render_template('import.html', store=store, result=result)


@bp.route('/staff')
def staff():
    return render_template('staff.html', store=s())
