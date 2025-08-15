import pandas as pd
import os

file_path = '../data/test_data.csv'

df = pd.read_csv(file_path)

df.info()

df.head()

def get_summary_stats(dataframe):
    # 1. Get descriptive statistics
    numeric_summary = dataframe.describe()
    
    # 2. Get groupby aggregation
    category_summary = dataframe.groupby('category').agg(
        mean_price=('price', 'mean'),
        total_quantity_sold=('quantity_sold', 'sum'),
        average_rating=('rating', 'mean')).reset_index()
    
    return numeric_summary, category_summary