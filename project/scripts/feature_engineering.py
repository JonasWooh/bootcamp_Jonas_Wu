import pandas as pd

def create_features(df):
    df['daily_return'] = df['close'].pct_change()
    df['rolling_avg_5d_close'] = df['close'].rolling(window=5).mean()
    df['rolling_vol_5d'] = df['daily_return'].rolling(window=5).std()
    return df
