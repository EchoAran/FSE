from __future__ import annotations

import json
import os
import re
import uuid
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse


@dataclass
class Product:
    id: str
    name: str
    description: str
    price: Optional[float]
    quantity: int
    active: bool = True
    category: str = "General"
    main_image: Optional[str] = None
    additional_images: List[str] = field(default_factory=list)
    min_qty: int = 1
    max_qty: Optional[int] = None

    def purchasable(self) -> bool:
        return bool(self.active and self.price is not None and self.price >= 0 and self.quantity > 0)


@dataclass
class Customer:
    id: str
    email: str
    name: str
    status: str = "active"


@dataclass
class CartItem:
    product_id: str
    quantity: int
    unit_price: float


@dataclass
class Order:
    id: str
    customer_id: str
    items: List[CartItem]
    status: str = "pending"
    payment_status: str = "pending"
    shipping_address: Dict[str, str] = field(default_factory=dict)
    total: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


STORE = {"catalog_ready": False, "products": {}, "customers": {}, "carts": {}, "orders": {}, "audit_log": []}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def audit(actor: str, action: str, before: Any = None, after: Any = None) -> None:
    STORE["audit_log"].append({"who": actor, "what": action, "when": now_iso(), "before": before, "after": after})


def product_to_dict(p: Product) -> Dict[str, Any]:
    return {"id": p.id, "name": p.name, "description": p.description, "price": p.price, "quantity": p.quantity, "active": p.active, "category": p.category, "main_image": p.main_image or "/static/placeholder.png", "additional_images": p.additional_images, "purchasable": p.purchasable(), "min_qty": p.min_qty, "max_qty": p.max_qty}


def validate_address(address: Dict[str, Any]) -> Optional[str]:
    required = ["street", "city", "postal_code", "country"]
    missing = [f for f in required if not str(address.get(f, "")).strip()]
    return f"Missing address fields: {', '.join(missing)}" if missing else None


def cart_for(customer_id: str) -> List[CartItem]:
    return STORE["carts"].setdefault(customer_id, [])


def recalc_cart_errors(customer_id: str) -> List[str]:
    errors: List[str] = []
    for item in cart_for(customer_id):
        p = STORE["products"].get(item.product_id)
        if not p:
            errors.append(f"Product {item.product_id} no longer exists")
            continue
        if not p.purchasable():
            errors.append(f"{p.name} is unavailable")
        if item.quantity < p.min_qty:
            errors.append(f"{p.name} minimum quantity is {p.min_qty}")
        if p.max_qty is not None and item.quantity > p.max_qty:
            errors.append(f"{p.name} maximum quantity is {p.max_qty}")
        if item.quantity > p.quantity:
            errors.append(f"{p.name} only has {p.quantity} available")
    return errors


def read_json(handler: BaseHTTPRequestHandler) -> Dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length).decode("utf-8") if length else "{}"
    return json.loads(raw or "{}")


