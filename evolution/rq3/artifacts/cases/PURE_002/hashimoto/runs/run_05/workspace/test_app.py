import json
import pytest
from app import handle, reset_state

@pytest.fixture(autouse=True)
def _reset():
    reset_state()

def req(method, path, payload=None):
    body = json.dumps(payload).encode() if payload is not None else b""
    status, headers, data = handle(method, path, body.decode() if body else "")
    return status, json.loads(data.decode())

def test_setup_and_health():
    assert req("GET", "/health")[1] == {"ok": True}
    status, _ = req("POST", "/setup", {"name": "Shop", "contact_details": "x", "currency": "USD", "shipping_methods": ["standard"], "payment_options": ["card"]})
    assert status == 200
    assert req("GET", "/settings")[1]["live"] is True

def test_product_customer_cart_order_flow():
    req("POST", "/setup", {"name": "Shop", "contact_details": "x", "currency": "USD", "shipping_methods": ["standard"], "payment_options": ["card"]})
    pid = req("POST", "/products", {"role": "owner", "name": "Widget", "price": 10, "stock": 3})[1]["id"]
    cid = req("POST", "/customers", {"name": "Alice", "email": "a@example.com", "password": "pw"})[1]["id"]
    assert req("POST", f"/cart/{cid}/items", {"product_id": pid, "qty": 2})[0] == 200
    status, order = req("POST", "/orders", {"customer_id": cid, "shipping_method": "standard", "payment_method": "card", "shipping_address": {"name": "Alice", "street_address": "1 Main", "city": "Town", "postal_code": "12345", "country": "US", "email": "a@example.com"}})
    assert status == 201 and order["status"] == "paid"
    assert req("GET", "/low-stock")[1]

def test_checkout_validation():
    req("POST", "/setup", {"name": "Shop", "contact_details": "x", "currency": "USD", "shipping_methods": ["standard"], "payment_options": ["card"]})
    pid = req("POST", "/products", {"role": "owner", "name": "Widget", "price": 10, "stock": 1})[1]["id"]
    cid = req("POST", "/customers", {"name": "Alice", "email": "a@example.com", "password": "pw"})[1]["id"]
    req("POST", f"/cart/{cid}/items", {"product_id": pid, "qty": 1})
    assert req("POST", "/orders", {"customer_id": cid, "shipping_method": "standard", "payment_method": "card", "shipping_address": {"name": "Alice"}})[0] == 400
