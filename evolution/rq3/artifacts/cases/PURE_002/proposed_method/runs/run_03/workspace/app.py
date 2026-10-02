from __future__ import annotations

import csv
import html
import io
import json
import os
import re
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qs, urlencode, urlparse
from wsgiref.simple_server import make_server

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "gammaj_store.db"
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def ensure_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            category TEXT NOT NULL DEFAULT 'General',
            price REAL,
            stock INTEGER,
            active INTEGER NOT NULL DEFAULT 1,
            min_qty INTEGER NOT NULL DEFAULT 1,
            max_qty INTEGER NOT NULL DEFAULT 99,
            image_main TEXT,
            image_extra TEXT,
            needs_review INTEGER NOT NULL DEFAULT 0,
            review_notes TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            status TEXT NOT NULL,
            payment_status TEXT NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
            product_id INTEGER,
            product_name TEXT NOT NULL,
            unit_price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            line_total REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            notes TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor TEXT NOT NULL,
            action TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            before_json TEXT,
            after_json TEXT,
            created_at TEXT NOT NULL
        );
        """
    )
    return conn


def seed_if_empty(conn: sqlite3.Connection) -> None:
    cur = conn.execute("SELECT COUNT(*) AS c FROM products")
    if cur.fetchone()["c"]:
        return
    now = utc_now()
    products = [
        ("SKU-001", "Basic T-Shirt", "Soft cotton shirt", "Apparel", 19.99, 25, 1, 1, 10, None, None, 0, "", now, now),
        ("SKU-002", "Coffee Mug", "Ceramic mug", "Home", 12.5, 50, 1, 1, 5, None, None, 0, "", now, now),
        ("SKU-003", "Notebook", "Ruled notebook", "Office", 6.0, 0, 1, 1, 20, None, None, 0, "", now, now),
    ]
    conn.executemany(
        """
        INSERT INTO products
        (sku, name, description, category, price, stock, active, min_qty, max_qty, image_main, image_extra, needs_review, review_notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        products,
    )
    conn.commit()


def parse_cookie(environ: dict[str, Any]) -> SimpleCookie:
    cookie = SimpleCookie()
    raw = environ.get("HTTP_COOKIE", "")
    if raw:
        cookie.load(raw)
    return cookie


def set_cookie(headers: list[tuple[str, str]], name: str, value: str, path: str = "/") -> None:
    headers.append(("Set-Cookie", f"{name}={value}; Path={path}; HttpOnly; SameSite=Lax"))


def get_session_id(environ: dict[str, Any]) -> str:
    cookie = parse_cookie(environ)
    sid = cookie.get("sid")
    if sid:
        return sid.value
    return f"sid-{os.urandom(8).hex()}"


def get_cart(conn: sqlite3.Connection, session_id: str) -> dict[int, int]:
    # stored in a JSON file per session for simplicity
    path = BASE_DIR / f"cart_{session_id}.json"
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text())
        return {int(k): int(v) for k, v in raw.items()}
    except Exception:
        return {}


def save_cart(session_id: str, cart: dict[int, int]) -> None:
    path = BASE_DIR / f"cart_{session_id}.json"
    path.write_text(json.dumps({str(k): v for k, v in cart.items()}))


def log_audit(conn: sqlite3.Connection, actor: str, action: str, entity_type: str, entity_id: str, before: Any, after: Any) -> None:
    conn.execute(
        "INSERT INTO audit_log(actor, action, entity_type, entity_id, before_json, after_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (actor, action, entity_type, entity_id, json.dumps(before), json.dumps(after), utc_now()),
    )
    conn.commit()


def read_post(environ: dict[str, Any]) -> dict[str, str]:
    try:
        size = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        size = 0
    body = environ["wsgi.input"].read(size).decode("utf-8", errors="replace")
    return {k: v[0] for k, v in parse_qs(body, keep_blank_values=True).items()}


