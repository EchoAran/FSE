import threading
import time
import urllib.request
import urllib.parse
from http.cookiejar import CookieJar
from urllib.request import build_opener, HTTPCookieProcessor

import server


def start_server():
    srv = server.ThreadingHTTPServer(('127.0.0.1', 8001), server.Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    time.sleep(0.2)
    return srv


def test_flow():
    srv = start_server()
    opener = build_opener(HTTPCookieProcessor(CookieJar()))
    body = opener.open('http://127.0.0.1:8001/products').read().decode()
    assert 'Products' in body
    pid = next(iter(server.PRODUCTS.keys()))
    opener.open(f'http://127.0.0.1:8001/cart/add/{pid}', data=b'')
    cart = opener.open('http://127.0.0.1:8001/cart').read().decode()
    assert 'Cart total' in cart
    data = urllib.parse.urlencode({'name':'A','email':'a@example.com','address':'X','contact_number':''}).encode()
    res = opener.open('http://127.0.0.1:8001/checkout', data=data).read().decode()
    assert 'Order placed successfully' in res
    srv.shutdown()

