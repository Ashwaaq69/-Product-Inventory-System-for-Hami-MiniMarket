from users import login

from inventory_menu import inventory_menu

from order import main as order_main

# Placeholder inventory menu

def main_menu():
    if not login():
        print("Access denied! Exiting...")
        return

    while True:
        print("\n--- Main Menu ---")
        print("1. Inventory Management")
        print("2. Take Order")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            inventory_menu()
        elif choice == "2":
            order_main()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main_menu()
