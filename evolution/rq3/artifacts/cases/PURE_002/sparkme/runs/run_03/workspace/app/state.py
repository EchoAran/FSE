from dataclasses import dataclass, field
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


@dataclass
class StoreState:
    store_info: dict = field(default_factory=lambda: {'name': '', 'currency': 'USD'})
    categories: list = field(default_factory=lambda: [])
    products: list = field(default_factory=lambda: [
        {'id': 1, 'name': 'Starter T-Shirt', 'sku': 'TSHIRT-001', 'price': 19.99, 'stock': 10, 'category': 'Apparel', 'available': True, 'description': 'A simple starter product.'},
        {'id': 2, 'name': 'Coffee Mug', 'sku': 'MUG-001', 'price': 12.5, 'stock': 25, 'category': 'Home', 'available': True, 'description': 'A plain mug for demos.'},
    ])
    customers: list = field(default_factory=lambda: [
        {'id': 1, 'name': 'Alex Customer', 'email': 'alex@example.com', 'address': '1 Main St', 'consent': True},
    ])
    orders: list = field(default_factory=lambda: [
        {'id': 1, 'customer': 'Alex Customer', 'total': 19.99, 'status': 'unpaid', 'payment': 'failed', 'shipping': 'pending', 'items': [{'name': 'Starter T-Shirt', 'qty': 1}], 'created_at': now()},
    ])
    cart: list = field(default_factory=list)
    logs: list = field(default_factory=lambda: [
        {'time': now(), 'actor': 'system', 'entity': 'order', 'action': 'created', 'reason': 'Seed data loaded'},
    ])
    notifications: list = field(default_factory=lambda: [
        {'priority': 'high', 'type': 'payment', 'message': 'Order #1 payment failed and is unpaid.'},
    ])
    import_result: dict = field(default_factory=dict)
    setup_steps: list = field(default_factory=lambda: [
        'Basic store information', 'Categories', 'Products', 'Customer account settings'
    ])


store = StoreState()
