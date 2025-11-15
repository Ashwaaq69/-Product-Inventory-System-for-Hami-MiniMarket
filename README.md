HamiMiniMarket — CLI & GUI Inventory & Order Management

A Python-based mini-market management system featuring inventory control, order processing, sales reporting, and staff authentication. Designed with modularity in mind, using Tkinter for the GUI and JSON/CSV for persistent storage.

🛠 Features
1. Core Features (Week 1)

Load product inventory from products.json or inventory.csv

Display available products with price, category (optional), and stock

Add, update, or delete products from inventory

Input validation ensures correct data types and prevents invalid operations

Persistent data storage in JSON or CSV files

2. Order Management (Week 2)

Take customer orders via CLI or GUI

Add multiple items to a cart

Merge duplicate items in the cart automatically

Remove items from the cart

Check stock availability before adding items

Calculate:

Subtotal

Tax (5%)

Discount (10% if subtotal > $20)

Total

Confirm orders and update inventory automatically

Generate receipts and save with timestamp in data/receipts/ (CLI) or sales/ (GUI)

3. GUI Interface (Week 3)

Tkinter-based GUI (app.py) for:

Viewing products in a treeview with ID, Name, Price, and Stock

Searching products by name

Adding items to cart with quantity selection

Removing items from cart

Confirming orders with optional customer name

Low-stock alert panel

CSV-based restock functionality (restock.csv)

Integration with SalesReport for readable sales reports

4. Sales Reporting

Daily sales reports saved in CSV (sales/)

Generate readable reports per customer or for all customers

Grand totals and itemized lines included

Handles missing sales gracefully

5. Authentication & Staff Management

Staff login required to access CLI system

Credentials stored in users.json

Create new staff users with create_user() function in users.py

6. Technical Details

Modular structure:

inventory.py → Inventory management

order.py → Order/cart management

report.py → Sales reporting

app.py → GUI interface

Persistent storage with JSON (Week 1) and CSV (Week 3)

Input validation for numeric values, stock availability, and product IDs

Try/except blocks to handle file errors and invalid inputs gracefully

7. Optional Bonus

Discounts for orders over $20

Receipts include timestamp, customer name, and itemized order

Automatic low-stock notifications in GUI

⚙ How to Run
1. CLI Version (Week 1 & Week 2)

Create a staff user (first time only):

python
>>> from users import create_user
>>> create_user()


Run the main CLI system:

python main.py


Follow on-screen prompts to:

Login

View products

Place orders

Generate receipts

2. GUI Version (Week 3)

Ensure you have Tkinter installed (usually included with Python).

Run the GUI app:

python gui.py