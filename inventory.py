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
        print("No products in inventory.")
        return
    
    print("\nID | Name       | Category    | Price | Quantity | Total Value")
    for product in products:
        print(f"ID: {product['id']}, Name: {product['name']}, Category: {product['category']}, Price: {product['price']}, Quantity: {product['quantity']}, total value: {product['price'] * product['quantity']}")
        
       
if __name__ == "__main__":
    # main()  
    # add_product()  
    view_products()

    