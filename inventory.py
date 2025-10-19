# Step 1: Project setup and basic CLI menu

def display_menu():
    print("\n ---Inventory Management System----")
    print("1. Add product")
    print("2. View all products")
    print("3 update product quantity")
    print("4. Delete product")
    print("5. calculate total inventory value")
    print("6. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("Add Product selected")
        elif choice == "2":
            print("View Products selected")
        elif choice == "3":
            print("Update Product selected")
        elif choice == "4":
            print("Delete Product selected")    
        elif choice == "5":
            print("Calculate Total Value selected")
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")
            
            
if __name__ == "__main__":
    main()            
                        