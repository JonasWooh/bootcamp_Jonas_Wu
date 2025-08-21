# Outlier Handling: Definition, Methods, Assumptions, and Risks  

## Definition  
Observations that significantly deviate from the overall distribution pattern are considered outliers; detection methods include IQR and Z-score.  

## Methods and Thresholds  
- **IQR**: k=1.5, using quartiles and the interquartile range to identify outliers.  
- **Z-score**: Threshold of 3.0, assumes approximate normality, more sensitive to heavy-tailed distributions.  
- **Winsorize**: Trimming at the 5th and 95th percentiles to reduce the impact of extreme values without deleting data.  

## Assumptions  
- Extreme observations are mostly noise or abnormal processes rather than genuine business events.  
- Missing values are excluded from statistical calculations; constant columns are not flagged as outliers (no variance).  

## Sensitivity Analysis Design  
- Compare mean/median/standard deviation between "original data," "IQR outlier removal," and "Winsorize."  
- If an independent variable x exists, perform simple bivariate regression to compare slope/intercept/R²/MAE.  

## Observations and Impact (Update based on actual results)  
- After removing outliers, MAE generally decreases while R² increases; the slope aligns more closely with the main trend (subject to actual output).  

## Risks  
- Risk of mistakenly removing genuine extreme events (e.g., rare but significant peaks).  
- Methods may misjudge in asymmetric or multimodal distributions; Z-score is less robust for heavy-tailed distributions.  
- Over-cleaning reduces sample size and increases model variance.  

## Mitigation Strategies  
- Prioritize Winsorizing or merely flagging key business metrics.  
- Record thresholds, deletion ratios, and changes in performance metrics; conduct business reviews if necessary.  
- Use robust loss functions or robust regression in downstream tasks.  

## Reproducing the Experiment  
- Data: `data/raw/outliers_homework.csv` (if missing, synthetic data will be automatically generated).  
- Scripts: `scripts/preprocess.py`, `scripts/sensitivity.py`.  
- Output: Comparison files and plots in `data/interim` and `data/processed`.
