from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from datetime import datetime, timezone
from typing import Any
import json, os, uuid

DATA_FILE = Path(os.environ.get('SPRAT_DATA_FILE', '/workspace/sprat_data.json'))
ROLES = {'admin', 'manager', 'analyst', 'guest'}
ROLE_PERMS = {'admin': {'read','write','compare','export','approve'}, 'manager': {'read','write','compare','export','approve'}, 'analyst': {'read','write','compare'}, 'guest': {'read','compare'}}

def now(): return datetime.now(timezone.utc).isoformat()
def load_state(): return json.loads(DATA_FILE.read_text()) if DATA_FILE.exists() else {'items': {}, 'links': [], 'audit': []}
def save_state(state): DATA_FILE.write_text(json.dumps(state, indent=2, sort_keys=True))
def audit(state, action, actor, details): state['audit'].append({'ts': now(), 'action': action, 'actor': actor, 'details': details})
def user():
    role = os.environ.get('SPRAT_ROLE', 'guest'); name = os.environ.get('SPRAT_USER', 'guest')
    if role not in ROLES: raise ValueError('invalid role')
    return {'name': name, 'role': role}
def require(state, perm):
    u = user()
    if perm not in ROLE_PERMS[u['role']]: raise PermissionError(f'role {u["role"]} lacks {perm}')
    return u
def visible(u, item): return not (u['role']=='guest' and (item.get('sensitive') or not item.get('approved')))

class App:
    def get(self, path, query):
        state = load_state(); u = user()
        if path == '/health': return 200, {'status': 'ok'}
        if path == '/items':
            items=[v for v in state['items'].values() if visible(u,v)]
            p=query.get('project',[None])[0]
            if p: items=[i for i in items if i.get('project')==p]
            return 200, {'items': items}
        if path.startswith('/items/'):
            iid = path.split('/')[-1]
            item = state['items'].get(iid)
            if not item: return 404, {'error':'not found'}
            if not visible(u,item): return 403, {'error':'restricted'}
            links=[l for l in state['links'] if l['source_id']==iid or l['target_id']==iid]
            return 200, {'item': item, 'links': links}
        if path == '/compare':
            require(state,'compare')
            a,b=query.get('a',[None])[0],query.get('b',[None])[0]
            ia,ib=state['items'].get(a),state['items'].get(b)
            if not ia or not ib: return 404, {'error':'missing item'}
            ca,cb=set(ia.get('classifications',[])),set(ib.get('classifications',[]))
            return 200, {'common': sorted(ca&cb), 'diff': {'only_a': sorted(ca-cb), 'only_b': sorted(cb-ca)}, 'items':[ia,ib]}
        if path == '/audit':
            require(state,'read'); return 200, {'audit': state['audit']}
        if path == '/export':
            require(state,'export'); fmt=query.get('format',['json'])[0]
            items=[v for v in state['items'].values() if visible(u,v)]
            if fmt=='csv':
                lines=['id,title,type,project,approved']+[f"{i['id']},{i['title']},{i['item_type']},{i.get('project','')},{i.get('approved',False)}" for i in items]
                return 200, {'csv':'\n'.join(lines)}
            return 200, {'items': items, 'links': state['links'], 'audit': state['audit']}
        return 404, {'error': 'unknown endpoint'}
    def post(self, path, body):
        state = load_state(); u = require(state,'write')
        if path == '/items':
            iid=str(uuid.uuid4()); body.update({'id':iid,'created_at':now(),'updated_at':now(),'created_by':u['name'],'updated_by':u['name'],'version':1,'approved': body.get('approved', False)})
            state['items'][iid]=body; audit(state,'create_item',u['name'],{'id':iid}); save_state(state); return 200, body
        if path == '/links':
            if body.get('source_id') not in state['items'] or body.get('target_id') not in state['items']: return 400, {'error':'missing source or target'}
            lid=str(uuid.uuid4()); body.update({'id':lid,'created_at':now(),'created_by':u['name']}); state['links'].append(body); audit(state,'create_link',u['name'],body); save_state(state); return 200, body
        if path.startswith('/items/') and path.endswith('/approve'):
            require(state,'approve'); iid=path.split('/')[-2]; item=state['items'].get(iid)
            if not item: return 404, {'error':'not found'}
            item['approved']=True; item['updated_at']=now(); item['updated_by']=u['name']; item['version']=item.get('version',0)+1; audit(state,'approve',u['name'],{'id':iid}); save_state(state); return 200, item
        return 404, {'error':'unknown endpoint'}
app = App()

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        data=json.dumps(obj).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        p=urlparse(self.path); code,obj=app.get(p.path, parse_qs(p.query)); self._send(code,obj)
    def do_POST(self):
        p=urlparse(self.path); n=int(self.headers.get('Content-Length','0')); raw=self.rfile.read(n).decode() if n else '{}'; body=json.loads(raw or '{}'); code,obj=app.post(p.path, body); self._send(code,obj)
    def log_message(self, *args): pass

def main():
    port=int(os.environ.get('PORT','8000'))
    server=ThreadingHTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

if __name__ == '__main__': main()
