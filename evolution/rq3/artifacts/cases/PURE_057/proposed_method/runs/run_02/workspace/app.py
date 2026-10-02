from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
import json
import copy

USERS = {
    "admin": {"role": "administrator", "projects": ["*"], "clearance": "high"},
    "pm": {"role": "project_manager", "projects": ["*"], "clearance": "medium"},
    "analyst": {"role": "analyst", "projects": ["alpha"], "clearance": "medium"},
    "guest": {"role": "guest", "projects": ["alpha"], "clearance": "low"},
}
STATE = {"projects": {"alpha": {"sensitivity": "normal", "items": {}, "analyses": {}, "audit": []}}}
COUNTERS = {"item": 0, "analysis": 0, "trace": 0}

def now(): return datetime.now(timezone.utc).isoformat()
def next_id(prefix): COUNTERS[prefix] += 1; return f"{prefix}-{COUNTERS[prefix]}"
def can_access(user, pid): return "*" in user["projects"] or pid in user["projects"]
def log(proj, action, data): proj["audit"].append({"time": now(), "action": action, **data})

class H(BaseHTTPRequestHandler):
    def _user(self): return USERS.get(self.headers.get("X-User", "guest"), USERS["guest"])
    def _send(self, code, obj, ctype="application/json"):
        self.send_response(code); self.send_header("Content-Type", ctype); self.end_headers()
        if isinstance(obj, (dict, list)): self.wfile.write(json.dumps(obj).encode())
        else: self.wfile.write(obj.encode())
    def do_GET(self):
        p = urlparse(self.path)
        qs = parse_qs(p.query)
        if p.path == "/health": return self._send(200, {"status": "ok"})
        if p.path.startswith("/items/"):
            pid = qs.get("project", [None])[0]
            if pid not in STATE["projects"]: return self._send(404, {"error": "unknown project"})
            item = STATE["projects"][pid]["items"].get(p.path.split("/")[-1])
            if not item: return self._send(404, {"error": "not found"})
            out = copy.deepcopy(item)
            if self._user()["role"] == "guest": out.pop("sensitive_notes", None)
            return self._send(200, out)
        if p.path == "/compare":
            pid, a, b = qs.get("project", [None])[0], qs.get("a", [None])[0], qs.get("b", [None])[0]
            proj = STATE["projects"].get(pid)
            if not proj or a not in proj["analyses"] or b not in proj["analyses"]: return self._send(404, {"error": "not found"})
            ia = {i["id"] for i in proj["analyses"][a]["items"]}; ib = {i["id"] for i in proj["analyses"][b]["items"]}
            return self._send(200, {"matches": sorted(ia & ib), "only_in_a": sorted(ia - ib), "only_in_b": sorted(ib - ia), "notes": "inline explanations available"})
        if p.path == "/export":
            pid, fmt = qs.get("project", [None])[0], qs.get("format", ["json"])[0]
            proj = STATE["projects"].get(pid)
            if not proj: return self._send(404, {"error": "not found"})
            if self._user()["role"] == "guest": return self._send(403, {"error": "forbidden"})
            data = {"project": pid, "items": list(proj["items"].values()), "audit": proj["audit"]}
            if fmt == "csv":
                lines = ["id,title,type"] + [f"{i['id']},{i['title']},{i['type']}" for i in proj["items"].values()]
                return self._send(200, "\n".join(lines), "text/csv")
            return self._send(200, data)
        return self._send(404, {"error": "not found"})
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0")); payload = json.loads(self.rfile.read(length) or b"{}")
        user = self._user(); path = self.path
        if path == "/items":
            pid = payload.get("project"); proj = STATE["projects"].get(pid)
            if not proj: return self._send(400, {"error": "project required"})
            if not can_access(user, pid): return self._send(403, {"error": "forbidden"})
            item = {"id": next_id("item"), "title": payload.get("title", ""), "description": payload.get("description", ""), "type": payload.get("type", "requirement"), "classifications": payload.get("classifications", []), "derived_from": payload.get("derived_from"), "sensitive_notes": payload.get("sensitive_notes", ""), "traces": [], "history": [], "version": 1, "active": True}
            proj["items"][item["id"]] = item; log(proj, "create_item", {"user": payload.get("user", "unknown"), "item": item["id"]})
            return self._send(201, item)
        if path == "/traces":
            pid = payload.get("project"); proj = STATE["projects"].get(pid)
            if not proj: return self._send(400, {"error": "project required"})
            if not can_access(user, pid): return self._send(403, {"error": "forbidden"})
            src, dst = proj["items"].get(payload.get("source_id")), proj["items"].get(payload.get("target_id"))
            if not src or not dst: return self._send(404, {"error": "items required"})
            if payload.get("policy_claim") and not payload.get("policy_reference"): return self._send(400, {"error": "trace links required for policy claims"})
            trace = {"id": next_id("trace"), "source_id": src["id"], "target_id": dst["id"], "policy_reference": payload.get("policy_reference"), "policy_excerpt": payload.get("policy_excerpt"), "rationale": payload.get("rationale", ""), "created_by": self.headers.get("X-User", "guest"), "created_at": now(), "primary": bool(payload.get("primary"))}
            dst["traces"].append(trace); log(proj, "create_trace", {"user": trace["created_by"], "trace": trace["id"]})
            return self._send(201, trace)
        if path == "/analyses":
            pid = payload.get("project"); proj = STATE["projects"].get(pid)
            if not proj: return self._send(400, {"error": "project required"})
            if not can_access(user, pid): return self._send(403, {"error": "forbidden"})
            an = {"id": next_id("analysis"), "name": payload.get("name", ""), "items": payload.get("items", [])}
            proj["analyses"][an["id"]] = an; log(proj, "create_analysis", {"user": self.headers.get("X-User", "guest"), "analysis": an["id"]})
            return self._send(201, an)
        return self._send(404, {"error": "not found"})

def main():
    ThreadingHTTPServer(("0.0.0.0", 8000), H).serve_forever()

if __name__ == "__main__":
    main()
