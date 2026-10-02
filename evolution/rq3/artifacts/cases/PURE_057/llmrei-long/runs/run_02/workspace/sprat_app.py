import json
import os
from copy import deepcopy
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

DATA_FILE = os.environ.get('SPRAT_DATA_FILE', os.path.join(os.path.dirname(__file__), 'data', 'sprat.json'))
DEFAULT_PORT = int(os.environ.get('PORT', '8000'))

ROLES = ['administrator', 'project_manager', 'analyst', 'guest']
ROLE_PERMISSIONS = {
    'administrator': {'read', 'write', 'admin'},
    'project_manager': {'read', 'write'},
    'analyst': {'read', 'write'},
    'guest': {'read'},
}
ARTIFACT_TYPES = {'goal', 'scenario', 'requirement', 'policy'}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if not os.path.exists(DATA_FILE):
        return {'artifacts': {}, 'next_id': 1, 'history': []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_state(state):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    tmp = DATA_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, sort_keys=True)
    os.replace(tmp, DATA_FILE)


def add_history(state, action, artifact_id=None, before=None, after=None, actor='system'):
    state['history'].append({
        'timestamp': now_iso(),
        'actor': actor,
        'action': action,
        'artifact_id': artifact_id,
        'before': deepcopy(before),
        'after': deepcopy(after),
    })


def create_artifact(state, artifact_type, title, content='', created_by='system', classifications=None, sources=None, primary_source_id=None):
    if artifact_type not in ARTIFACT_TYPES:
        raise ValueError('invalid artifact type')
    artifact_id = str(state['next_id'])
    state['next_id'] += 1
    artifact = {
        'id': artifact_id,
        'type': artifact_type,
        'title': title,
        'content': content,
        'classifications': classifications or [],
        'sources': sources or [],
        'primary_source_id': primary_source_id,
        'created_by': created_by,
        'created_at': now_iso(),
        'updated_at': now_iso(),
        'history': [],
    }
    state['artifacts'][artifact_id] = artifact
    add_history(state, 'create', artifact_id, None, artifact, created_by)
    artifact['history'].append({'timestamp': now_iso(), 'action': 'create', 'actor': created_by})
    return artifact


def update_artifact(state, artifact_id, updates, actor='system'):
    artifact = state['artifacts'][artifact_id]
    before = deepcopy(artifact)
    for key, value in updates.items():
        if key in {'title', 'content', 'classifications', 'sources', 'primary_source_id'}:
            artifact[key] = value
    artifact['updated_at'] = now_iso()
    artifact['history'].append({'timestamp': now_iso(), 'action': 'update', 'actor': actor, 'updates': deepcopy(updates)})
    add_history(state, 'update', artifact_id, before, artifact, actor)
    return artifact


def link_requirement_sources(state):
    by_source = {}
    for artifact in state['artifacts'].values():
        if artifact['type'] == 'requirement':
            for source in artifact.get('sources', []):
                by_source.setdefault(source, []).append(artifact['id'])
    return by_source


def with_traceability(state, artifact):
    result = deepcopy(artifact)
    if artifact['type'] == 'requirement':
        result['source_artifacts'] = [state['artifacts'][sid] for sid in artifact.get('sources', []) if sid in state['artifacts']]
    if artifact['type'] == 'policy':
        result['derived_requirements'] = [state['artifacts'][rid] for rid in link_requirement_sources(state).get(artifact['id'], []) if rid in state['artifacts']]
    return result


def role_from_request(handler):
    role = handler.headers.get('X-Role', 'guest').strip().lower()
    return role if role in ROLES else 'guest'


def can(role, permission):
    return permission in ROLE_PERMISSIONS.get(role, set())


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        data = json.dumps(payload).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        state = load_state()
        role = role_from_request(self)
        if not can(role, 'read'):
            return self._send(403, {'error': 'forbidden'})
        path = urlparse(self.path).path
        if path == '/health':
            return self._send(200, {'status': 'ok'})
        if path == '/artifacts':
            q = parse_qs(urlparse(self.path).query)
            items = list(state['artifacts'].values())
            if 'type' in q:
                items = [a for a in items if a['type'] == q['type'][0]]
            return self._send(200, {'artifacts': [with_traceability(state, a) for a in items]})
        if path.startswith('/artifacts/'):
            artifact_id = path.split('/')[-1]
            artifact = state['artifacts'].get(artifact_id)
            if not artifact:
                return self._send(404, {'error': 'not found'})
            return self._send(200, with_traceability(state, artifact))
        if path == '/compare':
            q = parse_qs(urlparse(self.path).query)
            a = state['artifacts'].get(q.get('a', [''])[0])
            b = state['artifacts'].get(q.get('b', [''])[0])
            if not a or not b:
                return self._send(404, {'error': 'not found'})
            return self._send(200, {'a': deepcopy(a), 'b': deepcopy(b), 'differences': diff_artifacts(a, b)})
        return self._send(404, {'error': 'not found'})

    def do_POST(self):
        state = load_state()
        role = role_from_request(self)
        if not can(role, 'write'):
            return self._send(403, {'error': 'forbidden'})
        path = urlparse(self.path).path
        if path == '/artifacts':
            length = int(self.headers.get('Content-Length', '0'))
            payload = json.loads(self.rfile.read(length) or b'{}')
            artifact = create_artifact(state, payload['type'], payload['title'], payload.get('content', ''), role, payload.get('classifications', []), payload.get('sources', []), payload.get('primary_source_id'))
            save_state(state)
            return self._send(201, with_traceability(state, artifact))
        if path.startswith('/artifacts/') and path.endswith('/history'):
            artifact_id = path.split('/')[2]
            artifact = state['artifacts'].get(artifact_id)
            if not artifact:
                return self._send(404, {'error': 'not found'})
            return self._send(200, {'history': artifact['history']})
        return self._send(404, {'error': 'not found'})

    def do_PUT(self):
        state = load_state()
        role = role_from_request(self)
        if not can(role, 'write'):
            return self._send(403, {'error': 'forbidden'})
        path = urlparse(self.path).path
        if path.startswith('/artifacts/'):
            artifact_id = path.split('/')[-1]
            if artifact_id not in state['artifacts']:
                return self._send(404, {'error': 'not found'})
            length = int(self.headers.get('Content-Length', '0'))
            payload = json.loads(self.rfile.read(length) or b'{}')
            artifact = update_artifact(state, artifact_id, payload, role)
            save_state(state)
            return self._send(200, with_traceability(state, artifact))
        return self._send(404, {'error': 'not found'})


def diff_artifacts(a, b):
    keys = ['type', 'title', 'content', 'classifications', 'sources', 'primary_source_id']
    diffs = {}
    for k in keys:
        if a.get(k) != b.get(k):
            diffs[k] = {'a': a.get(k), 'b': b.get(k)}
    return diffs


def main():
    httpd = ThreadingHTTPServer(('0.0.0.0', DEFAULT_PORT), Handler)
    print(f'SPRAT listening on http://0.0.0.0:{DEFAULT_PORT}', flush=True)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
