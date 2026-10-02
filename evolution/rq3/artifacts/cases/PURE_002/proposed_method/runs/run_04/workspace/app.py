from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json
from datetime import datetime
from uuid import uuid4

state = {
    "catalog_ready": False,
    "products": {},
    "orders": {},
    "audit": [],
    "carts": {},
}

VALID_STATUSES = ["pending", "review", "approved", "rejected", "fulfillment", "shipped", "canceled"]
ALLOWED_TRANSITIONS = {
    "pending": {"review", "approved", "rejected", "canceled"},
    "review": {"approved", "rejected", "pending", "canceled"},
    "approved": {"fulfillment", "shipped", "canceled"},
    "rejected": set(),
    "fulfillment": {"shipped", "canceled"},
    "shipped": set(),
    "canceled": set(),
}


def now():
    return datetime.utcnow().isoformat() + "Z"


def audit(action, actor, before, after):
    state["audit"].append({"id": str(uuid4()), "time": now(), "actor": actor, "action": action, "before": before, "after": after})


def product_purchasable(product):
    if not product.get("active", True):
        return False, "Product is inactive"
    if not product.get("price") or product.get("price", 0) <= 0:
        return False, "Product price is missing or invalid"
    if product.get("stock_control", True) and product.get("stock", 0) <= 0:
        return False, "Product is out of stock"
    if not state["catalog_ready"]:
        return False, "Catalog is not yet ready"
    return True, ""


def validate_product(payload):
    for key in ["name", "price"]:
        if key not in payload or payload[key] in [None, ""]:
            return f"Missing required field: {key}"
    if not isinstance(payload["price"], (int, float)) or payload["price"] <= 0:
        return "Price must be a positive number"
    if "stock" in payload and (not isinstance(payload["stock"], int) or payload["stock"] < 0):
        return "Stock must be a non-negative integer"
    return None


