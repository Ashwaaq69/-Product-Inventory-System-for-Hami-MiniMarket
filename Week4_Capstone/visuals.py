import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Dict, Any
import numpy as np

class SalesVisualizer:
    def __init__(self, charts_folder: str = "charts"):
        self.charts_folder = charts_folder
        self._setup_charts_folder()
        
    def _setup_charts_folder(self):
        """Create charts folder if it doesn't exist"""
        if not os.path.exists(self.charts_folder):
            os.makedirs(self.charts_folder)
    
    def create_daily_sales_trend(self, daily_trends: pd.DataFrame, 
                               metrics: Dict[str, Any]) -> str:
        """Create daily sales trend line chart"""
        if daily_trends.empty:
            return "No data available for daily trends"
        
        plt.figure(figsize=(12, 6))
        
        # Create subplot for revenue
        plt.subplot(1, 2, 1)
        plt.plot(daily_trends.index, daily_trends['daily_revenue'], 
                marker='o', linewidth=2, markersize=4, color='#2E86AB')
        plt.title('Daily Revenue Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Revenue')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Create subplot for orders
        plt.subplot(1, 2, 2)
        plt.plot(daily_trends.index, daily_trends['daily_orders'], 
                marker='s', linewidth=2, markersize=4, color='#A23B72')
        plt.title('Daily Orders Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Number of Orders')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = os.path.join(self.charts_folder, "daily_sales_trends.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_product_popularity_chart(self, top_products: pd.DataFrame, 
                                      by: str = 'revenue') -> str:
        """Create product popularity bar chart"""
        if top_products.empty:
            return "No data available for product popularity"
        
        plt.figure(figsize=(12, 8))
        
        if by == 'revenue':
            data = top_products['total_price']
            title = 'Top Products by Revenue'
            color = '#F18F01'
        else:  # by quantity
            data = top_products['quantity']
            title = 'Top Products by Quantity Sold'
            color = '#C73E1D'
        
        # Create horizontal bar chart
        y_pos = np.arange(len(data))
        plt.barh(y_pos, data.values, color=color, alpha=0.7)
        plt.yticks(y_pos, data.index)
        plt.xlabel('Revenue' if by == 'revenue' else 'Quantity Sold')
        plt.title(title, fontsize=16, fontweight='bold')
        plt.gca().invert_yaxis()  # highest value at top
        
        # Add value labels on bars
        for i, v in enumerate(data.values):
            plt.text(v + (v * 0.01), i, f'${v:,.2f}' if by == 'revenue' else f'{v:.0f}', 
                    va='center', fontsize=9)
        
        plt.tight_layout()
        
        filename = os.path.join(self.charts_folder, f"product_popularity_{by}.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_category_pie_chart(self, category_analysis: pd.DataFrame) -> str:
        """Create pie chart of sales by category"""
        if category_analysis.empty:
            return "No category data available"
        
        plt.figure(figsize=(10, 8))
        
        # Create pie chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(category_analysis)))
        wedges, texts, autotexts = plt.pie(category_analysis['category_revenue'], 
                                          labels=category_analysis.index,
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          startangle=90)
        
        # Improve text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.title('Sales Distribution by Category', fontsize=16, fontweight='bold')
        
        filename = os.path.join(self.charts_folder, "category_sales_pie.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_hourly_sales_chart(self, hourly_sales: pd.DataFrame) -> str:
        """Create hourly sales pattern chart"""
        if hourly_sales.empty:
            return "No hourly data available"
        
        plt.figure(figsize=(12, 6))
        
        # Create bar chart for hourly revenue
        hours = [f"{h:02d}:00" for h in hourly_sales.index]
        plt.bar(hours, hourly_sales['hourly_revenue'], 
               color='#6A8EAE', alpha=0.7)
        
        plt.title('Sales by Hour of Day', fontsize=16, fontweight='bold')
        plt.xlabel('Hour of Day')
        plt.ylabel('Revenue')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = os.path.join(self.charts_folder, "hourly_sales.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_metrics_dashboard(self, metrics: Dict[str, Any]) -> str:
        """Create a visual dashboard of key metrics"""
        plt.figure(figsize=(15, 10))
        
        # Define metrics to display
        key_metrics = [
            ('Total Revenue', f"${metrics.get('total_revenue', 0):,.2f}", '#2E86AB'),
            ('Total Orders', f"{metrics.get('total_orders', 0):,}", '#A23B72'),
            ('Avg Order Value', f"${metrics.get('average_order_value', 0):.2f}", '#F18F01'),
            ('Products Sold', f"{metrics.get('total_products_sold', 0):,}", '#C73E1D'),
            ('Daily Revenue', f"${metrics.get('daily_revenue', 0):,.2f}", '#6A8EAE'),
            ('Analysis Period', f"{metrics.get('analysis_period_days', 0)} days", '#495F41')
        ]
        
        # Create subplots for each metric
        for i, (title, value, color) in enumerate(key_metrics):
            plt.subplot(2, 3, i + 1)
            
            # Create a simple text display with background
            plt.text(0.5, 0.6, value, fontsize=24, fontweight='bold', 
                    ha='center', va='center', color=color)
            plt.text(0.5, 0.3, title, fontsize=14, 
                    ha='center', va='center', alpha=0.8)
            
            # Remove axes
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.axis('off')
        
        plt.suptitle('Hami MiniMarket - Sales Dashboard', fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        filename = os.path.join(self.charts_folder, "metrics_dashboard.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename