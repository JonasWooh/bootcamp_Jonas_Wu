from __future__ import annotations
import pandas as pd
import numpy as np
from typing import Iterable

def fill_missing_median(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns and pd.api.types.is_numeric_dtype(out[c]):
            med = out[c].median()
            out[c] = out[c].fillna(med)
    return out

def drop_missing(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    out = df.copy()
    # drop columns above threshold missing
    col_missing = out.isna().mean()
    to_drop = [c for c, r in col_missing.items() if r > threshold]
    if to_drop:
        out = out.drop(columns=to_drop)
    # drop remaining rows with any missing
    out = out.dropna(axis=0, how='any')
    return out

def normalize_data(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns and pd.api.types.is_numeric_dtype(out[c]):
            mu = out[c].mean()
            sigma = out[c].std(ddof=0)
            if sigma and not np.isnan(sigma) and sigma != 0:
                out[c] = (out[c] - mu) / sigma
    return out
