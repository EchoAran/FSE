from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json
import itertools

state = {
    "store": {"name": None, "contact_details": None, "currency": None, "tax_settings": None, "shipping_methods": [], "payment_options": [], "legal_details": None, "go_live": False},
    "users": [], "products": [], "orders": [], "cart": []
}
ids = {"user": itertools.count(1), "product": itertools.count(1), "order": itertools.count(1)}
ROLE_OWNER, ROLE_SALES, ROLE_CUSTOMER = "owner", "sales", "customer"
STATUS_PENDING, STATUS_BLOCKED, STATUS_ACTIVE = "pending", "blocked", "active"
ORDER_STATUSES = ["new", "paid", "packed", "shipped", "completed", "cancelled"]


def j(data, code=200): return code, json.dumps(data).encode(), "application/json"
def err(code, msg): return code, json.dumps({"error": msg}).encode(), "application/json"

def find_user(uid): return next((u for u in state["users"] if u["id"] == uid), None)
def product_by_id(pid): return next((p for p in state["products"] if p["id"] == pid), None)
def order_by_id(oid): return next((o for o in state["orders"] if o["id"] == oid), None)
def core_settings_complete():
    s = state["store"]
    return all([s["name"], s["contact_details"], s["currency"], s["tax_settings"], s["shipping_methods"], s["payment_options"]])

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def send(self, code, body, ctype="application/json"):
        self.send_response(code); self.send_header("Content-Type", ctype); self.end_headers(); self.wfile.write(body)
    def read_json(self):
        l = int(self.headers.get("Content-Length", 0));
        return json.loads(self.rfile.read(l) or b"{}")
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health": self.send(*j({"status": "ok"}))
        elif path == "/products": self.send(*j([p for p in state["products"] if p.get("active", True)]))
        elif path.startswith("/cart/"):
            cid = int(path.split("/")[-1]);
            if not find_user(cid): self.send(*err(404, "User not found")); return
            self.send(*j([c for c in state["cart"] if c["customer_id"] == cid]))
        elif path.startswith("/orders/"):
            cid = int(path.split("/")[-1]);
            if not find_user(cid): self.send(*err(404, "User not found")); return
            self.send(*j([o for o in state["orders"] if o["customer_id"] == cid]))
        elif path == "/admin/state": self.send(*j(state))
        else: self.send(*err(404, "Not found"))
    def do_POST(self):
        path = urlparse(self.path).path; data = self.read_json()
        if path == "/setup":
            for k in ["name", "contact_details", "currency", "tax_settings", "shipping_methods", "payment_options"]:
                if k not in data: self.send(*err(400, f"Missing {k}")); return
            state["store"].update({k: data[k] for k in ["name", "contact_details", "currency", "tax_settings", "shipping_methods", "payment_options"]}); state["store"]["legal_details"] = data.get("legal_details"); state["store"]["go_live"] = core_settings_complete(); self.send(*j(state["store"]))
        elif path == "/users":
            role = data.get("role")
            if role not in {ROLE_OWNER, ROLE_SALES, ROLE_CUSTOMER}: self.send(*err(400, "Invalid role")); return
            if not data.get("name") or not data.get("email"): self.send(*err(400, "Incomplete user")); return
            if any(u["email"] == data["email"] for u in state["users"]): self.send(*err(409, "Duplicate email")); return
            u = {"id": next(ids["user"]), "name": data["name"], "email": data["email"], "role": role, "status": data.get("status", STATUS_ACTIVE if role != ROLE_CUSTOMER else STATUS_PENDING)}; state["users"].append(u); self.send(*j(u, 201))
        elif path == "/products":
            actor = find_user(data.get("actor_id"))
            if not actor or actor["role"] not in {ROLE_OWNER, ROLE_SALES}: self.send(*err(403, "Forbidden")); return
            if not data.get("active", True): self.send(*err(400, "Products must be active in catalog")); return
            if not data.get("name") or data.get("price") is None: self.send(*err(400, "Incomplete product")); return
            p = {"id": next(ids["product"]), "name": data["name"], "price": data["price"], "stock": data.get("stock", 0), "active": True, "low_stock_threshold": data.get("low_stock_threshold", 5)}; state["products"].append(p); self.send(*j(p, 201))
        elif path == "/cart":
            customer = find_user(data.get("customer_id"))
            if not customer or customer["role"] != ROLE_CUSTOMER or customer["status"] in {STATUS_PENDING, STATUS_BLOCKED}: self.send(*err(403, "Forbidden")); return
            p = product_by_id(data.get("product_id")); qty = int(data.get("quantity", 1))
            if not p or not p.get("active", True): self.send(*err(404, "Product not found")); return
            if qty <= 0 or p["stock"] < qty: self.send(*err(400, "Insufficient stock")); return
            state["cart"].append({"customer_id": customer["id"], "product_id": p["id"], "quantity": qty}); self.send(*j({"cart": state["cart"]}))
        elif path == "/checkout":
            customer = find_user(data.get("customer_id"))
            if not customer or customer["role"] != ROLE_CUSTOMER or customer["status"] in {STATUS_PENDING, STATUS_BLOCKED}: self.send(*err(403, "Forbidden")); return
            items = [c for c in state["cart"] if c["customer_id"] == customer["id"]]
            if not items: self.send(*err(400, "Empty cart")); return
            ship = data.get("shipping_address", {})
            req = ["name", "street_address", "city", "postal_code", "country"]
            if any(not ship.get(k) for k in req) or not (ship.get("phone") or ship.get("email")): self.send(*err(400, "Incomplete shipping address")); return
            total, order_items = 0, []
            for item in items:
                p = product_by_id(item["product_id"])
                if not p or p["stock"] < item["quantity"]: self.send(*err(400, "Item unavailable")); return
                p["stock"] -= item["quantity"]; line = p["price"] * item["quantity"]; total += line; order_items.append({"product_id": p["id"], "quantity": item["quantity"], "line_total": line})
            o = {"id": next(ids["order"]), "customer_id": customer["id"], "items": order_items, "shipping_address": ship, "payment_method": data.get("payment_method", "card"), "shipping_method": data.get("shipping_method", "standard"), "status": "new", "total": total}; state["orders"].append(o); state["cart"] = [c for c in state["cart"] if c["customer_id"] != customer["id"]]; self.send(*j(o, 201))
        else: self.send(*err(404, "Not found"))
    def do_PATCH(self):
        path = urlparse(self.path).path; data = self.read_json()
        if not path.startswith("/orders/"): self.send(*err(404, "Not found")); return
        oid = int(path.split("/")[-1]); order = order_by_id(oid)
        if not order: self.send(*err(404, "Not found")); return
        actor = find_user(data.get("actor_id"))
        if not actor: self.send(*err(403, "Forbidden")); return
        if actor["role"] == ROLE_CUSTOMER:
            if actor["id"] != order["customer_id"] or data.get("status") != "cancelled" or order["status"] == "shipped": self.send(*err(403, "Forbidden")); return
            order["status"] = "cancelled"
        else:
            if data.get("status") not in ORDER_STATUSES: self.send(*err(400, "Invalid status")); return
            if order["status"] in {"shipped", "completed"} and data.get("status") not in {"completed"}: self.send(*err(403, "Forbidden")); return
            order["status"] = data["status"]
        self.send(*j(order))

def run(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
