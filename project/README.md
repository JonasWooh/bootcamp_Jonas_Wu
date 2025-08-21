# Outlier Analysis Project

## Overview
A small end-to-end pipeline integrating data acquisition, storage, preprocessing, and explicit outlier management with sensitivity analysis.

## Structure
- data/{raw,interim,processed}
- src/{config.py,storage.py,cleaning.py,outliers.py}
- scripts/{acquire.py,preprocess.py,sensitivity.py}
- docs/outliers.md
- notebooks/ (optional for visual analysis)

## Quickstart
1) python -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) cp .env.example .env  # optionally set ALPHAVANTAGE_API_KEY
4) python scripts/acquire.py  # optional: pull sample API/scrape data
5) python scripts/preprocess.py  # outlier flag/remove/winsorize
6) python scripts/sensitivity.py  # generate summary and plots

## Notes
- If data/raw/outliers_homework.csv doesn't exist, scripts will generate a synthetic dataset.
- Parquet writing gracefully falls back to CSV if engine is unavailable.
