import json
import os

# -----------------------------
# Global Variables
# -----------------------------
DATA_FILE = "products.json"  # JSON file to store product data
products = []                # List to hold product dictionaries
next_id = 1                  # Auto-incrementing ID for new products

# -----------------------------
# Data Persistence Functions
# -----------------------------
def save_data():
    """
    Save the current products list to the JSON file.
    This ensures data is persistent across program runs.
    """
    with open(DATA_FILE, "w") as f:
        json.dump(products, f, indent=4)
    print("💾 Data saved.")

def load_data():
    """
    Load products from the JSON file if it exists.
    Sets the global next_id based on the highest existing product ID.
    """
    global products, next_id
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            products = json.load(f)
        if products:
            next_id = max(p["id"] for p in products) + 1
        print("📂 Data loaded.")
    else:
        products = []

# -----------------------------
# Helper Functions
# -----------------------------
def get_positive_float(prompt):
    """
    Prompt user until they enter a positive float value.
    Used for price input.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("❌ Value must be positive.")
                continue
            return value
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def get_positive_int(prompt):
    """
    Prompt user until they enter a positive integer value.
    Used for quantity input.
    """
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("❌ Value must be positive.")
                continue
            return value
        except ValueError:
            print("❌ Invalid input. Please enter an integer.")

def get_existing_product_id():
    """
    Prompt user until they enter a valid existing product ID.
    Ensures update and delete operations only use valid IDs.
    """
    while True:
        try:
            product_id = int(input("Enter product ID: "))
            for p in products:
                if p["id"] == product_id:
                    return product_id
            print("❌ Product ID not found.")
        except ValueError:
            print("❌ Invalid input. Please enter an integer.")

# -----------------------------
# Inventory Feature Functions
# -----------------------------
def add_product():
    """
    Add a new product to inventory with validation:
    - Name and category must contain letters
    - Price must be a positive float
    - Quantity must be a positive integer
    """
    global next_id

    # Validate product name
    while True:
        name = input("Enter product name: ").strip()
        if not name:
            print("❌ Product name cannot be empty.")
        elif not any(c.isalpha() for c in name):
            print("❌ Product name must contain letters.")
        else:
            break

    # Validate category
    while True:
        category = input("Enter category: ").strip()
        if not category:
            print("❌ Category cannot be empty.")
        elif not any(c.isalpha() for c in category):
            print("❌ Category must contain letters.")
        else:
            break

    # Get validated price and quantity
    price = get_positive_float("Enter price: ")
    quantity = get_positive_int("Enter quantity: ")

    # Create and add product
    product = {
        "id": next_id,
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity
    }
    products.append(product)
    next_id += 1
    print(f"✅ Product '{name}' added successfully!")
    save_data()  # Auto-save after adding

def view_products():
    """
    Display all products in a formatted table:
    Shows ID, name, category, price, quantity, and total value.
    """
    if not products:
        print("📭 No products found.")
        return

    print("\nID | Name       | Category    | Price   | Quantity | Total Value")
    print("-" * 65)
    for p in products:
        total_value = p["price"] * p["quantity"]
        print(f"{p['id']:2} | {p['name']:<10} | {p['category']:<10} | {p['price']:<7.2f} | {p['quantity']:<8} | {total_value:.2f}")

def update_product_quantity():
    """
    Update the quantity of an existing product.
    Prompts for product ID and new quantity with validation.
    """
    product_id = get_existing_product_id()
    for p in products:
        if p["id"] == product_id:
            new_quantity = get_positive_int(f"Enter new quantity for {p['name']}: ")
            p["quantity"] = new_quantity
            print(f"✅ Quantity for '{p['name']}' updated to {new_quantity}.")
            save_data()  # Auto-save after updating
            return

def delete_product():
    """
    Delete a product from inventory.
    Prompts for product ID and confirmation before deletion.
    """
    product_id = get_existing_product_id()
    for p in products:
        if p["id"] == product_id:
            confirm = input(f"Are you sure you want to delete '{p['name']}'? (y/n): ").lower()
            if confirm == 'y':
                products.remove(p)
                print(f"✅ Product '{p['name']}' deleted successfully.")
                save_data()  # Auto-save after deletion
            else:
                print("❌ Deletion cancelled.")
            return

def calculate_total_inventory_value():
    """
    Calculate and display total value of all products in inventory.
    """
    total_value = sum(p["price"] * p["quantity"] for p in products)
    print(f"💰 Total inventory value: ${total_value:.2f}")

# -----------------------------
# Menu / Main Program Functions
# -----------------------------
def display_menu():
    """
    Display the main menu for the inventory system.
    Lists all available actions for the user.
    """
    print("\n--- Hami MiniMarket Inventory System ---")
    print("1. Add Product")
    print("2. View All Products")
    print("3. Update Product Quantity")
    print("4. Delete Product")
    print("5. Calculate Total Inventory Value")
    print("6. Exit")

def main():
    """
    Main program loop:
    - Loads data from file at start
    - Displays menu and executes chosen action
    - Saves data before exiting
    """
    load_data()  # Load data at start
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_product_quantity()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            calculate_total_inventory_value()
        elif choice == "6":
            save_data()  # Save data before exiting
            print("Exiting program...")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
