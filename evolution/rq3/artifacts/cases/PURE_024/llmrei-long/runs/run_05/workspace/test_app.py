import unittest
from app import app

class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_dashboard(self):
        r = self.client.get('/dashboard')
        self.assertEqual(r.status_code, 200)
        self.assertIn('open_spots', r.get_json())

    def test_move_next_respects_capacity(self):
        r = self.client.post('/enrollment/move_next/room-prek')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['status'], 'enrolled')

    def test_billing_summary(self):
        r = self.client.get('/billing')
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertTrue(len(data['outstanding']) >= 1)

if __name__ == '__main__':
    unittest.main()
