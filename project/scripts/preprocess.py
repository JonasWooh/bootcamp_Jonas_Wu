from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from src.outliers import flag_outliers_df, remove_outliers_df, winsorize_df

def ensure_dataset(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    # Fallback synthetic linear dataset with extremes
    x = np.linspace(0, 10, 200)
    y = 2.2 * x + 1 + np.random.normal(0, 1.2, size=x.size)
    y[10] += 15; y[120] -= 13; y[160] += 18
    df = pd.DataFrame({'x': x, 'y': y})
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df

def main():
    raw_path = Path("data/raw/outliers_homework.csv")
    df = ensure_dataset(raw_path)

    num_cols = df.select_dtypes(include='number').columns.tolist()
    if not num_cols:
        raise ValueError("No numeric columns found for outlier processing.")
    target_col = 'y' if 'y' in df.columns else num_cols[0]

    df_flagged = flag_outliers_df(df, columns=[target_col], method="iqr", method_params={"k": 1.5})

    df_removed = remove_outliers_df(df_flagged, flag_columns=[f"{target_col}_outlier_iqr"], how="any")
    df_wins = winsorize_df(df_flagged, columns=[target_col], lower=0.05, upper=0.95)

    Path("data/interim").mkdir(parents=True, exist_ok=True)
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    df_flagged.to_csv("data/interim/with_outlier_flags.csv", index=False)
    df_removed.to_csv("data/processed/removed_outliers.csv", index=False)
    df_wins.to_csv("data/processed/winsorized.csv", index=False)

    print("Wrote data/interim/with_outlier_flags.csv")
    print("Wrote data/processed/removed_outliers.csv")
    print("Wrote data/processed/winsorized.csv")

if __name__ == "__main__":
    main()
