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
            
          
          
# Step 2 —  Product Feature     

products = []
next_id = 1
def add_product():
    global next_id
    name = input("Enter product name: ")
    category = input("Enter category: ")
    
    # input validation for price and quantity
    while True:
        try:
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
            break
        except ValueError:
            print("Invalid input for price or quantity. Please enter integer values.")
        
    product = {
        "id": next_id,
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity    
    }
    products.append(product)
    next_id += 1
    print(f"Product {name} added successfully.")    
    
# Step 3 — View All Products
def view_products():
    if not products:
        print("📭 No products found.")
        return

    print("\nID | Name       | Category    | Price | Quantity | Total Value")
    print("-" * 60)
    for p in products:
        total_value = p["price"] * p["quantity"]
        print(f"{p['id']:2} | {p['name']:<10} | {p['category']:<10} | {p['price']:<5.2f} | {p['quantity']:<8} | {total_value:.2f}")

# Step 4 — Update Product Quantity
def update_product_quantity():
    try:
        product_id = int(input("Enter product ID to update quantity: "))
        for p in products:
            if p["id"] == product_id:
                new_quantity = int(input(f"Enter new quantity for {p['name']}: "))
                p["quantity"] = new_quantity
                print(f"Quantity for {p['name']} updated to {new_quantity}.")
                return
        print("Product ID not found.")
    except ValueError:
        print("Invalid input. Please enter integer values.")  

        
# Step 5 delete product

def delete_product():
    try:
        product_id = int(input("Enter product ID to delete: "))
        for p in products:
            if p["id"] == product_id:
                products.remove(p)
                print(f"Product {p['name']} deleted successfully.")
                return
        print("Product ID not found.")
    except ValueError:
        print("Invalid input. Please enter integer values.")              
            
   
if __name__ == "__main__":
    # main()  
    add_product()  
    view_products()
    update_product_quantity()
    delete_product()


    