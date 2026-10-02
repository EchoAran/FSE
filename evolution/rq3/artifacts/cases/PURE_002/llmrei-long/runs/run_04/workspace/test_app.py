import unittest
from app import app, PRODUCTS

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_browse(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Starter Mug', r.data)

    def test_checkout_requires_fields(self):
        with self.client.session_transaction() as s:
            s['cart'] = {'p1': 1}
        r = self.client.post('/checkout', data={'name': '', 'email': '', 'address': ''}, follow_redirects=True)
        self.assertIn(b'required', r.data)

    def test_staff_product_save(self):
        r = self.client.post('/staff/products', data={
            'name': 'New Item', 'description': 'Desc', 'price': '1.0', 'category': 'Other', 'availability': 'In stock', 'image': ''
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(any(p['name'] == 'New Item' for p in PRODUCTS))

if __name__ == '__main__':
    unittest.main()
