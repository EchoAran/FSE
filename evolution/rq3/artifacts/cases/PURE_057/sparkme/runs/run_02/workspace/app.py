from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json, uuid, os
from datetime import datetime
from copy import deepcopy

state = {
    "users": {"admin": {"role": "administrator"}, "pm": {"role": "project_manager"}, "analyst": {"role": "analyst"}, "guest": {"role": "guest"}},
    "projects": {},
    "glossary": {"policy": {"definition": "An approved rule or source policy.", "examples": ["Privacy Policy"]}, "goal": {"definition": "A desired outcome.", "examples": ["Reduce risk"]}, "requirement": {"definition": "A system requirement.", "examples": ["Must log changes"]}},
    "notifications": [],
}

def now(): return datetime.utcnow().isoformat() + "Z"
def get_user(headers): return headers.get("X-User", "guest"), state["users"].get(headers.get("X-User", "guest"), state["users"]["guest"])
def add_notification(msg): state["notifications"].append({"id": str(uuid.uuid4()), "message": msg, "timestamp": now()})

def json_response(handler, code, data):
    body = json.dumps(data).encode()
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers(); handler.wfile.write(body)

def read_json(handler):
    n = int(handler.headers.get("Content-Length", 0))
    return json.loads(handler.rfile.read(n) or b"{}")

def get_project(pid):
    p = state["projects"].get(pid)
    return p

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/health": return json_response(self, 200, {"status": "ok"})
        if p == "/notifications": return json_response(self, 200, state["notifications"])
        if p.startswith("/glossary/"):
            term = p.split("/", 2)[2].lower(); e = state["glossary"].get(term)
            return json_response(self, 200, {"term": term, "known": bool(e), **(e or {"suggestions": list(state['glossary'].keys())})})
        if p == "/projects": return json_response(self, 200, list(state["projects"].values()))
        if p.endswith("/artifacts"):
            pid = p.split("/")[2]; pr = get_project(pid)
            return json_response(self, 200, list(pr["artifacts"].values())) if pr else json_response(self, 404, {"error":"not found"})
        if p.endswith("/conflicts"):
            pid = p.split("/")[2]; pr = get_project(pid)
            return json_response(self, 200, pr["conflicts"]) if pr else json_response(self, 404, {"error":"not found"})
        return json_response(self, 404, {"error": "not found"})
    def do_POST(self):
        p = urlparse(self.path).path; username, user = get_user(self.headers)
        data = read_json(self)
        def forbidden(): return json_response(self, 403, {"error":"forbidden"})
        if p == "/projects":
            if user["role"] not in {"administrator","project_manager"}: return forbidden()
            pid=str(uuid.uuid4()); state["projects"][pid]={"id":pid,"name":data.get("name","Untitled Project"),"artifacts":{},"links":{},"imports":[],"conflicts":[]}
            return json_response(self, 201, state["projects"][pid])
        if p.endswith("/artifacts"):
            if user["role"] not in {"administrator","project_manager","analyst"}: return forbidden()
            pid=p.split("/")[2]; pr=get_project(pid)
            if not pr: return json_response(self,404,{"error":"not found"})
            title=data.get("title","").strip(); warnings=[]
            if title.lower() in state["glossary"]: warnings.append("term matches existing glossary entry")
            if any(a["title"].lower()==title.lower() for a in pr["artifacts"].values() if title): warnings.append("likely duplicate artifact title")
            aid=str(uuid.uuid4()); art={"id":aid,"title":title or "Untitled","type":data.get("type","requirement"),"content":data.get("content","") ,"status":data.get("status","draft"),"version":1,"versions":[],"trace_links":data.get("trace_links",[]),"comments":[],"created_at":now(),"updated_at":now(),"warnings":warnings}
            pr["artifacts"][aid]=art; return json_response(self,201,art)
        if p.endswith("/imports"):
            if user["role"] not in {"administrator","project_manager","analyst"}: return forbidden()
            pid=p.split("/")[2]; pr=get_project(pid)
            if not pr: return json_response(self,404,{"error":"not found"})
            staging=[]; unresolved=[]
            for item in data.get("items",[]):
                mapped=deepcopy(item); mapped.setdefault("source_value", item.get("title",""))
                if not item.get("title"): mapped["review_required"]=True; unresolved.append(mapped)
                staging.append(mapped)
            pr["imports"].append({"id":str(uuid.uuid4()),"staging":staging,"unresolved":unresolved,"status":"staged"})
            return json_response(self,201,{"staged":len(staging),"unresolved":len(unresolved)})
        if p.endswith("/simulate-conflict"):
            if user["role"] not in {"administrator","project_manager","analyst"}: return forbidden()
            pid=p.split("/")[2]; pr=get_project(pid)
            if not pr: return json_response(self,404,{"error":"not found"})
            c={"id":str(uuid.uuid4()),"message":"Overlapping edits detected","status":"needs review","created_at":now()}; pr["conflicts"].append(c); add_notification(f"Conflict in project {pr['name']}"); return json_response(self,201,c)
        return json_response(self,404,{"error":"not found"})
    def do_PUT(self):
        p=urlparse(self.path).path; _, user = get_user(self.headers); data=read_json(self)
        if not p.startswith("/projects/") or "/artifacts/" not in p: return json_response(self,404,{"error":"not found"})
        if user["role"] not in {"administrator","project_manager","analyst"}: return json_response(self,403,{"error":"forbidden"})
        _,_,pid,_,aid = p.split("/")[:5]
        pr=get_project(pid)
        if not pr or aid not in pr["artifacts"]: return json_response(self,404,{"error":"not found"})
        art=pr["artifacts"][aid]
        if art["status"]=="approved" and user["role"]!="administrator": return json_response(self,409,{"error":"approved artifacts require new version or admin reopen"})
        art["versions"].append(deepcopy({k: art[k] for k in ["title","content","status","trace_links"]})); art["version"]+=1
        for k in ["title","content","status","trace_links"]:
            if k in data: art[k]=data[k]
        art["updated_at"]=now(); return json_response(self,200,art)

def run(host="0.0.0.0", port=8000): ThreadingHTTPServer((host, port), Handler).serve_forever()

if __name__ == "__main__": run(port=int(os.getenv("PORT","8000")))
