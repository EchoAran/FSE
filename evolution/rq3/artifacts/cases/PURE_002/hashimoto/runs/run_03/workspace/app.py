from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from dataclasses import dataclass, asdict, field
from typing import List
from uuid import uuid4
from datetime import datetime
import json

@dataclass
class Settings:
    store_name: str = ""
    contact_details: str = ""
    currency: str = ""
    tax_settings: str = ""
    shipping_methods: List[str] = field(default_factory=list)
    payment_options: List[str] = field(default_factory=list)
    business_details: str = ""
    live: bool = False

@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int
    active: bool = True
    low_stock_threshold: int = 5

@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: dict
    status: str = "active"

@dataclass
class Order:
    id: str
    customer_id: str
    items: List[dict]
    status: str = "new"
    shipping_method: str = "standard"
    payment_method: str = "card"
    total: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

STATE = {"settings": Settings(), "products": {}, "customers": {}, "orders": {}}


def customer_valid(address):
    required = ["name", "street", "city", "postal_code", "country"]
    return all(address.get(k) for k in required) and bool(address.get("phone") or address.get("email"))


def reset_state():
    STATE["settings"] = Settings()
    STATE["products"].clear()
    STATE["customers"].clear()
    STATE["orders"].clear()


def create_product(name, price, stock, active=True, low_stock_threshold=5):
    pid = str(uuid4())
    p = Product(pid, name, float(price), int(stock), bool(active), int(low_stock_threshold))
    STATE["products"][pid] = p
    return p


def create_customer(name, address, status="active"):
    if not customer_valid(address):
        raise ValueError("invalid customer")
    if any(c.email == address["email"] for c in STATE["customers"].values()):
        raise ValueError("duplicate customer")
    cid = str(uuid4())
    c = Customer(cid, name, address["email"], address, status=status)
    STATE["customers"][cid] = c
    return c


def checkout(customer_id, items, shipping_method="standard", payment_method="card"):
    customer = STATE["customers"].get(customer_id)
    if not customer:
        raise ValueError("customer required")
    if customer.status in ["pending", "blocked", "held"]:
        raise PermissionError("customer account not eligible")
    if not customer_valid(customer.address):
        raise ValueError("missing shipping details")
    total = 0.0
    for item in items:
        product = STATE["products"].get(item["product_id"])
        qty = int(item.get("qty", 0))
        if not product or not product.active:
            raise ValueError("product unavailable")
        if qty > product.stock:
            raise ValueError("insufficient stock")
        total += product.price * qty
    for item in items:
        STATE["products"][item["product_id"]].stock -= int(item.get("qty", 0))
    oid = str(uuid4())
    order = Order(oid, customer_id, items, shipping_method=shipping_method, payment_method=payment_method, total=round(total, 2))
    STATE["orders"][oid] = order
    return order


def set_status(order_id, status):
    order = STATE["orders"].get(order_id)
    if not order:
        raise KeyError("not found")
    allowed = ["new", "paid", "packed", "shipped", "completed", "cancelled"]
    if status not in allowed:
        raise ValueError("invalid status")
    if order.status == "shipped" and status == "cancelled":
        raise PermissionError("cannot cancel shipped order")
    order.status = status
    return order


def low_stock_warnings():
    return [asdict(p) for p in STATE["products"].values() if p.stock <= p.low_stock_threshold]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._send(200, {"service": "GAMMA-J Web Store", "ready": STATE["settings"].live})
        elif self.path == "/products":
            self._send(200, [asdict(p) for p in STATE["products"].values() if p.active])
        elif self.path == "/low-stock":
            self._send(200, {"warnings": low_stock_warnings(), "recipients": ["owner", "inventory"]})
        elif self.path == "/shipping-options":
            self._send(200, [{"method": "standard"}, {"method": "express"}])
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, format, *args):
        return


def run(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    run()
