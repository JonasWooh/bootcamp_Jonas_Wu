# Financial Engineering Project

## Overview
This project provides a comprehensive, end-to-end pipeline for financial analysis, including data acquisition, preprocessing, feature engineering, modeling, evaluation, and productization.

## Project Structure
- `data/`: Raw, interim, and processed datasets
- `src/`: Reusable Python modules for core logic (e.g., cleaning, outlier detection)
- `scripts/`: Standalone Python scripts for pipeline stages (e.g., data acquisition, EDA)
- `notebooks/`: Jupyter notebooks for exploratory analysis and prototyping
- `models/`: Trained and serialized models (e.g., `model.pkl`)
- `reports/`: Generated reports and figures
- `app.py`: Flask application for model deployment

## Quickstart
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` (and optionally set `ALPHAVANTAGE_API_KEY`)
4. `python main.py` to run the full pipeline.

