import unittest
from app import app, orders

class WebStoreTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_product_page_loads(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Products', resp.data)

    def test_checkout_requires_fields(self):
        resp = self.client.post('/checkout', data={})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'required', resp.data)

    def test_order_flow(self):
        with self.client as c:
            c.post('/cart/add/1')
            resp = c.post('/checkout', data={'name':'Test User','email':'test@example.com','address':'123 Lane'})
            self.assertEqual(resp.status_code, 302)
            self.assertTrue(len(orders) >= 1)

if __name__ == '__main__':
    unittest.main()
