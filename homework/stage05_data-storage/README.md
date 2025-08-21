## Data Storage

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