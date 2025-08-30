import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Corrected function definition to accept two arguments
def run_eda(df: pd.DataFrame, output_dir: Path):
    """
    Generates and saves EDA plots to the specified directory.
    """
    sns.set(context='talk', style='whitegrid')
    
    # Plot 1: Close Price History
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='date', y='close')
    plt.title('AAPL Close Price History')
    plt.ylabel('Close Price (USD)')
    plt.xlabel('Date')
    plt.savefig(output_dir / 'eda_close_price.png', dpi=300)
    plt.close()

    # Plot 2: Daily Return Distribution
    # This check ensures the column exists before trying to plot it.
    if 'daily_return' not in df.columns:
        df['daily_return'] = df['close'].pct_change()
        
    plt.figure(figsize=(12, 6))
    sns.histplot(df['daily_return'].dropna(), kde=True, bins=100)
    plt.title('Distribution of Daily Returns')
    plt.xlabel('Daily Return')
    plt.savefig(output_dir / 'eda_daily_returns.png', dpi=300)
    plt.close()