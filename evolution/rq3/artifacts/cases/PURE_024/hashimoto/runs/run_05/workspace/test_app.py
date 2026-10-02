import unittest
import json
import threading
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
import app


class NeniosAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.families.clear()
        app.children.clear()
        app.classrooms.clear()
        app.invoices.clear()
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), app.NeniosHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def request(self, method, path, data=None):
        url = f'http://127.0.0.1:{self.port}{path}'
        headers = {'Content-Type': 'application/json'}
        body = None if data is None else json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode('utf-8'))

    def test_full_flow(self):
        status, family = self.request('POST', '/families', {'name': 'Smith Family'})
        self.assertEqual(status, 201)
        status, classroom = self.request('POST', '/classrooms', {'name': 'Toddlers', 'capacity': 1})
        self.assertEqual(status, 201)
        status, child = self.request('POST', '/children', {'family_id': family['id'], 'name': 'Ava'})
        self.assertEqual(status, 201)
        status, enrolled = self.request('POST', '/enrollments', {'child_id': child['id'], 'classroom_id': classroom['id']})
        self.assertEqual(status, 200)
        status, immunization = self.request('POST', '/immunizations', {'child_id': child['id'], 'vaccine': 'MMR'})
        self.assertEqual(status, 201)
        status, invoice = self.request('POST', '/invoices', {'family_id': family['id'], 'amount': 120.5})
        self.assertEqual(status, 201)
        status, summary = self.request('GET', '/reports/summary')
        self.assertEqual(status, 200)

        self.assertEqual(enrolled['status'], 'enrolled')
        self.assertEqual(immunization['vaccine'], 'MMR')
        self.assertEqual(invoice['amount'], 120.5)
        self.assertEqual(summary['families'], 1)
        self.assertEqual(summary['children'], 1)
        self.assertEqual(summary['enrolled_children'], 1)
        self.assertEqual(summary['invoices'], 1)

    def test_waiting_list_when_classroom_full(self):
        status, family = self.request('POST', '/families', {'name': 'Jones Family'})
        status, classroom = self.request('POST', '/classrooms', {'name': 'Infants', 'capacity': 1})
        status, child1 = self.request('POST', '/children', {'family_id': family['id'], 'name': 'Ben'})
        status, child2 = self.request('POST', '/children', {'family_id': family['id'], 'name': 'Mia'})
        self.request('POST', '/enrollments', {'child_id': child1['id'], 'classroom_id': classroom['id']})
        status, payload = self.request('POST', '/enrollments', {'child_id': child2['id'], 'classroom_id': classroom['id']})
        self.assertEqual(status, 202)
        self.assertEqual(payload['child']['status'], 'waiting')


if __name__ == '__main__':
    unittest.main()
