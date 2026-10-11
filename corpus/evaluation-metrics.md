# Evaluation Metrics

## Confusion matrix

TP, FP, TN, FN are the building blocks of classification metrics.

## Classification

- **Accuracy** = (TP+TN)/N — misleading under class imbalance.
- **Precision** = TP/(TP+FP) — of predicted positives, how many are correct.
- **Recall / Sensitivity** = TP/(TP+FN) — of actual positives, how many found.
- **F1** = harmonic mean of precision and recall.
- **ROC-AUC**: TPR vs FPR across thresholds; 0.5 = random.
- **PR-AUC**: preferred under heavy imbalance.
- **Log loss**: penalizes confident wrong probabilities.

Precision/recall trade off via the decision threshold.

## Regression

- **MAE**: robust to outliers, same units as target.
- **MSE / RMSE**: penalizes large errors more; RMSE in target units.
- **R²**: fraction of variance explained; can be negative.

## Cross-validation

- **k-fold**: split into k folds, train on k-1, validate on 1, average.
- **Stratified k-fold**: preserves class proportions per fold.
- **Time-series split**: respect temporal order, never train on the future.
- **Leave-one-out**: k = N; low bias, high variance, expensive.

## Data leakage

Any information from the test set leaking into training (e.g., scaling before
splitting, target leakage) inflates scores and destroys generalization.
Always fit preprocessing on the training split only.
