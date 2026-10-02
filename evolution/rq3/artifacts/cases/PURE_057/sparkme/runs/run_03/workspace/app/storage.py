import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone


class Storage:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def conn(self):
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        return c

    def _init_db(self):
        with self.conn() as c:
            c.executescript('''
            create table if not exists projects(id integer primary key, name text not null, description text default '', created_at text not null);
            create table if not exists glossary(id integer primary key, term text unique not null, definition text not null, examples text default '');
            create table if not exists artifacts(id integer primary key, project_id integer, type text not null, title text not null, content text default '', rationale text default '', source_notes text default '', assumptions text default '', status text default 'draft', lifecycle text default 'draft', version integer default 1, archived integer default 0, parent_id integer, created_at text not null, updated_at text not null, owner text default 'analyst', last_changed_by text default 'analyst', last_changed_at text not null);
            create table if not exists traces(id integer primary key, artifact_id integer, source_policy text, target_goal text, broken integer default 0, note text default '');
            create table if not exists comments(id integer primary key, artifact_id integer, body text not null, author text default 'analyst', created_at text not null);
            create table if not exists imports(id integer primary key, project_id integer, filename text, original_json text not null, stage_json text not null, status text default 'staging', created_at text not null);
            create table if not exists conflicts(id integer primary key, artifact_id integer, left_version integer, right_version integer, status text default 'open', detail text default '', created_at text not null, resolved_at text default '', resolution text default '', decision_by text default '');
            create table if not exists activities(id integer primary key, message text not null, created_at text not null);
            ''')
            c.commit()
            if not self.projects():
                self.seed()

    def now(self):
        return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

    def seed(self):
        with self.conn() as c:
            c.execute('insert into projects(name, description, created_at) values (?,?,?)', ('Demo Project', 'Seed project for SPRAT', self.now()))
            c.executemany('insert into glossary(term, definition, examples) values (?,?,?)', [
                ('requirement', 'A statement of needed capability.', 'Authentication requirement'),
                ('policy', 'An organizational rule or source constraint.', 'Data retention policy'),
                ('traceability', 'The ability to follow a relationship across artifacts.', 'Policy to requirement link')
            ])
            c.execute('insert into artifacts(project_id, type, title, content, rationale, source_notes, assumptions, status, lifecycle, version, created_at, updated_at, last_changed_by, last_changed_at) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (1, 'goal', 'Protect sensitive analysis work', 'Centralize secure collaborative analysis.', 'Aligns with security policy', 'Interview notes', 'Managed environment', 'approved', 'approved', 1, self.now(), self.now(), 'system', self.now()))
            c.execute('insert into traces(artifact_id, source_policy, target_goal, broken, note) values (?,?,?,?,?)', (1, 'Security policy S-1', 'Protect sensitive analysis work', 0, 'Initial trace'))
            c.execute('insert into activities(message, created_at) values (?,?)', ('System seeded with demo data', self.now()))
            c.commit()

    def projects(self):
        with self.conn() as c:
            return c.execute('select * from projects order by id').fetchall()

    def project(self, project_id):
        with self.conn() as c:
            return c.execute('select * from projects where id=?', (project_id,)).fetchone()

    def artifacts(self, q='', project_id=None):
        sql = 'select * from artifacts where 1=1'
        params = []
        if project_id:
            sql += ' and project_id=?'; params.append(project_id)
        if q:
            sql += " and (title like ? or content like ? or rationale like ? or source_notes like ? or assumptions like ?)"
            params.extend(['%'+q+'%']*5)
        sql += ' order by updated_at desc'
        with self.conn() as c:
            return c.execute(sql, params).fetchall()

    def artifact(self, aid):
        with self.conn() as c:
            return c.execute('select * from artifacts where id=?', (aid,)).fetchone()

    def save_artifact(self, data):
        with self.conn() as c:
            now = self.now()
            if data.get('id'):
                cur = c.execute('select * from artifacts where id=?', (data['id'],)).fetchone()
                if cur and cur['archived'] and not data.get('allow_reopen'):
                    raise ValueError('Archived items require reopen permission or new version')
                if cur and data.get('version') and int(data['version']) != int(cur['version']):
                    c.execute('insert into conflicts(artifact_id,left_version,right_version,detail,created_at) values (?,?,?,?,?)', (cur['id'], cur['version'], data['version'], 'Overlapping edit detected', now))
                c.execute('update artifacts set title=?, content=?, rationale=?, source_notes=?, assumptions=?, status=?, lifecycle=?, archived=?, updated_at=?, last_changed_by=?, last_changed_at=? where id=?',
                          (data['title'], data.get('content',''), data.get('rationale',''), data.get('source_notes',''), data.get('assumptions',''), data.get('status','draft'), data.get('lifecycle','draft'), int(data.get('archived',0)), now, data.get('user','analyst'), now, data['id']))
                aid = data['id']
            else:
                c.execute('insert into artifacts(project_id, type, title, content, rationale, source_notes, assumptions, status, lifecycle, version, archived, parent_id, created_at, updated_at, owner, last_changed_by, last_changed_at) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                          (data.get('project_id',1), data.get('type','requirement'), data['title'], data.get('content',''), data.get('rationale',''), data.get('source_notes',''), data.get('assumptions',''), data.get('status','draft'), data.get('lifecycle','draft'), 1, int(data.get('archived',0)), data.get('parent_id'), now, now, data.get('user','analyst'), data.get('user','analyst'), now))
                aid = c.execute('select last_insert_rowid()').fetchone()[0]
            c.execute('insert into activities(message, created_at) values (?,?)', (f"Artifact {aid} saved by {data.get('user','analyst')}", now))
            c.commit()
            return aid

    def glossary_check(self, term):
        term_l = term.lower().strip()
        with self.conn() as c:
            rows = c.execute('select * from glossary').fetchall()
        matches = []
        for r in rows:
            if term_l == r['term'].lower():
                matches.append(('duplicate', dict(r)))
            elif term_l in r['term'].lower() or r['term'].lower() in term_l:
                matches.append(('near', dict(r)))
        return matches

    def add_import(self, project_id, filename, payload):
        now = self.now()
        with self.conn() as c:
            c.execute('insert into imports(project_id, filename, original_json, stage_json, status, created_at) values (?,?,?,?,?,?)', (project_id, filename, json.dumps(payload), json.dumps(payload), 'staging', now))
            iid = c.execute('select last_insert_rowid()').fetchone()[0]
            c.execute('insert into activities(message, created_at) values (?,?)', (f'Import staged: {filename}', now))
            c.commit()
            return iid

    def data(self):
        with self.conn() as c:
            return {
                'projects': [dict(r) for r in c.execute('select * from projects').fetchall()],
                'artifacts': [dict(r) for r in c.execute('select * from artifacts order by updated_at desc').fetchall()],
                'glossary': [dict(r) for r in c.execute('select * from glossary order by term').fetchall()],
                'imports': [dict(r) for r in c.execute('select * from imports order by created_at desc').fetchall()],
                'conflicts': [dict(r) for r in c.execute('select * from conflicts order by created_at desc').fetchall()],
                'activities': [dict(r) for r in c.execute('select * from activities order by created_at desc').fetchall()],
            }
