import json
import threading
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from app import STORE, run_server


def request(method, path, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = Request(f"http://127.0.0.1:8765{path}", data=body, method=method, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=3) as resp:
            return resp.status, json.loads(resp.read().decode())
    except HTTPError as e:
        return e.code, json.loads(e.read().decode())


def reset():
    STORE["catalog_ready"] = False
    STORE["products"] = {}
    STORE["customers"] = {}
    STORE["carts"] = {}
    STORE["orders"] = {}
    STORE["audit_log"] = []


def main():
    reset()
    t = threading.Thread(target=run_server, kwargs={"host": "127.0.0.1", "port": 8765}, daemon=True)
    t.start()
    time.sleep(0.2)
    assert request("GET", "/health")[0] == 200
    code, prod = request("POST", "/admin/products", {"name": "Widget", "description": "A useful item", "price": 9.99, "quantity": 5, "category": "General"})
    assert code == 201
    code, cust = request("POST", "/customers", {"email": "a@example.com", "name": "Alice"})
    assert code == 201
    code, _ = request("POST", f"/cart/{cust['id']}/items", {"product_id": prod["id"], "quantity": 2})
    assert code == 201
    code, checkout = request("POST", "/checkout", {"customer_id": cust["id"], "shipping_address": {"street": "1 Main", "city": "Town", "postal_code": "12345", "country": "US"}})
    assert code == 201
    code, pay = request("POST", f"/orders/{checkout['order_number']}/pay", {"payment_method": "card"})
    assert code == 200 and pay["status"] == "success"
    code, order = request("GET", f"/orders/{checkout['order_number']}")
    assert code == 200 and order["status"] == "confirmed" and order["payment_status"] == "paid"
    code, _ = request("POST", "/admin/products", {"name": "Out", "description": "No stock", "price": 3.0, "quantity": 0, "category": "General"})
    assert code == 201
    code, badcust = request("POST", "/customers", {"email": "b@example.com", "name": "Bob"})
    assert code == 201
    code, resp = request("POST", f"/cart/{badcust['id']}/items", {"product_id": list(STORE['products'].keys())[-1], "quantity": 1})
    assert code == 400
    code, audit = request("GET", "/audit")
    assert code == 200 and len(audit["entries"]) >= 2
    print("OK")


if __name__ == "__main__":
    main()
