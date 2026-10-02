import pytest
from app import app, PRODUCTS, ORDERS

@pytest.fixture(autouse=True)
def clear_state():
    PRODUCTS.clear()
    ORDERS.clear()
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess.clear()
    yield


def test_homepage_loads():
    c = app.test_client()
    r = c.get('/')
    assert r.status_code == 200
    assert b'GAMMA-J Web Store' in r.data


def test_add_and_checkout_flow():
    c = app.test_client()
    r = c.post('/cart/add/p1', data={'qty': 1}, follow_redirects=True)
    assert r.status_code == 200
    assert b'Starter Book' in r.data
    r = c.post('/checkout', follow_redirects=False)
    assert r.status_code == 302
    oid = r.location.rsplit('/', 1)[-1]
    r = c.post(f'/order/{oid}/pay', follow_redirects=True)
    assert b'confirmed' in r.data


def test_unavailable_product_blocked():
    c = app.test_client()
    PRODUCTS['x'] = {'id': 'x', 'name': 'X', 'description': 'x', 'price': None, 'quantity': 1, 'active': True, 'available': True, 'category': 'Books', 'images': []}
    r = c.post('/cart/add/x', follow_redirects=True)
    assert b'unavailable' in r.data.lower() or r.status_code == 400
