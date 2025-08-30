import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np # Ensure numpy is imported

def plot_predictions(y_true: pd.Series, y_pred: np.ndarray, output_dir: Path):
    """
    Generates and saves a scatter plot of actual vs. predicted values.
    """
    plt.figure(figsize=(10, 10))
    sns.scatterplot(x=y_true, y=y_pred, alpha=0.5)
    
    # Add a red line for perfect predictions (y=x)
    # Determine the plot limits to make the line span the entire plot
    limits = [
        min(y_true.min(), y_pred.min()),
        max(y_true.max(), y_pred.max())
    ]
    plt.plot(limits, limits, color='red', linestyle='--', lw=2, label='Perfect Prediction')
    
    plt.title('Actual vs. Predicted Daily Returns')
    plt.xlabel('Actual Returns')
    plt.ylabel('Predicted Returns')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_dir / 'report_predictions_vs_actual.png', dpi=300)
    plt.close()