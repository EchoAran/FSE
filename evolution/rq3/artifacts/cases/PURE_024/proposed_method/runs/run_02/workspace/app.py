#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import json
import os
import sqlite3
import threading
import time
from dataclasses import dataclass
from datetime import datetime, date
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DB_PATH = Path(__file__).with_name('nenios.db')
LOCK = threading.Lock()


def now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with LOCK:
        conn = connect()
        cur = conn.cursor()
        cur.executescript('''
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS families (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            billing_notes TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            family_id INTEGER NOT NULL REFERENCES families(id) ON DELETE CASCADE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT DEFAULT '',
            site TEXT DEFAULT 'Main',
            classroom_id INTEGER,
            immunization_status TEXT DEFAULT 'missing',
            allergy_alert TEXT DEFAULT '',
            pickup_authority TEXT DEFAULT '',
            compliant INTEGER DEFAULT 0,
            enrolled INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS classrooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            name TEXT NOT NULL,
            room_type TEXT DEFAULT '',
            capacity INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL REFERENCES children(id) ON DELETE CASCADE,
            action TEXT NOT NULL,
            ts TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            family_id INTEGER NOT NULL REFERENCES families(id) ON DELETE CASCADE,
            child_id INTEGER,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            balance REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
            payer_name TEXT NOT NULL,
            amount REAL NOT NULL,
            method TEXT NOT NULL,
            status TEXT NOT NULL,
            reason TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            reference_id INTEGER,
            requested_by TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            reason TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            decided_at TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS waiting_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            family_id INTEGER NOT NULL REFERENCES families(id) ON DELETE CASCADE,
            child_name TEXT NOT NULL,
            desired_site TEXT DEFAULT 'Main',
            desired_classroom TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'waiting',
            created_at TEXT NOT NULL
        );
        ''')
        conn.commit()
        conn.close()


