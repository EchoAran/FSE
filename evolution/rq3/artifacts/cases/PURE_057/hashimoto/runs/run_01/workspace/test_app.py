import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import app


def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_port}"


def request(method, url, data=None, headers=None):
    headers = headers or {}
    body = None if data is None else json.dumps(data).encode()
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode())


def test_create_and_review():
    server, base = start_server()
    try:
        status, created = request("POST", base + "/items", {"title": "T1"}, {"X-Role": "analyst", "X-User": "alice"})
        assert status == 201
        item_id = created["item_id"]
        status, item = request("GET", base + f"/items/{item_id}", headers={"X-Role": "analyst", "X-User": "alice"})
        assert status == 200 and item["status"] == "draft"
        status, reviewed = request("POST", base + f"/items/{item_id}/review", {"status": "final"}, {"X-Role": "project_manager", "X-User": "pm"})
        assert status == 200 and reviewed["status"] == "final"
    finally:
        server.shutdown()


def test_guest_cannot_create():
    server, base = start_server()
    try:
        try:
            request("POST", base + "/items", {"title": "T1"})
            assert False, "expected failure"
        except Exception:
            pass
    finally:
        server.shutdown()
