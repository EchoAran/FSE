from flask import Flask, request, redirect, url_for, render_template_string, abort
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import itertools

app = Flask(__name__)
app.secret_key = "gamma-j-demo"

@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    category: str
    availability: int
    image_url: str = ""

@dataclass
class Customer:
    id: int
    name: str
    email: str
    address: str
    phone: str = ""

@dataclass
class Order:
    id: int
    customer_name: str
    email: str
    address: str
    phone: str
    items: List[dict]
    total: float

PRODUCTS: Dict[int, Product] = {
    1: Product(1, "Starter Laptop", "Simple laptop for beginners", 599.99, "Electronics", 5, ""),
    2: Product(2, "Wireless Mouse", "Comfortable mouse", 19.99, "Electronics", 30, ""),
    3: Product(3, "Office Chair", "Basic office chair", 149.00, "Furniture", 10, ""),
}
CUSTOMERS: Dict[int, Customer] = {
    1: Customer(1, "Alice Smith", "alice@example.com", "123 Main St", "555-0100")
}
ORDERS: Dict[int, Order] = {}
CART: Dict[int, int] = {}
_product_ids = itertools.count(4)
_customer_ids = itertools.count(2)
_order_ids = itertools.count(1)

PAGE = """
<!doctype html><html><head><title>GAMMA-J Web Store</title></head><body>
<nav>
<a href='{{ url_for("index") }}'>Products</a> |
<a href='{{ url_for("cart_view") }}'>Cart ({{ cart_count }})</a> |
<a href='{{ url_for("checkout") }}'>Checkout</a> |
<a href='{{ url_for("orders") }}'>Order History</a> |
<a href='{{ url_for("staff") }}'>Staff</a>
</nav><hr>
{{ body|safe }}
</body></html>
"""


def cart_count():
    return sum(CART.values())


def render_page(body: str, **ctx):
    return render_template_string(PAGE, body=body, cart_count=cart_count(), **ctx)


@app.get("/")
def index():
    q = request.args.get("q", "").lower().strip()
    category = request.args.get("category", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()
    products = list(PRODUCTS.values())
    if q:
        products = [p for p in products if q in p.name.lower()]
    if category:
        products = [p for p in products if p.category.lower() == category.lower()]
    try:
        if min_price:
            products = [p for p in products if p.price >= float(min_price)]
        if max_price:
            products = [p for p in products if p.price <= float(max_price)]
    except ValueError:
        pass
    body = ["<h1>Products</h1>", "<form method='get'>Search <input name='q' value='%s'> Category <input name='category' value='%s'> Min <input name='min_price' value='%s'> Max <input name='max_price' value='%s'><button>Filter</button></form>" % (q, category, min_price, max_price)]
    body.append("<ul>")
    for p in products:
        img = f"<img src='{p.image_url}' alt='image' width='40'>" if p.image_url else ""
        body.append(f"<li>{img}<strong>{p.name}</strong> - {p.description} - ${p.price:.2f} - {p.category} - Available: {p.availability} <a href='/cart/add/{p.id}'>Add to cart</a></li>")
    body.append("</ul>")
    body.append("<p><a href='/products/new'>Staff: create product</a> | <a href='/customers'>Staff: customers</a></p>")
    return render_page("".join(body))


@app.get("/cart/add/<int:pid>")
def add_to_cart(pid):
    if pid not in PRODUCTS:
        abort(404)
    CART[pid] = CART.get(pid, 0) + 1
    return redirect(url_for("cart_view"))


@app.route("/cart", methods=["GET", "POST"])
def cart_view():
    if request.method == "POST":
        for pid in list(CART):
            qty = int(request.form.get(f"qty_{pid}", CART[pid]))
            if qty <= 0:
                CART.pop(pid, None)
            else:
                CART[pid] = qty
        return redirect(url_for("cart_view"))
    total = 0.0
    items = ["<h1>Shopping Cart</h1>", "<form method='post'><table border='1'><tr><th>Product</th><th>Qty</th><th>Price</th><th>Subtotal</th></tr>"]
    for pid, qty in CART.items():
        p = PRODUCTS[pid]
        subtotal = p.price * qty
        total += subtotal
        items.append(f"<tr><td>{p.name}</td><td><input type='number' min='0' name='qty_{pid}' value='{qty}'></td><td>${p.price:.2f}</td><td>${subtotal:.2f}</td></tr>")
    items.append(f"</table><p>Total: ${total:.2f}</p><button type='submit'>Update cart</button></form>")
    return render_page("".join(items))


@app.get("/cart/remove/<int:pid>")
def remove_from_cart(pid):
    CART.pop(pid, None)
    return redirect(url_for("cart_view"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()
        if not name or not email or not address or not CART:
            return render_page("<h1>Checkout</h1><p>Missing required fields or empty cart.</p>"), 400
        items = []
        total = 0.0
        for pid, qty in CART.items():
            p = PRODUCTS[pid]
            items.append({"product_id": pid, "name": p.name, "qty": qty, "price": p.price})
            total += p.price * qty
        oid = next(_order_ids)
        ORDERS[oid] = Order(oid, name, email, address, phone, items, total)
        CART.clear()
        return render_page(f"<h1>Order Confirmed</h1><p>Your purchase was successful. Order #{oid} total: ${total:.2f}</p>")
    return render_page("""
    <h1>Checkout</h1>
    <form method='post'>
      Name* <input name='name'><br>
      Email* <input name='email'><br>
      Address* <input name='address'><br>
      Phone <input name='phone'><br>
      <button type='submit'>Submit order</button>
    </form>
    <p>Required: name, email, address. Phone is optional.</p>
    """)


@app.get("/orders")
def orders():
    body = ["<h1>Order History</h1><ul>"]
    for o in ORDERS.values():
        body.append(f"<li>Order #{o.id} for {o.customer_name} - ${o.total:.2f}</li>")
    body.append("</ul>")
    return render_page("".join(body))


@app.get("/staff")
def staff():
    revenue = sum(o.total for o in ORDERS.values())
    body = f"<h1>Staff Dashboard</h1><p>New orders: {len(ORDERS)}</p><p>Sales revenue: ${revenue:.2f}</p>"
    return render_page(body)


@app.route("/products/new", methods=["GET", "POST"])
def product_new():
    if request.method == "POST":
        p = Product(next(_product_ids), request.form["name"], request.form.get("description", ""), float(request.form["price"]), request.form.get("category", "General"), int(request.form.get("availability", 0)), request.form.get("image_url", ""))
        PRODUCTS[p.id] = p
        return redirect(url_for("index"))
    return render_page("<h1>Create Product</h1><form method='post'>Name <input name='name'> Description <input name='description'> Price <input name='price'> Category <input name='category'> Availability <input name='availability'> Image URL <input name='image_url'><button>Create</button></form>")


@app.route("/customers", methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        c = Customer(next(_customer_ids), request.form["name"], request.form["email"], request.form.get("address", ""), request.form.get("phone", ""))
        CUSTOMERS[c.id] = c
        return redirect(url_for("customers"))
    items = ["<h1>Customers</h1><ul>"]
    for c in CUSTOMERS.values():
        items.append(f"<li>{c.name} - {c.email} - {c.address}</li>")
    items.append("</ul><h2>Create/Update Customer</h2><form method='post'>Name <input name='name'> Email <input name='email'> Address <input name='address'> Phone <input name='phone'><button>Save</button></form>")
    return render_page("".join(items))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
