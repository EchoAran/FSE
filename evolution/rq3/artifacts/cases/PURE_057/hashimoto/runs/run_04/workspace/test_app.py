import unittest
from app import app, DATA


class TestSPRAT(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        DATA['projects'].clear()

    def test_create_and_read_item(self):
        r = self.client.post('/projects/p1/items', headers={'X-User': 'analyst'}, json={'title': 'Req1', 'summary': 'short'})
        self.assertEqual(r.status_code, 201)
        item_id = r.get_json()['item']['id']
        r2 = self.client.get(f'/projects/p1/items/{item_id}', headers={'X-User': 'analyst'})
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.get_json()['metadata']['title'], 'Req1')

    def test_guest_cannot_create(self):
        r = self.client.post('/projects/p1/items', json={'title': 'nope'})
        self.assertEqual(r.status_code, 403)

    def test_review_finalizes_item(self):
        create = self.client.post('/projects/p1/items', headers={'X-User': 'analyst'}, json={'title': 'Req1', 'reviewers': ['pm']})
        item_id = create.get_json()['item']['id']
        rev = self.client.post(f'/projects/p1/items/{item_id}/review', headers={'X-User': 'pm'}, json={'approved': True})
        self.assertEqual(rev.status_code, 200)
        got = self.client.get(f'/projects/p1/items/{item_id}', headers={'X-User': 'pm'}).get_json()
        self.assertEqual(got['metadata']['status'], 'final')

    def test_compare_and_import(self):
        a = self.client.post('/projects/p1/items', headers={'X-User': 'analyst'}, json={'title': 'A', 'traceability': ['p1']}).get_json()['item']['id']
        b = self.client.post('/projects/p1/items', headers={'X-User': 'analyst'}, json={'title': 'B', 'traceability': ['p2']}).get_json()['item']['id']
        cmp = self.client.get(f'/projects/p1/compare?a={a}&b={b}')
        self.assertEqual(cmp.status_code, 200)
        self.assertEqual(cmp.get_json()['a']['title'], 'A')
        imp = self.client.post('/projects/p2/import', headers={'X-User': 'admin'}, json={'items': [{'title': 'Imported', 'traceability': ['policy']} ]})
        self.assertEqual(imp.status_code, 201)


if __name__ == '__main__':
    unittest.main()
