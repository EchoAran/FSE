from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json, uuid

store = {
    "setup_complete": False,
    "settings": {"store_name": "", "contact_details": "", "currency": "", "tax_setting": "pre_tax", "shipping_methods": ["standard"], "payment_options": ["card"]},
    "products": {}, "customers": {}, "carts": {}, "orders": {}, "low_stock_threshold": 5,
}
ORDER_STATUSES = ["new", "paid", "packed", "shipped", "completed", "cancelled"]

def new_id(prefix): return f"{prefix}_{uuid.uuid4().hex[:10]}"
def j(body, code=200): return code, {"Content-Type": "application/json"}, json.dumps(body).encode()

def validate_address(addr):
    req = ["name", "street", "city", "postal_code", "country"]
    return all(addr.get(k) for k in req) and (addr.get("phone") or addr.get("email"))

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _read(self):
        l = int(self.headers.get("Content-Length", 0) or 0)
        return json.loads(self.rfile.read(l).decode() or "{}") if l else {}
    def _send(self, code, headers, body):
        self.send_response(code)
        for k, v in headers.items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/": return self._send(*j({"service": "GAMMA-J Web Store", "setup_complete": store["setup_complete"]}))
        if p == "/products": return self._send(*j(list(store["products"].values())))
        if p == "/warnings/low-stock": return self._send(*j([p for p in store["products"].values() if p["stock"] <= p["low_stock_threshold"]]))
        if p.startswith("/customers/") and p.endswith("/cart"):
            cid = p.split("/")[2]; return self._send(*j(store["carts"].get(cid, {})))
        self._send(*j({"error": "not_found"}, 404))
    def do_POST(self):
        p = urlparse(self.path).path; data = self._read()
        if p == "/setup":
            if not all(data.get(k) for k in ["store_name", "contact_details", "currency"]): return self._send(*j({"error": "missing_setup_fields"}, 400))
            store["settings"].update({"store_name": data["store_name"], "contact_details": data["contact_details"], "currency": data["currency"], "tax_setting": data.get("tax_setting", "pre_tax"), "shipping_methods": data.get("shipping_methods", ["standard"]), "payment_options": data.get("payment_options", ["card"])})
            store["setup_complete"] = True; return self._send(*j({"ok": True}))
        if p == "/products":
            if not store["setup_complete"]: return self._send(*j({"error": "store_not_setup"}, 400))
            if not data.get("name") or data.get("price") is None: return self._send(*j({"error": "missing_product_fields"}, 400))
            pid = new_id("prod"); store["products"][pid] = {"id": pid, "name": data["name"], "price": float(data["price"]), "stock": int(data.get("stock", 0)), "active": bool(data.get("active", True)), "low_stock_threshold": int(data.get("low_stock_threshold", store["low_stock_threshold"]))}; return self._send(*j(store["products"][pid], 201))
        if p == "/customers":
            if not store["setup_complete"]: return self._send(*j({"error": "store_not_setup"}, 400))
            if not data.get("name") or not data.get("email"): return self._send(*j({"error": "missing_customer_details"}, 400))
            if any(c["email"].lower() == data["email"].lower() for c in store["customers"].values()): return self._send(*j({"error": "duplicate_customer"}, 400))
            cid = new_id("cust"); store["customers"][cid] = {"id": cid, "name": data["name"], "email": data["email"], "status": data.get("status", "active")}; return self._send(*j(store["customers"][cid], 201))
        if p.startswith("/customers/") and p.endswith("/cart/items"):
            cid = p.split("/")[2]
            if cid not in store["customers"]: return self._send(*j({"error": "customer_not_found"}, 404))
            pid, qty = data.get("product_id"), int(data.get("quantity", 1))
            prod = store["products"].get(pid)
            if not prod or not prod["active"] or prod["stock"] < qty: return self._send(*j({"error": "product_unavailable"}, 400))
            cart = store["carts"].setdefault(cid, {}); cart[pid] = cart.get(pid, 0) + qty; return self._send(*j({"customer_id": cid, "cart": cart}))
        if p == "/checkout":
            cid = data.get("customer_id"); cust = store["customers"].get(cid)
            if not cust: return self._send(*j({"error": "customer_not_found"}, 404))
            if cust.get("status") != "active": return self._send(*j({"error": "customer_not_active"}, 400))
            if not validate_address(data.get("shipping_address", {})): return self._send(*j({"error": "invalid_shipping_address"}, 400))
            cart = store["carts"].get(cid, {})
            if not cart: return self._send(*j({"error": "empty_cart"}, 400))
            if data.get("payment_method", "card") not in store["settings"]["payment_options"]: return self._send(*j({"error": "payment_method_not_supported"}, 400))
            if data.get("shipping_method", "standard") not in store["settings"]["shipping_methods"]: return self._send(*j({"error": "shipping_method_not_supported"}, 400))
            items, total = [], 0.0
            for pid, qty in cart.items():
                prod = store["products"].get(pid)
                if not prod or not prod["active"] or prod["stock"] < qty: return self._send(*j({"error": "item_unavailable"}, 400))
                prod["stock"] -= qty; items.append({"product_id": pid, "quantity": qty, "unit_price": prod["price"]}); total += prod["price"] * qty
            oid = new_id("ord"); store["orders"][oid] = {"id": oid, "customer_id": cid, "items": items, "status": "new", "payment_method": data.get("payment_method", "card"), "shipping_method": data.get("shipping_method", "standard"), "shipping_address": data["shipping_address"], "total": round(total, 2)}; store["carts"][cid] = {}; return self._send(*j(store["orders"][oid], 201))
        if p.startswith("/orders/") and p.endswith("/status"):
            oid = p.split("/")[2]; order = store["orders"].get(oid)
            if not order: return self._send(*j({"error": "order_not_found"}, 404))
            st = data.get("status")
            if st not in ORDER_STATUSES: return self._send(*j({"error": "invalid_status"}, 400))
            order["status"] = st; return self._send(*j(order))
        self._send(*j({"error": "not_found"}, 404))

def main():
    ThreadingHTTPServer(("0.0.0.0", 8000), H).serve_forever()

if __name__ == "__main__": main()
