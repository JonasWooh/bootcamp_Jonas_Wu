# Outlier Analysis: Definitions, Assumptions, and Risks

This document outlines the approach to outlier detection and handling, detailing the definitions, underlying assumptions, and potential risks associated with these methods.

## 1. Definition of Outliers

An **outlier** is generally defined as an observation point that lies an abnormal distance from other values in a random sample from a population. Essentially, it's a data point that significantly deviates from the rest of the dataset.

Outliers can arise from various sources:
*   **Measurement Errors**: Errors during data collection or input.
*   **Data Entry Errors**: Mistakes when manually entering data.
*   **Experimental Errors**: Anomalies in experimental procedures.
*   **Natural Variation (True Extremes)**: Genuine, albeit rare, events that are part of the true underlying process (e.g., market shocks, extreme weather events). These are not "errors" but rather significant observations.
*   **Novelty/Anomaly**: Data points representing new or unusual patterns that might be indicative of a significant change.

Distinguishing between true extremes and errors is crucial, as handling them differently can significantly impact analysis and conclusions.

## 2. Outlier Detection and Handling Methods Used

In the accompanying sensitivity analysis, the following methods were employed:

### Detection Methods:
*   **Interquartile Range (IQR) Rule**: This method flags values that fall outside the range `[Q1 - k * IQR, Q3 + k * IQR]`, where Q1 is the 25th percentile, Q3 is the 75th percentile, IQR = Q3 - Q1, and `k` is a multiplier (typically 1.5 for "mild" outliers or 3 for "extreme" outliers).
    *   **Why**: It is robust to non-normal distributions and skewness, as it relies on rank-based statistics rather than means and standard deviations which are heavily influenced by outliers themselves. We used `k=1.5` as a standard, conservative threshold.
*   **Z-score Method**: This method flags values where the absolute Z-score `(|(x - μ) / σ|)` exceeds a certain threshold (e.g., 2, 3).
    *   **Why**: It's simple to compute and interpret. We used a `threshold=3.0` for `|z| > 3.0` as a common cutoff for values highly unlikely to occur in a normal distribution (representing about 0.27% of data in a perfect normal distribution). It serves as a good cross-check, especially if the data has some degree of normality.

### Handling Method:
*   **Winsorization**: This technique involves capping extreme values in a dataset to a specified percentile, effectively "pulling in" the tails of the distribution. For example, values below the 5th percentile are set to the 5th percentile value, and values above the 95th percentile are set to the 95th percentile value.
    *   **Why**: Unlike removal, winsorization retains all observations, which can be important if the sample size is small or if the extreme values, even if clipped, still hold some information. It reduces the impact of outliers without discarding data points entirely. We used 5th and 95th percentiles as reasonable bounds.

## 3. Assumptions Behind Choices

*   **Distributional Assumptions**:
    *   The **IQR method** assumes that the central 50% of the data (between Q1 and Q3) provides a reasonable representation of the data's typical spread, even if the overall distribution is skewed or heavy-tailed. It does not assume normality.
    *   The **Z-score method** implicitly assumes an approximately normal distribution. Its effectiveness diminishes with highly skewed or fat-tailed data, where true extremes can significantly inflate the standard deviation, making outliers appear less extreme, or conversely, in very thin-tailed data, it might over-flag.
    *   **Winsorization** assumes that the most extreme `X%` of values (e.g., 5% at each tail) are atypical and can be safely clipped without losing critical information, or that their exact values are less important than their relative position.
*   **Semantic Assumptions about "Outliers"**:
    *   **Detection is not Deletion**: The primary assumption is that detection merely flags potential anomalies for further investigation, rather than automatically implying removal or modification. Some "outliers" may be genuine, significant events (e.g., market shocks, medical anomalies) that carry critical information.
    *   **Parameter Choices**: The specific parameters chosen (`k=1.5` for IQR, `threshold=3.0` for Z-score, `5th/95th` percentiles for winsorization) are standard starting points. The assumption is that these values offer a reasonable balance between identifying true anomalies and avoiding over-flagging, though they may require tuning based on domain knowledge.
