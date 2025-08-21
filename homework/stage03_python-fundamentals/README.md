## Stage 03: Python Fundamentals — Exploratory Analysis and Summary

This component delivers a complete exploratory analysis workflow using NumPy and pandas. It contrasts loop-based execution with vectorized array operations, loads a starter dataset, produces descriptive and grouped summaries, saves artifacts for downstream use, and encapsulates reusable logic in a small utility function.

### Computation Modes (NumPy)
- Vectorized Operations:
  - Usage: Perform elementwise arithmetic (addition, subtraction, multiplication, division), comparisons, boolean masking, and basic reductions (sum/mean/std) on ndarrays.
  - Reasoning: Vectorization minimizes Python-level loops, leveraging optimized C backends for speed and clarity.
- Loop vs Vectorized Timing:
  - Usage: Compare execution time using a small benchmark (e.g., time.perf_counter or %timeit in the notebook) for a representative operation on large arrays.
  - Reasoning: Demonstrates the practical performance advantage and motivates consistent use of vectorized patterns.

### Dataset Loading
- Source:
  - Usage: Read the provided CSV file (data/starter_data.csv) via pandas, with robust handling of dtypes and optional date parsing (parse_dates for timestamp-like columns).
  - Reasoning: Ensures reliable ingestion and consistent typing across platforms and runs.
- Path Management:
  - Usage: Build file paths via pathlib.Path, rooted at the project’s data directory (e.g., DATA_DIR=./data from .env) to avoid hard-coded absolute paths.
  - Reasoning: Improves portability and keeps the notebook environment-agnostic.

### Summary Statistics and Grouped Aggregations
- Descriptive Statistics:
  - Usage: Use DataFrame.describe() to obtain count/mean/std/min/max and quantiles for numeric columns.
  - Reasoning: Provides a quick quantitative snapshot to validate ranges, spot anomalies, and guide preprocessing.
- Grouped Aggregations:
  - Usage: Apply groupby on a categorical key and compute aggregates (e.g., count, mean, sum, min, max) over relevant numeric features.
  - Reasoning: Surfaces segment-level patterns and supports targeted analysis.

### Outputs and Artifacts
- Summary Exports:
  - Usage: Persist the overall descriptive statistics and grouped summaries to data/processed/summary.csv (with optional JSON export for interchange).
  - Reasoning: Creates reproducible, shareable artifacts for downstream analysis and reporting.
- Optional Visualization:
  - Usage: Generate a basic plot (e.g., distribution or grouped bar) and save alongside outputs (e.g., plots/summary.png).
  - Reasoning: Offers a quick visual validation and improves interpretability.

### Reusable Utilities
- Utility Function:
  - Usage: Implement get_summary_stats(df) to compute and return key statistics; optionally place it in src/utils.py and import it into the notebook.
  - Reasoning: Encapsulates repeated logic, improves readability, and facilitates testing or reuse across notebooks.

### Validation
- Shape and Null Checks:
  - Usage: Confirm expected row/column counts after loading, and inspect null distributions (isna().sum()).
  - Reasoning: Guards against partial loads, encoding issues, or silent schema drift.
- Type Integrity:
  - Usage: Verify critical columns retain intended dtypes (e.g., numeric for measures, datetime for timestamp fields).
  - Reasoning: Prevents subtle calculation errors and ensures consistent aggregations.

### Notebook Execution
- Location:
  - Usage: notebooks/hw03_python_fundamentals.ipynb executes top-to-bottom without errors, producing the described artifacts in data/processed/.
  - Reasoning: Guarantees reproducibility and a clean audit trail of steps and outputs.