# src/utils.py
import pandas as pd

def summarize_data(data):
    """
    Generates a descriptive summary of a DataFrame.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    return data.describe()

def preprocess_features(feature_list):
    """
    A mock preprocessing function. In a real scenario, this would
    handle scaling, encoding, etc.
    """
    print("Preprocessing features...")
    return feature_list