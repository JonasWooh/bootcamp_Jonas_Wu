## Stage 06: Data Preprocessing — Cleaning Pipeline and Documentation

This component implements a modular data-cleaning pipeline with clearly scoped functions for imputation, missing-data handling, and feature scaling. The workflow is applied to the raw dataset, produces a processed artifact, and documents all assumptions and trade-offs.

### Cleaning Functions (src/cleaning.py)
- fill_missing_median()
  - Usage: Impute missing values in numeric columns with the median computed from the column (optionally by group if a grouping key is provided).
  - Reasoning: Median imputation is robust to outliers and preserves central tendency better than mean for skewed distributions.
- drop_missing()
  - Usage: Drop rows (or columns, configurable) that exceed a missingness threshold; supports a strict mode to remove rows with any NA in required fields.
  - Reasoning: Prevents excessive imputation, keeps critical fields reliable, and simplifies downstream models.
- normalize_data()
  - Usage: Apply feature scaling (e.g., z-score standardization or min–max normalization) to selected numeric columns while excluding identifiers and categorical keys.
  - Reasoning: Puts features on comparable scales, stabilizing optimization and improving model performance.

### Pipeline Workflow
- Loading:
  - Usage: Read the raw source from data/raw/ using pandas, with explicit dtype specifications and optional parse_dates.
  - Reasoning: Ensures consistent schema and a stable foundation for transformations.
- Transformation Sequence:
  - Usage: Apply fill_missing_median() → drop_missing() → normalize_data() in a deterministic order; persist intermediate checkpoints if needed for debugging.
  - Reasoning: Impute before dropping to minimize data loss, then bring features to a consistent scale for analysis.
- Saving:
  - Usage: Write the final cleaned dataset to data/processed/ in Parquet format (preferred) or CSV as required by downstream tools.
  - Reasoning: Parquet provides efficient columnar storage, compression, and dtype fidelity; CSV maintains broad compatibility.

### Environment-Driven Configuration
- Path Management:
  - Usage: Read directories from .env (e.g., DATA_DIR_RAW=data/raw and DATA_DIR_PROCESSED=data/processed) via python-dotenv, constructed with pathlib.
  - Reasoning: Avoids hard-coded paths, enabling the same code to run across machines and CI environments without edits.

### Assumptions and Exclusions
- Feature Scope:
  - Usage: Only numeric columns are imputed/scaled; ID fields, categorical codes, and datetime columns are excluded from normalization.
  - Reasoning: Prevents semantic distortion of identifiers and preserves temporal semantics.
- Thresholds and Policies:
  - Usage: Missingness thresholds and scaling method are configurable parameters with documented defaults; decisions are recorded in the notebook.
  - Reasoning: Makes trade-offs explicit and reproducible for future reviewers.

### Validation and Comparisons
- Shape and Completeness:
  - Usage: Compare original vs. cleaned row/column counts and confirm null counts are reduced or eliminated as intended.
  - Reasoning: Ensures the pipeline achieves its cleaning objectives without unintended data loss.
- Statistical Checks:
  - Usage: Inspect distributions pre/post normalization (means ~0, std ~1 for z-score; min/max within [0,1] for min–max).
  - Reasoning: Verifies scaling correctness and guards against leakage or mis-specification.
- Schema and Dtypes:
  - Usage: Confirm critical columns retain expected data types after the full transform/save/reload cycle.
  - Reasoning: Protects downstream code from type-related failures.

### Artifacts and Documentation
- Notebook:
  - Usage: A preprocessing notebook demonstrates the full pipeline, records assumptions, and shows side-by-side comparisons of original vs. cleaned data.
  - Reasoning: Provides a transparent, reproducible narrative of the decisions and their effects.
- Outputs:
  - Usage: Cleaned dataset saved to data/processed/, with log-like notes or metadata (e.g., parameters and timestamp) captured alongside the artifact.
  - Reasoning: Facilitates downstream consumption and auditability across iterations.