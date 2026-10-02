from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from itertools import count
from typing import Any

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float | None
    quantity: int
    category: str = "General"
    active: bool = True
    images: list[str] = field(default_factory=list)
    min_qty: int = 1
    max_qty: int | None = None

    def purchasable(self) -> tuple[bool, str]:
        if not self.active:
            return False, "Product is inactive"
        if self.price is None or self.price <= 0:
            return False, "Price is missing or invalid"
        if self.quantity <= 0:
            return False, "Out of stock"
        return True, ""


@dataclass
class Order:
    id: int
    items: list[dict[str, Any]]
    shipping_address: str
    payment_method: str
    status: str = "pending"
    payment_status: str = "unpaid"
    total: float = 0.0
    created_at: str = field(default_factory=now_iso)
    customer_email: str = "customer@example.com"


@dataclass
class CustomerAccount:
    id: int
    name: str
    email: str
    status: str = "active"
    review_status: str = "approved"
    notes: str = ""


class StoreState:
    def __init__(self) -> None:
        self.products: dict[int, Product] = {}
        self.orders: dict[int, Order] = {}
        self.customers: dict[int, CustomerAccount] = {}
        self.audit_log: list[dict[str, Any]] = []
        self.catalog_ready = False
        self.product_ids = count(1)
        self.order_ids = count(1)
        self.customer_ids = count(1)

    def audit(self, actor: str, action: str, before: Any = None, after: Any = None) -> None:
        self.audit_log.append({
            "when": now_iso(),
            "who": actor,
            "action": action,
            "before": before,
            "after": after,
        })


