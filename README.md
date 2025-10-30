
---

## 🛠 Features

### 1. Core Features
- Load product inventory from a JSON file (`products.json`)  
- Display available products with price, category, and stock  
- Add, update, or delete products from inventory  
- Take customer orders and check stock availability  
- Calculate subtotal, tax (5%), discount (10% if subtotal > $20), and total  
- Generate and save receipts with timestamp (`data/receipts/`)  

### 2. Authentication
- Staff login required to access the system  
- Staff credentials stored in `users.json`  
- Function to create new staff users: `create_user()` in `users.py`  

### 3. Technical Requirements
- Modular structure with separate files for inventory, orders, and authentication  
- Input validation for numeric values, stock, and product IDs  
- Persistent data storage in JSON files  
- Try/except blocks handle file and input errors gracefully  

### 4. Optional Bonus
- Discount system applied for orders exceeding $20  
- Receipts include itemized list and total cost  

---

## ⚙ How to Run

1. **Create a user** (first time only):

```bash
python
>>> from users import create_user
>>> create_user()