*   **Modeling Context (if applicable)**:
    *   If using simple linear regression, the assumption is that the underlying relationship is linear, and outliers are distorting this linear fit. Removing or mitigating their influence is intended to reveal the true underlying relationship more accurately.

## 4. Observed Impact on Results (General Observations)

Based on typical outlier analyses:

*   **Summary Statistics**:
    *   **Mean**: Often the most sensitive statistic, showing a noticeable shift after outlier removal or winsorization (moving towards the center of the non-outlying data).
    *   **Standard Deviation**: Significantly decreases as extreme values, which contribute heavily to variance, are removed or clipped.
    *   **Median**: Generally robust to outliers, showing minimal change, especially compared to the mean.
*   **Visualizations**:
    *   **Boxplots**: Outlier markers disappear, and the whiskers may shorten significantly after removal. Winsorization will show shortened whiskers but no individual outlier points.
    *   **Histograms**: The tails of the distribution will visibly shrink or become less pronounced after outlier handling.
*   **Regression Models**:
    *   **Coefficients (Slope/Intercept)**: Can show noticeable changes, often becoming steeper or shallower depending on the leverage of the removed/clipped outliers. The model might become less biased by extreme points.
    *   **Performance Metrics (e.g., MAE, R²)**: Typically improve *in-sample* (lower MAE, higher R²) because the model fits the "cleaned" data better. However, this doesn't guarantee better out-of-sample performance or generalization.

## 5. Risks if Assumptions are Wrong (Discarding True Events)

Incorrectly handling outliers carries several significant risks:

*   **Underestimating Tail Risk / Discarding True Events**:
    *   **Problem**: If "outliers" are actually genuine, rare, but impactful events (e.g., market crashes, disease outbreaks, critical system failures), removing or heavily modifying them leads to a distorted view of reality.
    *   **Consequence**: Financial models might underestimate extreme losses; risk management strategies could be dangerously optimistic; healthcare analyses might miss crucial disease patterns; engineering systems might not be designed for rare but catastrophic loads. This is particularly relevant in the financial dataset provided (`daily_return`) where "shocks" are explicitly injected.
*   **Misclassification and Biased Models**:
    *   **Problem**: Aggressive outlier removal can introduce selection bias, leading to a dataset that no longer accurately represents the underlying population.
    *   **Consequence**: Models built on such data may generalize poorly to new, unseen data, especially if that new data contains genuine extreme events. The model's coefficients might be biased, leading to incorrect inferences.
*   **Loss of Information**:
    *   **Problem**: Even if an outlier is a measurement error, its very existence might signal a problem with the data collection process that needs addressing. Simply removing it without investigation might hide systemic issues.
    *   **Consequence**: Missed opportunities for process improvement or deeper understanding of data generation mechanisms.
*   **Parameter Sensitivity and Arbitrariness**:
    *   **Problem**: The choice of `k` for IQR, `threshold` for Z-score, or percentiles for winsorization is often somewhat arbitrary. Different choices can lead to different sets of flagged points and different analytical outcomes.
    *   **Consequence**: The robustness of the conclusions might be questionable, and results could be manipulated by selecting specific thresholds.
*   **Reduced Interpretability**:
    *   **Problem**: When data is heavily manipulated (e.g., many points removed or winsorized), the resulting model or statistics may be harder to interpret in the context of the original, real-world process.
    *   **Consequence**: Difficulty in communicating findings to non-technical stakeholders or relating them back to domain knowledge.
*   **Governance and Audit Trail**:
    *   **Problem**: Lack of clear documentation regarding outlier detection and handling steps, including the parameters used and the justification for these choices.
    *   **Consequence**: Reduced reproducibility, difficulty in auditing results, and challenges in maintaining data integrity over time.

In conclusion, while outlier handling is essential for robust analysis, it must be approached with caution and domain knowledge. A sensitivity analysis, as performed in the notebook, helps quantify the impact of different outlier strategies and highlights the trade-offs involved.