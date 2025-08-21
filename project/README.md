# Project Title: Recommendation Engine for Customer Retention

**Stage:** Problem Framing & Scoping (Stage 01) 

## Problem Statement
The goal of this project is to address the core challenges of new customer guidance and existing customer retention for businesses in the service (mainly food service) industry. New customers often feel overwhelmed by unfamiliar menus, while returning customers may miss new items they would enjoy. Both scenarios lead to potential lost sales and decreased customer satisfaction. Businesses generally lack a data-driven tool to optimize the customer's ordering experience to increase sales and loyalty. 

## Stakeholder & User
The primary decision-maker is the restaurant/cafe owner or manager. They will use the insights to decide on weekly specials, promotional combos, and targeted marketing efforts. The end-users are the customers (both new and returning) who receive the recommendations to enhance their dining experience.

## Useful Answer & Decision
A useful answer is a hybrid system:

**Descriptive:** For new customers, a ranked list of "Most Popular Items" or "Frequently Paired Items".

**Predictive:** For returning customers, a list of personalized recommendations based on their order history from other places.

The final artifact will be code containing the analysis and model prototype, accompanied by a summary report. This will help the owner decide which items to promote to drive sales.

## Assumptions & Constraints
**Assumption:** 
* Historical transaction data, including customer IDs (or a proxy like a loyalty card number) and items purchased, is available and accessible.
* Item popularity is a reasonably good indicator of quality and a safe recommendation for new customers.

**Constraint:** 
* This project will deliver a proof-of-concept prototype, not a real-time, production-ready application.
* The analysis will be based on past data and may not account for sudden changes in customer taste or seasonal trends. 

## Known Unknowns / Risks
**Risk:** 
* The quality of the transaction data may be poor (inconsistent item names, missing entries), requiring significant time for cleaning.
* The dataset may not be large enough to generate statistically significant personalized recommendations.

**Mitigation:** 
* We will perform thorough Exploratory Data Analysis to assess data quality and sparsity. If personalization is not feasible, the project will focus on robust descriptive recommendations for all users, try to find a more "neutral" sulution. 

## Lifecycle Mapping
| Goal | Stage & Deliverable |
| :--- | :--- |
| **Define the project scope, stakeholders, and success criteria.** | **Stage 01: Problem Framing & Scoping** <br>  Deliverable: A detailed `README.md` file and a Stakeholder Memo. |
| **Collect, clean, and understand the transaction data; identify patterns and limitations.** | **Stage 02: Data Exploration & Preparation** <br>  Deliverable: An Exploratory Data Analysis (EDA) Jupyter Notebook with key visualizations (something like, item popularity charts, sales trends) and a data quality assessment. |
| **Develop recommendation logic for both new and returning customers.** | **Stage 03: Modeling & Analysis** <br>  Deliverable: A modeling Jupyter Notebook containing code for both: (1) The descriptive model for new customers (for example, top-N popular items) and (2) The predictive model for returning customers (like collaborative filtering). |
| **Assess the model's effectiveness and the business relevance of the recommendations.** | **Stage 04: Evaluation** <br>  Deliverable: An evaluation section within the modeling notebook, including offline metrics for the predictive model and a qualitative analysis of the recommendations. |
| **Collect all findings into a clear, actionable report for the stakeholder.** | **Stage 05: Reporting & Delivery** <br>  Deliverable: A final summary report for the business owner, explaining the findings and business suggestions in non-technical terms. A clean, well-commented final version of the project notebook. |
## Repo Plan
* **/data/:** Raw and processed datasets.
* **/notebooks/:** Jupyter Notebooks(.ipynb) for analysis, modeling, and exploration.
* **/src/:** Reusable Python functions and classes.
* **/docs/:** Project documentation, including the stakeholder memo and final report.
* **Cadence:** The repo will be updated at the end of each major stage of the project lifecycle.

## Stage 02: Tooling Setup — Reproducible Project Scaffold

This repository implements a clean, reproducible Python project scaffold with isolated environments, environment-driven configuration, a verification notebook, and an initialized GitHub remote, following the Stage 02 assignment guidelines [1].

### Environment Setup
- Usage: Create a dedicated Python 3.11 environment (conda or venv) and install base packages (python-dotenv, numpy, jupyter).
- Reasoning: Isolation prevents dependency conflicts and ensures experiments are reproducible across machines.

