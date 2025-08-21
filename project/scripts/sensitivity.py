from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from src.outliers import flag_outliers_df, winsorize_series

np.random.seed(17)

def ensure_dataset(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    x = np.linspace(0, 10, 200)
    y = 2.2 * x + 1 + np.random.normal(0, 1.2, size=x.size)
    y[10] += 15; y[120] -= 13; y[160] += 18
    df = pd.DataFrame({'x': x, 'y': y})
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df

def main():
    data_path = Path('data/raw/outliers_homework.csv')
    df = ensure_dataset(data_path)
    target_col = 'y' if 'y' in df.columns else df.select_dtypes(include='number').columns[0]

    df = flag_outliers_df(df, columns=[target_col], method="iqr", method_params={"k": 1.5})
    df = flag_outliers_df(df, columns=[target_col], method="zscore", method_params={"threshold": 3.0})

    pct_iqr = df[f'{target_col}_outlier_iqr'].mean() * 100
    pct_z = df[f'{target_col}_outlier_z'].mean() * 100
    print(f"Flagged (%): IQR={pct_iqr:.2f}%, Z={pct_z:.2f}%")

    plt.figure()
    plt.boxplot(df[target_col].dropna())
    plt.title(f'Boxplot: {target_col}')
    plt.tight_layout()
    plt.savefig('data/interim/boxplot.png')
    plt.close()

    plt.figure()
    plt.hist(df[target_col].dropna(), bins=30)
    plt.title(f'Histogram: {target_col}')
    plt.tight_layout()
    plt.savefig('data/interim/hist.png')
    plt.close()

    summ_all = df[target_col].describe()[['mean', '50%', 'std']].rename({'50%': 'median'})
    summ_filtered = df.loc[~df[f'{target_col}_outlier_iqr'], target_col].describe()[['mean', '50%', 'std']].rename({'50%': 'median'})
    w = winsorize_series(df[target_col], lower=0.05, upper=0.95)
    summ_w = w.describe()[['mean', '50%', 'std']].rename({'50%': 'median'})

    comp = pd.concat({'all': summ_all, 'filtered_iqr': summ_filtered, 'winsorized': summ_w}, axis=1)
    comp.to_csv('data/interim/sensitivity_summary.csv')
    print("Wrote data/interim/sensitivity_summary.csv")

    if 'x' in df.columns:
        X_all = df[['x']].to_numpy(); y_all = df[target_col].to_numpy()
        X_flt = df.loc[~df[f'{target_col}_outlier_iqr'], ['x']].to_numpy()
        y_flt = df.loc[~df[f'{target_col}_outlier_iqr'], target_col].to_numpy()

        model_all = LinearRegression().fit(X_all, y_all)
        model_flt = LinearRegression().fit(X_flt, y_flt)

        mae_all = mean_absolute_error(y_all, model_all.predict(X_all))
        mae_flt = mean_absolute_error(y_flt, model_flt.predict(X_flt))

        results = pd.DataFrame({
            'slope': [model_all.coef_[0], model_flt.coef_[0]],
            'intercept': [model_all.intercept_, model_flt.intercept_],
            'r2': [model_all.score(X_all, y_all), model_flt.score(X_flt, y_flt)],
            'mae': [mae_all, mae_flt]
        }, index=['all', 'filtered_iqr'])
        results.to_csv('data/interim/regression_comparison.csv')
        print("Wrote data/interim/regression_comparison.csv")
    else:
        print("No 'x' column; skipped regression comparison.")

if __name__ == "__main__":
    main()
