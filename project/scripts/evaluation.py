import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from pathlib import Path
import textwrap

def save_evaluation_metrics(y_true: np.ndarray, y_pred: np.ndarray, output_path: Path):
    """
    Calculates regression metrics and saves them to a formatted text file.
    """
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)

    # Using textwrap.dedent to format the string cleanly
    report_content = textwrap.dedent(f"""
    # Model Evaluation Report
    
    This report summarizes the performance of the regression model based on the test dataset.
    
    ## Performance Metrics
    -----------------------------------
    - R-squared (R²):           {r2:.4f}
    - Root Mean Squared Error (RMSE): {rmse:.6f}
    - Mean Absolute Error (MAE):    {mae:.6f}
    -----------------------------------
    
    ## Interpretation
    - **R-squared (R²)**: This value indicates that approximately {r2:.2%} of the variance in the target variable (daily returns) can be explained by our model. An R² close to 0, as seen here, suggests the model has very little predictive power, which is common in financial markets for simple models.
    - **RMSE & MAE**: These metrics measure the average error of the model's predictions in the same units as the target (daily returns). For example, an RMSE of {rmse:.4f} means the typical prediction error is about {rmse:.2%}.
    """)

    # Write the formatted content to the specified file path
    with open(output_path, 'w') as f:
        f.write(report_content)