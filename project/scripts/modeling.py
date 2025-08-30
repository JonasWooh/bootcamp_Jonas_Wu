import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

def train_regression_model(df: pd.DataFrame):
    """
    Trains a linear regression model to predict the next day's return.
    
    Returns:
        - Trained model object (lr)
        - X_test (features for the test set)
        - y_test (true target values for the test set)
        - y_pred (predicted values for the test set)
    """
    # Target variable is the next day's return
    if 'daily_return' not in df.columns:
        df['daily_return'] = df['close'].pct_change()
    
    y = df['daily_return'].shift(-1)
    
    # Define features to be used for modeling
    features = [col for col in ['open', 'high', 'low', 'close', 'volume', 'daily_return', 'rolling_avg_5d_close', 'rolling_vol_5d'] if col in df.columns]
    X = df[features]
    
    # Align X and y by concatenating and dropping rows with NaNs
    # This is crucial for time series data
    combined = pd.concat([y.rename('target_return'), X], axis=1)
    combined.dropna(inplace=True)
    
    y_aligned = combined['target_return']
    X_aligned = combined.drop(columns='target_return')
    
    # Split data chronologically for time series analysis
    X_train, X_test, y_train, y_test = train_test_split(X_aligned, y_aligned, test_size=0.2, shuffle=False)
    
    # Train the model
    lr = LinearRegression().fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = lr.predict(X_test)
    
    # Print baseline metrics
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f'Baseline (predicting returns)   R²={r2:.4f}  RMSE={rmse:.6f}')
    
    # Ensure four values are returned
    return lr, X_test, y_test, y_pred