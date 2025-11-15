import pandas as pd
import os
import sys
from data_loader import DataLoader
from analytics import SalesAnalytics
from visuals import SalesVisualizer
from datetime import datetime

class HamiMiniMarketDashboard:
    def __init__(self):
        self.data_loader = DataLoader()
        self.analytics = None
        self.visualizer = SalesVisualizer()
        
    def load_data(self) -> bool:
        """Load sales data and initialize analytics"""
        print("🚀 Hami MiniMarket Sales Dashboard")
        print("=" * 50)
        
        sales_data = self.data_loader.load_sales_files()
        
        if sales_data.empty:
            print("\n❌ No sales data found or data is empty.")
            print("Please ensure you have sales CSV files in the 'sales_data' folder.")
            return False
        
        self.analytics = SalesAnalytics(sales_data)
        print(f"\n✅ Successfully loaded {len(sales_data)} sales records")
        return True
    
    def generate_report(self):
        """Generate comprehensive sales report"""
        if self.analytics is None:
            print("Please load data first!")
            return
        
        print("\n📊 Generating Sales Report...")
        print("=" * 50)
        
        # Calculate metrics
        metrics = self.analytics.calculate_key_metrics()
        
        # Display key metrics
        self._display_metrics(metrics)
        
        # Generate visualizations
        self._generate_visualizations(metrics)
        
        # Export summary
        self._export_summary(metrics)
        
        print(f"\n✅ Report generation complete!")
        print(f"📁 Charts saved in 'charts/' folder")
        print(f"📄 Summary saved in 'sales_summary.txt'")
    
    def _display_metrics(self, metrics: dict):
        """Display key metrics in console"""
        print("\n📈 KEY METRICS:")
        print("-" * 30)
        print(f"Total Revenue: ${metrics.get('total_revenue', 0):,.2f}")
        print(f"Total Orders: {metrics.get('total_orders', 0):,}")
        print(f"Products Sold: {metrics.get('total_products_sold', 0):,}")
        print(f"Average Order Value: ${metrics.get('average_order_value', 0):.2f}")
        print(f"Daily Revenue: ${metrics.get('daily_revenue', 0):,.2f}")
        print(f"Analysis Period: {metrics.get('analysis_period_days', 0)} days")
        
        # Display top products
        top_products = self.analytics.get_top_selling_products(5)
        if not top_products.empty:
            print(f"\n🏆 TOP 5 PRODUCTS BY REVENUE:")
            print("-" * 40)
            for i, (product, row) in enumerate(top_products.iterrows(), 1):
                print(f"{i}. {product}: ${row['total_price']:,.2f}")
        
        # Display low stock items
        low_stock = self.analytics.get_low_stock_items()
        if not low_stock.empty:
            print(f"\n⚠️  LOW STOCK ITEMS:")
            print("-" * 30)
            for product, row in low_stock.iterrows():
                print(f"• {product}: {row['stock']} units")
    
    def _generate_visualizations(self, metrics: dict):
        """Generate all visualizations"""
        print("\n🎨 Generating Visualizations...")
        
        # Metrics dashboard
        self.visualizer.create_metrics_dashboard(metrics)
        print("✅ Created metrics dashboard")
        
        # Daily trends
        daily_trends = self.analytics.get_daily_sales_trends()
        if not daily_trends.empty:
            self.visualizer.create_daily_sales_trend(daily_trends, metrics)
            print("✅ Created daily sales trends")
        
        # Product popularity
        top_products = self.analytics.get_top_selling_products(10)
        if not top_products.empty:
            self.visualizer.create_product_popularity_chart(top_products, 'revenue')
            self.visualizer.create_product_popularity_chart(top_products, 'quantity')
            print("✅ Created product popularity charts")
        
        # Category analysis
        category_analysis = self.analytics.get_category_analysis()
        if not category_analysis.empty:
            self.visualizer.create_category_pie_chart(category_analysis)
            print("✅ Created category analysis chart")
        
        # Hourly sales
        hourly_sales = self.analytics.get_sales_by_hour()
        if not hourly_sales.empty:
            self.visualizer.create_hourly_sales_chart(hourly_sales)
            print("✅ Created hourly sales chart")
    
    def _export_summary(self, metrics: dict):
        """Export summary to text file"""
        summary_file = "sales_summary.txt"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("Hami MiniMarket - Sales Summary Report\n")
            f.write("=" * 50 + "\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("KEY METRICS:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Revenue: ${metrics.get('total_revenue', 0):,.2f}\n")
            f.write(f"Total Orders: {metrics.get('total_orders', 0):,}\n")
            f.write(f"Products Sold: {metrics.get('total_products_sold', 0):,}\n")
            f.write(f"Average Order Value: ${metrics.get('average_order_value', 0):.2f}\n")
            f.write(f"Daily Revenue: ${metrics.get('daily_revenue', 0):,.2f}\n")
            f.write(f"Analysis Period: {metrics.get('analysis_period_days', 0)} days\n\n")
            
            # Top products
            top_products = self.analytics.get_top_selling_products(10)
            if not top_products.empty:
                f.write("TOP 10 PRODUCTS BY REVENUE:\n")
                f.write("-" * 40 + "\n")
                for i, (product, row) in enumerate(top_products.iterrows(), 1):
                    f.write(f"{i}. {product}: ${row['total_price']:,.2f} "
                           f"({row['quantity']} units)\n")
                f.write("\n")
        
        print(f"✅ Summary exported to {summary_file}")
    
    def run_cli_menu(self):
        """Run interactive CLI menu"""
        while True:
            print("\n" + "=" * 50)
            print("🏪 Hami MiniMarket Analytics Menu")
            print("=" * 50)
            print("1. 📊 Generate Full Report")
            print("2. 📈 View Key Metrics")
            print("3. 🎨 Generate Specific Chart")
            print("4. 🔄 Reload Data")
            print("5. 📤 Export Data Summary")
            print("6. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.generate_report()
            elif choice == '2':
                if self.analytics:
                    metrics = self.analytics.calculate_key_metrics()
                    self._display_metrics(metrics)
                else:
                    print("Please load data first!")
            elif choice == '3':
                self._chart_menu()
            elif choice == '4':
                self.load_data()
            elif choice == '5':
                if self.analytics:
                    metrics = self.analytics.calculate_key_metrics()
                    self._export_summary(metrics)
                else:
                    print("Please load data first!")
            elif choice == '6':
                print("Thank you for using Hami MiniMarket Dashboard! 👋")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _chart_menu(self):
        """Chart generation sub-menu"""
        if not self.analytics:
            print("Please load data first!")
            return
        
        while True:
            print("\n📊 Chart Generation Menu:")
            print("1. Metrics Dashboard")
            print("2. Daily Sales Trends")
            print("3. Product Popularity (Revenue)")
            print("4. Product Popularity (Quantity)")
            print("5. Category Distribution")
            print("6. Hourly Sales Pattern")
            print("7. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            metrics = self.analytics.calculate_key_metrics()
            
            if choice == '1':
                filename = self.visualizer.create_metrics_dashboard(metrics)
                print(f"✅ Created: {filename}")
            elif choice == '2':
                daily_trends = self.analytics.get_daily_sales_trends()
                filename = self.visualizer.create_daily_sales_trend(daily_trends, metrics)
                print(f"✅ Created: {filename}")
            elif choice == '3':
                top_products = self.analytics.get_top_selling_products(10)
                filename = self.visualizer.create_product_popularity_chart(top_products, 'revenue')
                print(f"✅ Created: {filename}")
            elif choice == '4':
                top_products = self.analytics.get_top_selling_products(10)
                filename = self.visualizer.create_product_popularity_chart(top_products, 'quantity')
                print(f"✅ Created: {filename}")
            elif choice == '5':
                category_analysis = self.analytics.get_category_analysis()
                filename = self.visualizer.create_category_pie_chart(category_analysis)
                print(f"✅ Created: {filename}")
            elif choice == '6':
                hourly_sales = self.analytics.get_sales_by_hour()
                filename = self.visualizer.create_hourly_sales_chart(hourly_sales)
                print(f"✅ Created: {filename}")
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    """Main application entry point"""
    dashboard = HamiMiniMarketDashboard()
    
    # Load data
    if not dashboard.load_data():
        return
    
    # Run interactive menu
    dashboard.run_cli_menu()

if __name__ == "__main__":
    main()