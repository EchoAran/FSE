import unittest
from urllib import request as urlrequest
import json, threading, time
from http.server import ThreadingHTTPServer
from app import Handler

class SpratTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start(); time.sleep(0.1)
    @classmethod
    def tearDownClass(cls): cls.server.shutdown()
    def post(self, path, obj, user='analyst'):
        data=json.dumps(obj).encode(); req=urlrequest.Request(f'http://127.0.0.1:{self.port}{path}', data=data, headers={'Content-Type':'application/json','X-User':user}, method='POST'); return urlrequest.urlopen(req)
    def get(self, path, user='guest'):
        req=urlrequest.Request(f'http://127.0.0.1:{self.port}{path}', headers={'X-User':user}); return urlrequest.urlopen(req)
    def test_create_and_validate_requirement(self):
        r=self.post('/api/items', {'type':'requirement','title':'Encrypt data','project':'default','source_policy_reference':'POL-1','trace_links':['x']})
        self.assertEqual(r.status, 201)
        v=self.get('/api/validate'); self.assertEqual(v.status, 200)
    def test_guest_cannot_export(self):
        with self.assertRaises(Exception): self.post('/api/export', {'format':'json','project':'default'}, user='guest')
    def test_compare(self):
        self.post('/api/items', {'type':'goal','title':'A','project':'default'}, user='analyst')
        self.post('/api/items', {'type':'goal','title':'A','project':'sensitive'}, user='admin')
        r=self.get('/api/compare?a=default&b=sensitive'); self.assertEqual(r.status, 200)
        self.assertIn('A', json.load(r)['shared_titles'])

if __name__ == '__main__': unittest.main()
