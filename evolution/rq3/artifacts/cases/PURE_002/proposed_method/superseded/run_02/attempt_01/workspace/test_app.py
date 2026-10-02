import json
import threading
import time
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

import app


def setup_function(_):
    app.PRODUCTS.clear()
    app.ORDERS.clear()
    app.AUDIT_LOG.clear()
    app.COUNTERS['product'] = __import__('itertools').count(1)
    app.COUNTERS['order'] = __import__('itertools').count(1001)


def start_server():
    server = ThreadingHTTPServer(('127.0.0.1', 0), app.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.05)
    return server, server.server_address[1]


def request(port, method, path, body=None, headers=None):
    conn = HTTPConnection('127.0.0.1', port)
    headers = headers or {}
    if body is not None and 'Content-Type' not in headers:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    conn.request(method, path, body=body, headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, dict(resp.getheaders()), data


def test_add_and_browse_product():
    server, port = start_server()
    try:
        status, _, _ = request(port, 'POST', '/admin/products', body=json.dumps({'name': 'Widget', 'description': 'A thing', 'price': 9.99, 'quantity': 5}), headers={'Content-Type': 'application/json'})
        assert status == 201
        status, _, data = request(port, 'GET', '/store')
        assert status == 200
        assert b'Widget' in data
    finally:
        server.shutdown()


def test_unavailable_product_blocks_add_to_cart():
    server, port = start_server()
    try:
        request(port, 'POST', '/admin/products', body=json.dumps({'name': 'Sold out', 'description': '', 'price': 10, 'quantity': 0}), headers={'Content-Type': 'application/json'})
        status, _, data = request(port, 'POST', '/cart/add/1')
        assert status == 400
        assert b'out of stock' in data
    finally:
        server.shutdown()


def test_checkout_creates_order_and_reduces_stock():
    server, port = start_server()
    try:
        request(port, 'POST', '/admin/products', body=json.dumps({'name': 'Widget', 'description': 'A thing', 'price': 9.99, 'quantity': 5}), headers={'Content-Type': 'application/json'})
        request(port, 'POST', '/cart/add/1')
        status, _, data = request(port, 'POST', '/checkout')
        assert status == 200
        payload = json.loads(data)
        assert payload['status'] == 'confirmed'
        assert payload['payment_status'] == 'paid'
        assert app.PRODUCTS[1].quantity == 4
    finally:
        server.shutdown()


def test_cart_quantity_limit():
    server, port = start_server()
    try:
        request(port, 'POST', '/admin/products', body=json.dumps({'name': 'Widget', 'description': 'A thing', 'price': 9.99, 'quantity': 100}), headers={'Content-Type': 'application/json'})
        status, _, data = request(port, 'POST', '/cart/add/1', body='qty=11')
        assert status == 400
        assert b'exceeds maximum' in data
    finally:
        server.shutdown()
