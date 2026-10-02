from dataclasses import dataclass, field, asdict
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from json import dumps, loads
from typing import List
from urllib.parse import urlparse
from uuid import uuid4

@dataclass
class StoreSettings:
    name: str = ""
    contact_details: str = ""
    currency: str = "USD"
    tax_settings: str = "standard"
    shipping_methods: List[str] = field(default_factory=lambda: ["standard"])
    payment_options: List[str] = field(default_factory=lambda: ["card"])
    legal_details: str = ""
    live: bool = False

@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int
    active: bool = True
    low_stock_threshold: int = 5
    category: str = ""

@dataclass
class Customer:
    id: str
    name: str
    email: str
    password: str
    status: str = "active"
    address: dict = field(default_factory=dict)
    orders: List[str] = field(default_factory=list)

@dataclass
class Order:
    id: str
    customer_id: str
    items: List[dict]
    shipping_method: str
    payment_method: str
    status: str = "new"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    total: float = 0.0
    shipping_address: dict = field(default_factory=dict)

state = {
    "settings": StoreSettings(),
    "products": {},
    "customers": {},
    "carts": {},
    "orders": {},
}

def reset_state():
    state["settings"] = StoreSettings()
    state["products"].clear()
    state["customers"].clear()
    state["carts"].clear()
    state["orders"].clear()

def validate_customer_data(data):
    for f in ("name", "email", "password"):
        if not data.get(f):
            raise ValueError("missing customer details")
    if any(c.email == data["email"] for c in state["customers"].values()):
        raise ValueError("duplicate customer")

def validate_address(address):
    required = ["name", "street_address", "city", "postal_code", "country"]
    if not all(address.get(k) for k in required):
        raise ValueError("incomplete shipping address")
    if not (address.get("phone") or address.get("email")):
        raise ValueError("missing shipping contact")

def cart_for(customer_id):
    return state["carts"].setdefault(customer_id, [])

def json_response(status, payload):
    return status, {"Content-Type": "application/json"}, dumps(payload).encode()

def handle(method, path, body):
    data = loads(body) if body else {}
    parsed = urlparse(path)
    p = parsed.path
    if method == "GET" and p == "/health":
        return json_response(200, {"ok": True})
    if method == "GET" and p == "/settings":
        return json_response(200, asdict(state["settings"]))
    if method == "POST" and p == "/setup":
        s = state["settings"]
        for k in ["name", "contact_details", "currency", "tax_settings", "shipping_methods", "payment_options", "legal_details"]:
            if k in data:
                setattr(s, k, data[k])
        if s.name and s.contact_details and s.currency:
            s.live = True
        return json_response(200, asdict(s))
    if method == "POST" and p == "/products":
        if data.get("role") not in {"owner", "sales"}:
            return json_response(403, {"error": "forbidden"})
        if data.get("role") == "sales" and not data.get("active", True):
            return json_response(403, {"error": "forbidden"})
        prod = Product(id=str(uuid4()), name=data["name"], price=float(data["price"]), stock=int(data.get("stock", 0)), active=bool(data.get("active", True)), low_stock_threshold=int(data.get("low_stock_threshold", 5)), category=data.get("category", ""))
        state["products"][prod.id] = prod
        return json_response(201, asdict(prod))
    if method == "GET" and p == "/products":
        return json_response(200, [asdict(x) for x in state["products"].values() if x.active])
    if method == "PATCH" and p.startswith("/products/"):
        pid = p.split("/")[-1]
        prod = state["products"].get(pid)
        if not prod:
            return json_response(404, {"error": "not found"})
        if not prod.active and data.get("role") == "sales":
            return json_response(403, {"error": "forbidden"})
        for k in ["name", "price", "stock", "active", "low_stock_threshold", "category"]:
            if k in data:
                setattr(prod, k, data[k])
        return json_response(200, asdict(prod))
    if method == "POST" and p == "/customers":
        try:
            validate_customer_data(data)
        except ValueError as e:
            return json_response(400 if "missing" in str(e) else 409, {"error": str(e)})
        cust = Customer(id=str(uuid4()), name=data["name"], email=data["email"], password=data["password"], status=data.get("status", "active"), address=data.get("address", {}))
        state["customers"][cust.id] = cust
        return json_response(201, {"id": cust.id, "status": cust.status})
    if method == "POST" and p.startswith("/cart/") and p.endswith("/items"):
        customer_id = p.split("/")[2]
        prod = state["products"].get(data["product_id"])
        if not prod or not prod.active:
            return json_response(404, {"error": "not found"})
        qty = int(data.get("qty", 1))
        if qty > prod.stock:
            return json_response(400, {"error": "insufficient stock"})
        cart_for(customer_id).append({"product_id": prod.id, "qty": qty})
        return json_response(200, cart_for(customer_id))
    if method == "GET" and p.startswith("/cart/"):
        customer_id = p.split("/")[2]
        return json_response(200, cart_for(customer_id))
    if method == "POST" and p == "/orders":
        customer_id = data["customer_id"]
        customer = state["customers"].get(customer_id)
        if not customer or customer.status != "active":
            return json_response(403, {"error": "forbidden"})
        try:
            validate_address(data.get("shipping_address", {}))
        except ValueError as e:
            return json_response(400, {"error": str(e)})
        items = cart_for(customer_id)
        if not items:
            return json_response(400, {"error": "empty cart"})
        shipping_method = data.get("shipping_method", "standard")
        payment_method = data.get("payment_method", "card")
        if shipping_method not in state["settings"].shipping_methods:
            return json_response(400, {"error": "shipping method unavailable"})
        if payment_method not in state["settings"].payment_options:
            return json_response(400, {"error": "payment method unavailable"})
        total = 0.0
        for item in items:
            prod = state["products"].get(item["product_id"])
            if not prod or prod.stock < item["qty"]:
                return json_response(400, {"error": "item unavailable"})
            total += prod.price * item["qty"]
        order = Order(id=str(uuid4()), customer_id=customer_id, items=items.copy(), shipping_method=shipping_method, payment_method=payment_method, total=total, shipping_address=data["shipping_address"], status="paid")
        for item in items:
            state["products"][item["product_id"]].stock -= item["qty"]
        state["orders"][order.id] = order
        customer.orders.append(order.id)
        state["carts"][customer_id] = []
        return json_response(201, asdict(order))
    if method == "PATCH" and p.startswith("/orders/"):
        oid = p.split("/")[-1]
        order = state["orders"].get(oid)
        if not order:
            return json_response(404, {"error": "not found"})
        if data.get("status") and data.get("role") in {"owner", "sales"}:
            order.status = data["status"]
            return json_response(200, asdict(order))
        return json_response(403, {"error": "forbidden"})
    if method == "GET" and p == "/low-stock":
        warnings = []
        for prod in state["products"].values():
            if prod.stock <= prod.low_stock_threshold:
                warnings.append({"product_id": prod.id, "name": prod.name, "stock": prod.stock})
        return json_response(200, warnings)
    return json_response(404, {"error": "not found"})

class Handler(BaseHTTPRequestHandler):
    def do_GET(self): self.respond()
    def do_POST(self): self.respond()
    def do_PATCH(self): self.respond()
    def respond(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode() if length else ""
        status, headers, payload = handle(self.command, self.path, body)
        self.send_response(status)
        for k, v in headers.items(): self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload)

if __name__ == "__main__":
    print("Serving on http://0.0.0.0:8000")
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
