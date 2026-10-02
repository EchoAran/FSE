import json
from flask import Blueprint, current_app, render_template, request, redirect, url_for, jsonify

bp = Blueprint('bp', __name__)

@bp.get('/')
def index():
    st = current_app.config['STORAGE']
    q = request.args.get('q','')
    project_id = request.args.get('project_id', type=int)
    term = request.args.get('term','')
    glossary = st.glossary_check(term) if term else []
    return render_template('index.html', data=st.data(), artifacts=st.artifacts(q, project_id), q=q, project_id=project_id, term=term, glossary=glossary)

@bp.post('/artifact/save')
def save_artifact():
    st = current_app.config['STORAGE']
    aid = st.save_artifact(request.form.to_dict())
    return redirect(url_for('bp.artifact_view', aid=aid))

@bp.get('/artifact/<int:aid>')
def artifact_view(aid):
    st = current_app.config['STORAGE']
    a = st.artifact(aid)
    return render_template('artifact.html', artifact=a)

@bp.post('/import')
def do_import():
    st = current_app.config['STORAGE']
    file = request.files.get('file')
    payload = json.loads(file.read().decode('utf-8')) if file else {'error':'no file'}
    iid = st.add_import(request.form.get('project_id',1), file.filename if file else 'unknown', payload)
    return redirect(url_for('bp.import_view', iid=iid))

@bp.get('/import/<int:iid>')
def import_view(iid):
    return render_template('import.html', iid=iid)

@bp.get('/api/search')
def api_search():
    st = current_app.config['STORAGE']
    return jsonify(st.data())
