import pandas as pd

def get_summary_stats(dataframe):
    # 1. Get descriptive statistics
    numeric_summary = dataframe.describe()
    
    # 2. Get groupby aggregation
    category_summary = dataframe.groupby('category').agg(
        mean_value=('value', 'mean'),
        sum_value=('value', 'sum')).reset_index()
    
    return numeric_summary, category_summary