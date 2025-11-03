from inventory import load_inventory, save_inventory
from datetime import datetime
import os
import json

DATA_DIR = "data"
RECEIPT_DIR = os.path.join(DATA_DIR, "receipts")
os.makedirs(RECEIPT_DIR, exist_ok=True)

TAX_RATE = 0.05
DISCOUNT_THRESHOLD = 20
DISCOUNT_RATE = 0.10


def display_products(inventory):
    print("\nID | Name                 | Price    | Available")
    print("-" * 50)
    for pid, item in inventory.items():
        print(f"{pid:2} | {item['name']:<20} | $ {item['price']:>6.2f} | {item['stock']:>9}")
    print("-" * 50)


def get_valid_product_id(inventory):
    """Prompt until user enters a valid product ID or 'q'."""
    while True:
        product_id = input("Product ID (or 'q'): ").strip()
        if product_id.lower() == 'q':
            return None
        if product_id not in inventory:
            print("❌ Invalid product ID! Please try again.")
        elif inventory[product_id]['stock'] <= 0:
            print("⚠️  Product out of stock! Choose another one.")
        else:
            return product_id


def get_valid_quantity(stock):
    """Prompt until user enters a valid quantity."""
    while True:
        qty_input = input("Enter quantity: ").strip()
        if not qty_input.isdigit():
            print("❌ Please enter a valid positive number.")
            continue
        qty = int(qty_input)
        if qty <= 0:
            print("❌ Quantity must be greater than zero.")
        elif qty > stock:
            print(f"⚠️  Only {stock} available. Try again.")
        else:
            return qty


def calculate_totals(cart):
    subtotal = sum(item['price'] * item['qty'] for item in cart)
    tax = subtotal * TAX_RATE
    discount = subtotal * DISCOUNT_RATE if subtotal > DISCOUNT_THRESHOLD else 0
    total = subtotal + tax - discount
    return subtotal, tax, discount, total


def save_receipt(cart, subtotal, tax, discount, total):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    receipt_path = os.path.join(RECEIPT_DIR, f"receipt_{now}.txt")

    with open(receipt_path, "w") as f:
        f.write("===== Hami MiniMarket Receipt =====\n")
        f.write(f"Date: {datetime.now()}\n\n")
        f.write(f"{'Item':20} {'Qty':>5} {'Price':>8} {'Total':>8}\n")
        f.write("-" * 45 + "\n")
        for item in cart:
            total_item = item['price'] * item['qty']
            f.write(f"{item['name']:20} {item['qty']:>5} {item['price']:>8.2f} {total_item:>8.2f}\n")
        f.write("-" * 45 + "\n")
        f.write(f"Subtotal: ${subtotal:.2f}\n")
        f.write(f"Tax (5%): ${tax:.2f}\n")
        f.write(f"Discount: -${discount:.2f}\n")
        f.write(f"TOTAL: ${total:.2f}\n")
        f.write("==============================\n")

    print(f"✅ Receipt saved: {receipt_path}")


def main():
    try:
        inventory = load_inventory()
        if not inventory:
            print("⚠️  Inventory is empty! Please load products first.")
            return

        cart = []
        display_products(inventory)

        while True:
            print("Enter product ID to add to cart, or 'q' to finish.")
            product_id = get_valid_product_id(inventory)
            if product_id is None:
                break

            qty = get_valid_quantity(inventory[product_id]['stock'])
            item = inventory[product_id]
            cart.append({'name': item['name'], 'price': item['price'], 'qty': qty})
            inventory[product_id]['stock'] -= qty

            print(f"✅ Added {qty} x {item['name']} to cart.\n")

        if not cart:
            print("🚫 No items added. Order cancelled.")
            return

        subtotal, tax, discount, total = calculate_totals(cart)

        print("\n--- Order Summary ---")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax (5%): ${tax:.2f}")
        print(f"Discount: -${discount:.2f}")
        print(f"TOTAL: ${total:.2f}")

        save_receipt(cart, subtotal, tax, discount, total)
        save_inventory(inventory)
        print("💾 Data saved.")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
