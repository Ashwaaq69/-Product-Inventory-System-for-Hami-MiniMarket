## File: order.py
from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime

@dataclass
class OrderItem:
    """
    Represents a single item in an order.
    """
    product_id: str
    name: str
    price: float
    qty: int

class Order:
    """
    Handles customer orders:
    - Add/remove items
    - Calculate total
    - Confirm orders (update inventory)
    """
    def __init__(self, inventory):
        """
        Initialize an order with an inventory reference.
        """
        self.inventory = inventory       # Reference to Inventory object
        self.items: List[OrderItem] = []  # List of OrderItem objects
        self.created_at = datetime.now()  # Timestamp when order created
        self.customer_name = ''          # Customer name (optional)

    def add_item(self, product_id: str, qty: int) -> Tuple[bool, str]:
        """
        Add an item to the order.
        
        Args:
            product_id: ID of the product to add
            qty: quantity to add
        
        Returns:
            Tuple of (success flag, message)
        """
        # Check if product exists in inventory
        p = self.inventory.get_by_id(product_id)
        if not p:
            return False, 'Product not found'
        if qty <= 0:
            return False, 'Quantity must be at least 1'
        if p.stock < qty:
            return False, f'Not enough stock (available: {p.stock})'

        # Merge with existing item if already in cart
        for it in self.items:
            if it.product_id == product_id:
                it.qty += qty
                return True, 'Added to cart'

        # Otherwise, add new item to cart
        self.items.append(OrderItem(product_id=product_id, name=p.name, price=p.price, qty=qty))
        return True, 'Added to cart'

    def remove_item(self, product_id: str):
        """
        Remove an item from the order by product ID.
        """
        self.items = [it for it in self.items if it.product_id != product_id]

    def total(self) -> float:
        """
        Calculate total price of the current order.
        """
        return sum(it.price * it.qty for it in self.items)

    def confirm(self, customer_name: str = '') -> dict:
        """
        Confirm the order:
        - Deduct quantities from inventory
        - Return order data
        - Clear current items (cart)
        
        Args:
            customer_name: optional customer name
        
        Returns:
            Dictionary containing order details: timestamp, customer, items, total
        """
        # Update inventory stock
        for it in self.items:
            self.inventory.update_stock(it.product_id, -it.qty)

        self.customer_name = customer_name

        # Prepare order data for saving/reporting
        data = {
            'timestamp': self.created_at.isoformat(),
            'customer': self.customer_name,
            'items': [{'product_id': it.product_id, 'name': it.name, 'price': it.price, 'qty': it.qty} for it in self.items],
            'total': self.total()
        }

        # Clear the cart after confirmation
        self.items = []

        return data
