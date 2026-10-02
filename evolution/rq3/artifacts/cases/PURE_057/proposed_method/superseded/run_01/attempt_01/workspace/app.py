from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Set, Literal, Any
from pathlib import Path
from datetime import datetime, timezone
import json
import uuid
import os

DATA_FILE = Path(os.environ.get('SPRAT_DATA_FILE', '/workspace/sprat_data.json'))
app = FastAPI(title='SPRAT', version='1.0')

ROLES = {'admin', 'manager', 'analyst', 'guest'}
ROLE_PERMS = {
    'admin': {'read', 'write', 'compare', 'export', 'approve', 'admin'},
    'manager': {'read', 'write', 'compare', 'export', 'approve'},
    'analyst': {'read', 'write', 'compare'},
    'guest': {'read', 'compare_published'},
}

class User(BaseModel):
    name: str
    role: Literal['admin', 'manager', 'analyst', 'guest']

class Item(BaseModel):
    title: str
    description: str = ''
    item_type: Literal['goal', 'scenario', 'policy', 'requirement', 'analysis']
    classifications: List[str] = Field(default_factory=list)
    actor: Optional[str] = None
    trigger: Optional[str] = None
    outcome: Optional[str] = None
    source_policy_ref: Optional[str] = None
    source_policy_part: Optional[str] = None
    rationale: Optional[str] = None
    approved: bool = False
    sensitive: bool = False
    project: str = 'default'

class Link(BaseModel):
    source_id: str
    target_id: str
    link_type: Literal['supports', 'derived-from', 'trace', 'reviewed-against']
    primary: bool = False
    note: str = ''

class ExportRequest(BaseModel):
    format: Literal['json', 'csv']
    redacted: bool = True


def now():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {'items': {}, 'links': [], 'users': {}, 'audit': [], 'version_meta': {}}


def save_state(state):
    DATA_FILE.write_text(json.dumps(state, indent=2, sort_keys=True))


def audit(state, action, actor, details):
    state['audit'].append({'ts': now(), 'action': action, 'actor': actor, 'details': details})


def current_user(state) -> User:
    name = os.environ.get('SPRAT_USER', 'guest')
    role = os.environ.get('SPRAT_ROLE', 'guest')
    if role not in ROLES:
        raise HTTPException(400, 'Invalid role')
    return User(name=name, role=role)


def require_perm(state, perm):
    user = current_user(state)
    if perm not in ROLE_PERMS[user.role]:
        raise HTTPException(403, f'Role {user.role} lacks {perm}')
    return user


def item_visible(user: User, item: dict):
    if user.role == 'guest' and (item.get('sensitive') or not item.get('approved')):
        return False
    return True


def linked_items(state, item_id):
    out = []
    for link in state['links']:
        if link['source_id'] == item_id or link['target_id'] == item_id:
            out.append(link)
    return out

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/items')
def create_item(item: Item):
    state = load_state()
    user = require_perm(state, 'write')
    iid = str(uuid.uuid4())
    data = item.dict()
    data.update({'id': iid, 'created_at': now(), 'updated_at': now(), 'created_by': user.name, 'updated_by': user.name, 'version': 1})
    state['items'][iid] = data
    audit(state, 'create_item', user.name, {'id': iid, 'type': item.item_type})
    save_state(state)
    return data

@app.get('/items')
def list_items(project: Optional[str] = None):
    state = load_state()
    user = current_user(state)
    items = [v for v in state['items'].values() if item_visible(user, v)]
    if project:
        items = [i for i in items if i.get('project') == project]
    return {'items': items}

@app.post('/links')
def create_link(link: Link):
    state = load_state()
    user = require_perm(state, 'write')
    if link.source_id not in state['items'] or link.target_id not in state['items']:
        raise HTTPException(400, 'Missing source or target')
    lid = str(uuid.uuid4())
    data = link.dict(); data['id'] = lid; data['created_at'] = now(); data['created_by'] = user.name
    state['links'].append(data)
    audit(state, 'create_link', user.name, data)
    save_state(state)
    return data

@app.get('/items/{item_id}')
def get_item(item_id: str):
    state = load_state()
    user = current_user(state)
    item = state['items'].get(item_id)
    if not item:
        raise HTTPException(404, 'Not found')
    if not item_visible(user, item):
        raise HTTPException(403, 'Restricted')
    return {'item': item, 'links': linked_items(state, item_id)}

@app.get('/compare')
def compare(a: str = Query(...), b: str = Query(...)):
    state = load_state()
    user = require_perm(state, 'compare')
    ia, ib = state['items'].get(a), state['items'].get(b)
    if not ia or not ib:
        raise HTTPException(404, 'Missing item')
    common = sorted(set(ia.get('classifications', [])) & set(ib.get('classifications', [])))
    diff = {'only_a': sorted(set(ia.get('classifications', [])) - set(ib.get('classifications', []))), 'only_b': sorted(set(ib.get('classifications', [])) - set(ia.get('classifications', [])))}
    return {'user': user.dict(), 'common': common, 'diff': diff, 'items': [ia, ib]}

@app.post('/items/{item_id}/approve')
def approve(item_id: str):
    state = load_state()
    user = require_perm(state, 'approve')
    item = state['items'].get(item_id)
    if not item:
        raise HTTPException(404, 'Not found')
    item['approved'] = True
    item['updated_at'] = now()
    item['updated_by'] = user.name
    item['version'] += 1
    audit(state, 'approve', user.name, {'id': item_id})
    save_state(state)
    return item

@app.get('/audit')
def get_audit():
    state = load_state()
    require_perm(state, 'read')
    return {'audit': state['audit']}

@app.get('/export')
def export(format: Literal['json', 'csv'] = 'json'):
    state = load_state()
    user = require_perm(state, 'export')
    items = [v for v in state['items'].values() if item_visible(user, v)]
    if format == 'json':
        return JSONResponse({'items': items, 'links': state['links'], 'audit': state['audit']})
    lines = ['id,title,type,project,approved']
    for i in items:
        lines.append(f"{i['id']},{i['title']},{i['item_type']},{i.get('project','')},{i.get('approved',False)}")
    return JSONResponse({'csv': '\n'.join(lines)})

@app.get('/')
def root():
    return {'name': 'SPRAT', 'endpoints': ['/health', '/items', '/links', '/compare', '/export', '/audit']}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
