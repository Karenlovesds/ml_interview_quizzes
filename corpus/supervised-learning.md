# Supervised Learning Fundamentals

Supervised learning learns a mapping `f: X -> Y` from labeled examples.
The two canonical tasks are **regression** (continuous `Y`) and
**classification** (discrete `Y`).

## Linear regression

Fits `y_hat = w·x + b` by minimizing mean squared error (MSE). The closed-form
solution is the normal equation `w = (XᵀX)⁻¹Xᵀy`. MSE is the maximum-likelihood
estimator under Gaussian noise.

## Logistic regression

Models the probability of a binary label with the sigmoid:
`p = σ(w·x + b)`, `σ(z) = 1/(1+e⁻ᶻ)`. It is a **linear** classifier in the
input space but produces calibrated probabilities. Trained by minimizing
binary cross-entropy / log loss.

## k-Nearest Neighbors

Non-parametric, instance-based. Prediction is a vote/average over the `k`
closest training points. No training cost, expensive inference. Sensitive to
feature scaling and the curse of dimensionality.

## Support Vector Machines

Find the maximum-margin hyperplane separating classes. The **kernel trick**
maps data implicitly into a higher-dimensional space (RBF, polynomial) so
non-linear boundaries become linear. Hinge loss + L2 regularization. Support
vectors are the points on/near the margin.

## Naive Bayes

Applies Bayes' theorem with a conditional-independence assumption between
features. Fast, works well for text. Variants: Gaussian, Multinomial, Bernoulli.

## Discriminative vs generative

- **Discriminative** models `p(y|x)` directly (logistic regression, SVM, trees).
- **Generative** models `p(x,y)` then use Bayes (Naive Bayes, GMM, HMM).
Generative models can generate data and handle missing values; discriminative
models often achieve better accuracy with enough data.

## No Free Lunch

No single algorithm is best for every problem. Model choice depends on data
size, dimensionality, noise, and the metric that matters.
