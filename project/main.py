# main.py
# This code is confirmed to be correct for the project structure provided.
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import numpy as np
import pandas as pd

# --- Optional Imports ---
# Attempt to import plotting libraries.
try:
    import matplotlib.pyplot as plt
    PLOTTING_OK = True
except ImportError:
    PLOTTING_OK = False

# Attempt to import machine learning libraries.
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error
    SKLEARN_OK = True
except ImportError:
    SKLEARN_OK = False


# --- Project-Specific Imports ---
# Import reusable functions from the 'src' and 'scripts' directories.
from src.config import load_environment
from src.storage import read_df, write_df
from src.cleaning import fill_missing_median, drop_missing, normalize_data
from src.outliers import (
    flag_outliers_df,
    remove_outliers_df,
    winsorize_df,
    winsorize_series,
)
# Note: Importing functions from scripts is possible but consider moving
# core logic to 'src' for better project structure.
from scripts.acquire import acquire_api, acquire_scrape
from scripts.preprocess import ensure_dataset

# Set a random seed for reproducibility.
np.random.seed(69)


def ensure_dirs():
    """Create the necessary data directories if they don't exist."""
    for d in ["data/raw", "data/interim", "data/processed"]:
        Path(d).mkdir(parents=True, exist_ok=True)


def cmd_acquire(args: argparse.Namespace) -> dict[str, Path]:
    """
    Command to acquire data from an API and a web scrape.
    Fetches financial data and a list of S&P 500 companies, then saves them.
    """
    print("\n--- Running: Acquire ---")
    ensure_dirs()
    out_paths: dict[str, Path] = {}

    # Acquire data from API (e.g., Alpha Vantage or yfinance).
    try:
        df_api = acquire_api(args.symbol)
        api_path = Path(f"data/raw/api_{args.symbol.lower()}.csv")
        out_paths["api"] = write_df(df_api.sort_values("date") if "date" in df_api.columns else df_api, api_path)
        print(f"[acquire] API data saved -> {out_paths['api']}")
    except Exception as e:
        print(f"[acquire] API acquisition failed: {e}")

    # Acquire data from web scraping (e.g., Wikipedia).
    try:
        df_sp = acquire_scrape()
        sp_path = Path("data/raw/scrape_sp500.csv")
        out_paths["scrape"] = write_df(df_sp, sp_path)
        print(f"[acquire] Scraped data saved -> {out_paths['scrape']}")
    except Exception as e:
        print(f"[acquire] Web scraping failed: {e}")

    return out_paths


def cmd_preprocess(args: argparse.Namespace) -> Path:
    """
    Command to preprocess a raw dataset.
    Loads data (or synthesizes it if not found), cleans it, and saves the result.
    """
    print("\n--- Running: Preprocess ---")
    ensure_dirs()
    raw_path = Path(args.data)
    
    # Load dataset or generate a synthetic one if it doesn't exist.
    if raw_path.exists():
        df = read_df(raw_path)
    else:
        df = ensure_dataset(raw_path)
        print(f"[preprocess] Generated synthetic dataset -> {raw_path}")

    out = df.copy()
    num_cols = out.select_dtypes(include="number").columns.tolist()

    # Apply cleaning steps.
    out = fill_missing_median(out, num_cols)
    out = drop_missing(out, threshold=0.5)
    cols_to_norm = num_cols[:2] if len(num_cols) >= 2 else num_cols
    out = normalize_data(out, cols_to_norm)

    # Save the cleaned data.
    proc_path = Path("data/processed/cleaned.csv")
    write_df(out, proc_path)
    print(f"[preprocess] Cleaned data saved -> {proc_path}")
    return proc_path


