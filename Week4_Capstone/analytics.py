import pandas as pd
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta

class SalesAnalytics:
    def __init__(self, sales_data: pd.DataFrame):
        self.sales_data = sales_data
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data for analysis"""
        if self.sales_data.empty:
            return
            
        # Ensure we have required columns
        if 'total_price' not in self.sales_data.columns:
            # Calculate total price if not present
            if 'quantity' in self.sales_data.columns and 'price' in self.sales_data.columns:
                self.sales_data['total_price'] = self.sales_data['quantity'] * self.sales_data['price']
            else:
                self.sales_data['total_price'] = 0
        
        # Ensure we have a date column
        if 'sale_date' not in self.sales_data.columns:
            self.sales_data['sale_date'] = pd.to_datetime('today')
    
    def calculate_key_metrics(self) -> Dict[str, Any]:
        """Calculate key sales metrics"""
        if self.sales_data.empty:
            return {}
        
        metrics = {}
        
        # Basic metrics
        metrics['total_revenue'] = self.sales_data['total_price'].sum()
        metrics['total_orders'] = self.sales_data.get('order_id', pd.Series([1] * len(self.sales_data))).nunique()
        metrics['total_products_sold'] = self.sales_data['quantity'].sum()
        metrics['average_order_value'] = metrics['total_revenue'] / max(metrics['total_orders'], 1)
        
        # Date-based metrics
        if 'sale_date' in self.sales_data.columns:
            date_range = self.sales_data['sale_date'].max() - self.sales_data['sale_date'].min()
            metrics['analysis_period_days'] = date_range.days + 1
            metrics['daily_revenue'] = metrics['total_revenue'] / max(metrics['analysis_period_days'], 1)
        else:
            metrics['analysis_period_days'] = 1
            metrics['daily_revenue'] = metrics['total_revenue']
        
        return metrics
    
    def get_top_selling_products(self, top_n: int = 10) -> pd.DataFrame:
        """Get top selling products by revenue and quantity"""
        if self.sales_data.empty:
            return pd.DataFrame()
        
        product_sales = self.sales_data.groupby('product_name').agg({
            'total_price': 'sum',
            'quantity': 'sum',
            'product_id': 'count'
        }).rename(columns={'product_id': 'transaction_count'})
        
        product_sales = product_sales.sort_values('total_price', ascending=False)
        return product_sales.head(top_n)
    
    def get_low_stock_items(self, threshold: int = 10) -> pd.DataFrame:
        """Identify low stock items (if stock data is available)"""
        if self.sales_data.empty or 'stock' not in self.sales_data.columns:
            return pd.DataFrame()
        
        low_stock = self.sales_data[self.sales_data['stock'] <= threshold]
        
        if not low_stock.empty:
            # Get the most recent stock level for each product
            low_stock_items = low_stock.sort_values('sale_date').groupby('product_name').last()
            return low_stock_items[['stock', 'product_id']].sort_values('stock')
        
        return pd.DataFrame()
    
    def get_daily_sales_trends(self) -> pd.DataFrame:
        """Get daily sales trends"""
        if self.sales_data.empty or 'sale_date' not in self.sales_data.columns:
            return pd.DataFrame()
        
        daily_trends = self.sales_data.groupby(
            self.sales_data['sale_date'].dt.date
        ).agg({
            'total_price': 'sum',
            'quantity': 'sum',
            'order_id': 'nunique'
        }).rename(columns={
            'total_price': 'daily_revenue',
            'order_id': 'daily_orders'
        })
        
        return daily_trends
    
    def get_category_analysis(self) -> pd.DataFrame:
        """Analyze sales by category (if category data is available)"""
        if self.sales_data.empty or 'category' not in self.sales_data.columns:
            return pd.DataFrame()
        
        category_analysis = self.sales_data.groupby('category').agg({
            'total_price': 'sum',
            'quantity': 'sum',
            'product_id': 'nunique'
        }).rename(columns={
            'product_id': 'unique_products',
            'total_price': 'category_revenue'
        }).sort_values('category_revenue', ascending=False)
        
        return category_analysis
    
    def get_sales_by_hour(self) -> pd.DataFrame:
        """Analyze sales by hour of day (if time data is available)"""
        if self.sales_data.empty or 'sale_date' not in self.sales_data.columns:
            return pd.DataFrame()
        
        # Extract hour if we have time information
        if pd.api.types.is_datetime64_any_dtype(self.sales_data['sale_date']):
            self.sales_data['hour'] = self.sales_data['sale_date'].dt.hour
            hourly_sales = self.sales_data.groupby('hour').agg({
                'total_price': 'sum',
                'quantity': 'sum',
                'order_id': 'nunique'
            }).rename(columns={
                'total_price': 'hourly_revenue',
                'order_id': 'hourly_orders'
            })
            return hourly_sales
        
        return pd.DataFrame()