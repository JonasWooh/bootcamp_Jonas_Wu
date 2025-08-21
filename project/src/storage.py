from __future__ import annotations
import pandas as pd
from pathlib import Path

def detect_format(path: str | Path) -> str:
    ext = str(path).lower().rsplit('.', 1)[-1]
    if ext in ('csv', 'parquet'):
        return ext
    raise ValueError(f'Unsupported file extension: {ext}')

def write_df(df: pd.DataFrame, path: str | Path) -> Path:
    path = Path(path)
    fmt = detect_format(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == 'csv':
        df.to_csv(path, index=False)
        return path
    elif fmt == 'parquet':
        try:
            df.to_parquet(path, index=False)
        except Exception:
            fallback = path.with_suffix('.csv')
            df.to_csv(fallback, index=False)
            return fallback
        return path
    else:
        raise ValueError(f'Unsupported format: {fmt}')

def read_df(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    fmt = detect_format(path)
    if fmt == 'csv':
        df = pd.read_csv(path)
        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'])
            except Exception:
                pass
        return df
    elif fmt == 'parquet':
        return pd.read_parquet(path)
    else:
        raise ValueError(f'Unsupported format: {fmt}')
