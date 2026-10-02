import json, time
from pathlib import Path
from wsgiref.simple_server import make_server

BASE_DIR = Path('/workspace')
DATA_DIR = BASE_DIR / 'data'
STATE_FILE = DATA_DIR / 'sprat_state.json'
DEFAULT_STATE = {'users': [{'username': 'admin', 'role': 'administrator'}, {'username': 'manager', 'role': 'project_manager'}, {'username': 'analyst', 'role': 'analyst'}, {'username': 'guest', 'role': 'guest'}], 'projects': [{'id': 1, 'name': 'Sample Project', 'status': 'active', 'items': [{'id': 1, 'type': 'goal', 'title': 'Protect user data', 'policy': 'Privacy Policy A', 'status': 'draft', 'last_modified_by': 'analyst', 'updated_at': time.time(), 'source': 'imported', 'trace_links': [1]}, {'id': 2, 'type': 'policy', 'title': 'Privacy Policy A', 'status': 'approved', 'last_modified_by': 'manager', 'updated_at': time.time(), 'source': 'manual', 'trace_links': []}], 'conflicts': [], 'imports': [], 'glossary': {'requirement': {'definition': 'A statement of needed system behavior.'}, 'policy': {'definition': 'A governing rule or principle.'}}}], 'audit_log': []}


def load_state():
    DATA_DIR.mkdir(exist_ok=True)
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else DEFAULT_STATE


def save_state(state):
    DATA_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def create_app():
    state = load_state()

    def app(environ, start_response):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        user = environ.get('HTTP_X_USER', 'guest')
        actor = next((u for u in state['users'] if u['username'] == user), {'username': user, 'role': 'guest'})

        def body_json(obj, status='200 OK'):
            data = json.dumps(obj).encode()
            start_response(status, [('Content-Type', 'application/json'), ('Content-Length', str(len(data)))])
            return [data]

        def forbidden(): return body_json({'error': 'forbidden'}, '403 Forbidden')
        def not_found(): return body_json({'error': 'not_found'}, '404 Not Found')
        def read_body():
            n = int(environ.get('CONTENT_LENGTH') or 0)
            return json.loads(environ['wsgi.input'].read(n) or b'{}')

        if path == '/' and method == 'GET':
            return body_json({'name': 'SPRAT', 'description': 'Security and Privacy Requirements Analysis Tool', 'projects': len(state['projects']), 'roles': ['administrator', 'project_manager', 'analyst', 'guest']})
        if path == '/dashboard' and method == 'GET':
            project = state['projects'][0]
            unresolved = [i for i in project['items'] if i.get('status') in ('needs review', 'conflicting mapping', 'unresolved import')]
            return body_json({'project': project['name'], 'recent_items': project['items'][-5:], 'unresolved': unresolved, 'audit_log_entries': len(state['audit_log'])})
        if path.startswith('/search') and method == 'GET':
            q = (environ.get('QUERY_STRING', '').split('q=')[-1]).lower()
            matches = []
            for project in state['projects']:
                for item in project['items']:
                    if q and q in json.dumps(item).lower(): matches.append({'project_id': project['id'], 'item': item})
            return body_json({'query': q, 'matches': matches})
        if path == '/projects/1/items' and method == 'POST':
            if actor['role'] not in ('administrator', 'project_manager', 'analyst'): return forbidden()
            payload = read_body(); project = state['projects'][0]
            new_id = max([i['id'] for i in project['items']] + [0]) + 1
            item = {'id': new_id, 'type': payload.get('type', 'requirement'), 'title': payload.get('title', 'Untitled'), 'status': payload.get('status', 'draft'), 'policy': payload.get('policy'), 'source': payload.get('source', 'manual'), 'trace_links': payload.get('trace_links', []), 'last_modified_by': actor['username'], 'updated_at': time.time(), 'rationale': payload.get('rationale'), 'notes': payload.get('notes'), 'assumptions': payload.get('assumptions')}
            project['items'].append(item); state['audit_log'].append({'action': 'create_item', 'user': actor['username'], 'item_id': new_id, 'ts': time.time()}); save_state(state); return body_json(item, '201 Created')
        if path == '/projects/1/conflicts' and method == 'POST':
            if actor['role'] not in ('administrator', 'project_manager', 'analyst'): return forbidden()
            payload = read_body(); project = state['projects'][0]; conflict = {'id': len(project['conflicts']) + 1, 'item_id': payload.get('item_id'), 'status': 'needs review', 'details': payload.get('details', ''), 'comments': []}; project['conflicts'].append(conflict); save_state(state); return body_json(conflict, '201 Created')
        if path == '/projects/1/imports' and method == 'POST':
            if actor['role'] not in ('administrator', 'project_manager', 'analyst'): return forbidden()
            payload = read_body(); project = state['projects'][0]; staging = []
            for raw in payload.get('items', []):
                mapped = dict(raw); mapped['import_status'] = 'review_required' if raw.get('ambiguous') else 'staged'; staging.append(mapped)
            project['imports'].append({'created_by': actor['username'], 'staging': staging, 'published': False}); save_state(state); return body_json({'staged_count': len(staging), 'review_queue': [i for i in staging if i['import_status'] == 'review_required']}, '202 Accepted')
        if path.startswith('/projects/1/glossary/') and method == 'GET':
            term = path.rsplit('/', 1)[-1]; project = state['projects'][0]; definition = project['glossary'].get(term.lower())
            return body_json({'term': term, 'accepted_definition': definition['definition'], 'context': 'approved glossary term'} if definition else {'term': term, 'warnings': ['possible duplicate or near match'] if any(term.lower() in existing for existing in project['glossary']) else [], 'suggestions': list(project['glossary'].keys())})
        return not_found()
    return app


def run(host='0.0.0.0', port=8000):
    with make_server(host, port, create_app()) as httpd:
        httpd.serve_forever()