def send(handler: BaseHTTPRequestHandler, code: int, payload: Dict[str, Any]) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class StoreHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        if path == "/health":
            return send(self, 200, {"status": "ok"})
        if path == "/products":
            category = qs.get("category", [None])[0]
            q = (qs.get("q", [""])[0]).lower()
            results = []
            for p in STORE["products"].values():
                if category and p.category != category:
                    continue
                if q and q not in p.name.lower() and q not in p.description.lower():
                    continue
                results.append(product_to_dict(p))
            return send(self, 200, {"catalog_ready": STORE["catalog_ready"], "products": results})
        if path.startswith("/products/"):
            p = STORE["products"].get(path.split("/")[-1])
            return send(self, 200, product_to_dict(p)) if p else send(self, 404, {"error": "Not found"})
        if path.startswith("/cart/"):
            customer_id = path.split("/")[2]
            items = []
            total = 0.0
            for item in cart_for(customer_id):
                p = STORE["products"].get(item.product_id)
                if not p:
                    continue
                line = item.quantity * item.unit_price
                total += line
                items.append({"product_id": item.product_id, "name": p.name, "quantity": item.quantity, "unit_price": item.unit_price, "line_total": line})
            return send(self, 200, {"items": items, "total": total, "errors": recalc_cart_errors(customer_id)})
        if path.startswith("/orders/"):
            order = STORE["orders"].get(path.split("/")[-1])
            return send(self, 200, {"order_number": order.id, "customer_id": order.customer_id, "items": [{"product_id": i.product_id, "quantity": i.quantity, "unit_price": i.unit_price} for i in order.items], "total": order.total, "status": order.status, "payment_status": order.payment_status, "shipping_details": order.shipping_address}) if order else send(self, 404, {"error": "Not found"})
        if path == "/audit":
            return send(self, 200, {"entries": STORE["audit_log"]})
        send(self, 404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        data = read_json(self)
        if path == "/admin/products":
            for field_name in ["name", "description", "category"]:
                if not data.get(field_name):
                    return send(self, 400, {"error": f"Missing {field_name}"})
            try:
                price = data.get("price")
                price = None if price in (None, "") else float(price)
                quantity = int(data.get("quantity", 0))
                min_qty = int(data.get("min_qty", 1))
                max_qty = data.get("max_qty")
                max_qty = None if max_qty in (None, "") else int(max_qty)
            except ValueError:
                return send(self, 400, {"error": "Invalid numeric value"})
            if data.get("main_image") and not re.search(r"\.(jpg|jpeg|png)$", data["main_image"], re.I):
                return send(self, 400, {"error": "Invalid image format"})
            pid = str(uuid.uuid4())
            p = Product(pid, data["name"], data["description"], price, quantity, bool(data.get("active", True)), data["category"], data.get("main_image"), list(data.get("additional_images", []))[:3], min_qty, max_qty)
            STORE["products"][pid] = p
            audit("staff", "add_product", None, product_to_dict(p))
            return send(self, 201, product_to_dict(p))
        if path.startswith("/admin/products/"):
            product_id = path.split("/")[-1]
            p = STORE["products"].get(product_id)
            if not p:
                return send(self, 404, {"error": "Not found"})
            before = product_to_dict(p)
            for k in ["name", "description", "category"]:
                if k in data and data[k]: setattr(p, k, data[k])
            if "price" in data: p.price = None if data["price"] in (None, "") else float(data["price"])
            if "quantity" in data: p.quantity = int(data["quantity"])
            if "active" in data: p.active = bool(data["active"])
            if "main_image" in data:
                if data["main_image"] and not re.search(r"\.(jpg|jpeg|png)$", data["main_image"], re.I): return send(self, 400, {"error": "Invalid image format"})
                p.main_image = data["main_image"]
            if "additional_images" in data: p.additional_images = list(data["additional_images"] )[:3]
            after = product_to_dict(p)
            audit("staff", "update_product", before, after)
            return send(self, 200, after)
        if path == "/customers":
            if not data.get("email") or not data.get("name"):
                return send(self, 400, {"error": "Missing customer fields"})
            cid = str(uuid.uuid4())
            c = Customer(cid, data["email"], data["name"])
            STORE["customers"][cid] = c
            audit("staff", "create_customer", None, data)
            return send(self, 201, {"id": cid, "email": c.email, "name": c.name, "status": c.status})
        if path.startswith("/cart/") and path.endswith("/items"):
            customer_id = path.split("/")[2]
            if customer_id not in STORE["customers"]:
                return send(self, 404, {"error": "Customer not found"})
            p = STORE["products"].get(data.get("product_id"))
            if not p:
                return send(self, 404, {"error": "Product not found"})
            if not p.purchasable():
                return send(self, 400, {"error": "Product unavailable"})
            qty = int(data.get("quantity", 1))
            if qty < p.min_qty or (p.max_qty is not None and qty > p.max_qty): return send(self, 400, {"error": "Quantity outside limits"})
            if qty > p.quantity: return send(self, 400, {"error": "Insufficient stock"})
            cart_for(customer_id).append(CartItem(p.id, qty, p.price or 0.0))
            return send(self, 201, {"status": "added"})
        if path == "/checkout":
            customer_id = data.get("customer_id")
            if customer_id not in STORE["customers"]:
                return send(self, 404, {"error": "Customer not found"})
            addr_error = validate_address(data.get("shipping_address", {}))
            if addr_error:
                return send(self, 400, {"error": addr_error})
            errors = recalc_cart_errors(customer_id)
            if errors:
                return send(self, 400, {"error": "Cart has issues", "issues": errors})
            items = cart_for(customer_id)
            if not items:
                return send(self, 400, {"error": "Cart is empty"})
            total = sum(i.quantity * i.unit_price for i in items)
            oid = str(uuid.uuid4())
            order = Order(oid, customer_id, deepcopy(items), total=total, shipping_address=data["shipping_address"])
            STORE["orders"][oid] = order
            return send(self, 201, {"order_number": oid, "items": [{"product_id": i.product_id, "quantity": i.quantity, "unit_price": i.unit_price} for i in items], "total": total, "shipping_details": data["shipping_address"], "payment_status": order.payment_status, "status": order.status})
        if path.startswith("/orders/") and path.endswith("/pay"):
            order_id = path.split("/")[2]
            order = STORE["orders"].get(order_id)
            if not order:
                return send(self, 404, {"error": "Not found"})
            method = data.get("payment_method", "card")
            if data.get("simulate_failure"):
                order.payment_status = "failed"
                return send(self, 200, {"status": "failure", "message": "Payment declined by provider", "next_steps": ["try again", "choose a different payment method", "review order"]})
            order.payment_status = "paid"
            order.status = "confirmed"
            return send(self, 200, {"status": "success", "message": f"Payment accepted via {method}", "order_status": order.status})
        if path == "/admin/catalog/ready":
            STORE["catalog_ready"] = True
            audit("staff", "mark_catalog_ready", False, True)
            return send(self, 200, {"catalog_ready": True})
        send(self, 404, {"error": "Not found"})

    def log_message(self, format, *args):
        return


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    ThreadingHTTPServer((host, port), StoreHandler).serve_forever()


if __name__ == "__main__":
    run_server(port=int(os.environ.get("PORT", "8000")))
