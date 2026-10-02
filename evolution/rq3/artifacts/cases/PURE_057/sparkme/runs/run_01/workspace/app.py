import json
import os
import re
import threading
import time
from copy import deepcopy
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

DATA_FILE = os.path.join(os.path.dirname(__file__), 'sprat_data.json')
DEFAULT_DATA = {
    'users': [
        {'username': 'admin', 'password': 'admin', 'role': 'administrator'},
        {'username': 'pm', 'password': 'pm', 'role': 'project_manager'},
        {'username': 'analyst', 'password': 'analyst', 'role': 'analyst'},
        {'username': 'guest', 'password': 'guest', 'role': 'guest'},
    ],
    'glossary': {'policy': 'An approved rule or control source', 'requirement': 'A statement the system shall satisfy'},
    'projects': [],
    'sessions': {},
    'next_ids': {'project': 1, 'artifact': 1, 'comment': 1, 'notification': 1, 'version': 1},
}

lock = threading.RLock()


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return deepcopy(DEFAULT_DATA)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, sort_keys=True)


def next_id(data, key):
    value = data['next_ids'][key]
    data['next_ids'][key] += 1
    return value


def find_user(data, username):
    return next((u for u in data['users'] if u['username'] == username), None)


def find_project(data, project_id):
    return next((p for p in data['projects'] if p['id'] == project_id), None)


def find_artifact(project, artifact_id):
    return next((a for a in project['artifacts'] if a['id'] == artifact_id), None)


def create_notification(data, username, message):
    data['notifications'] = data.get('notifications', [])
    data['notifications'].append({'id': next_id(data, 'notification'), 'username': username, 'message': message, 'ts': time.time()})


def term_warnings(data, term):
    warnings = []
    glossary = data.get('glossary', {})
    lower = term.lower()
    for existing in glossary:
        if existing.lower() == lower:
            warnings.append({'type': 'duplicate', 'message': f'{term} already exists in glossary.'})
        elif existing.lower() in lower or lower in existing.lower() or levenshtein(existing.lower(), lower) <= 2:
            warnings.append({'type': 'near_match', 'message': f'{term} is close to approved term {existing}.'})
    return warnings


def levenshtein(a, b):
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[-1] + 1, previous[j - 1] + (ca != cb)))
        previous = current
    return previous[-1]


def auth_user(data, handler):
    cookie = handler.headers.get('Cookie', '')
    m = re.search(r'session=([a-f0-9]+)', cookie)
    if not m:
        return None
    return data.get('sessions', {}).get(m.group(1))


def can_edit(role):
    return role in {'administrator', 'project_manager', 'analyst'}


