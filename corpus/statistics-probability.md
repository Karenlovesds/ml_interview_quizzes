# Statistics & Probability for ML

## Bayes' theorem

`P(A|B) = P(B|A)·P(A) / P(B)`. Posterior ∝ likelihood × prior. Underpins
Naive Bayes, Bayesian inference, and calibration.

## Common distributions

- **Bernoulli / Binomial**: binary outcomes / counts of successes.
- **Gaussian (Normal)**: sums of many small effects (CLT); basis of MSE.
- **Poisson**: counts of rare events per interval.
- **Exponential**: time between Poisson events.

## Central Limit Theorem

The sampling distribution of the mean approaches a normal distribution as
`n` grows, regardless of the underlying distribution (finite variance). Basis
for confidence intervals and hypothesis tests.

## Estimation & inference

- **MLE**: choose parameters maximizing the likelihood of observed data.
- **MAP**: MLE with a prior; equivalent to MLE + regularization (e.g.,
  Gaussian prior → L2).
- **Probability vs likelihood**: probability fixes parameters and varies data;
  likelihood fixes data and varies parameters.

## Hypothesis testing

- **p-value**: probability of observing a result at least as extreme under
  `H₀`. Not the probability that `H₀` is true.
- **Type I error**: false positive (reject true `H₀`).
  **Type II error**: false negative.
- **Confidence interval**: range covering the true parameter in repeated
  sampling with a given frequency.

## Correlation vs causation

Correlation does not imply causation. Confounders, Simpson's paradox, and
selection bias can produce misleading associations.

## Expectation & variance identities

- `E[aX + b] = aE[X] + b`
- `Var(aX + b) = a²Var(X)`
- `Var(X) = E[X²] - (E[X])²`
- `Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y)`
