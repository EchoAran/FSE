import os, threading, time, json, urllib.request

os.environ['SPRAT_DATA_FILE'] = '/workspace/test_data.json'
os.environ['SPRAT_ROLE'] = 'admin'
os.environ['SPRAT_USER'] = 'alice'
if os.path.exists('/workspace/test_data.json'):
    os.remove('/workspace/test_data.json')

from sprat import ThreadingHTTPServer, Handler


def start_server():
    srv = ThreadingHTTPServer(('127.0.0.1', 8765), Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start(); time.sleep(0.2)
    return srv


def req(method, path, data=None):
    url = f'http://127.0.0.1:8765{path}'
    body = None if data is None else json.dumps(data).encode()
    r = urllib.request.Request(url, data=body, method=method, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(r) as resp:
        return resp.status, json.loads(resp.read().decode())


def test_flow():
    srv = start_server()
    try:
        s, g = req('POST', '/items', {'title':'G1','item_type':'goal','classifications':['c1']}); assert s == 200
        s, r = req('POST', '/items', {'title':'R1','item_type':'requirement','classifications':['c1','c2']}); assert s == 200
        s, _ = req('POST', '/links', {'source_id':g['id'],'target_id':r['id'],'link_type':'supports'}); assert s == 200
        s, c = req('GET', f"/compare?a={g['id']}&b={r['id']}"); assert s == 200 and c['common'] == ['c1']
        s, e = req('GET', '/export?format=json'); assert s == 200 and len(e['items']) == 2
        s, _ = req('POST', f"/items/{r['id']}/approve", {}); assert s == 200
        s, a = req('GET', '/audit'); assert s == 200 and len(a['audit']) >= 3
    finally:
        srv.shutdown()
