from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for
from datetime import datetime
import csv, io

bp = Blueprint('main', __name__)


def now(): return datetime.utcnow().isoformat() + 'Z'

def data(): return current_app.storage.load()

def save(d): current_app.storage.save(d)

def log(d, entity, action, details=''):
    d['audit_log'].append({'time': now(), 'entity': entity, 'action': action, 'details': details})

def notify(d, kind, message, priority='normal'):
    d['notifications'].append({'time': now(), 'kind': kind, 'message': message, 'priority': priority, 'unresolved': True})
    d['issues'].append({'time': now(), 'kind': kind, 'message': message, 'priority': priority, 'unresolved': True})

@bp.get('/')
def index():
    d = data()
    return render_template('index.html', d=d)

@bp.post('/setup')
def setup():
    d = data(); d['store_info'] = {'name': request.form.get('name','').strip(), 'currency': request.form.get('currency','USD').strip() or 'USD'}; d['setup_completed'] = True; log(d,'store','setup','Basic store information saved'); save(d); return redirect(url_for('main.index'))

@bp.post('/products')
def add_product():
    d = data(); p = {'id': len(d['products'])+1,'name': request.form.get('name','').strip(),'sku': request.form.get('sku','').strip(),'barcode': request.form.get('barcode','').strip(),'category': request.form.get('category','').strip(),'price': request.form.get('price','').strip(),'stock': int(request.form.get('stock') or 0),'available': request.form.get('available')=='on'}; d['products'].append(p); log(d,'product','add',p['name']); save(d); return redirect(url_for('main.index'))

@bp.post('/cart/add/<int:product_id>')
def cart_add(product_id):
    d = data(); d['cart'].append({'product_id': product_id, 'qty': int(request.form.get('qty') or 1)}); log(d,'cart','add',str(product_id)); save(d); return redirect(url_for('main.index'))

@bp.post('/orders')
def place_order():
    d = data(); customer = request.form.get('customer','').strip(); address = request.form.get('address','').strip(); payment = request.form.get('payment','').strip(); errors = []
    if not customer: errors.append('Customer name is required')
    if not address: errors.append('Shipping address is required')
    if not payment or len(payment) < 4: errors.append('Payment details look incomplete')
    if errors:
        notify(d,'validation','; '.join(errors),'high'); save(d); return render_template('index.html', d=d, validation_errors=errors), 400
    order = {'id': len(d['orders'])+1,'customer': customer,'address': address,'payment_status': 'paid','items': d['cart'][:],'created_at': now(),'status': 'new'}; d['orders'].append(order); d['cart'] = []; log(d,'order','create',f'Order {order["id"]}'); save(d); return redirect(url_for('main.index'))

@bp.post('/orders/<int:order_id>/fail-payment')
def fail_payment(order_id):
    d = data(); order = next((o for o in d['orders'] if o['id']==order_id), None)
    if order: order['payment_status'] = 'unpaid'; order['status'] = 'payment_failed'; notify(d,'payment',f'Payment failed for order {order_id}','critical'); log(d,'order','payment_failed',str(order_id)); save(d)
    return redirect(url_for('main.index'))

@bp.post('/notifications/<int:index>/resolve')
def resolve_notification(index):
    d = data();
    if 0 <= index < len(d['notifications']): d['notifications'][index]['unresolved'] = False
    if 0 <= index < len(d['issues']): d['issues'][index]['unresolved'] = False
    save(d); return redirect(url_for('main.index'))

@bp.post('/import/products')
def import_products():
    d = data(); file = request.files.get('file')
    if not file: return 'missing file', 400
    text = file.stream.read().decode('utf-8-sig'); reader = csv.DictReader(io.StringIO(text)); rows = list(reader); summary = {'succeeded': 0, 'skipped': 0, 'needs_attention': 0, 'duplicates': 0}
    existing = {(p.get('name','').lower(), p.get('sku','').lower(), p.get('barcode','').lower()) for p in d['products']}
    for row in rows:
        key = (row.get('name','').lower(), row.get('sku','').lower(), row.get('barcode','').lower())
        if not row.get('name') or not row.get('price'):
            summary['needs_attention'] += 1; continue
        if key in existing:
            summary['duplicates'] += 1; summary['skipped'] += 1; continue
        d['products'].append({'id': len(d['products'])+1,'name': row.get('name','').strip(),'sku': row.get('sku','').strip(),'barcode': row.get('barcode','').strip(),'category': row.get('category','').strip(),'price': row.get('price','').strip(),'stock': int(row.get('stock') or 0),'available': True})
        summary['succeeded'] += 1
    d['import_history'].append({'time': now(), 'summary': summary})
    log(d,'import','products',str(summary)); save(d); return render_template('index.html', d=d, import_summary=summary)

@bp.get('/api/state')
def api_state(): return jsonify(data())
