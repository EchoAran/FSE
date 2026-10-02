import json, threading, time, urllib.request, urllib.error
import app
from http.server import ThreadingHTTPServer

server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
port = server.server_address[1]
th = threading.Thread(target=server.serve_forever, daemon=True)
th.start(); time.sleep(0.1)
base = f"http://127.0.0.1:{port}"

def req(path, method="GET", data=None, user="guest"):
    headers={"X-User":user}
    body=None
    if data is not None:
        body=json.dumps(data).encode(); headers["Content-Type"]="application/json"
    r=urllib.request.Request(base+path, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

assert req("/health")[0]==200
assert req("/projects", method="POST", data={"name":"P1"}, user="pm")[0]==201
pid=req("/projects")[1][0]["id"]
assert req(f"/projects/{pid}/artifacts", method="POST", data={"title":"policy"}, user="analyst")[0]==201
assert req("/glossary/policy")[1]["known"] is True
assert req("/projects", method="POST", data={"name":"P2"}, user="guest")[0]==403
server.shutdown()
print("ok")
