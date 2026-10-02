import unittest
from app import app, store


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        store.families.clear()
        store.children.clear()
        store.waiting_list.clear()
        store.invoices.clear()
        store.classrooms.clear()
        store.family_ids = iter(range(1, 1000000))
        store.child_ids = iter(range(1, 1000000))
        store.waiting_ids = iter(range(1, 1000000))
        store.invoice_ids = iter(range(1, 1000000))
        store.classroom_ids = iter(range(1, 1000000))
        self.client.post('/api/classrooms', json={'name': 'Infants', 'capacity': 5})

    def test_family_child_enrollment_invoice_and_report(self):
        fam = self.client.post('/api/families', json={
            'name': 'Smith', 'contact_name': 'Alice', 'contact_email': 'a@example.com', 'contact_phone': '555-1'
        })
        self.assertEqual(fam.status_code, 201)
        family_id = fam.get_json()['id']

        child = self.client.post('/api/children', json={
            'family_id': family_id, 'name': 'Ben', 'date_of_birth': '2020-01-01', 'classroom_id': 1
        })
        self.assertEqual(child.status_code, 201)
        child_id = child.get_json()['id']

        imm = self.client.post('/api/immunizations', json={
            'child_id': child_id, 'name': 'MMR'
        })
        self.assertEqual(imm.status_code, 200)
        self.assertEqual(len(imm.get_json()['immunizations']), 1)

        invoice = self.client.post('/api/invoices', json={
            'family_id': family_id, 'child_id': child_id, 'amount': 120.50
        })
        self.assertEqual(invoice.status_code, 201)

        report = self.client.get('/api/reports/operations')
        self.assertEqual(report.status_code, 200)
        self.assertGreaterEqual(report.get_json()['families'], 1)

    def test_waiting_list_and_invalid_classroom(self):
        fam = self.client.post('/api/families', json={'name': 'Lee'})
        family_id = fam.get_json()['id']
        waiting = self.client.post('/api/waiting-list', json={
            'family_id': family_id, 'child_name': 'Zoe', 'preferred_classroom_id': 999
        })
        self.assertEqual(waiting.status_code, 404)

    def test_classroom_capacity_is_enforced(self):
        fam = self.client.post('/api/families', json={'name': 'Cap Fam'})
        family_id = fam.get_json()['id']
        self.client.post('/api/children', json={'family_id': family_id, 'name': 'A', 'date_of_birth': '2020-01-01', 'classroom_id': 1})
        self.client.post('/api/children', json={'family_id': family_id, 'name': 'B', 'date_of_birth': '2020-01-02', 'classroom_id': 1})
        self.client.post('/api/children', json={'family_id': family_id, 'name': 'C', 'date_of_birth': '2020-01-03', 'classroom_id': 1})
        self.client.post('/api/children', json={'family_id': family_id, 'name': 'D', 'date_of_birth': '2020-01-04', 'classroom_id': 1})
        self.client.post('/api/children', json={'family_id': family_id, 'name': 'E', 'date_of_birth': '2020-01-05', 'classroom_id': 1})
        resp = self.client.post('/api/children', json={'family_id': family_id, 'name': 'F', 'date_of_birth': '2020-01-06', 'classroom_id': 1})
        self.assertEqual(resp.status_code, 409)


if __name__ == '__main__':
    unittest.main()
