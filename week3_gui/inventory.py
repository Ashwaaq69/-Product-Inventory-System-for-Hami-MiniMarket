# inventory.py
from dataclasses import dataclass
import csv
from typing import List, Optional
import os
import sys

@dataclass
class Product:
    product_id: str
    name: str
    price: float
    stock: int

class Inventory:
    def __init__(self, path='inventory.csv'):
        self.path = path
        self.products: List[Product] = []
        self.load()

    def _create_sample_inventory(self):
        sample = [
            {'product_id':'1','name':'Espresso','price':'2.50','stock':'10'},
            {'product_id':'2','name':'Cappuccino','price':'3.00','stock':'8'},
            {'product_id':'3','name':'Latte','price':'3.50','stock':'4'},
            {'product_id':'4','name':'Mocha','price':'3.75','stock':'2'},
            {'product_id':'5','name':'Americano','price':'2.00','stock':'12'},
            
        ]
        try:
            with open(self.path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['product_id','name','price','stock'])
                writer.writeheader()
                for r in sample:
                    writer.writerow(r)
            print(f'[inventory] Created sample inventory at {self.path}')
        except Exception as e:
            print(f'[inventory][ERROR] Could not create sample inventory: {e}', file=sys.stderr)

    def load(self):
        self.products = []
        if not os.path.isfile(self.path):
            print(f'[inventory] {self.path} not found. Creating sample inventory...', file=sys.stderr)
            self._create_sample_inventory()

        try:
            with open(self.path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                expected = ['product_id','name','price','stock']
                headers = reader.fieldnames or []
                # basic header check
                if not all(h in headers for h in expected):
                    print(f"[inventory][WARNING] CSV headers mismatch. Found: {headers}. Expected: {expected}", file=sys.stderr)
                for r in reader:
                    try:
                        pid = r.get('product_id','').strip()
                        name = r.get('name','').strip()
                        price = float(r.get('price', 0) or 0)
                        stock = int(float(r.get('stock', 0) or 0))
                        if not pid:
                            # fallback: use name as id if product_id missing
                            pid = name or f'pid-{len(self.products)+1}'
                        self.products.append(Product(product_id=pid, name=name, price=price, stock=stock))
                    except Exception as e:
                        print(f"[inventory][WARN] Skipping row due to parse error: {r} -> {e}", file=sys.stderr)
        except Exception as e:
            print(f"[inventory][ERROR] Failed to read {self.path}: {e}", file=sys.stderr)

    def save(self):
        try:
            with open(self.path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['product_id','name','price','stock'])
                writer.writeheader()
                for p in self.products:
                    writer.writerow({'product_id': p.product_id, 'name': p.name, 'price': p.price, 'stock': p.stock})
        except Exception as e:
            print(f"[inventory][ERROR] Failed to save {self.path}: {e}", file=sys.stderr)

    def get_by_name(self, name: str) -> Optional[Product]:
        for p in self.products:
            if p.name.lower() == name.lower():
                return p
        return None

    def get_by_id(self, pid: str) -> Optional[Product]:
        for p in self.products:
            if p.product_id == pid:
                return p
        return None

    def update_stock(self, product_id: str, delta: int):
        p = self.get_by_id(product_id)
        if p:
            p.stock += delta
            if p.stock < 0:
                p.stock = 0
            self.save()

    def restock_from_csv(self, restock_path='restock.csv'):
        if not os.path.isfile(restock_path):
            print(f'[inventory] restock file {restock_path} not found', file=sys.stderr)
            return
        try:
            with open(restock_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        pid = r.get('product_id','').strip()
                        name = r.get('name','').strip()
                        qty = int(float(r.get('qty', 0) or 0))
                        price = float(r.get('price', 0) or 0)
                        if pid:
                            p = self.get_by_id(pid)
                            if p:
                                p.stock += qty
                            else:
                                self.products.append(Product(product_id=pid, name=name or f'item-{pid}', price=price, stock=qty))
                    except Exception as e:
                        print(f"[inventory][WARN] Skipping restock row {r}: {e}", file=sys.stderr)
            self.save()
            print(f'[inventory] Restock applied from {restock_path}')
        except Exception as e:
            print(f"[inventory][ERROR] Failed to restock from {restock_path}: {e}", file=sys.stderr)

    def list_products(self) -> List[Product]:
        return self.products

    def low_stock(self, threshold=5) -> List[Product]:
        return [p for p in self.products if p.stock < threshold]
