from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import json
from datetime import datetime, timezone

class Store:
    def __init__(self):
        self.reset()
    def reset(self):
        self.sessions = {}
        self.users = {
            'admin': {'password': 'admin', 'roles': ['administrator', 'office']},
            'teacher': {'password': 'teacher', 'roles': ['teacher']},
            'office': {'password': 'office', 'roles': ['office']},
        }
        self.families = []
        self.children = []
        self.invoices = []
        self.audits = []
        self.next_id = 1

STORE = Store()

def now(): return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

def nid(prefix):
    v = f'{prefix}{STORE.next_id}'
    STORE.next_id += 1
    return v

def render(body, title='Nenios'):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title></head><body><nav><a href="/">Home</a> | <a href="/login">Login</a> | <a href="/logout">Logout</a> | <a href="/families/new">New Family</a> | <a href="/children/new">New Child</a> | <a href="/invoices/new">New Invoice</a> | <a href="/audit">Audit</a> | <a href="/export/invoices">Export</a></nav>{body}</body></html>'

def page_index(user):
    def li(items): return ''.join(f'<li>{x}</li>' for x in items)
    return render(f"<h1>Nenios Child Care Management</h1><p>{'Logged in as '+user if user else 'Not logged in'}</p><h2>Families</h2><ul>{li([f['id']+' '+f['name'] for f in STORE.families])}</ul><h2>Children</h2><ul>{li([c['id']+' '+c['name']+' '+c['status'] for c in STORE.children])}</ul><h2>Invoices</h2><ul>{li([i['id']+' '+i['status']+' paid='+str(i['paid']) for i in STORE.invoices])}</ul>")

def audit(action, kind, rid, detail='', user='system'):
    STORE.audits.append({'time': now(), 'user': user, 'action': action, 'kind': kind, 'id': rid, 'detail': detail})

class Handler(BaseHTTPRequestHandler):
    def send_html(self, html, status=200, cookie=None):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        if cookie: self.send_header('Set-Cookie', cookie)
        self.end_headers(); self.wfile.write(html.encode())
    def send_json(self, obj, status=200):
        self.send_response(status); self.send_header('Content-Type', 'application/json'); self.end_headers(); self.wfile.write(json.dumps(obj).encode())
    def user(self):
        cookie = self.headers.get('Cookie','')
        if cookie.startswith('user='): return cookie.split('=',1)[1]
    def do_GET(self):
        p = urlparse(self.path).path
        u = self.user()
        if p == '/': return self.send_html(page_index(u))
        if p == '/login': return self.send_html(render('<form method="post"><input name="username"><input name="password" type="password"><button>Login</button></form><p>Demo users: admin/admin, teacher/teacher, office/office</p>'))
        if p == '/logout': return self.send_html(render('<p>Logged out</p>'), cookie='user=; Max-Age=0')
        if p == '/families/new': return self.send_html(render('<form method="post"><input name="name"><input name="contact"><button>Create</button></form>'))
        if p == '/children/new': return self.send_html(render('<form method="post"><input name="name"><input name="family"><input name="allergies"><input name="immunizations"><button>Create</button></form>'))
        if p == '/invoices/new': return self.send_html(render('<form method="post"><input name="family"><input name="amount"><button>Create</button></form>'))
        if p == '/audit': return self.send_html(render('<ul>' + ''.join(f"<li>{a['time']} {a['user']} {a['action']} {a['kind']} {a['id']} {a['detail']}</li>" for a in STORE.audits) + '</ul>'))
        if p == '/export/invoices':
            if not u: return self.send_html('login required', 302)
            return self.send_json(STORE.invoices)
        self.send_html('not found', 404)
    def do_POST(self):
        p = urlparse(self.path).path
        n = int(self.headers.get('Content-Length','0'))
        data = parse_qs(self.rfile.read(n).decode())
        if p == '/login':
            user = STORE.users.get(data.get('username',[''])[0])
            if user and user['password'] == data.get('password',[''])[0]:
                audit('login', 'user', data['username'][0], user=data['username'][0])
                return self.send_html(page_index(data['username'][0]), cookie=f'user={data["username"][0]}')
            return self.send_html(render('<p>Invalid login</p>'), 403)
        if not self.user(): return self.send_html('login required', 302)
        if p == '/families/new':
            fam = {'id': nid('F'), 'name': data.get('name',[''])[0], 'contact': data.get('contact',[''])[0], 'status': 'active', 'updated': now()}
            STORE.families.append(fam); audit('create', 'family', fam['id'], fam['name'], self.user()); return self.send_html(page_index(self.user()))
        if p == '/children/new':
            c = {'id': nid('C'), 'name': data.get('name',[''])[0], 'family': data.get('family',[''])[0], 'allergies': data.get('allergies',[''])[0], 'immunizations': data.get('immunizations',[''])[0], 'status': 'draft', 'updated': now()}
            STORE.children.append(c); audit('create', 'child', c['id'], c['name'], self.user()); return self.send_html(page_index(self.user()))
        if p == '/invoices/new':
            i = {'id': nid('I'), 'family': data.get('family',[''])[0], 'amount': float(data.get('amount',['0'])[0]), 'paid': 0.0, 'status': 'submitted', 'history': []}
            STORE.invoices.append(i); audit('create', 'invoice', i['id'], str(i['amount']), self.user()); return self.send_html(page_index(self.user()))
        if p.startswith('/invoices/') and p.endswith('/pay'):
            iid = p.split('/')[2]
            inv = next((x for x in STORE.invoices if x['id']==iid), None)
            if not inv: return self.send_html('not found', 404)
            amt = float(data.get('amount',['0'])[0]); inv['paid'] += amt; inv['history'].append({'time': now(), 'amount': amt}); inv['status'] = 'paid' if inv['paid'] >= inv['amount'] else 'partial'; audit('payment', 'invoice', iid, str(amt), self.user()); return self.send_html(page_index(self.user()))
        self.send_html('not found', 404)

def main():
    server = ThreadingHTTPServer(('0.0.0.0', 8000), Handler)
    print('Serving on http://127.0.0.1:8000')
    server.serve_forever()

if __name__ == '__main__':
    main()
