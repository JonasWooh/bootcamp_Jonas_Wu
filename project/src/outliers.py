from __future__ import annotations
from typing import Iterable, Dict, Optional, Literal
import numpy as np
import pandas as pd

OutlierMethod = Literal["iqr", "zscore"]
HandleMode = Literal["flag", "remove", "winsorize", "none"]

__all__ = [
    "detect_outliers_iqr",
    "detect_outliers_zscore",
    "winsorize_series",
    "flag_outliers_df",
    "remove_outliers_df",
    "winsorize_df",
]

def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    s = series.dropna()
    if s.empty:
        return pd.Series(False, index=series.index)
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    mask = (series < lower) | (series > upper)
    return mask.fillna(False)

def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    mu = series.mean(skipna=True)
    sigma = series.std(ddof=0, skipna=True)
    if sigma == 0 or np.isnan(sigma):
        return pd.Series(False, index=series.index)
    z = (series - mu) / sigma
    mask = z.abs() > threshold
    return mask.fillna(False)

def winsorize_series(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    if series.dropna().empty:
        return series
    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lower=lo, upper=hi)

def flag_outliers_df(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    method: OutlierMethod = "iqr",
    method_params: Optional[Dict] = None,
    flag_suffix: Optional[str] = None,
) -> pd.DataFrame:
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    method_params = method_params or {}
    out = df.copy()
    for col in columns:
        if not pd.api.types.is_numeric_dtype(out[col]):
            continue
        if method == "iqr":
            mask = detect_outliers_iqr(out[col], **method_params)
            suffix = flag_suffix or "outlier_iqr"
        elif method == "zscore":
            mask = detect_outliers_zscore(out[col], **method_params)
            suffix = flag_suffix or "outlier_z"
        else:
            raise ValueError(f"Unsupported method: {method}")
        out[f"{col}_{suffix}"] = mask
    return out

def remove_outliers_df(
    df: pd.DataFrame,
    flag_columns: Optional[Iterable[str]] = None,
    how: Literal["any", "all"] = "any",
) -> pd.DataFrame:
    if flag_columns is None:
        flag_columns = [c for c in df.columns if "outlier" in c]
    if not flag_columns:
        return df.copy()
    mask = df[flag_columns].any(axis=1) if how == "any" else df[flag_columns].all(axis=1)
    return df.loc[~mask].copy()

def winsorize_df(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    lower: float = 0.05,
    upper: float = 0.95,
) -> pd.DataFrame:
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    out = df.copy()
    for col in columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = winsorize_series(out[col], lower=lower, upper=upper)
    return out
