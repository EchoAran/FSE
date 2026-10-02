import csv, io, json, sqlite3, datetime as dt
from pathlib import Path
from urllib.parse import parse_qs

DB_PATH = Path('/workspace/sprat.sqlite3')
ROLE_LEVEL = {'guest': 0, 'analyst': 1, 'manager': 2, 'admin': 3}

def now_iso(): return dt.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect_db(); cur = conn.cursor()
    cur.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, sensitivity TEXT NOT NULL DEFAULT 'low', owner TEXT NOT NULL DEFAULT 'admin');
    CREATE TABLE IF NOT EXISTS analyses(id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT 'draft');
    CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY AUTOINCREMENT, analysis_id INTEGER NOT NULL, kind TEXT NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL DEFAULT '', actor TEXT, trigger TEXT, outcome TEXT, classifications TEXT NOT NULL DEFAULT '[]', source_policy_ref TEXT, source_policy_excerpt TEXT, rationale TEXT, sensitive_notes TEXT, legal_compliance TEXT, active INTEGER NOT NULL DEFAULT 1, created_by TEXT NOT NULL, created_at TEXT NOT NULL, updated_by TEXT NOT NULL, updated_at TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 1);
    CREATE TABLE IF NOT EXISTS links(id INTEGER PRIMARY KEY AUTOINCREMENT, source_item_id INTEGER NOT NULL, target_item_id INTEGER NOT NULL, relation TEXT NOT NULL, primary_link INTEGER NOT NULL DEFAULT 0, created_by TEXT NOT NULL, created_at TEXT NOT NULL, note TEXT NOT NULL DEFAULT '');
    CREATE TABLE IF NOT EXISTS audits(id INTEGER PRIMARY KEY AUTOINCREMENT, entity_type TEXT NOT NULL, entity_id INTEGER NOT NULL, action TEXT NOT NULL, previous_state TEXT, new_state TEXT, changed_by TEXT NOT NULL, changed_at TEXT NOT NULL);
    ''')
    if cur.execute('SELECT COUNT(*) c FROM projects').fetchone()['c'] == 0:
        cur.execute("INSERT INTO projects(name,sensitivity,owner) VALUES('Demo project','low','admin')")
        cur.execute("INSERT INTO analyses(project_id,name,description,status) VALUES(1,'Baseline analysis','Initial example analysis','approved')")
    conn.commit(); conn.close()

def app_json(start, code, payload):
    data = json.dumps(payload).encode(); start(f'{code} OK', [('Content-Type','application/json'), ('Content-Length', str(len(data)))])
    return [data]

def bad(start, code, msg): return app_json(start, code, {'error': msg})

def parse_req(environ):
    try: length = int(environ.get('CONTENT_LENGTH') or 0)
    except ValueError: length = 0
    body = environ['wsgi.input'].read(length) if length else b''
    return json.loads(body.decode() or '{}') if body else {}

def actor(environ):
    return {'role': environ.get('HTTP_X_ROLE','guest').lower(), 'user': environ.get('HTTP_X_USER', environ.get('HTTP_X_ROLE','guest')), 'project': environ.get('HTTP_X_PROJECT','1')}

def app(environ, start_response):
    method = environ['REQUEST_METHOD']; path = environ['PATH_INFO']; a = actor(environ)
    db = connect_db(); init_db()
    def q(sql, args=()): return db.execute(sql, args).fetchall()
    def one(sql, args=()): return db.execute(sql, args).fetchone()
    def exec(sql, args=()): cur=db.execute(sql,args); db.commit(); return cur
    if path == '/' and method == 'GET': return app_json(start_response, 200, {'service':'SPRAT','status':'ok'})
    if path == '/projects' and method == 'GET': return app_json(start_response, 200, [dict(r) for r in q('SELECT * FROM projects')])
    if path == '/projects' and method == 'POST':
        if ROLE_LEVEL.get(a['role'],0) < 3: return bad(start_response,403,'forbidden')
        d=parse_req(environ); cur=exec('INSERT INTO projects(name,sensitivity,owner) VALUES(?,?,?)',(d['name'],d.get('sensitivity','low'),d.get('owner',a['user']))); return app_json(start_response,201,{'id':cur.lastrowid})
    if path == '/analyses' and method == 'POST':
        if ROLE_LEVEL.get(a['role'],0) < 1: return bad(start_response,403,'forbidden')
        d=parse_req(environ); cur=exec('INSERT INTO analyses(project_id,name,description,status) VALUES(?,?,?,?)',(d['project_id'],d['name'],d.get('description',''),d.get('status','draft'))); return app_json(start_response,201,{'id':cur.lastrowid})
    if path.startswith('/analyses/') and path.endswith('/items') and method == 'GET':
        aid=int(path.split('/')[2]); rows=[dict(r) | {'classifications': json.loads(r['classifications'])} for r in q('SELECT * FROM items WHERE analysis_id=? ORDER BY id',(aid,))]; return app_json(start_response,200,rows)
    if path.startswith('/analyses/') and path.endswith('/items') and method == 'POST':
        if ROLE_LEVEL.get(a['role'],0) < 1: return bad(start_response,403,'forbidden')
        aid=int(path.split('/')[2]); d=parse_req(environ)
        if d.get('source_policy_ref') and not d.get('rationale'): return bad(start_response,400,'trace links and rationale required for policy-derived requirements')
        cur=exec('''INSERT INTO items(analysis_id,kind,title,description,actor,trigger,outcome,classifications,source_policy_ref,source_policy_excerpt,rationale,sensitive_notes,legal_compliance,created_by,created_at,updated_by,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?,?)''',(aid,d['kind'],d['title'],d.get('description',''),d.get('actor'),d.get('trigger'),d.get('outcome'),json.dumps(d.get('classifications',[])),d.get('source_policy_ref'),d.get('source_policy_excerpt'),d.get('rationale'),d.get('sensitive_notes'),d.get('legal_compliance'),a['user'],now_iso(),a['user'],now_iso()))
        return app_json(start_response,201,{'id':cur.lastrowid})
    if path.startswith('/export/') and path.endswith('.json') and method == 'GET':
        aid=int(path.split('/')[2].split('.')[0]); analysis=one('SELECT * FROM analyses WHERE id=?',(aid,))
        if not analysis: return bad(start_response,404,'not found')
        project=one('SELECT * FROM projects WHERE id=?',(analysis['project_id'],))
        if project['sensitivity']=='sensitive' and a['role']=='guest': return bad(start_response,403,'forbidden')
        items=[dict(r) for r in q('SELECT * FROM items WHERE analysis_id=?',(aid,))]
        return app_json(start_response,200,{'analysis':dict(analysis),'items':items})
    if path.startswith('/compare/') and method == 'GET':
        _,_,x,y = path.split('/')
        ia=[dict(r) for r in q('SELECT * FROM items WHERE analysis_id=?',(int(x),))]; ib=[dict(r) for r in q('SELECT * FROM items WHERE analysis_id=?',(int(y),))]
        return app_json(start_response,200,{'analysis_a':int(x),'analysis_b':int(y),'items_a':ia,'items_b':ib})
    if path.startswith('/validate/') and method == 'GET':
        aid=int(path.split('/')[2]); items=q('SELECT * FROM items WHERE analysis_id=?',(aid,)); findings=[]
        for item in items:
            if item['kind']=='requirement' and item['source_policy_ref'] and not item['rationale']:
                findings.append({'item_id': item['id'], 'severity': 'warning', 'message': 'trace link missing rationale'})
        return app_json(start_response,200,{'analysis_id':aid,'findings':findings})
    return bad(start_response,404,'not found')

def create_app():
    return app
