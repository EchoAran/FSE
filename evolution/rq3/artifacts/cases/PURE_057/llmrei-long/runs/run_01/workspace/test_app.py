import unittest
from app import app, store

class SpratTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        store.clear()

    def headers(self, role="admin", user="tester"):
        return {"X-Role": role, "X-User": user}

    def test_create_and_trace_requirement(self):
        pol = self.client.post("/artifacts", json={"type": "policy", "title": "Policy A"}, headers=self.headers()).get_json()
        req = self.client.post("/artifacts", json={"type": "requirement", "title": "Req A", "sources": [pol["id"]], "primary_source": pol["id"]}, headers=self.headers()).get_json()
        trace = self.client.get(f"/artifacts/{req['id']}/trace", headers=self.headers(role="guest")).get_json()
        self.assertEqual(trace["sources"][0]["id"], pol["id"])
        self.assertEqual(trace["requirements"], [])

    def test_rbac_blocks_guest_write(self):
        resp = self.client.post("/artifacts", json={"type": "goal", "title": "G"}, headers=self.headers(role="guest"))
        self.assertEqual(resp.status_code, 403)

    def test_compare_and_history(self):
        a = self.client.post("/artifacts", json={"type": "goal", "title": "A"}, headers=self.headers()).get_json()
        b = self.client.post("/artifacts", json={"type": "goal", "title": "B"}, headers=self.headers()).get_json()
        cmp_resp = self.client.get(f"/compare?left={a['id']}&right={b['id']}", headers=self.headers(role="guest"))
        self.assertEqual(cmp_resp.status_code, 200)
        hist = self.client.get(f"/artifacts/{a['id']}/history", headers=self.headers(role="analyst")).get_json()
        self.assertGreaterEqual(len(hist), 1)

if __name__ == "__main__":
    unittest.main()
