## File: `order.py`
from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime

@dataclass
class OrderItem:
    product_id: str
    name: str
    price: float
    qty: int

class Order:
    def __init__(self, inventory):
        self.inventory = inventory
        self.items: List[OrderItem] = []
        self.created_at = datetime.now()
        self.customer_name = ''

    def add_item(self, product_id: str, qty: int) -> Tuple[bool, str]:
        p = self.inventory.get_by_id(product_id)
        if not p:
            return False, 'Product not found'
        if qty <= 0:
            return False, 'Quantity must be at least 1'
        if p.stock < qty:
            return False, f'Not enough stock (available: {p.stock})'
        # merge if existing
        for it in self.items:
            if it.product_id == product_id:
                it.qty += qty
                return True, 'Added to cart'
        self.items.append(OrderItem(product_id=product_id, name=p.name, price=p.price, qty=qty))
        return True, 'Added to cart'

    def remove_item(self, product_id: str):
        self.items = [it for it in self.items if it.product_id != product_id]
    def total(self) -> float:
        return sum(it.price * it.qty for it in self.items)

    def confirm(self, customer_name: str = '') -> dict:
        # update inventory
        for it in self.items:
            self.inventory.update_stock(it.product_id, -it.qty)
        self.customer_name = customer_name
        data = {
            'timestamp': self.created_at.isoformat(),
            'customer': self.customer_name,
            'items': [{'product_id': it.product_id, 'name': it.name, 'price': it.price, 'qty': it.qty} for it in self.items],
            'total': self.total()
        }
        # clear cart
        self.items = []
        return data

