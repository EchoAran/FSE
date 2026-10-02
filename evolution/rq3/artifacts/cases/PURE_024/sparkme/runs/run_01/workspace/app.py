from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json, itertools, hashlib, hmac

now = lambda: datetime.utcnow().isoformat(timespec='seconds') + 'Z'
_id_counter = itertools.count(1)

def next_id(): return next(_id_counter)

@dataclass
class User:
    username: str; password: str; roles: list

@dataclass
class Record:
    id: int; created_at: str; updated_at: str; created_by: str; updated_by: str; status: str='active'; archived: bool=False; history: list=field(default_factory=list)

@dataclass
class Family(Record):
    name: str=''; contact: str=''; children: list=field(default_factory=list)

@dataclass
class Child(Record):
    family_id: int=0; name: str=''; allergies: str=''; immunizations: str=''; classroom: str=''; active: bool=True

@dataclass
class Enrollment(Record):
    family_id: int=0; child_id: int=0; classroom: str=''; status: str='draft'

@dataclass
class Invoice(Record):
    family_id: int=0; child_id: int=0; amount: float=0.0; paid_amount: float=0.0; status: str='unpaid'; transactions: list=field(default_factory=list)

users={'admin':User('admin','admin',['administrator']),'teacher':User('teacher','teacher',['teacher']),'office':User('office','office',['office','billing'])}
families={}; children={}; enrollments={}; invoices={}
sessions={}

def token_for(username): return hmac.new(b'secret', username.encode(), hashlib.sha256).hexdigest()

def log(record, user, action, detail=''):
    record.history.append({'at': now(), 'by': user, 'action': action, 'detail': detail}); record.updated_at=now(); record.updated_by=user

class Handler(BaseHTTPRequestHandler):
    def sendj(self, obj, code=200):
        data=json.dumps(obj).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def user(self):
        cookie=self.headers.get('Cookie','')
        token=None
        for part in cookie.split(';'):
            if part.strip().startswith('session='): token=part.strip().split('=',1)[1]
        return sessions.get(token)
    def roles(self):
        u=users.get(self.user()); return u.roles if u else []
    def auth(self, allowed=None):
        u=self.user()
        if not u: self.sendj({'error':'unauthorized'},401); return None
        if allowed and not any(r in self.roles() for r in allowed): self.sendj({'error':'forbidden'},403); return None
        return u
    def read_json(self):
        n=int(self.headers.get('Content-Length','0') or 0)
        return json.loads(self.rfile.read(n).decode() or '{}') if n else {}
    def do_GET(self):
        p=urlparse(self.path)
        if p.path=='/': return self.sendj({'service':'Nenios Child Care Management','logged_in_as':self.user(),'roles':self.roles()})
        if p.path=='/search':
            if not self.auth(): return
            q=parse_qs(p.query).get('q',[''])[0].lower()
            return self.sendj({'families':[asdict(v) for v in families.values() if q in v.name.lower() or q in v.contact.lower()],'children':[asdict(v) for v in children.values() if q in v.name.lower()],'invoices':[asdict(v) for v in invoices.values() if q in str(v.id)]})
        if p.path=='/status':
            if not self.auth(): return
            return self.sendj({'families':len(families),'children':len(children),'enrollments':len(enrollments),'invoices':len(invoices)})
        if p.path=='/login':
            self.send_response(200); self.send_header('Content-Type','text/html'); self.end_headers(); self.wfile.write(b'<form method="post"></form>'); return
        self.sendj({'error':'not found'},404)
    def do_POST(self):
        p=urlparse(self.path); data=self.read_json()
        if p.path=='/login':
            u=users.get(data.get('username'))
            if u and u.password==data.get('password'):
                t=token_for(u.username); sessions[t]=u.username; self.send_response(200); self.send_header('Set-Cookie', f'session={t}; Path=/'); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps({'ok':True}).encode()); return
            return self.sendj({'error':'invalid credentials'},401)
        if p.path=='/logout': sessions.clear(); return self.sendj({'ok':True})
        u=self.auth(['administrator','office','billing'] if p.path in ['/families','/children','/enrollments','/invoices'] else ['administrator'])
        if not u: return
        username=u
        if p.path=='/families':
            fid=next_id(); f=Family(id=fid,created_at=now(),updated_at=now(),created_by=username,updated_by=username,name=data.get('name',''),contact=data.get('contact','')); families[fid]=f; log(f,username,'create'); return self.sendj(asdict(f),201)
        if p.path=='/children':
            cid=next_id(); c=Child(id=cid,created_at=now(),updated_at=now(),created_by=username,updated_by=username,family_id=data.get('family_id',0),name=data.get('name',''),allergies=data.get('allergies',''),immunizations=data.get('immunizations',''),classroom=data.get('classroom','')); children[cid]=c; log(c,username,'create'); return self.sendj(asdict(c),201)
        if p.path.startswith('/children/') and p.path.endswith('/archive'):
            cid=int(p.path.split('/')[2]); c=children[cid]; c.archived=True; c.active=False; c.status='archived'; log(c,username,'archive'); return self.sendj(asdict(c))
        if p.path=='/enrollments':
            eid=next_id(); e=Enrollment(id=eid,created_at=now(),updated_at=now(),created_by=username,updated_by=username,family_id=data.get('family_id',0),child_id=data.get('child_id',0),classroom=data.get('classroom',''),status=data.get('status','draft')); enrollments[eid]=e; log(e,username,'create'); return self.sendj(asdict(e),201)
        if p.path=='/invoices':
            iid=next_id(); inv=Invoice(id=iid,created_at=now(),updated_at=now(),created_by=username,updated_by=username,family_id=data.get('family_id',0),child_id=data.get('child_id',0),amount=float(data.get('amount',0))); invoices[iid]=inv; log(inv,username,'create'); return self.sendj(asdict(inv),201)
        if p.path.startswith('/invoices/') and p.path.endswith('/pay'):
            iid=int(p.path.split('/')[2]); inv=invoices[iid]; amt=float(data.get('amount',0)); inv.paid_amount+=amt; inv.transactions.append({'at':now(),'amount':amt,'by':username}); inv.status='paid' if inv.paid_amount>=inv.amount else 'partial'; log(inv,username,'payment',str(amt)); return self.sendj(asdict(inv))
        self.sendj({'error':'not found'},404)

def main():
    ThreadingHTTPServer(('0.0.0.0',8000), Handler).serve_forever()

if __name__=='__main__': main()
