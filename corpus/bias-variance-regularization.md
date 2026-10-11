# Bias-Variance Tradeoff & Regularization

## Decomposition

Expected test error decomposes into:

```
E[error] = Bias² + Variance + Irreducible noise
```

- **Bias**: error from overly simple assumptions (underfitting). High training
  and test error, small gap.
- **Variance**: sensitivity to the particular training sample (overfitting).
  Low training error, high test error, large gap.
- **Irreducible noise**: Bayes error, cannot be removed.

As model complexity grows, bias falls and variance rises. The sweet spot
minimizes total error.

## Diagnosing

| Symptom | Diagnosis | Fix |
|---|---|---|
| High train + high test error | Underfitting (high bias) | Bigger model, more features, train longer |
| Low train, high test error | Overfitting (high variance) | More data, regularization, simpler model |

## Regularization

- **L2 / Ridge**: penalizes `λ·Σwᵢ²`. Shrinks weights smoothly, never exactly
  zero. Handles multicollinearity.
- **L1 / Lasso**: penalizes `λ·Σ|wᵢ|`. Produces **sparse** solutions (feature
  selection), because the penalty has a corner at zero.
- **Elastic Net**: mix of L1 and L2.
- **Dropout**: randomly zeroes activations during training — an ensemble-like
  regularizer for neural nets.
- **Early stopping**: stop when validation loss stops improving.

The regularization strength `λ` (or `C = 1/λ` in scikit-learn SVMs) is a
hyperparameter tuned on a validation set.

## Learning curves

Plotting train/validation error vs. training-set size distinguishes the two:
- Curves converge at a high error → high bias.
- A persistent gap that shrinks slowly with more data → high variance.
