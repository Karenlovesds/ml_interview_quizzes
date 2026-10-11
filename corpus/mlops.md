# MLOps: Data, Deployment & Monitoring

## Data splitting

Always split **before** preprocessing. Fit scalers/encoders on train only,
then transform validation/test, to avoid leakage. For time series, split by
time.

## Class imbalance

Resampling (oversample minority / undersample majority), SMOTE (synthetic
minority samples), class weights, or threshold tuning. Prefer metrics like
PR-AUC over accuracy.

## Feature scaling

- **Standardization** (z-score): mean 0, std 1 — for PCA, SVMs, k-NN,
  linear models, neural nets.
- **Min-max**: bounded [0,1].
- Tree-based models don't need scaling.

## Deployment patterns

- **Batch** vs **online (real-time)** inference.
- **Model registry** + versioning, reproducible training, CI/CD.
- **Shadow / canary / A-B** rollouts to limit risk.
- **REST/gRPC** serving, containerization, autoscaling.

## Monitoring & drift

- **Data drift**: input distribution `P(X)` changes.
- **Concept drift**: relationship `P(Y|X)` changes.
- **Label drift**: target distribution changes.
Track performance, feature distributions, and prediction distributions;
set alerts and retraining triggers.

## Reproducibility

Pin data versions, code, environment (containers), and random seeds. Log
hyperparameters and metrics (e.g., MLflow, W&B).
