import pandas as pd
from pathlib import Path
import pickle
import argparse
from datetime import datetime # Import the datetime library

# Import our custom modules
from src.storage import read_df, write_df
from src.cleaning import drop_missing
from src.outliers import winsorize_df

# Import pipeline stage scripts
from scripts import eda, feature_engineering, modeling, evaluation, reporting

def parse_arguments():
    """
    Parses command-line arguments for the pipeline.
    """
    parser = argparse.ArgumentParser(description="Run the end-to-end financial data pipeline.")
    
    parser.add_argument(
        "--raw-data-path",
        type=Path,
        default=Path("project/data/raw/api_aapl.csv"),
        help="Path to the input raw data CSV file."
    )
    # Changed to accept a directory for processed data
    parser.add_argument(
        "--processed-data-dir",
        type=Path,
        default=Path("project/data/processed"),
        help="Directory to save the processed data with a timestamp."
    )
    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path("project/models/regression_model.pkl"),
        help="Path to save the trained regression model."
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=Path("project/reports"),
        help="Directory to save reports and figures."
    )
    
    return parser.parse_args()

def main():
    """
    Main function to run the end-to-end data processing and modeling pipeline.
    """
    args = parse_arguments()
    
    # --- Create a timestamp for unique output file names ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("--- Starting pipeline with the following configuration ---")
    print(f"Run timestamp: {timestamp}")
    print(f"Raw data: {args.raw_data_path}")
    print(f"Processed data output directory: {args.processed_data_dir}")
    print(f"Model output: {args.model_path}")
    print(f"Reports directory: {args.reports_dir}")
    print("----------------------------------------------------------")

    # --- Construct dynamic paths using the timestamp ---
    processed_filename = f"aapl_processed_{timestamp}.csv"
    PROCESSED_DATA_PATH = args.processed_data_dir / processed_filename
    FIGURES_DIR = args.reports_dir / "figures"
    EVALUATION_REPORT_PATH = args.reports_dir / "evaluation_metrics.txt"
    
    # --- Ensure output directories exist ---
    args.processed_data_dir.mkdir(parents=True, exist_ok=True)
    args.model_path.parent.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # --- 1. Load Data ---
    print(f"1. Loading data from {args.raw_data_path}...")
    if not args.raw_data_path.exists():
        print(f"Error: Input data file not found at {args.raw_data_path}")
        return
    df = read_df(args.raw_data_path)
    print("Data loaded successfully.")

    # --- 2. Data Cleaning & Outlier Handling ---
    print("2. Cleaning data and handling outliers...")
    df_clean = drop_missing(df)
    numeric_cols = df_clean.select_dtypes(include='number').columns
    df_winsorized = winsorize_df(df_clean, columns=numeric_cols, lower=0.01, upper=0.99)
    print("Cleaning and outlier handling complete.")

    # --- 3. Exploratory Data Analysis ---
    print("3. Generating EDA plots...")
    eda.run_eda(df_winsorized, FIGURES_DIR)
    print(f"EDA plots saved to {FIGURES_DIR}")

    # --- 4. Feature Engineering ---
    print("4. Creating new features...")
    df_featured = feature_engineering.create_features(df_winsorized)
    df_featured.dropna(inplace=True)
    print("Feature engineering complete.")
    
    # Save processed data with the timestamped filename
    write_df(df_featured, PROCESSED_DATA_PATH)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")

    # --- 5. Modeling ---
    print("5. Training regression model...")
    model, X_test, y_test, y_pred = modeling.train_regression_model(df_featured)
    print("Model training complete.")
    
    # Save the trained model
    with open(args.model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {args.model_path}")

    # --- 6. Evaluation ---
    print("6. Evaluating model performance...")
    evaluation.save_evaluation_metrics(y_test, y_pred, EVALUATION_REPORT_PATH)
    print(f"Evaluation report saved to {EVALUATION_REPORT_PATH}")

    # --- 7. Reporting ---
    print("7. Generating final report plots...")
    reporting.plot_predictions(y_test, y_pred, FIGURES_DIR)
    print(f"Prediction plot saved to {FIGURES_DIR}")

    print("--- Pipeline finished successfully ---")

if __name__ == "__main__":
    main()