def html_page(title: str, body: str) -> bytes:
    return f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>{esc(title)}</title>
    <style>
    body{{font-family:system-ui,Arial,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;line-height:1.4}}
    nav a{{margin-right:1rem}}
    table{{border-collapse:collapse;width:100%}} td,th{{border:1px solid #ccc;padding:.4rem;text-align:left;vertical-align:top}}
    .msg{{padding:.75rem;background:#f5f5f5;border:1px solid #ddd;margin:1rem 0}}
    .bad{{background:#fff3f3;border-color:#e2a3a3}} .good{{background:#f2fff2;border-color:#a3e2a3}}
    .muted{{color:#666}} .pill{{display:inline-block;padding:.1rem .4rem;border:1px solid #999;border-radius:999px;font-size:.8rem}}
    </style></head><body>{body}</body></html>""".encode()


def nav() -> str:
    return "<nav><a href='/'>Store</a><a href='/cart'>Cart</a><a href='/admin'>Admin</a><a href='/audit'>Audit log</a></nav><hr>"


def product_visible(row: sqlite3.Row) -> bool:
    return bool(row["active"])


def product_purchasable(row: sqlite3.Row) -> tuple[bool, str]:
    if not row["active"]:
        return False, "Product is inactive"
    if row["price"] is None or row["price"] <= 0:
        return False, "Price is missing or invalid"
    if row["stock"] is not None and row["stock"] <= 0:
        return False, "Out of stock"
    return True, "Available"


def load_products(conn: sqlite3.Connection, q: str = "") -> list[sqlite3.Row]:
    if q:
        return conn.execute(
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ? OR category LIKE ? ORDER BY id DESC",
            (f"%{q}%", f"%{q}%", f"%{q}%"),
        ).fetchall()
    return conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()


def handle_index(environ: dict[str, Any], conn: sqlite3.Connection) -> tuple[str, list[tuple[str, str]], bytes]:
    params = parse_qs(urlparse(environ.get("PATH_INFO", "/")).query)
    q = params.get("q", [""])[0]
    products = load_products(conn, q)
    rows = []
    for p in products:
        purch, reason = product_purchasable(p)
        rows.append(
            f"<tr><td><a href='/product/{p['id']}'>{esc(p['name'])}</a></td><td>{esc(p['category'])}</td><td>${p['price'] if p['price'] is not None else 'N/A'}</td><td>{esc(reason)}</td><td>{'Yes' if purch else 'No'}</td></tr>"
        )
    body = nav() + f"<h1>GAMMA-J Web Store</h1><form><input name='q' placeholder='Search' value='{esc(q)}'><button>Search</button></form><table><tr><th>Name</th><th>Category</th><th>Price</th><th>Status</th><th>Purchasable</th></tr>{''.join(rows)}</table>"
    return "200 OK", [], html_page("Store", body)


def product_detail(environ: dict[str, Any], conn: sqlite3.Connection, pid: int) -> tuple[str, list[tuple[str, str]], bytes]:
    p = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    if not p:
        return "404 Not Found", [], html_page("Not found", nav() + "<p>Product not found.</p>")
    purch, reason = product_purchasable(p)
    body = nav() + f"<h1>{esc(p['name'])}</h1><p>{esc(p['description'])}</p><p>Category: {esc(p['category'])}</p><p>Price: ${p['price'] if p['price'] is not None else 'N/A'}</p><p>Stock: {esc(p['stock']) if p['stock'] is not None else 'N/A'}</p><p>Status: {esc(reason)}</p>"
    if purch:
        body += f"<form method='post' action='/cart/add'><input type='hidden' name='product_id' value='{p['id']}'><label>Qty <input name='qty' type='number' min='1' value='1'></label><button>Add to cart</button></form>"
    else:
        body += "<p class='msg bad'>This item is not purchasable right now.</p>"
    return "200 OK", [], html_page(p["name"], body)


def cart_page(environ: dict[str, Any], conn: sqlite3.Connection, session_id: str) -> tuple[str, list[tuple[str, str]], bytes]:
    cart = get_cart(conn, session_id)
    lines = []
    total = 0.0
    for pid, qty in cart.items():
        p = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if not p:
            continue
        price = p["price"] or 0
        line = price * qty
        total += line
        purch, reason = product_purchasable(p)
        lines.append(f"<tr><td>{esc(p['name'])}</td><td>{qty}</td><td>${price:.2f}</td><td>${line:.2f}</td><td>{esc(reason)}</td></tr>")
    body = nav() + f"<h1>Cart</h1><table><tr><th>Item</th><th>Qty</th><th>Unit</th><th>Line</th><th>Status</th></tr>{''.join(lines)}</table><p><strong>Total:</strong> ${total:.2f}</p>"
    if cart:
        body += "<p><a href='/checkout'>Proceed to checkout</a></p>"
    return "200 OK", [], html_page("Cart", body)


def checkout_get(environ: dict[str, Any], conn: sqlite3.Connection, session_id: str) -> tuple[str, list[tuple[str, str]], bytes]:
    body = nav() + """
    <h1>Checkout</h1>
    <form method='post'>
      <p><label>Name <input name='customer_name' required></label></p>
      <p><label>Email <input name='email' type='email' required></label></p>
      <p><label>Address <input name='address' required></label></p>
      <p><label>Payment method <select name='payment_method'><option>TrustedProvider</option></select></label></p>
      <button>Submit order</button>
    </form>
    <p class='muted'>Payment details are not stored by this demo; only a success/failure response is shown.</p>
    """
    return "200 OK", [], html_page("Checkout", body)


def checkout_post(environ: dict[str, Any], conn: sqlite3.Connection, session_id: str) -> tuple[str, list[tuple[str, str]], bytes]:
    form = read_post(environ)
    cart = get_cart(conn, session_id)
    if not cart:
        return "400 Bad Request", [], html_page("Empty cart", nav() + "<p class='msg bad'>Your cart is empty.</p>")
    problems = []
    items = []
    total = 0.0
    for pid, qty in cart.items():
        p = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if not p:
            problems.append(f"Item {pid} no longer exists")
            continue
        purch, reason = product_purchasable(p)
        if not purch:
            problems.append(f"{p['name']}: {reason}")
        if qty < p["min_qty"] or qty > p["max_qty"]:
            problems.append(f"{p['name']}: quantity must be between {p['min_qty']} and {p['max_qty']}")
        if p["stock"] is not None and qty > p["stock"]:
            problems.append(f"{p['name']}: not enough stock")
        price = float(p["price"] or 0)
        line = price * qty
        total += line
        items.append((p, qty, price, line))
    if not form.get("address") or len(form["address"].split()) < 3:
        problems.append("Shipping address is incomplete")
    if problems:
        return "400 Bad Request", [], html_page("Checkout blocked", nav() + "<div class='msg bad'><strong>Checkout blocked</strong><ul>" + "".join(f"<li>{esc(x)}</li>" for x in problems) + "</ul></div>")

    order_no = f"GJ-{int(time.time())}"
    now = utc_now()
    conn.execute(
        "INSERT INTO orders(order_no, customer_name, email, address, status, payment_status, total, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (order_no, form["customer_name"], form["email"], form["address"], "pending", "paid", total, now, now),
    )
    order_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    for p, qty, price, line in items:
        conn.execute(
            "INSERT INTO order_items(order_id, product_id, product_name, unit_price, quantity, line_total) VALUES (?, ?, ?, ?, ?, ?)",
            (order_id, p["id"], p["name"], price, qty, line),
        )
        if p["stock"] is not None:
            conn.execute("UPDATE products SET stock=?, updated_at=? WHERE id=?", (p["stock"] - qty, now, p["id"]))
    conn.execute("UPDATE orders SET status='fulfilled', updated_at=? WHERE id=? AND payment_status='paid'", (now, order_id))
    conn.commit()
    save_cart(session_id, {})
    log_audit(conn, form["email"], "create_order", "order", str(order_id), None, {"order_no": order_no, "total": total})
    body = nav() + f"<div class='msg good'><h1>Order confirmed</h1><p>Order number: <strong>{esc(order_no)}</strong></p><p>Total: ${total:.2f}</p><p>Payment status: paid</p><p>Order status: fulfilled</p></div>"
    return "200 OK", [], html_page("Order confirmed", body)


def admin_page(environ: dict[str, Any], conn: sqlite3.Connection) -> tuple[str, list[tuple[str, str]], bytes]:
    products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    rows = []
    for p in products:
        rows.append(f"<tr><td>{p['id']}</td><td>{esc(p['sku'])}</td><td>{esc(p['name'])}</td><td>{esc(p['category'])}</td><td>{p['price']}</td><td>{p['stock']}</td><td>{'yes' if p['active'] else 'no'}</td><td><a href='/admin/product/{p['id']}'>edit</a></td></tr>")
    body = nav() + "<h1>Admin</h1><p><a href='/admin/product/new'>Add product</a> | <a href='/admin/import'>Import catalog</a></p><table><tr><th>ID</th><th>SKU</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Active</th><th></th></tr>" + "".join(rows) + "</table>"
    return "200 OK", [], html_page("Admin", body)


def product_form(product: sqlite3.Row | None = None) -> str:
    p = product or {"sku":"","name":"","description":"","category":"General","price":"","stock":"","active":1,"min_qty":1,"max_qty":99}
    return f"""
    <form method='post'>
      <p><label>SKU <input name='sku' value='{esc(p['sku'])}'></label></p>
      <p><label>Name <input name='name' value='{esc(p['name'])}' required></label></p>
      <p><label>Description <textarea name='description'>{esc(p['description'])}</textarea></label></p>
      <p><label>Category <input name='category' value='{esc(p['category'])}'></label></p>
      <p><label>Price <input name='price' type='number' step='0.01' value='{esc(p['price'])}'></label></p>
      <p><label>Stock <input name='stock' type='number' value='{esc(p['stock'])}'></label></p>
      <p><label>Active <input name='active' type='checkbox' {'checked' if int(p['active']) else ''}></label></p>
      <p><label>Min qty <input name='min_qty' type='number' value='{esc(p['min_qty'])}'></label></p>
      <p><label>Max qty <input name='max_qty' type='number' value='{esc(p['max_qty'])}'></label></p>
      <p><button>Save</button></p>
    </form>
    """


def app(environ: dict[str, Any], start_response):
    conn = ensure_db()
    seed_if_empty(conn)
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET").upper()
    headers = [("Content-Type", "text/html; charset=utf-8")]
    sid = get_session_id(environ)
    set_cookie(headers, "sid", sid)

    try:
        if path == "/":
            status, extra, body = handle_index(environ, conn)
        elif path.startswith("/product/") and method == "GET":
            status, extra, body = product_detail(environ, conn, int(path.rsplit("/", 1)[1]))
        elif path == "/cart":
            status, extra, body = cart_page(environ, conn, sid)
        elif path == "/cart/add" and method == "POST":
            form = read_post(environ)
            pid = int(form["product_id"])
            qty = max(1, int(form.get("qty", "1")))
            p = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
            if not p:
                status, extra, body = "404 Not Found", [], html_page("Not found", nav() + "<p>Product not found.</p>")
            else:
                purch, reason = product_purchasable(p)
                if not purch:
                    status, extra, body = "400 Bad Request", [], html_page("Blocked", nav() + f"<p class='msg bad'>Cannot add item: {esc(reason)}</p>")
                else:
                    cart = get_cart(conn, sid)
                    cart[pid] = cart.get(pid, 0) + qty
                    save_cart(sid, cart)
                    status, extra, body = "200 OK", [("Location", "/cart")], b""
        elif path == "/checkout" and method == "GET":
            status, extra, body = checkout_get(environ, conn, sid)
        elif path == "/checkout" and method == "POST":
            status, extra, body = checkout_post(environ, conn, sid)
        elif path == "/admin":
            status, extra, body = admin_page(environ, conn)
        elif path == "/admin/product/new":
            if method == "GET":
                status, extra, body = "200 OK", [], html_page("New product", nav() + "<h1>New product</h1>" + product_form())
            else:
                form = read_post(environ)
                now = utc_now()
                conn.execute(
                    "INSERT INTO products(sku,name,description,category,price,stock,active,min_qty,max_qty,image_main,image_extra,needs_review,review_notes,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        form.get("sku") or None, form["name"], form.get("description", ""), form.get("category", "General"),
                        float(form["price"]) if form.get("price") else None,
                        int(form["stock"]) if form.get("stock") else None,
                        1 if form.get("active") == "on" else 0,
                        int(form.get("min_qty", "1")), int(form.get("max_qty", "99")), None, None, 0, "", now, now,
                    ),
                )
                conn.commit()
                status, extra, body = "302 Found", [("Location", "/admin")], b""
        elif path.startswith("/admin/product/"):
            pid = int(path.rsplit("/", 1)[1])
            p = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
            if not p:
                status, extra, body = "404 Not Found", [], html_page("Not found", nav() + "<p>Product not found.</p>")
            elif method == "GET":
                status, extra, body = "200 OK", [], html_page("Edit product", nav() + f"<h1>Edit product {esc(p['name'])}</h1>" + product_form(p))
            else:
                before = dict(p)
                form = read_post(environ)
                now = utc_now()
                after = {
                    "sku": form.get("sku") or None,
                    "name": form["name"],
                    "description": form.get("description", ""),
                    "category": form.get("category", "General"),
                    "price": float(form["price"]) if form.get("price") else None,
                    "stock": int(form["stock"]) if form.get("stock") else None,
                    "active": 1 if form.get("active") == "on" else 0,
                    "min_qty": int(form.get("min_qty", "1")),
                    "max_qty": int(form.get("max_qty", "99")),
                }
                conn.execute("UPDATE products SET sku=?, name=?, description=?, category=?, price=?, stock=?, active=?, min_qty=?, max_qty=?, updated_at=? WHERE id=?",
                             (after['sku'], after['name'], after['description'], after['category'], after['price'], after['stock'], after['active'], after['min_qty'], after['max_qty'], now, pid))
                conn.commit()
                log_audit(conn, "admin", "update_product", "product", str(pid), {k: before[k] for k in after}, after)
                status, extra, body = "302 Found", [("Location", "/admin")], b""
        elif path == "/admin/import":
            if method == "GET":
                body = nav() + "<h1>Import catalog</h1><p>Upload CSV with headers: sku,name,description,category,price,stock,active</p><form method='post' enctype='multipart/form-data'><input type='file' name='file'><button>Import</button></form>"
                status, extra, body = "200 OK", [], html_page("Import", body)
            else:
                raw = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH") or 0))
                text = raw.decode("utf-8", errors="replace")
                # Simple multipart handling for one file field.
                m = re.search(r"\r\n\r\n(.*)\r\n--", text, re.S)
                csv_text = m.group(1) if m else text
                reader = csv.DictReader(io.StringIO(csv_text))
                imported = 0
                rejected = []
                now = utc_now()
                for i, row in enumerate(reader, 1):
                    if not row.get("name"):
                        rejected.append(f"Row {i}: missing name")
                        continue
                    try:
                        conn.execute(
                            "INSERT INTO products(sku,name,description,category,price,stock,active,min_qty,max_qty,image_main,image_extra,needs_review,review_notes,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                row.get("sku") or None,
                                row["name"], row.get("description", ""), row.get("category", "General"),
                                float(row["price"]) if row.get("price") else None,
                                int(row["stock"]) if row.get("stock") else None,
                                1 if str(row.get("active", "1")).strip() not in ("0", "false", "no") else 0,
                                1, 99, None, None, 0, "", now, now,
                            ),
                        )
                        imported += 1
                    except Exception as e:
                        rejected.append(f"Row {i}: {e}")
                conn.commit()
                status = "200 OK"
                body = html_page("Import result", nav() + f"<div class='msg good'>Imported {imported} rows.</div><pre>{esc('\n'.join(rejected) or 'No errors')}</pre>")
                extra = []
        elif path == "/audit":
            rows = conn.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 50").fetchall()
            out = [f"<tr><td>{r['created_at']}</td><td>{esc(r['actor'])}</td><td>{esc(r['action'])}</td><td>{esc(r['entity_type'])}</td><td>{esc(r['entity_id'])}</td><td><pre>{esc(r['before_json'])}</pre></td><td><pre>{esc(r['after_json'])}</pre></td></tr>" for r in rows]
            status, extra, body = "200 OK", [], html_page("Audit", nav() + "<h1>Audit log</h1><table><tr><th>When</th><th>Who</th><th>Action</th><th>Entity</th><th>ID</th><th>Before</th><th>After</th></tr>" + "".join(out) + "</table>")
        else:
            status, extra, body = "404 Not Found", [], html_page("Not found", nav() + "<p>Page not found.</p>")
    finally:
        conn.close()

    start_response(status, headers + extra)
    return [body]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Serving on http://127.0.0.1:{port}")
    with make_server("127.0.0.1", port, app) as httpd:
        httpd.serve_forever()