def seed_if_empty():
    with LOCK:
        conn = connect()
        cur = conn.cursor()
        if cur.execute('SELECT COUNT(*) FROM families').fetchone()[0] == 0:
            cur.execute('INSERT INTO families(name,address,phone,email,billing_notes) VALUES (?,?,?,?,?)',
                        ('Smith Family', '123 Maple St', '555-0100', 'smith@example.com', 'Auto-pay enabled'))
            family_id = cur.lastrowid
            cur.execute('INSERT INTO classrooms(site,name,room_type,capacity) VALUES (?,?,?,?)',
                        ('Main', 'Sunflowers', 'Toddler', 8))
            classroom_id = cur.lastrowid
            cur.execute('INSERT INTO children(family_id,first_name,last_name,dob,site,classroom_id,immunization_status,allergy_alert,pickup_authority,compliant,enrolled) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        (family_id, 'Ava', 'Smith', '2022-04-11', 'Main', classroom_id, 'current', 'Peanut allergy', 'Mom, Dad', 1, 1))
            child_id = cur.lastrowid
            cur.execute('INSERT INTO invoices(family_id,child_id,description,amount,balance,status,created_at) VALUES (?,?,?,?,?,?,?)',
                        (family_id, child_id, 'Weekly tuition', 200.0, 200.0, 'open', now_iso()))
            conn.commit()
        conn.close()


def q(sql, params=(), one=False, commit=False):
    with LOCK:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall() if sql.lstrip().upper().startswith('SELECT') else None
        if commit:
            conn.commit()
        last = cur.lastrowid
        conn.close()
        if one:
            return (rows[0] if rows else None) if rows is not None else None
        return rows if rows is not None else last


def html_page(title, body):
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>{title}</title>
    <style>body{{font-family:sans-serif;max-width:1200px;margin:24px auto;padding:0 12px}} table{{border-collapse:collapse;width:100%}} td,th{{border:1px solid #ccc;padding:6px;vertical-align:top}} nav a{{margin-right:12px}} .ok{{color:green}} .bad{{color:#b00}} .warn{{color:#a60}}</style>
    </head><body><nav><a href='/'>Dashboard</a><a href='/families'>Families</a><a href='/children'>Children</a><a href='/classrooms'>Classrooms</a><a href='/attendance'>Attendance</a><a href='/invoices'>Invoices</a><a href='/reports'>Reports</a><a href='/export.csv'>Export CSV</a></nav><hr>{body}</body></html>"""


def render_dashboard():
    families = q('SELECT COUNT(*) c FROM families', one=True)['c']
    children = q('SELECT COUNT(*) c FROM children', one=True)['c']
    open_invoices = q("SELECT COUNT(*) c FROM invoices WHERE status='open'", one=True)['c']
    pending = q("SELECT COUNT(*) c FROM approvals WHERE status='pending'", one=True)['c']
    body = f"<h1>Nenios Child Care Management</h1><p>Families: {families} | Children: {children} | Open invoices: {open_invoices} | Pending approvals: {pending}</p>"
    body += "<p>This demo supports registration, capacity tracking, immunization statuses, attendance, billing, approvals, and CSV import/export.</p>"
    body += "<h2>Search</h2><form method='get' action='/search'><input name='q' placeholder='Child or family name'><button>Search</button></form>"
    return html_page('Dashboard', body)


def list_families():
    rows = q('SELECT * FROM families ORDER BY id DESC')
    body = "<h1>Families</h1><form method='post' action='/families/add'>"
    body += "Name <input name='name' required> Address <input name='address'> Phone <input name='phone'> Email <input name='email'> <button>Add Family</button></form>"
    body += '<table><tr><th>ID</th><th>Name</th><th>Contact</th><th>Children</th></tr>'
    for r in rows:
        count = q('SELECT COUNT(*) c FROM children WHERE family_id=?', (r['id'],), one=True)['c']
        body += f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['phone']}<br>{r['email']}<br>{r['address']}</td><td>{count}</td></tr>"
    body += '</table>'
    return html_page('Families', body)


def list_children():
    rows = q('''SELECT c.*, f.name family_name, cl.name classroom_name, cl.capacity cap, cl.site classroom_site,
               (SELECT COUNT(*) FROM children x WHERE x.classroom_id=c.classroom_id AND x.enrolled=1) enrolled_count
               FROM children c JOIN families f ON f.id=c.family_id LEFT JOIN classrooms cl ON cl.id=c.classroom_id ORDER BY c.id DESC''')
    body = "<h1>Children</h1><form method='post' action='/children/add'>Family ID <input name='family_id' required size='4'> First <input name='first_name' required> Last <input name='last_name' required> DOB <input name='dob'> Site <input name='site' value='Main'> Classroom ID <input name='classroom_id' size='4'> Immunization <select name='immunization_status'><option>current</option><option>due soon</option><option>overdue</option><option>exempt</option><option>missing</option><option>incomplete</option><option>expired</option></select> Allergy <input name='allergy_alert'> Pickup <input name='pickup_authority'> <button>Add Child</button></form>"
    body += '<table><tr><th>ID</th><th>Name</th><th>Family</th><th>Classroom</th><th>Status</th><th>Safety</th><th>Actions</th></tr>'
    for r in rows:
        cap = ''
        if r['classroom_name']:
            cap = f"{r['classroom_name']} ({r['enrolled_count']}/{r['cap']})"
        status = r['immunization_status']
        cls = 'ok' if status == 'current' else 'warn' if status in ('due soon', 'exempt') else 'bad'
        body += f"<tr><td>{r['id']}</td><td>{r['first_name']} {r['last_name']}</td><td>{r['family_name']}</td><td>{cap}</td><td class='{cls}'>{status} {'✓' if r['compliant'] else 'not compliant'}</td><td>{r['allergy_alert']}<br>{r['pickup_authority']}</td><td><a href='/children/{r['id']}/checkin'>Check in</a> | <a href='/children/{r['id']}/checkout'>Check out</a> | <a href='/children/{r['id']}/compliance'>Verify compliance</a></td></tr>"
    body += '</table>'
    return html_page('Children', body)


def list_classrooms():
    rows = q('SELECT *,(SELECT COUNT(*) FROM children c WHERE c.classroom_id=classrooms.id AND c.enrolled=1) enrolled_count FROM classrooms ORDER BY id DESC')
    body = "<h1>Classrooms</h1><form method='post' action='/classrooms/add'>Site <input name='site' value='Main'> Name <input name='name' required> Type <input name='room_type'> Capacity <input name='capacity' type='number' min='0' required> <button>Add Classroom</button></form>"
    body += '<table><tr><th>ID</th><th>Site</th><th>Name</th><th>Type</th><th>Capacity</th><th>Status</th></tr>'
    for r in rows:
        status = 'full' if r['enrolled_count'] >= r['capacity'] else 'available'
        cls = 'bad' if status == 'full' else 'ok'
        body += f"<tr><td>{r['id']}</td><td>{r['site']}</td><td>{r['name']}</td><td>{r['room_type']}</td><td>{r['enrolled_count']} / {r['capacity']}</td><td class='{cls}'>{status}</td></tr>"
    body += '</table>'
    return html_page('Classrooms', body)


def list_attendance():
    rows = q('''SELECT a.*, c.first_name||' '||c.last_name child_name FROM attendance a JOIN children c ON c.id=a.child_id ORDER BY a.id DESC LIMIT 100''')
    body = "<h1>Attendance</h1><p>Use the links on the Children page to check in or out.</p><table><tr><th>Child</th><th>Action</th><th>Time</th></tr>"
    for r in rows:
        body += f"<tr><td>{r['child_name']}</td><td>{r['action']}</td><td>{r['ts']}</td></tr>"
    body += '</table>'
    return html_page('Attendance', body)


def list_invoices():
    rows = q('''SELECT i.*, f.name family_name, c.first_name||' '||c.last_name child_name FROM invoices i JOIN families f ON f.id=i.family_id LEFT JOIN children c ON c.id=i.child_id ORDER BY i.id DESC''')
    body = "<h1>Invoices</h1><table><tr><th>ID</th><th>Family</th><th>Child</th><th>Description</th><th>Amount</th><th>Balance</th><th>Status</th><th>Payment</th></tr>"
    for r in rows:
        body += f"<tr><td>{r['id']}</td><td>{r['family_name']}</td><td>{r['child_name'] or ''}</td><td>{r['description']}</td><td>{r['amount']}</td><td>{r['balance']}</td><td>{r['status']}</td><td><form method='post' action='/payments/add'><input type='hidden' name='invoice_id' value='{r['id']}'><input name='payer_name' placeholder='Payer'><input name='amount' type='number' step='0.01' min='0'><select name='method'><option>credit card</option><option>debit card</option><option>bank transfer</option></select><button>Pay</button></form></td></tr>"
    body += '</table>'
    return html_page('Invoices', body)


def reports():
    body = "<h1>Reports</h1>"
    body += f"<p>Full classrooms: {q('SELECT COUNT(*) c FROM classrooms WHERE (SELECT COUNT(*) FROM children c WHERE c.classroom_id=classrooms.id AND c.enrolled=1) >= capacity', one=True)['c']}</p>"
    body += f"<p>Children not compliant: {q('SELECT COUNT(*) c FROM children WHERE compliant=0', one=True)['c']}</p>"
    body += f"<p>Pending approvals: {q("SELECT COUNT(*) c FROM approvals WHERE status='pending'", one=True)['c']}</p>"
    body += '<p><a href="/export.csv">Download CSV export</a></p>'
    return html_page('Reports', body)


def export_csv():
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(['type', 'id', 'name', 'extra'])
    for r in q('SELECT id,name,address,phone,email FROM families'):
        w.writerow(['family', r['id'], r['name'], json.dumps(dict(r))])
    for r in q('SELECT id,first_name,last_name,site,immunization_status,compliant FROM children'):
        w.writerow(['child', r['id'], f"{r['first_name']} {r['last_name']}", json.dumps(dict(r))])
    data = output.getvalue().encode()
    return data, 'text/csv; charset=utf-8'


class Handler(BaseHTTPRequestHandler):
    def send_html(self, body, status=200):
        data = body.encode()
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, loc='/'):
        self.send_response(303)
        self.send_header('Location', loc)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == '/': return self.send_html(render_dashboard())
        if path == '/families': return self.send_html(list_families())
        if path == '/children': return self.send_html(list_children())
        if path == '/classrooms': return self.send_html(list_classrooms())
        if path == '/attendance': return self.send_html(list_attendance())
        if path == '/invoices': return self.send_html(list_invoices())
        if path == '/reports': return self.send_html(reports())
        if path == '/export.csv':
            data, ct = export_csv()
            self.send_response(200)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Content-Disposition', 'attachment; filename="nenios_export.csv"')
            self.end_headers(); self.wfile.write(data); return
        if path.startswith('/children/') and path.endswith('/checkin'):
            child_id = int(path.split('/')[2])
            q('INSERT INTO attendance(child_id,action,ts) VALUES (?,?,?)', (child_id, 'check-in', now_iso()), commit=True)
            return self.redirect('/attendance')
        if path.startswith('/children/') and path.endswith('/checkout'):
            child_id = int(path.split('/')[2])
            q('INSERT INTO attendance(child_id,action,ts) VALUES (?,?,?)', (child_id, 'check-out', now_iso()), commit=True)
            return self.redirect('/attendance')
        if path.startswith('/children/') and path.endswith('/compliance'):
            child_id = int(path.split('/')[2])
            q("UPDATE children SET compliant=1, immunization_status='current' WHERE id=?", (child_id,), commit=True)
            return self.redirect('/children')
        if path == '/search':
            qtxt = parse_qs(parsed.query).get('q', [''])[0].strip().lower()
            fams = q('SELECT * FROM families WHERE lower(name) LIKE ?', (f'%{qtxt}%',)) if qtxt else []
            kids = q('SELECT c.*, f.name family_name FROM children c JOIN families f ON f.id=c.family_id WHERE lower(c.first_name||" "||c.last_name) LIKE ? OR lower(f.name) LIKE ?', (f'%{qtxt}%', f'%{qtxt}%')) if qtxt else []
            body = f"<h1>Search results for {qtxt}</h1><p>Families: {len(fams)} Children: {len(kids)}</p>"
            return self.send_html(html_page('Search', body))
        self.send_html(html_page('Not found', '<h1>404</h1>'), 404)

    def do_POST(self):
        length = int(self.headers.get('Content-Length', '0'))
        data = parse_qs(self.rfile.read(length).decode())
        path = urlparse(self.path).path
        def g(k, default=''):
            return data.get(k, [default])[0]
        if path == '/families/add':
            q('INSERT INTO families(name,address,phone,email) VALUES (?,?,?,?)', (g('name'), g('address'), g('phone'), g('email')), commit=True)
            return self.redirect('/families')
        if path == '/classrooms/add':
            q('INSERT INTO classrooms(site,name,room_type,capacity) VALUES (?,?,?,?)', (g('site') or 'Main', g('name'), g('room_type'), int(g('capacity') or 0)), commit=True)
            return self.redirect('/classrooms')
        if path == '/children/add':
            family_id = int(g('family_id'))
            classroom_id = int(g('classroom_id')) if g('classroom_id') else None
            q('INSERT INTO children(family_id,first_name,last_name,dob,site,classroom_id,immunization_status,allergy_alert,pickup_authority,compliant,enrolled) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
              (family_id, g('first_name'), g('last_name'), g('dob'), g('site') or 'Main', classroom_id, g('immunization_status') or 'missing', g('allergy_alert'), g('pickup_authority'), 1 if g('immunization_status') == 'current' else 0, 1), commit=True)
            return self.redirect('/children')
        if path == '/payments/add':
            invoice_id = int(g('invoice_id'))
            amount = float(g('amount') or 0)
            inv = q('SELECT * FROM invoices WHERE id=?', (invoice_id,), one=True)
            status = 'completed'
            reason = ''
            if amount <= 0:
                status = 'failed'; reason = 'Invalid amount'
            elif amount > float(inv['balance']):
                status = 'review'; reason = 'Unusually large or excess payment'
            q('INSERT INTO payments(invoice_id,payer_name,amount,method,status,reason,created_at) VALUES (?,?,?,?,?,?,?)', (invoice_id, g('payer_name') or 'Unknown', amount, g('method') or 'credit card', status, reason, now_iso()), commit=True)
            if status == 'completed':
                newbal = max(0.0, float(inv['balance']) - amount)
                newstatus = 'paid' if newbal == 0 else 'open'
                q('UPDATE invoices SET balance=?, status=? WHERE id=?', (newbal, newstatus, invoice_id), commit=True)
            else:
                q('INSERT INTO approvals(kind,reference_id,requested_by,status,reason,created_at) VALUES (?,?,?,?,?,?)', ('payment', invoice_id, g('payer_name') or 'Unknown', 'pending', reason, now_iso()), commit=True)
            return self.redirect('/invoices')
        self.send_html(html_page('Not found', '<h1>404</h1>'), 404)


def main():
    init_db(); seed_if_empty()
    port = int(os.environ.get('PORT', '8000'))
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'Serving on http://127.0.0.1:{port}', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