def json_response(handler, code, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            return json_response(self, 200, {"message": "GAMMA-J Web Store", "catalog_ready": state["catalog_ready"]})
        if path == "/products":
            products = []
            for product in state["products"].values():
                purchasable, reason = product_purchasable(product)
                p = dict(product)
                p["purchasable"] = purchasable
                if not purchasable:
                    p["unavailable_reason"] = reason
                products.append(p)
            return json_response(self, 200, products)
        if path.startswith("/cart/"):
            customer_id = path.split("/")[2]
            cart = state["carts"].get(customer_id, {})
            items, total = [], 0.0
            for pid, qty in cart.items():
                product = state["products"].get(pid)
                if product:
                    line = product["price"] * qty
                    total += line
                    items.append({"product_id": pid, "name": product["name"], "quantity": qty, "price": product["price"], "line_total": line})
            return json_response(self, 200, {"customer_id": customer_id, "items": items, "total": total})
        if path.startswith("/orders/"):
            order_id = path.split("/")[2]
            order = state["orders"].get(order_id)
            return json_response(self, 200 if order else 404, order or {"error": "Order not found"})
        if path == "/audit":
            return json_response(self, 200, state["audit"])
        return json_response(self, 404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        data = self.read_json()
        if path == "/admin/catalog/ready":
            before = {"catalog_ready": state["catalog_ready"]}
            state["catalog_ready"] = bool(data.get("ready", True))
            audit("catalog_ready", data.get("actor", "system"), before, {"catalog_ready": state["catalog_ready"]})
            return json_response(self, 200, {"catalog_ready": state["catalog_ready"]})
        if path == "/admin/products":
            err = validate_product(data)
            if err:
                return json_response(self, 400, {"error": err})
            pid = str(uuid4())
            product = {"id": pid, "name": data["name"], "description": data.get("description", ""), "price": float(data["price"]), "stock": int(data.get("stock", 0)), "active": bool(data.get("active", True)), "stock_control": bool(data.get("stock_control", True)), "category": data.get("category", "Uncategorized"), "images": data.get("images", []), "min_qty": int(data.get("min_qty", 1)), "max_qty": data.get("max_qty")}
            state["products"][pid] = product
            audit("create_product", data.get("actor", "staff"), None, product)
            return json_response(self, 201, product)
        if path.startswith("/cart/") and path.endswith("/items"):
            customer_id = path.split("/")[2]
            pid = data.get("product_id")
            qty = int(data.get("quantity", 1))
            if qty <= 0:
                return json_response(self, 400, {"error": "Quantity must be positive"})
            product = state["products"].get(pid)
            if not product:
                return json_response(self, 404, {"error": "Product not found"})
            purchasable, reason = product_purchasable(product)
            if not purchasable:
                return json_response(self, 400, {"error": reason})
            cart = state["carts"].setdefault(customer_id, {})
            cart[pid] = cart.get(pid, 0) + qty
            max_qty = product.get("max_qty")
            if max_qty is not None and cart[pid] > max_qty:
                cart[pid] -= qty
                return json_response(self, 400, {"error": f"Cart exceeds max quantity for {product['name']}"})
            return json_response(self, 200, {"customer_id": customer_id, "items": cart})
        if path.startswith("/checkout/"):
            customer_id = path.split("/")[2]
            cart = state["carts"].get(customer_id, {})
            if not cart:
                return json_response(self, 400, {"error": "Cart is empty"})
            address = data.get("shipping_address", {})
            for field in ["street", "city", "postal_code", "country"]:
                if not address.get(field):
                    return json_response(self, 400, {"error": f"Shipping address missing {field}"})
            items, total = [], 0.0
            for pid, qty in cart.items():
                product = state["products"].get(pid)
                if not product:
                    return json_response(self, 400, {"error": "Product missing from catalog"})
                purchasable, reason = product_purchasable(product)
                if not purchasable:
                    return json_response(self, 400, {"error": reason})
                if product.get("stock_control", True) and product["stock"] < qty:
                    return json_response(self, 400, {"error": f"Insufficient stock for {product['name']}"})
                items.append({"product_id": pid, "name": product["name"], "quantity": qty, "price": product["price"]})
                total += product["price"] * qty
            order_id = str(uuid4())
            order = {"id": order_id, "customer_id": customer_id, "items": items, "total": total, "status": "pending", "payment_status": "unpaid", "shipping_address": address, "created_at": now()}
            state["orders"][order_id] = order
            state["carts"][customer_id] = {}
            return json_response(self, 201, order)
        if path.startswith("/orders/") and path.endswith("/pay"):
            order_id = path.split("/")[2]
            order = state["orders"].get(order_id)
            if not order:
                return json_response(self, 404, {"error": "Order not found"})
            if data.get("simulate_failure"):
                order["payment_status"] = "failed"
                order["status"] = "pending"
                return json_response(self, 402, {"status": "failure", "message": "Payment failed. You can retry or choose another method.", "payment_method": data.get("payment_method", "trusted_provider")})
            order["payment_status"] = "paid"
            order["status"] = "approved"
            return json_response(self, 200, {"status": "success", "message": "Payment accepted and order confirmed.", "order_id": order_id, "payment_method": data.get("payment_method", "trusted_provider")})
        if path.startswith("/orders/") and path.endswith("/status"):
            order_id = path.split("/")[2]
            order = state["orders"].get(order_id)
            if not order:
                return json_response(self, 404, {"error": "Order not found"})
            new_status = data.get("status")
            if new_status not in VALID_STATUSES:
                return json_response(self, 400, {"error": "Unknown order status"})
            cur = order["status"]
            if new_status not in ALLOWED_TRANSITIONS.get(cur, set()):
                return json_response(self, 400, {"error": f"Cannot change order from {cur} to {new_status}"})
            if new_status == "fulfillment" and order.get("payment_status") != "paid":
                return json_response(self, 400, {"error": "Unpaid order cannot move into fulfillment"})
            before = dict(order)
            order["status"] = new_status
            audit("change_order_status", data.get("actor", "staff"), before, dict(order))
            return json_response(self, 200, order)
        return json_response(self, 404, {"error": "Not found"})


def main():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("Serving on http://127.0.0.1:8000", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
