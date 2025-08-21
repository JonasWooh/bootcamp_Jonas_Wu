import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def fill_missing_median(df, columns):

    df_cleaned = df.copy()
    for col in columns:
        if col in df_cleaned.columns and pd.api.types.is_numeric_dtype(df_cleaned[col]):
            median_val = df_cleaned[col].median()
            df_cleaned[col] = df_cleaned[col].fillna(median_val)
    return df_cleaned

def drop_missing(df, threshold=0.5):

    df_cleaned = df.copy()

    # Drop columns with missing value proportion above threshold
    initial_cols = df_cleaned.shape[1]
    cols_to_drop = [col for col in df_cleaned.columns if df_cleaned[col].isnull().sum() / len(df_cleaned) > threshold]
    df_cleaned = df_cleaned.drop(columns=cols_to_drop)
    print(f"Dropped {len(cols_to_drop)} columns due to more than {threshold*100}% missing values.")

    # Drop any remaining rows with missing values
    initial_rows = df_cleaned.shape[0]
    df_cleaned = df_cleaned.dropna()
    print(f"Dropped {initial_rows - df_cleaned.shape[0]} rows due to remaining missing values.")

    return df_cleaned

def normalize_data(df, columns, method='minmax'):

    df_normalized = df.copy()
    
    if method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'standard':
        scaler = StandardScaler()
    else:
        raise ValueError("Method must be 'minmax' or 'standard'.")

    for col in columns:
        if col in df_normalized.columns and pd.api.types.is_numeric_dtype(df_normalized[col]):
            # Reshape the column for the scaler (expects 2D array)
            df_normalized[col] = scaler.fit_transform(df_normalized[[col]])
        else:
            print(f"Warning: Column '{col}' not found or not numeric. Skipping normalization for this column.")
            
    return df_normalized
