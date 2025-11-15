import pandas as pd
import os
import glob
from typing import List, Dict, Any

class DataLoader:
    def __init__(self, data_folder: str = "sales_data"):
        self.data_folder = data_folder
        self.sales_data = None
        
    def load_sales_files(self) -> pd.DataFrame:
        """Load and combine all sales CSV files from the data folder"""
        try:
            # Create data folder if it doesn't exist
            if not os.path.exists(self.data_folder):
                os.makedirs(self.data_folder)
                print(f"Created {self.data_folder} folder. Please add your sales CSV files there.")
                return pd.DataFrame()
            
            # Find all sales CSV files
            pattern = os.path.join(self.data_folder, "sales_*.csv")
            sales_files = glob.glob(pattern)
            
            if not sales_files:
                print("No sales files found. Please add sales_YYYY-MM-DD.csv files to the sales_data folder.")
                return pd.DataFrame()
            
            # Load and combine all files
            data_frames = []
            for file_path in sales_files:
                try:
                    df = pd.read_csv(file_path)
                    df['file_source'] = os.path.basename(file_path)
                    data_frames.append(df)
                    print(f"Loaded: {os.path.basename(file_path)} - {len(df)} records")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    continue
            
            if not data_frames:
                raise ValueError("No valid sales files could be loaded")
            
            # Combine all data
            self.sales_data = pd.concat(data_frames, ignore_index=True)
            
            # Data cleaning and preprocessing
            self.sales_data = self._clean_data(self.sales_data)
            
            print(f"Successfully loaded {len(self.sales_data)} total records from {len(sales_files)} files")
            return self.sales_data
            
        except Exception as e:
            print(f"Error loading sales data: {e}")
            return pd.DataFrame()
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the sales data"""
        # Create a copy to avoid modifying the original
        df_clean = df.copy()
        
        # Convert date columns to datetime
        date_columns = ['sale_date', 'order_date', 'date']
        for col in date_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                break
        else:
            # If no date column found, create one from filename
            df_clean['sale_date'] = pd.to_datetime(
                df_clean['file_source'].str.extract(r'sales_(\d{4}-\d{2}-\d{2})')[0],
                errors='coerce'
            )
        
        # Ensure numeric columns are properly typed
        numeric_columns = ['quantity', 'price', 'total_price', 'revenue', 'amount']
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Fill missing numeric values with 0
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col].fillna(0, inplace=True)
        
        # Remove rows with critical missing data
        critical_columns = ['product_id', 'product_name']
        for col in critical_columns:
            if col in df_clean.columns:
                df_clean = df_clean.dropna(subset=[col])
        
        return df_clean
    
    def get_sales_data(self) -> pd.DataFrame:
        """Get the loaded sales data"""
        if self.sales_data is None:
            self.load_sales_files()
        return self.sales_data