### Project Structure
- Usage: Organize source and assets under a minimal, conventional layout:
  - data/
  - notebooks/
  - src/
  - README.md, .gitignore
- Reasoning: Consistent structure accelerates onboarding and keeps code, notebooks, and data clearly separated.

### Secrets Management (.env)
- Usage: Provide `.env.example` and copy to `.env` with:
  - API_KEY=dummy_key_123
  - DATA_DIR=./data
- Reasoning: Environment variables keep secrets and paths out of code and version control while remaining easy to configure.

### Configuration Helper (src/config.py)
- Usage: Implement load_env() to load variables from `.env` and get_key() to read environment values at runtime.
- Reasoning: Centralized configuration access reduces boilerplate and avoids hard-coded constants.

### Jupyter Verification
- Usage: Add notebooks/00_project_setup.ipynb with:
  - A short “Environment & Config Check” section,
  - Code to load `.env` and confirm the presence of `API_KEY`,
  - A simple NumPy demonstration (e.g., small array operation).
- Reasoning: Provides a quick, executable sanity check that the environment and configuration are wired correctly (“API_KEY present: True”).

### Dependency Lockfile
- Usage: Export a lockfile with `pip freeze > requirements.txt`.
- Reasoning: Captures exact versions to reproduce the environment in CI or on collaborator machines.

### Version Control & Remote
- Usage: Initialize Git, make initial commits, add a remote, and push to GitHub; ensure `.env` (and optionally `/data/`) is listed in `.gitignore`.
- Reasoning: Establishes history, enables collaboration, and protects sensitive files from being committed.

### Reproducibility & Validation
- Environment: New machine can recreate the environment from requirements.txt.
- Configuration: `.env` provides portable, non-hard-coded paths and keys; config helper reads them in code.
- Notebook: Runs top-to-bottom without errors and prints the expected checks.
- Repository: Clear initial commits with a tidy scaffold and documentation.

### Submission
- Usage: Share the GitHub repository URL per the assignment instructions. [1]
- Reasoning: Allows reviewers to verify structure, notebook execution, and version history.

### Integrity & Hygiene
- Do not commit real secrets; only dummy keys in examples.
- Keep notebooks executable from top to bottom and avoid side effects beyond the project workspace.

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


## Stage 05: Data Storage

This project utilizes a structured approach to data storage, managing file paths with environment variables and leveraging both CSV and Parquet formats to separate raw from processed data. This ensures portability and efficiency.

### Folder Structure

The project's data is organized into the following directories:

-   `data/raw/`: This directory holds original, immutable data. In this assignment, the initial stock data is loaded from this location, and any new raw files are saved here as CSVs.
-   `data/processed/`: This directory is for cleaned, transformed, or optimized data. Processed DataFrames are saved here in the Parquet format for subsequent analysis.

### Data Formats

Two primary data formats are used in this project:

-   **CSV (Comma-Separated Values)**:
    -   **Usage**: Storing raw data in `data/raw/`.
    -   **Reasoning**: CSV is chosen for its universal compatibility and human-readability, making it ideal for initial data ingestion and inspection.

-   **Parquet**:
    -   **Usage**: Storing processed data in `data/processed/`.
    -   **Reasoning**: Parquet is an efficient columnar storage format that provides excellent compression and significantly faster read performance, as queries can select individual columns. It also natively preserves data types (like `datetime`), which prevents potential type-casting errors upon reloading.

### Environment-Driven Configuration

To avoid hard-coding file paths, the project relies on a `.env` file to manage data directories. The `python-dotenv` library loads these variables at runtime, ensuring the code is portable and can be executed in different environments without modification.

The required variables in the `.env` file are:

-   `DATA_DIR_RAW=data/raw`
-   `DATA_DIR_PROCESSED=data/processed`

### Data Validation

After saving and reloading data, the script performs validation checks to ensure data integrity. These checks include:

-   **Shape Equality**: Confirms that the reloaded DataFrame has the exact same dimensions (rows and columns) as the original.
-   **Dtype Integrity**: Verifies that critical columns like `date` and `close` maintain their expected data types (`datetime` and `numeric`, respectively) after the save/load cycle.


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