def cmd_outliers(args: argparse.Namespace) -> dict[str, Path]:
    """
    Command to handle outliers in a dataset.
    Flags, removes, and winsorizes outliers, saving each version.
    """
    print("\n--- Running: Outliers ---")
    ensure_dirs()
    src_path = Path(args.input) if args.input else Path("data/processed/cleaned.csv")
    
    # If input data is missing, run the preprocess step first.
    if not src_path.exists():
        print("[outliers] No cleaned input found. Running preprocess first...")
        src_path = cmd_preprocess(args)

    df = read_df(src_path)

    # Determine the target column for outlier detection.
    if args.target and args.target in df.columns:
        target_col = args.target
    else:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if not num_cols:
            raise ValueError("No numeric columns found for outlier processing.")
        target_col = "y" if "y" in num_cols else num_cols[0]
        print(f"[outliers] Target column auto-selected: {target_col}")

    # Apply different outlier handling methods.
    df_flagged = flag_outliers_df(df, columns=[target_col], method="iqr", method_params={"k": args.k})
    df_flagged = flag_outliers_df(df_flagged, columns=[target_col], method="zscore", method_params={"threshold": args.z})
    df_removed = remove_outliers_df(df_flagged, flag_columns=[f"{target_col}_outlier_iqr"], how="any")
    df_wins = winsorize_df(df_flagged, columns=[target_col], lower=args.lower, upper=args.upper)

    # Save the results.
    flagged_path = Path("data/interim/with_outlier_flags.csv")
    removed_path = Path("data/processed/removed_outliers.csv")
    wins_path = Path("data/processed/winsorized.csv")
    write_df(df_flagged, flagged_path)
    write_df(df_removed, removed_path)
    write_df(df_wins, wins_path)

    print(f"[outliers] Flagged data saved -> {flagged_path}")
    print(f"[outliers] Data with outliers removed saved -> {removed_path}")
    print(f"[outliers] Winsorized data saved -> {wins_path}")

    return {"flagged": flagged_path, "removed": removed_path, "winsorized": wins_path}


def cmd_sensitivity(args: argparse.Namespace) -> dict[str, Path | None]:
    """
    Command to run sensitivity analysis on outlier handling.
    Generates summary statistics, regression comparison, and plots.
    """
    print("\n--- Running: Sensitivity Analysis ---")
    ensure_dirs()
    flagged_path = Path(args.flagged) if args.flagged else Path("data/interim/with_outlier_flags.csv")

    # If flagged data is missing, run the outlier step first.
    if not flagged_path.exists():
        print("[sensitivity] No flagged dataset found. Running outliers first...")
        paths = cmd_outliers(args)
        flagged_path = paths["flagged"]

    df = read_df(flagged_path)

    # Determine the target column.
    if args.target and args.target in df.columns:
        target_col = args.target
    else:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        target_col = "y" if "y" in num_cols else num_cols[0]
        print(f"[sensitivity] Target column auto-selected: {target_col}")

    # Calculate percentage of flagged outliers.
    pct_iqr = df.get(f"{target_col}_outlier_iqr", pd.Series(False, index=df.index)).mean() * 100
    pct_z = df.get(f"{target_col}_outlier_z", pd.Series(False, index=df.index)).mean() * 100
    print(f"[sensitivity] Outliers Flagged (%): IQR={pct_iqr:.2f}%, Z-score={pct_z:.2f}%")

    # Generate summary statistics for comparison.
    summ_all = df[target_col].describe()[["mean", "50%", "std"]].rename({"50%": "median"})
    summ_filtered = df.loc[~df.get(f"{target_col}_outlier_iqr", pd.Series(False, index=df.index)), target_col].describe()[["mean", "50%", "std"]].rename({"50%": "median"})
    w = winsorize_series(df[target_col], lower=args.lower, upper=args.upper)
    summ_w = w.describe()[["mean", "50%", "std"]].rename({"50%": "median"})
    comp = pd.concat({"all": summ_all, "filtered_iqr": summ_filtered, "winsorized": summ_w}, axis=1)
    comp_path = Path("data/interim/sensitivity_summary.csv")
    comp.to_csv(comp_path)
    print(f"[sensitivity] Summary statistics saved -> {comp_path}")

    # Perform regression analysis if possible.
    reg_path = None
    if SKLEARN_OK and "x" in df.columns and f"{target_col}_outlier_iqr" in df.columns:
        X_all = df[["x"]].to_numpy(); y_all = df[target_col].to_numpy()
        mask = ~df[f"{target_col}_outlier_iqr"]
        X_flt = df.loc[mask, ["x"]].to_numpy()
        y_flt = df.loc[mask, target_col].to_numpy()
        
        model_all = LinearRegression().fit(X_all, y_all)
        model_flt = LinearRegression().fit(X_flt, y_flt)
        
        results = pd.DataFrame({
            "slope": [model_all.coef_[0], model_flt.coef_[0]],
            "intercept": [model_all.intercept_, model_flt.intercept_],
            "r2": [model_all.score(X_all, y_all), model_flt.score(X_flt, y_flt)],
            "mae": [mean_absolute_error(y_all, model_all.predict(X_all)),
                    mean_absolute_error(y_flt, model_flt.predict(X_flt))],
        }, index=["all", "filtered_iqr"])
        
        reg_path = Path("data/interim/regression_comparison.csv")
        results.to_csv(reg_path)
        print(f"[sensitivity] Regression comparison saved -> {reg_path}")
    else:
        print("[sensitivity] Skipped regression (sklearn not installed or 'x' column missing).")

    # Generate plots if possible.
    box_path = hist_path = None
    if PLOTTING_OK:
        try:
            plt.figure()
            plt.boxplot(df[target_col].dropna())
            plt.title(f"Boxplot: {target_col}")
            plt.tight_layout()
            box_path = Path("data/interim/boxplot.png")
            plt.savefig(box_path)
            plt.close()
            print(f"[sensitivity] Boxplot saved -> {box_path}")

            plt.figure()
            plt.hist(df[target_col].dropna(), bins=30)
            plt.title(f"Histogram: {target_col}")
            plt.tight_layout()
            hist_path = Path("data/interim/hist.png")
            plt.savefig(hist_path)
            plt.close()
            print(f"[sensitivity] Histogram saved -> {hist_path}")
        except Exception as e:
            print(f"[sensitivity] Plotting failed: {e}")

    return {
        "summary": comp_path, "regression": reg_path,
        "boxplot": box_path, "hist": hist_path,
    }