state = StoreState()
state.products[1] = Product(id=1, name="Sample T-Shirt", description="Comfortable cotton shirt", price=19.99, quantity=10, category="Apparel")
state.products[2] = Product(id=2, name="Coffee Mug", description="Ceramic mug", price=9.5, quantity=0, category="Home")
state.product_ids = count(3)
state.customers[1] = CustomerAccount(id=1, name="Jane Customer", email="jane@example.com")
state.customer_ids = count(2)


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"

    def cart() -> list[dict[str, Any]]:
        return session.setdefault("cart", [])

    @app.context_processor
    def inject_globals() -> dict[str, Any]:
        return {"catalog_ready": state.catalog_ready, "current_cart_count": len(session.get("cart", []))}

    @app.get("/")
    def index():
        products = list(state.products.values())
        q = request.args.get("q", "").strip().lower()
        category = request.args.get("category", "").strip().lower()
        filtered = []
        for p in products:
            if q and q not in p.name.lower() and q not in p.description.lower():
                continue
            if category and category != p.category.lower():
                continue
            filtered.append(p)
        return render_template("index.html", products=filtered, categories=sorted({p.category for p in products}))

    @app.get("/product/<int:pid>")
    def product_detail(pid: int):
        product = state.products.get(pid) or abort(404)
        purchasable, reason = product.purchasable()
        return render_template("product.html", product=product, purchasable=purchasable, reason=reason)

    @app.post("/cart/add/<int:pid>")
    def add_to_cart(pid: int):
        product = state.products.get(pid) or abort(404)
        purchasable, reason = product.purchasable()
        if not purchasable:
            flash(f"Cannot add product: {reason}")
            return redirect(url_for("product_detail", pid=pid))
        qty = int(request.form.get("qty", "1"))
        if qty < product.min_qty or (product.max_qty is not None and qty > product.max_qty):
            flash("Quantity is outside allowed limits.")
            return redirect(url_for("product_detail", pid=pid))
        c = cart()
        c.append({"product_id": pid, "qty": qty})
        session["cart"] = c
        flash("Added to cart")
        return redirect(url_for("view_cart"))

    @app.get("/cart")
    def view_cart():
        items = []
        for line in session.get("cart", []):
            p = state.products.get(line["product_id"])
            if p:
                items.append({"product": p, "qty": line["qty"], "line_total": (p.price or 0) * line["qty"]})
        total = sum(i["line_total"] for i in items)
        return render_template("cart.html", items=items, total=total)

    @app.post("/checkout")
    def checkout():
        cart_items = session.get("cart", [])
        if not cart_items:
            flash("Cart is empty")
            return redirect(url_for("index"))
        shipping_address = request.form.get("shipping_address", "").strip()
        payment_method = request.form.get("payment_method", "").strip() or "trusted-provider"
        email = request.form.get("email", "customer@example.com").strip() or "customer@example.com"
        if len(shipping_address.split()) < 3:
            flash("Shipping address is incomplete.")
            return redirect(url_for("view_cart"))
        items = []
        total = 0.0
        for line in cart_items:
            product = state.products.get(line["product_id"])
            if not product:
                flash("A cart item is no longer available.")
                return redirect(url_for("view_cart"))
            purchasable, reason = product.purchasable()
            if not purchasable:
                flash(f"Checkout blocked: {reason}")
                return redirect(url_for("view_cart"))
            if line["qty"] > product.quantity:
                flash(f"Not enough stock for {product.name}")
                return redirect(url_for("view_cart"))
            line_total = (product.price or 0) * line["qty"]
            total += line_total
            items.append({"product_id": product.id, "name": product.name, "qty": line["qty"], "price": product.price, "line_total": line_total})

        if request.form.get("payment_result") == "fail":
            flash("Payment failed. Please try again or choose a different payment method.")
            return redirect(url_for("view_cart"))

        order = Order(id=next(state.order_ids), items=items, shipping_address=shipping_address, payment_method=payment_method, payment_status="paid", status="confirmed", total=total, customer_email=email)
        state.orders[order.id] = order
        for line in cart_items:
            state.products[line["product_id"]].quantity -= line["qty"]
        session["cart"] = []
        state.audit("system", "create_order", before=None, after=asdict(order))
        return render_template("confirmation.html", order=order)

    @app.get("/admin")
    def admin_home():
        return render_template("admin.html", products=list(state.products.values()), orders=list(state.orders.values()), customers=list(state.customers.values()), audit_log=reversed(state.audit_log), catalog_ready=state.catalog_ready)

    @app.post("/admin/product")
    def admin_add_product():
        name = request.form.get("name", "").strip()
        price_raw = request.form.get("price", "").strip()
        qty = int(request.form.get("quantity", "0"))
        if not name:
            flash("Product name is required")
            return redirect(url_for("admin_home"))
        try:
            price = float(price_raw)
        except ValueError:
            price = None
        p = Product(id=next(state.product_ids), name=name, description=request.form.get("description", ""), price=price, quantity=qty, category=request.form.get("category", "General"))
        state.products[p.id] = p
        state.audit("staff", "add_product", before=None, after=asdict(p))
        flash("Product added")
        return redirect(url_for("admin_home"))

    @app.post("/admin/catalog/ready")
    def mark_catalog_ready():
        state.catalog_ready = True
        state.audit("staff", "mark_catalog_ready")
        flash("Catalog marked ready")
        return redirect(url_for("admin_home"))

    @app.post("/admin/order/<int:oid>/status")
    def update_order_status(oid: int):
        order = state.orders.get(oid) or abort(404)
        new_status = request.form.get("status", "").strip()
        allowed = {
            "pending": ["confirmed", "on_hold", "canceled"],
            "confirmed": ["fulfillment", "on_hold", "canceled"],
            "on_hold": ["confirmed", "rejected"],
            "fulfillment": ["shipped"],
            "canceled": [],
            "rejected": [],
            "shipped": [],
        }
        if new_status not in allowed.get(order.status, []):
            flash(f"Invalid status transition from {order.status} to {new_status}.")
            return redirect(url_for("admin_home"))
        before = asdict(order)
        order.status = new_status
        state.audit("staff", "update_order_status", before=before, after=asdict(order))
        flash("Order status updated")
        return redirect(url_for("admin_home"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