def html_page(title, body):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>body{{font-family:sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:.4rem;vertical-align:top}}.warn{{color:#8a5}}.err{{color:#b00}}.muted{{color:#666}}textarea,input,select{{width:100%;box-sizing:border-box}}</style></head><body>{body}</body></html>'


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with lock:
            data = load_data()
            user = auth_user(data, self)
            parsed = urlparse(self.path)
            path = parsed.path
            if path == '/':
                self.respond(HTTPStatus.OK, html_page('SPRAT', self.dashboard(data, user)))
            elif path == '/login':
                self.respond(HTTPStatus.OK, html_page('Login', self.login_form()))
            elif path == '/project/new':
                self.respond(HTTPStatus.OK, html_page('New Project', self.project_form(user)))
            elif path.startswith('/project/'):
                self.route_project_get(data, user, path)
            elif path == '/api/warnings':
                qs = parse_qs(parsed.query)
                term = qs.get('term', [''])[0]
                self.json({'warnings': term_warnings(data, term)})
            else:
                self.respond(HTTPStatus.NOT_FOUND, 'Not found')

    def do_POST(self):
        with lock:
            data = load_data()
            user = auth_user(data, self)
            length = int(self.headers.get('Content-Length', 0))
            payload = self.rfile.read(length).decode('utf-8')
            form = parse_qs(payload)
            path = urlparse(self.path).path
            if path == '/login':
                self.handle_login(data, form)
            elif path == '/project/new':
                self.handle_project_new(data, user, form)
            elif path.startswith('/project/'):
                self.route_project_post(data, user, path, form)
            else:
                self.respond(HTTPStatus.NOT_FOUND, 'Not found')

    def route_project_get(self, data, user, path):
        parts = path.strip('/').split('/')
        if len(parts) == 2:
            project = find_project(data, int(parts[1]))
            if not project:
                return self.respond(HTTPStatus.NOT_FOUND, 'Project not found')
            return self.respond(HTTPStatus.OK, html_page(project['name'], self.project_view(project, user, data)))
        if len(parts) == 4 and parts[2] == 'artifact' and parts[3].isdigit():
            project = find_project(data, int(parts[1]))
            art = find_artifact(project, int(parts[3]))
            return self.respond(HTTPStatus.OK, html_page('Artifact', self.artifact_view(project, art, user, data)))
        self.respond(HTTPStatus.NOT_FOUND, 'Not found')

    def route_project_post(self, data, user, path, form):
        parts = path.strip('/').split('/')
        if len(parts) == 2 and parts[1].isdigit() and form.get('action', [''])[0] == 'add_artifact':
            return self.handle_add_artifact(data, user, int(parts[1]), form)
        if len(parts) == 4 and parts[2] == 'artifact' and form.get('action', [''])[0] == 'save_artifact':
            return self.handle_save_artifact(data, user, int(parts[1]), int(parts[3]), form)
        self.respond(HTTPStatus.NOT_FOUND, 'Not found')

    def handle_login(self, data, form):
        user = find_user(data, form.get('username', [''])[0])
        if not user or user['password'] != form.get('password', [''])[0]:
            return self.respond(HTTPStatus.UNAUTHORIZED, 'Invalid login')
        sid = f'{int(time.time()*1000):x}'
        data.setdefault('sessions', {})[sid] = user
        save_data(data)
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header('Set-Cookie', f'session={sid}; Path=/')
        self.send_header('Location', '/')
        self.end_headers()

    def handle_project_new(self, data, user, form):
        if not user or not can_edit(user['role']):
            return self.respond(HTTPStatus.FORBIDDEN, 'Forbidden')
        project = {'id': next_id(data, 'project'), 'name': form.get('name', ['Untitled'])[0], 'artifacts': [], 'created_by': user['username']}
        data['projects'].append(project)
        save_data(data)
        self.redirect(f'/project/{project["id"]}')

    def handle_add_artifact(self, data, user, project_id, form):
        if not user or not can_edit(user['role']):
            return self.respond(HTTPStatus.FORBIDDEN, 'Forbidden')
        project = find_project(data, project_id)
        artifact = {
            'id': next_id(data, 'artifact'),
            'title': form.get('title', ['New item'])[0],
            'type': form.get('type', ['requirement'])[0],
            'content': form.get('content', [''])[0],
            'status': 'draft',
            'versions': [],
            'trace_links': [],
            'comments': [],
            'history': [],
            'flags': term_warnings(data, form.get('title', [''])[0]),
            'created_by': user['username'],
        }
        project['artifacts'].append(artifact)
        save_data(data)
        self.redirect(f'/project/{project_id}/artifact/{artifact["id"]}')

    def handle_save_artifact(self, data, user, project_id, artifact_id, form):
        if not user or not can_edit(user['role']):
            return self.respond(HTTPStatus.FORBIDDEN, 'Forbidden')
        project = find_project(data, project_id)
        artifact = find_artifact(project, artifact_id)
        if artifact.get('lock') and artifact['lock'] != user['username']:
            return self.respond(HTTPStatus.CONFLICT, 'Overlapping edit detected')
        old = deepcopy(artifact)
        artifact['title'] = form.get('title', [''])[0]
        artifact['content'] = form.get('content', [''])[0]
        artifact['status'] = form.get('status', [artifact['status']])[0]
        artifact['versions'].append({'id': next_id(data, 'version'), 'snapshot': old, 'ts': time.time(), 'user': user['username']})
        artifact['history'].append({'user': user['username'], 'ts': time.time(), 'changed': ['title', 'content', 'status']})
        artifact['flags'] = term_warnings(data, artifact['title'])
        save_data(data)
        self.redirect(f'/project/{project_id}/artifact/{artifact_id}')

    def dashboard(self, data, user):
        projects = ''.join(f'<li><a href="/project/{p["id"]}">{p["name"]}</a></li>' for p in data['projects']) or '<li class="muted">No projects yet</li>'
        notifications = ''.join(f'<li>{n["message"]}</li>' for n in data.get('notifications', []) if not user or n['username'] == user['username']) or '<li class="muted">No notifications</li>'
        login = f'<p>Logged in as <b>{user["username"]}</b> ({user["role"]})</p>' if user else '<p><a href="/login">Login</a></p>'
        return f'''{login}<h1>SPRAT Dashboard</h1><p>Traceability, glossary warnings, versions, review queue, and import staging are supported in a compact demo form.</p><p><a href="/project/new">Create project</a></p><h2>Projects</h2><ul>{projects}</ul><h2>Notifications</h2><ul>{notifications}</ul>'''

    def login_form(self):
        return '<form method="post"><label>Username<input name="username"></label><label>Password<input name="password" type="password"></label><button>Login</button></form>'

    def project_form(self, user):
        if not user or not can_edit(user['role']):
            return '<p>Login as administrator, project manager, or analyst to create projects.</p>'
        return '<form method="post"><label>Name<input name="name"></label><button>Create project</button></form>'

    def project_view(self, project, user, data):
        items = ''.join(f'<tr><td><a href="/project/{project["id"]}/artifact/{a["id"]}">{a["title"]}</a></td><td>{a["type"]}</td><td>{a["status"]}</td><td>{len(a.get("flags",[]))}</td></tr>' for a in project['artifacts']) or '<tr><td colspan="4">No artifacts</td></tr>'
        add = '' if not user or not can_edit(user['role']) else f'''<h2>Add artifact</h2><form method="post"><input type="hidden" name="action" value="add_artifact"><label>Title<input name="title"></label><label>Type<select name="type"><option>goal</option><option>scenario</option><option>policy</option><option>requirement</option></select></label><label>Content<textarea name="content"></textarea></label><button>Add</button></form>'''
        return f'{add}<h2>Artifacts</h2><table><tr><th>Title</th><th>Type</th><th>Status</th><th>Warnings</th></tr>{items}</table><p><a href="/">Back</a></p>'

    def artifact_view(self, project, art, user, data):
        flags = ''.join(f'<li class="warn">{f["message"]}</li>' for f in art.get('flags', [])) or '<li class="muted">No warnings</li>'
        comments = ''.join(f'<li>{c["user"]}: {c["text"]}</li>' for c in art['comments']) or '<li class="muted">No comments</li>'
        versions = ''.join(f'<li>v{v["id"]} by {v["user"]}</li>' for v in art['versions']) or '<li class="muted">No versions yet</li>'
        form = ''
        if user and can_edit(user['role']):
            form = f'''<h2>Edit</h2><form method="post"><input type="hidden" name="action" value="save_artifact"><label>Title<input name="title" value="{art['title']}"></label><label>Status<input name="status" value="{art['status']}"></label><label>Content<textarea name="content">{art['content']}</textarea></label><button>Save</button></form>'''
        return f'<p><a href="/project/{project["id"]}">Back to project</a></p><p><b>Type:</b> {art["type"]} <b>Status:</b> {art["status"]}</p><h2>Warnings</h2><ul>{flags}</ul><h2>Comments</h2><ul>{comments}</ul><h2>Versions</h2><ul>{versions}</ul>{form}'

    def respond(self, code, body):
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def redirect(self, location):
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header('Location', location)
        self.end_headers()

    def json(self, obj):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode('utf-8'))


def main():
    host = os.environ.get('SPRAT_HOST', '127.0.0.1')
    port = int(os.environ.get('SPRAT_PORT', '8000'))
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f'SPRAT running on http://{host}:{port}', flush=True)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
