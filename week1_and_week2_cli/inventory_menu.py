from inventory import load_inventory, save_inventory

def display_products(inventory):
    """Display all products in a formatted table."""
    if not inventory:
        print("📭 No products found.")
        return

    print("\nID | Name                 | Category      | Price    | Stock")
    print("-" * 60)
    for pid, item in inventory.items():
        print(f"{pid:2} | {item['name']:<20} | {item['category']:<12} | $ {item['price']:>6.2f} | {item['stock']:>5}")
    print("-" * 60)


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("❌ Must be positive.")
                continue
            return value
        except ValueError:
            print("❌ Invalid number.")


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("❌ Must be positive.")
                continue
            return value
        except ValueError:
            print("❌ Invalid integer.")


def add_product():
    inventory = load_inventory()

    name = input("Enter product name: ").strip()
    category = input("Enter category: ").strip()
    price = get_positive_float("Enter price: ")
    stock = get_positive_int("Enter quantity: ")

    # Determine next ID
    next_id = max([int(pid) for pid in inventory.keys()], default=0) + 1
    inventory[str(next_id)] = {"name": name, "category": category, "price": price, "stock": stock}

    save_inventory(inventory)
    print(f"✅ Product '{name}' added successfully!")


def update_product():
    inventory = load_inventory()
    display_products(inventory)

    pid = input("Enter product ID to update: ").strip()
    if pid not in inventory:
        print("❌ Invalid ID.")
        return

    stock = get_positive_int(f"Enter new quantity for {inventory[pid]['name']}: ")
    inventory[pid]['stock'] = stock
    save_inventory(inventory)
    print(f"✅ Quantity updated for '{inventory[pid]['name']}'.")


def delete_product():
    inventory = load_inventory()
    display_products(inventory)

    pid = input("Enter product ID to delete: ").strip()
    if pid not in inventory:
        print("❌ Invalid ID.")
        return

    confirm = input(f"Are you sure you want to delete '{inventory[pid]['name']}'? (y/n): ").lower()
    if confirm == 'y':
        inventory.pop(pid)
        save_inventory(inventory)
        print("✅ Product deleted.")
    else:
        print("❌ Deletion cancelled.")


def inventory_menu():
    while True:
        print("\n--- Inventory Menu ---")
        print("1. View Products")
        print("2. Add Product")
        print("3. Update Product Quantity")
        print("4. Delete Product")
        print("5. Back to Main Menu")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            display_products(load_inventory())
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice.")
