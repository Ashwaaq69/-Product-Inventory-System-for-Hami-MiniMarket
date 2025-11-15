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




HamiMiniMarket - Sales Dashboard & Analytics (Week 4)
A Python-based sales analytics and visualization tool that transforms raw sales data into actionable business insights. Built as the capstone project for the HamiSkills Python Development Track.

📊 Features
Core Analytics
Multi-file Data Processing: Automatically loads and combines sales data from multiple CSV files

Key Business Metrics: Total revenue, order count, average order value, daily revenue

Product Performance: Identify top-selling products and revenue drivers

Trend Analysis: Daily sales patterns and performance tracking

Inventory Insights: Low-stock alerts and product movement analysis

Visualization & Reporting
Interactive Charts: Multiple chart types including line, bar, and pie charts

Metrics Dashboard: Comprehensive overview of key business indicators

Daily Trends: Revenue and order patterns over time

Product Popularity: Top performers by revenue and quantity

Category Analysis: Sales distribution across product categories

Automated Reporting: Generate and export summary reports

Technical Features
Modular Architecture: Separated data loading, analytics, and visualization

Data Validation: Handles missing or malformed data gracefully

Automated Chart Export: Saves visualizations as PNG images

Interactive CLI: User-friendly menu system for analysis

CSV/Text Export: Summary reports in multiple formats

🛠 Project Structure
text
Week4_Capstone/
│
├── main.py                 # Main application entry point
├── data_loader.py          # Data loading and preprocessing
├── analytics.py            # Business logic and calculations
├── visuals.py              # Chart generation and visualization
├── generate_sample_data.py # Sample data generator
├── requirements.txt        # Python dependencies
│
├── sales_data/             # Input sales CSV files
│   ├── sales_2024-01-15.csv
│   ├── sales_2024-01-16.csv
│   └── ...
│
├── charts/                 # Generated visualization exports
│   ├── metrics_dashboard.png
│   ├── daily_sales_trends.png
│   ├── product_popularity_revenue.png
│   └── ...
│
└── sales_summary.txt       # Automated summary report
📁 Data Format
Input CSV Structure
Sales data should be in CSV files with naming pattern: sales_YYYY-MM-DD.csv

Required Columns:

order_id: Unique order identifier

product_id: Product SKU/code

product_name: Product description

quantity: Units sold

price: Unit price

total_price: Line total (quantity × price)

sale_date: Transaction date (YYYY-MM-DD)

Optional Columns:

category: Product category for enhanced analysis

stock: Current inventory levels

Sample Data Format
csv
order_id,product_id,product_name,category,quantity,price,total_price,sale_date
ORD001,P001,Coca-Cola 330ml,Beverages,2,1.50,3.00,2024-01-15
ORD001,P003,Lays Classic Chips,Snacks,1,2.00,2.00,2024-01-15
ORD002,P007,Milk 1L,Dairy,1,2.20,2.20,2024-01-15
🚀 Quick Start
Prerequisites
Python 3.7+

Required packages: pandas, matplotlib, numpy

Installation
bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data (optional)
python generate_sample_data.py

# Run the dashboard
python main.py
CLI Menu Options
📊 Generate Full Report - Complete analysis with all visualizations

📈 View Key Metrics - Display business metrics in console

🎨 Generate Specific Chart - Create individual chart types

🔄 Reload Data - Refresh data from source files

📤 Export Data Summary - Save comprehensive report

🚪 Exit - Close application

📈 Generated Outputs
Visualizations
Metrics Dashboard: Key performance indicators overview

Daily Sales Trends: Revenue and order patterns over time

Product Popularity: Top products by revenue and quantity

Category Distribution: Sales breakdown by product category

Hourly Sales Patterns: Time-based sales analysis (if time data available)

Reports
Console Metrics: Immediate business insights

Chart Exports: PNG images in charts/ folder

Text Summary: Comprehensive report in sales_summary.txt

🔧 Technical Implementation
Modules Overview
data_loader.py: Handles CSV loading, data validation, and preprocessing

analytics.py: Business logic for metrics calculation and trend analysis

visuals.py: Matplotlib-based chart generation and export

main.py: Application orchestration and CLI interface

Key Metrics Calculated
Total Revenue

Number of Orders

Products Sold

Average Order Value

Daily Revenue

Analysis Period

Top-performing Products

Low-stock Items

🎯 Integration with Previous Weeks
This Week 4 capstone builds upon:

Week 1: Inventory data structure and product information

Week 2: Order processing and sales data generation

Week 3: GUI interface and data persistence

The sales CSV files generated by previous weeks' order systems can be directly analyzed by this dashboard.

📊 Sample Output
Console Display
text
📈 KEY METRICS:
------------------------------
Total Revenue: $2,847.50
Total Orders: 312
Products Sold: 823
Average Order Value: $9.13
Daily Revenue: $203.39

🏆 TOP 5 PRODUCTS BY REVENUE:
----------------------------------------
1. Shampoo: $245.30
2. Eggs 12pcs: $228.00
3. Milk 1L: $198.00
Generated Files
charts/metrics_dashboard.png

charts/daily_sales_trends.png

charts/product_popularity_revenue.png

sales_summary.txt

🐛 Troubleshooting
Common Issues:

"No sales data found" → Ensure CSV files are in sales_data/ folder

Import errors → Run pip install -r requirements.txt

Chart generation fails → Verify matplotlib installation and folder permissions

Data Validation:

Handles missing values automatically

Converts data types where possible

Provides clear error messages for malformed data

📚 Learning Outcomes
This project demonstrates:

Data analysis with pandas

Business intelligence visualization

Modular Python application design

Automated reporting systems

CSV data processing and validation

Professional chart generation with matplotlib