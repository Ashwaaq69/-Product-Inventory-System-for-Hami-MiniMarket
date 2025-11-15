import pandas as pd
import os
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample sales data for testing the dashboard"""
    
    # Create sales_data folder if it doesn't exist
    if not os.path.exists('sales_data'):
        os.makedirs('sales_data')
    
    print("🎯 Generating sample sales data for Hami MiniMarket...")
    
    # Sample products with categories
    products = [
        {'product_id': 'P001', 'product_name': 'Coca-Cola 330ml', 'category': 'Beverages', 'price': 1.50},
        {'product_id': 'P002', 'product_name': 'Pepsi 330ml', 'category': 'Beverages', 'price': 1.45},
        {'product_id': 'P003', 'product_name': 'Lays Classic Chips', 'category': 'Snacks', 'price': 2.00},
        {'product_id': 'P004', 'product_name': 'Doritos Nacho Cheese', 'category': 'Snacks', 'price': 2.20},
        {'product_id': 'P005', 'product_name': 'Whole Wheat Bread', 'category': 'Bakery', 'price': 3.50},
        {'product_id': 'P006', 'product_name': 'Croissant', 'category': 'Bakery', 'price': 1.80},
        {'product_id': 'P007', 'product_name': 'Milk 1L', 'category': 'Dairy', 'price': 2.20},
        {'product_id': 'P008', 'product_name': 'Yogurt 500g', 'category': 'Dairy', 'price': 3.00},
        {'product_id': 'P009', 'product_name': 'Eggs 12pcs', 'category': 'Dairy', 'price': 4.00},
        {'product_id': 'P010', 'product_name': 'Mineral Water 500ml', 'category': 'Beverages', 'price': 1.00},
        {'product_id': 'P011', 'product_name': 'Chocolate Bar', 'category': 'Snacks', 'price': 1.80},
        {'product_id': 'P012', 'product_name': 'Toothpaste', 'category': 'Personal Care', 'price': 3.20},
        {'product_id': 'P013', 'product_name': 'Shampoo', 'category': 'Personal Care', 'price': 5.50},
        {'product_id': 'P014', 'product_name': 'Apples 1kg', 'category': 'Fruits', 'price': 2.80},
        {'product_id': 'P015', 'product_name': 'Bananas 1kg', 'category': 'Fruits', 'price': 1.50},
    ]
    
    # Generate data for the last 14 days
    base_date = datetime.now().date() - timedelta(days=14)
    
    for day in range(14):
        sales_date = base_date + timedelta(days=day)
        filename = f"sales_data/sales_{sales_date.strftime('%Y-%m-%d')}.csv"
        
        sales_records = []
        
        # Generate different number of sales per day (more on weekends)
        if sales_date.weekday() >= 5:  # Weekend
            num_orders = random.randint(25, 40)
        else:  # Weekday
            num_orders = random.randint(15, 30)
        
        order_counter = 1
        
        for order in range(num_orders):
            # Each order has 1-4 items
            num_items = random.randint(1, 4)
            order_id = f"ORD{sales_date.strftime('%Y%m%d')}{order_counter:03d}"
            
            for item in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                total_price = product['price'] * quantity
                
                sale_record = {
                    'order_id': order_id,
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'category': product['category'],
                    'quantity': quantity,
                    'price': product['price'],
                    'total_price': total_price,
                    'sale_date': sales_date.strftime('%Y-%m-%d')
                }
                
                sales_records.append(sale_record)
            
            order_counter += 1
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(sales_records)
        df.to_csv(filename, index=False)
        print(f"✅ Created: {filename} - {len(sales_records)} records")
    
    print(f"\n🎉 Successfully generated {14} days of sample sales data!")
    print("📊 You can now run: python main.py")

if __name__ == "__main__":
    generate_sample_data()