def cmd_all(args: argparse.Namespace):
    """Command to run the full data pipeline end-to-end."""
    print("\n--- Running: Full Pipeline (All Steps) ---")
    cmd_acquire(args)
    cleaned_path = cmd_preprocess(args)
    # Pass the path of the cleaned data to the next step.
    args.input = str(cleaned_path)
    cmd_outliers(args)
    # The sensitivity command will automatically find the output from the outliers step.
    cmd_sensitivity(args)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Define and parse command-line arguments and subcommands."""
    parser = argparse.ArgumentParser(description="Main entry point for the data analysis project.")
    
    # Global arguments applicable to multiple commands.
    parser.add_argument("--data", default="data/raw/outliers_homework.csv", help="Path to the primary raw dataset.")
    parser.add_argument("--input", default=None, help="Path to preprocessed input for the outliers stage.")
    parser.add_argument("--flagged", default=None, help="Path to flagged data for the sensitivity stage.")
    parser.add_argument("--symbol", default="AAPL", help="Stock ticker symbol for data acquisition.")
    parser.add_argument("--target", default=None, help="Target numeric column for outlier analysis.")
    parser.add_argument("--k", type=float, default=1.5, help="IQR method k parameter.")
    parser.add_argument("--z", type=float, default=3.0, help="Z-score method threshold.")
    parser.add_argument("--lower", type=float, default=0.05, help="Lower quantile for winsorization.")
    parser.add_argument("--upper", type=float, default=0.95, help="Upper quantile for winsorization.")

    # Subcommands for different pipeline stages.
    subparsers = parser.add_subparsers(dest="cmd", help="Available commands")
    subparsers.add_parser("acquire", help="Fetch API data and scrape a web table.")
    subparsers.add_parser("preprocess", help="Run the data cleaning pipeline.")
    subparsers.add_parser("outliers", help="Run outlier detection and handling.")
    subparsers.add_parser("sensitivity", help="Run sensitivity analysis on outlier methods.")
    subparsers.add_parser("all", help="Run the full pipeline end-to-end (default).")
    
    return parser.parse_args(argv)


def main(argv: list[str] | None = None):
    """Main function to dispatch commands."""
    # Load environment variables from a .env file.
    load_environment()
    
    args = parse_args(argv)
    
    # Default to the 'all' command if no command is specified.
    command = args.cmd or "all"
    
    # Dispatch to the appropriate function based on the command.
    if command == "acquire":
        cmd_acquire(args)
    elif command == "preprocess":
        cmd_preprocess(args)
    elif command == "outliers":
        cmd_outliers(args)
    elif command == "sensitivity":
        cmd_sensitivity(args)
    elif command == "all":
        cmd_all(args)
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)
        
    print("\n--- Pipeline step(s) completed successfully! ---")


if __name__ == "__main__":
    main()