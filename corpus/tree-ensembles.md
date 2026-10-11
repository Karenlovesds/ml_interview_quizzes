# Decision Trees & Ensembles

## Decision trees

Recursively split data on the feature that best separates the target.
- **Classification criteria**: Gini impurity, entropy (information gain).
- **Regression criterion**: variance / MSE reduction.
- Axis-aligned splits, no scaling needed, interpretable.
- Prone to overfitting; control with `max_depth`, `min_samples_leaf`,
  pruning.

## Bagging (Bootstrap Aggregating)

Train many models on bootstrap samples and average (regression) or vote
(classification). **Reduces variance** without increasing bias. Random Forest =
bagging of decorrelated trees (each split considers a random feature subset).

## Boosting

Train models sequentially, each fitting the residual errors of the previous
ensemble. **Reduces bias** (and variance). Examples:
- **AdaBoost**: reweights misclassified points.
- **Gradient Boosting**: fits each new tree to the negative gradient of the
  loss.
- **XGBoost / LightGBM / CatBoost**: optimized gradient boosting with
  regularization, handling of missing values, and fast histogram splits.

## Bagging vs boosting

| | Bagging | Boosting |
|---|---|---|
| Training | Parallel, independent | Sequential |
| Main effect | Lower variance | Lower bias |
| Weak learners | Strong-ish, deep trees | Shallow trees (stumps) |
| Overfitting risk | Low | Higher if not tuned |

## Feature importance

- **Impurity/Gini importance**: biased toward high-cardinality features.
- **Permutation importance**: shuffle a feature and measure metric drop;
  more reliable.
- **SHAP**: consistent, additive per-prediction attributions.
