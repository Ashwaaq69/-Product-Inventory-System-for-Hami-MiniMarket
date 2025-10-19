# Hami MiniMarket Inventory System

A **Python command-line application** for managing products in a small community shop (fruits and vegetables).  
This system allows the shopkeeper to **add, view, update, and delete products**, as well as **calculate the total inventory value**. Data is stored in a JSON file to persist across program runs.

---

## Features

- **Add Product**  
  Add a new product with name, category, price, and quantity. Input is validated to ensure correct data types.
  
- **View All Products**  
  Display all products in a **formatted table** showing ID, name, category, price, quantity, and total value.
  
- **Update Product Quantity**  
  Update the stock quantity of an existing product using its ID.

- **Delete Product**  
  Remove a product from the inventory after confirmation.

- **Calculate Total Inventory Value**  
  Calculate the total value of all products in stock.

- **Data Persistence**  
  Products are saved to `products.json` automatically after every change and loaded on program start.

- **Input Validation**  
  Ensures product name and category contain letters, price and quantity are positive numbers, and product IDs are valid.

---

## Requirements

- Python 3.x
- No external libraries required (uses built-in `json` and `os` modules)

---

## Getting Started

1. **Clone the repository**
   ```bash
   git clonehttps://github.com/Ashwaaq69/-Product-Inventory-System-for-Hami-MiniMarket.git
 