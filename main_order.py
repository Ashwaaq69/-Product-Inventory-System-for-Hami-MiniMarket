import json
import os
from datetime import datetime

# -----------------------------
# File & Global Variables
# -----------------------------
DATA_FILE = "data/products.json"
RECEIPT_DIR = "data/receipts"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
os.makedirs(RECEIPT_DIR, exist_ok=True)

products = []
next_id = 1
TAX_RATE = 0.05
DISCOUNT_THRESHOLD = 20
DISCOUNT_RATE = 0.10

# -----------------------------
# Data Functions
# -----------------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(products, f, indent=4)

def load_data():
    global products, next_id
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            products = json.load(f)
        if products:
            next_id = max(p["id"] for p in products) + 1
    else:
        products = []

# -----------------------------
# Helper Functions
# -----------------------------
def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("❌ Must be positive.")
            else:
                return value
        except ValueError:
            print("❌ Invalid number.")

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("❌ Must be positive.")
            else:
                return value
        except ValueError:
            print("❌ Invalid integer.")

def get_existing_product_id():
    while True:
        try:
            pid = int(input("Enter product ID: "))
            for p in products:
                if p["id"] == pid:
                    return pid
            print("❌ Product ID not found.")
        except ValueError:
            print("❌ Invalid input.")

# -----------------------------
# Inventory Management
# -----------------------------
def add_product():
    global next_id
    name = input("Product name: ").strip()
    category = input("Category: ").strip()
    price = get_positive_float("Price: ")
    quantity = get_positive_int("Quantity: ")
    products.append({"id": next_id, "name": name, "category": category, "price": price, "quantity": quantity})
    next_id += 1
    save_data()
    print(f"✅ '{name}' added.")

def view_products():
    if not products:
        print("📭 No products.")
        return
    print("\nID | Name       | Category    | Price   | Quantity | Total")
    print("-"*60)
    for p in products:
        total = p["price"]*p["quantity"]
        print(f"{p['id']:2} | {p['name']:<10} | {p['category']:<10} | ${p['price']:<6.2f} | {p['quantity']:<8} | ${total:.2f}")

def update_product_quantity():
    pid = get_existing_product_id()
    for p in products:
        if p["id"] == pid:
            new_qty = get_positive_int(f"New quantity for {p['name']}: ")
            p["quantity"] = new_qty
            save_data()
            print(f"✅ Quantity updated to {new_qty}.")
            return

def delete_product():
    pid = get_existing_product_id()
    for p in products:
        if p["id"] == pid:
            confirm = input(f"Delete '{p['name']}'? (y/n): ").lower()
            if confirm == 'y':
                products.remove(p)
                save_data()
                print(f"✅ Deleted '{p['name']}'")
            return

def total_inventory_value():
    total = sum(p["price"]*p["quantity"] for p in products)
    print(f"💰 Total inventory value: ${total:.2f}")

# -----------------------------
# Order Management
# -----------------------------
def create_order():
    if not products:
        print("⚠️ Inventory empty.")
        return

    cart = []
    while True:
        view_products()
        choice = input("Enter product ID to add to cart (q to finish): ").strip()
        if choice.lower() == "q":
            break
        if not choice.isdigit():
            print("❌ Invalid ID.")
            continue
        pid = int(choice)
        item = next((p for p in products if p["id"] == pid), None)
        if not item:
            print("❌ Not found.")
            continue
        if item["quantity"] == 0:
            print("⚠️ Out of stock.")
            continue
        qty = get_positive_int(f"Quantity for '{item['name']}' (available {item['quantity']}): ")
        if qty > item["quantity"]:
            print(f"⚠️ Only {item['quantity']} available.")
            continue
        cart.append({"name": item["name"], "price": item["price"], "qty": qty})
        item["quantity"] -= qty
        print(f"✅ Added {qty} x {item['name']}.")

    if not cart:
        print("🚫 No items added.")
        return

    subtotal = sum(i["price"]*i["qty"] for i in cart)
    tax = subtotal*TAX_RATE
    discount = subtotal*DISCOUNT_RATE if subtotal>DISCOUNT_THRESHOLD else 0
    total = subtotal + tax - discount

    print("\n--- Order Summary ---")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax (5%): ${tax:.2f}")
    print(f"Discount: -${discount:.2f}")
    print(f"TOTAL: ${total:.2f}")

    # Save receipt
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(RECEIPT_DIR, f"receipt_{now}.txt")
    with open(path, "w") as f:
        f.write("===== Receipt =====\n")
        f.write(f"Date: {datetime.now()}\n\n")
        for i in cart:
            f.write(f"{i['name']:20} x{i['qty']} ${i['price']} -> ${i['qty']*i['price']}\n")
        f.write(f"\nSubtotal: ${subtotal:.2f}\nTax: ${tax:.2f}\nDiscount: ${discount:.2f}\nTOTAL: ${total:.2f}\n")
    save_data()
    print(f"✅ Receipt saved: {path}")

# -----------------------------
# Main Menu
# -----------------------------
def main_menu():
    load_data()
    while True:
        print("\n--- Hami MiniMarket ---")
        print("1. Inventory Management")
        print("2. Create Order")
        print("3. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            while True:
                print("\n--- Inventory ---")
                print("1. Add Product")
                print("2. View Products")
                print("3. Update Quantity")
                print("4. Delete Product")
                print("5. Total Inventory Value")
                print("6. Back")
                inv_choice = input("Choice: ").strip()
                if inv_choice == "1": add_product()
                elif inv_choice == "2": view_products()
                elif inv_choice == "3": update_product_quantity()
                elif inv_choice == "4": delete_product()
                elif inv_choice == "5": total_inventory_value()
                elif inv_choice == "6": break
                else: print("❌ Invalid.")
        elif choice == "2":
            create_order()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice.")

# -----------------------------
# Entry
# -----------------------------
if __name__ == "__main__":
    main_menu()
