import threading
import time
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
import app


def start_server():
    server = ThreadingHTTPServer(('127.0.0.1', 8001), app.App)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    time.sleep(0.2)
    return server


def get(path, headers=None):
    conn = HTTPConnection('127.0.0.1', 8001)
    conn.request('GET', path, headers=headers or {})
    res = conn.getresponse()
    body = res.read().decode()
    return res, body


def post(path, body, headers=None):
    conn = HTTPConnection('127.0.0.1', 8001)
    headers = headers or {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    conn.request('POST', path, body=body, headers=headers)
    res = conn.getresponse()
    data = res.read().decode()
    return res, data


server = start_server()
try:
    res, body = get('/')
    assert res.status == 200 and 'Starter Coffee Mug' in body
    res, body = get('/?name=notebook')
    assert 'Welcome Notebook' in body and 'Starter Coffee Mug' not in body

    res, _ = post('/cart/add', 'product_id=1')
    assert res.status == 302
    res, body = get('/cart', headers={'Cookie': 'cart={"1": 1}'})
    assert 'Cart total' in body

    res, body = post('/checkout', 'name=Ada&email=ada@example.com&address=42+Road', headers={'Cookie': 'cart={"1": 1}'})
    assert res.status == 200 and 'Order confirmed' in body

    res, body = get('/orders')
    assert 'Order History' in body

    res, body = get('/staff')
    assert 'Basic Sales Report' in body
finally:
    server.shutdown()
