import unittest
from app import app, DB

class TestNenios(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess.clear()
        DB['families'].clear(); DB['children'].clear(); DB['invoices'].clear(); DB['audit'].clear(); DB['imports'].clear()

    def login(self, username, password):
        return self.client.post('/login', json={'username': username, 'password': password})

    def test_login_and_role_access(self):
        r = self.login('admin', 'admin')
        self.assertEqual(r.status_code, 200)
        r = self.client.get('/me')
        self.assertEqual(r.json['roles'], ['administrator'])

    def test_create_family_child_invoice_and_payment(self):
        self.login('admin', 'admin')
        fam = self.client.post('/families', json={'name': 'Smith'})
        self.assertEqual(fam.status_code, 201)
        child = self.client.post('/children', json={'family_id': fam.json['id'], 'name': 'Ava'})
        self.assertEqual(child.status_code, 201)
        inv = self.client.post('/invoices', json={'family_id': fam.json['id'], 'amount': 100, 'draft': True})
        self.assertEqual(inv.json['status'], 'unpaid')
        pay = self.client.post(f"/invoices/{inv.json['id']}/pay", json={'amount': 100})
        self.assertEqual(pay.json['status'], 'paid')

    def test_archive_and_import(self):
        self.login('admin', 'admin')
        fam = self.client.post('/families', json={'name': 'Doe'})
        child = self.client.post('/children', json={'family_id': fam.json['id'], 'name': 'Ben'})
        arch = self.client.post(f"/children/{child.json['id']}/archive")
        self.assertTrue(arch.json['archived'])
        report = self.client.post('/import', json={'families': [{'name': 'Imported'}], 'children': [{'name': 'X', 'family_id': fam.json['id']} ]})
        self.assertEqual(report.status_code, 201)
        self.assertGreaterEqual(report.json['created']['families'], 1)

if __name__ == '__main__':
    unittest.main()
