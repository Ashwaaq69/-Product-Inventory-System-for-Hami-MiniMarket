import csv
from datetime import datetime
import os

class SalesReport:
    def __init__(self, outdir='sales'):
        self.outdir = outdir
        os.makedirs(self.outdir, exist_ok=True)

    def sales_filename(self, date: datetime):
        return os.path.join(self.outdir, f'sales_{date.strftime("%Y-%m-%d")}.csv')

    def save_order(self, order_data: dict):
        dt = datetime.fromisoformat(order_data['timestamp'])
        path = self.sales_filename(dt)
        file_exists = os.path.isfile(path)
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp','customer','product_id','name','price','qty','line_total'])
            if not file_exists:
                writer.writeheader()
            for it in order_data['items']:
                writer.writerow({
                    'timestamp': order_data['timestamp'],
                    'customer': order_data['customer'],
                    'product_id': it['product_id'],
                    'name': it['name'],
                    'price': it['price'],
                    'qty': it['qty'],
                    'line_total': float(it['price']) * int(it['qty'])
                })

    def readable_daily_report(self, date=None):
        """Print a readable daily report for all sales."""
        if date is None:
            date = datetime.now()
        path = self.sales_filename(date)

        if not os.path.exists(path):
            print(f"No sales found for {date.strftime('%Y-%m-%d')}.")
            return

        print(f"\n🧾 Hami MiniMarket — Daily Sales Report ({date.strftime('%B %d, %Y')})")
        print("-" * 60)

        total_sales = 0.0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = datetime.fromisoformat(row['timestamp'])
                print(f"Time: {ts.strftime('%I:%M:%S %p')}")
                print(f"Customer: {row['customer']}")
                print(f"Product ID: {row['product_id']}")
                print(f"Product Name: {row['name']}")
                print(f"Unit Price: ${float(row['price']):.2f}")
                print(f"Quantity: {row['qty']}")
                print(f"Line Total: ${float(row['line_total']):.2f}")
                print("-" * 60)
                total_sales += float(row['line_total'])

        print(f"💰 Total Sales for the Day: ${total_sales:.2f}\n")

    def daily_summary(self, date: datetime):
        path = self.sales_filename(date)
        summary = {'date': date.strftime('%Y-%m-%d'), 'total_sales': 0.0, 'items_sold': {}}
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    lt = float(r.get('line_total', 0))
                    summary['total_sales'] += lt
                    name = r.get('name')
                    qty = int(r.get('qty', 0))
                    summary['items_sold'][name] = summary['items_sold'].get(name, 0) + qty
        except FileNotFoundError:
            pass
        return summary

    # 🧾 Generate readable report per customer
    def generate_customer_report(self, customer_name: str, date: datetime = None):
        if date is None:
            date = datetime.now()
        path = self.sales_filename(date)

        if not os.path.exists(path):
            print(f"No sales found for {date.strftime('%Y-%m-%d')}.")
            return None

        report_dir = os.path.join(self.outdir, "readable_reports")
        os.makedirs(report_dir, exist_ok=True)

        total = 0.0
        report_lines = []

        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['customer'].strip().lower() == customer_name.strip().lower():
                    ts = datetime.fromisoformat(row['timestamp'])
                    date_str = ts.strftime('%B %d, %Y')
                    time_str = ts.strftime('%I:%M %p')
                    report_lines.append(f"""
🧾 Hami MiniMarket — Customer Sales Report
------------------------------------------
Date: {date_str} | Time: {time_str}
Customer: {row['customer']}
------------------------------------------
Product ID: {row['product_id']}
Product Name: {row['name']}
Unit Price: ${float(row['price']):.2f}
Quantity: {row['qty']}
Line Total: ${float(row['line_total']):.2f}
------------------------------------------
""")
                    total += float(row['line_total'])

        if not report_lines:
            print(f"No purchases found for customer '{customer_name}'.")
            return None

        report_lines.append(f"💰 Grand Total: ${total:.2f}\n")
        report_lines.append("Thank you for shopping with Hami MiniMarket!\n")

        filename = f"{customer_name}_{date.strftime('%Y%m%d_%H%M%S')}.txt"
        report_path = os.path.join(report_dir, filename)

        with open(report_path, "w", encoding="utf-8") as rf:
            rf.writelines(report_lines)

        print(f"✅ Customer report saved: {report_path}")
        return report_path

    # 🧾 Generate readable reports for all customers in a day
    def generate_reports_for_all_customers(self, date=None):
        if date is None:
            date = datetime.now()
        path = self.sales_filename(date)

        if not os.path.exists(path):
            print(f"No sales found for {date.strftime('%Y-%m-%d')}.")
            return []

        # Collect unique customer names
        customers = set()
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                customers.add(row['customer'].strip())

        # Generate report for each customer
        report_paths = []
        for customer in customers:
            rp = self.generate_customer_report(customer, date)
            if rp:
                report_paths.append(rp)

        print(f"✅ Generated {len(report_paths)} customer reports.")
        return report_paths


# ✅ Add this block to run readable_daily_report directly
if __name__ == "__main__":
    report = SalesReport()
    report.readable_daily_report(datetime(2025, 11, 3))
