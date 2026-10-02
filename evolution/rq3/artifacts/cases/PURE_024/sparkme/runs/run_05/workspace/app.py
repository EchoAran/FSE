from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from html import escape
from dataclasses import dataclass, field
from datetime import datetime
import json, os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'seed.json')

@dataclass
class Family:
    id: int; name: str; contact: str; active: bool = True; archived: bool = False
@dataclass
class Child:
    id: int; family_id: int; name: str; allergy_notes: str = ''; immunizations: str = ''; active: bool = True; archived: bool = False
@dataclass
class Invoice:
    id: int; family_id: int; child_id: int | None; amount: float; status: str = 'draft'; payment_state: str = 'unpaid'; created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec='seconds')); history: list = field(default_factory=list)

state={'families':{},'children':{},'invoices':{},'next_ids':{'family':1,'child':1,'invoice':1}}

def seed():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r',encoding='utf-8') as f: data=json.load(f)
        state['families']={f['id']:Family(**f) for f in data.get('families',[])}
        state['children']={c['id']:Child(**c) for c in data.get('children',[])}
        state['invoices']={i['id']:Invoice(**i) for i in data.get('invoices',[])}
        for k in ['family','child','invoice']:
            mx=max([0]+list(getattr(v,'id') for v in state[f'{k}s'].values()))
            state['next_ids'][k]=mx+1

def save_seed():
    os.makedirs(os.path.dirname(DATA_FILE),exist_ok=True)
    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump({'families':[vars(v) for v in state['families'].values()],'children':[vars(v) for v in state['children'].values()],'invoices':[vars(v) for v in state['invoices'].values()]},f,indent=2)

def page(title, body): return f'<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><nav><a href="/">Home</a> <a href="/families">Families</a> <a href="/children">Children</a> <a href="/invoices">Invoices</a></nav>{body}</body></html>'

class H(BaseHTTPRequestHandler):
    def do_GET(self): self.respond(*self.route('GET'))
    def do_POST(self): self.respond(*self.route('POST'))
    def route(self, method):
        p=urlparse(self.path)
        if method=='GET' and p.path=='/': return 200,page('Nenios','<h1>Nenios Child Care Management</h1>')
        if p.path=='/families':
            if method=='POST':
                d=self.form(); i=state['next_ids']['family']; state['next_ids']['family']+=1; state['families'][i]=Family(i,d['name'][0],d['contact'][0]); save_seed(); return 303,'/families'
            items=''.join(f'<li>#{f.id} {escape(f.name)} — {escape(f.contact)}</li>' for f in state['families'].values())
            form='<form method="post"><input name="name" required><input name="contact" required><button>Add family</button></form>'
            return 200,page('Families',f'<h1>Families</h1>{form}<ul>{items}</ul>')
        if p.path=='/children':
            if method=='POST':
                d=self.form(); i=state['next_ids']['child']; state['next_ids']['child']+=1; state['children'][i]=Child(i,int(d['family_id'][0]),d['name'][0],d.get('allergy_notes',[''])[0],d.get('immunizations',[''])[0]); save_seed(); return 303,'/children'
            fams=''.join(f'<option value="{f.id}">{escape(f.name)}</option>' for f in state['families'].values())
            items=''.join(f'<li>#{c.id} {escape(c.name)} (family {c.family_id})</li>' for c in state['children'].values())
            form=f'<form method="post"><select name="family_id">{fams}</select><input name="name" required><button>Add child</button></form>'
            return 200,page('Children',f'<h1>Children</h1>{form}<ul>{items}</ul>')
        if p.path=='/invoices':
            if method=='POST':
                d=self.form(); i=state['next_ids']['invoice']; state['next_ids']['invoice']+=1; inv=Invoice(i,int(d['family_id'][0]),int(d['child_id'][0]) if d.get('child_id',[""])[0] else None,float(d['amount'][0])); inv.history.append({'event':'created','when':inv.created_at}); state['invoices'][i]=inv; save_seed(); return 303,'/invoices'
            fams=''.join(f'<option value="{f.id}">{escape(f.name)}</option>' for f in state['families'].values())
            kids=''.join(f'<option value="{c.id}">{escape(c.name)}</option>' for c in state['children'].values())
            items=''.join(f'<li>#{i.id} ${i.amount:.2f} status={i.status} payment={i.payment_state} <form method="post" action="/invoices/{i.id}/pay" style="display:inline"><button>Mark paid</button></form></li>' for i in state['invoices'].values())
            form=f'<form method="post"><select name="family_id">{fams}</select><select name="child_id"><option value="">-- optional child --</option>{kids}</select><input name="amount" type="number" step="0.01" required><button>Create invoice</button></form>'
            return 200,page('Invoices',f'<h1>Invoices</h1>{form}<ul>{items}</ul>')
        if method=='POST' and p.path.startswith('/invoices/') and p.path.endswith('/pay'):
            inv=state['invoices'][int(p.path.split('/')[2])]; inv.payment_state='paid'; inv.status='completed'; inv.history.append({'event':'paid','when':datetime.utcnow().isoformat(timespec='seconds')}); save_seed(); return 303,'/invoices'
        return 404,page('Not found','<h1>Not found</h1>')
    def form(self):
        l=int(self.headers.get('Content-Length','0')); return parse_qs(self.rfile.read(l).decode())
    def respond(self, code, body):
        if code==303:
            self.send_response(303); self.send_header('Location',body); self.end_headers(); return
        self.send_response(code); self.send_header('Content-Type','text/html; charset=utf-8'); self.end_headers(); self.wfile.write(body.encode())

seed()

def run(host='0.0.0.0', port=8000): ThreadingHTTPServer((host,port),H).serve_forever()
if __name__=='__main__': run()
