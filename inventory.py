
import json
import os

DATA_FILE = "data/products.json"

# Ensure data folder exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def load_inventory():
    """Load inventory as a dictionary keyed by product id."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            products_list = json.load(f)
        inventory = {}
        for p in products_list:
            inventory[str(p["id"])] = {
                "name": p["name"],
                "category": p["category"],
                "price": p["price"],
                "stock": p["quantity"]
            }
        return inventory
    except Exception as e:
        print(f"❌ Error loading inventory: {e}")
        return {}

def save_inventory(inventory):
    """Save inventory dict back to products.json in list format."""
    try:
        products_list = []
        for pid, item in inventory.items():
            products_list.append({
                "id": int(pid),
                "name": item["name"],
                "category": item.get("category", ""),
                "price": item["price"],
                "quantity": item["stock"]
            })
        with open(DATA_FILE, "w") as f:
            json.dump(products_list, f, indent=4)
    except Exception as e:
        print(f"❌ Error saving inventory: {e}")
