import unittest
import app

class StoreTests(unittest.TestCase):
    def setUp(self):
        app.reset_state()

    def test_setup_like_flow_and_low_stock(self):
        p = app.create_product('Widget', 10, 2)
        self.assertEqual(app.low_stock_warnings()[0]['id'], p.id)

    def test_checkout_and_stock_update(self):
        p = app.create_product('Widget', 10, 2)
        c = app.create_customer('A', {'name':'A','street':'s','city':'c','postal_code':'p','country':'US','email':'a@example.com'})
        o = app.checkout(c.id, [{'product_id': p.id, 'qty': 1}])
        self.assertEqual(o.status, 'new')
        self.assertEqual(app.STATE['products'][p.id].stock, 1)

    def test_insufficient_stock(self):
        p = app.create_product('Widget', 10, 1)
        c = app.create_customer('A', {'name':'A','street':'s','city':'c','postal_code':'p','country':'US','email':'a@example.com'})
        with self.assertRaises(ValueError):
            app.checkout(c.id, [{'product_id': p.id, 'qty': 2}])

    def test_shipped_cannot_cancel(self):
        p = app.create_product('Widget', 10, 2)
        c = app.create_customer('A', {'name':'A','street':'s','city':'c','postal_code':'p','country':'US','email':'a@example.com'})
        o = app.checkout(c.id, [{'product_id': p.id, 'qty': 1}])
        app.set_status(o.id, 'shipped')
        with self.assertRaises(PermissionError):
            app.set_status(o.id, 'cancelled')

if __name__ == '__main__':
    unittest.main()
