from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import csv, io, json, os, uuid

DATA_FILE = Path('/workspace/sprat_data.json')
ROLE_ORDER = {'guest': 0, 'analyst': 1, 'manager': 2, 'admin': 3}


def now(): return datetime.now(timezone.utc).isoformat()

def load_data():
    if DATA_FILE.exists(): return json.loads(DATA_FILE.read_text())
    return {'users': {'admin': {'role':'admin','projects':['default']}, 'manager': {'role':'manager','projects':['default']}, 'analyst': {'role':'analyst','projects':['default']}, 'guest': {'role':'guest','projects':['default']}}, 'projects': {'default': {'sensitivity':'low'}, 'sensitive': {'sensitivity':'high'}}, 'artifacts': [], 'traces': [], 'audit': [], 'exceptions': []}

def save_data(data): DATA_FILE.write_text(json.dumps(data, indent=2))

def log_audit(data, action, obj_type, obj_id, before=None, after=None): data['audit'].append({'ts': now(), 'action': action, 'type': obj_type, 'id': obj_id, 'before': before, 'after': after})

def user_from(headers, data): return headers.get('X-User', 'guest'), data['users'].get(headers.get('X-User', 'guest'), data['users']['guest'])

def json_response(handler, obj, code=200):
    body = json.dumps(obj).encode()
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers(); handler.wfile.write(body)

def text_response(handler, text, code=200, ctype='text/plain'):
    body = text.encode()
    handler.send_response(code)
    handler.send_header('Content-Type', ctype)
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers(); handler.wfile.write(body)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = load_data(); u = user_from(self.headers, data)[1]
        p = urlparse(self.path)
        if p.path == '/': return text_response(self, '<html><body><h1>SPRAT</h1></body></html>', ctype='text/html')
        if p.path == '/api': return json_response(self, {'endpoints':['/api/items','/api/traces','/api/compare','/api/export','/api/audit','/api/validate','/api/exceptions']})
        if p.path == '/api/items':
            project = parse_qs(p.query).get('project', [None])[0]
            items = [dict(i, notes=None, draft_comments=None, personal_data=None) if u['role']=='guest' else i for i in data['artifacts'] if not project or i['project']==project]
            return json_response(self, items)
        if p.path == '/api/compare':
            q = parse_qs(p.query); a=q.get('a',[''])[0]; b=q.get('b',[''])[0]
            A=[i for i in data['artifacts'] if i['project']==a]; B=[i for i in data['artifacts'] if i['project']==b]
            ma={i['title']:i for i in A}; mb={i['title']:i for i in B}
            return json_response(self, {'shared_titles':sorted(set(ma)&set(mb)),'only_in_a':sorted(set(ma)-set(mb)),'only_in_b':sorted(set(mb)-set(ma))})
        if p.path == '/api/audit': return json_response(self, data['audit'])
        if p.path == '/api/validate':
            warnings=[]; ids={i['id'] for i in data['artifacts']}
            for i in data['artifacts']:
                if i['type']=='requirement' and i.get('source_policy_reference') and not i.get('trace_links'): warnings.append({'item':i['id'],'issue':'requirement claims policy source but has no trace links'})
            for t in data['traces']:
                if t['source_id'] not in ids or t['target_id'] not in ids: warnings.append({'trace':t['id'],'issue':'broken link'})
            return json_response(self, {'warnings':warnings})
        return text_response(self, 'not found', 404)

    def do_POST(self):
        data = load_data(); username, u = user_from(self.headers, data)
        length = int(self.headers.get('Content-Length', '0'))
        payload = json.loads(self.rfile.read(length) or b'{}')
        if self.path == '/api/items':
            item={'id':str(uuid.uuid4()),'project':payload.get('project','default'),'type':payload.get('type'),'title':payload.get('title',''),'description':payload.get('description',''),'classification':payload.get('classification','uncategorized'),'status':payload.get('status','draft'),'source_policy_reference':payload.get('source_policy_reference'),'policy_excerpt':payload.get('policy_excerpt'),'rationale':payload.get('rationale'),'actor':payload.get('actor'),'trigger':payload.get('trigger'),'outcome':payload.get('outcome'),'derived_from':payload.get('derived_from',[]),'trace_links':payload.get('trace_links',[]),'created_by':username,'created_at':now(),'updated_at':now(),'version':1,'sensitivity':payload.get('sensitivity','normal')}
            data['artifacts'].append(item); log_audit(data,'create','item',item['id'],after=item); save_data(data); return json_response(self, item, 201)
        if self.path == '/api/traces':
            if u['role']=='guest': return json_response(self, {'error':'guest cannot create traces'}, 403)
            tr={'id':str(uuid.uuid4()),'source_id':payload['source_id'],'target_id':payload['target_id'],'kind':payload.get('kind','derived-from'),'primary':bool(payload.get('primary',False)),'created_by':username,'created_at':now(),'approved':False}
            data['traces'].append(tr); log_audit(data,'create','trace',tr['id'],after=tr); save_data(data); return json_response(self, tr, 201)
        if self.path == '/api/export':
            if u['role']=='guest': return json_response(self, {'error':'raw exports restricted'}, 403)
            project=payload.get('project','default'); fmt=payload.get('format','json'); items=[i for i in data['artifacts'] if i['project']==project]
            if fmt=='csv':
                out=io.StringIO(); w=csv.DictWriter(out, fieldnames=['id','type','title','description','classification','created_by','created_at']); w.writeheader(); [w.writerow({k:i.get(k,'') for k in w.fieldnames}) for i in items]
                return text_response(self, out.getvalue(), ctype='text/csv')
            return json_response(self, {'items':items,'traces':[t for t in data['traces'] if any(i['id']==t['source_id'] or i['id']==t['target_id'] for i in items)]})
        if self.path == '/api/exceptions':
            if ROLE_ORDER[u['role']] < ROLE_ORDER['manager']: return json_response(self, {'error':'manager approval required'}, 403)
            exc={'id':str(uuid.uuid4()),'reason':payload.get('reason',''),'workaround':payload.get('workaround',''),'target':payload.get('target',''),'expires_at':payload.get('expires_at'),'created_by':username,'created_at':now(),'approved':False}
            data['exceptions'].append(exc); log_audit(data,'create','exception',exc['id'],after=exc); save_data(data); return json_response(self, exc, 201)
        return text_response(self, 'not found', 404)


def main():
    port=int(os.environ.get('PORT','8000')); httpd=ThreadingHTTPServer(('0.0.0.0', port), Handler); httpd.serve_forever()

if __name__ == '__main__': main()
