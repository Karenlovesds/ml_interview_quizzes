# Deep Learning

## Neural network basics

A feed-forward network is a stack of affine transforms + non-linearities:
`h = φ(Wx + b)`. Without non-linear activations the whole network collapses
to a single linear map.

- **ReLU** `max(0,z)`: cheap, mitigates vanishing gradients, can "die".
- **Sigmoid / tanh**: saturate → vanishing gradients in deep nets.
- **Softmax**: converts logits to a probability distribution for multiclass.

## Backpropagation

Computes gradients of the loss w.r.t. every parameter via the chain rule,
reusing intermediate results (reverse-mode autodiff). Optimizers:
- **SGD**: `θ ← θ - η∇L`.
- **Momentum**: accumulates velocity to smooth updates.
- **Adam**: per-parameter adaptive learning rates using first and second
  moment estimates; robust default.

## Training issues

- **Vanishing/exploding gradients** → residual connections, normalization
  (BatchNorm/LayerNorm), gradient clipping, careful init.
- **Internal covariate shift** → batch normalization.
- **Overfitting** → dropout, weight decay, data augmentation, early stopping.

## Architectures

- **CNN**: weight sharing + local receptive fields for grid data (images).
  Convolution → non-linearity → pooling.
- **RNN / LSTM / GRU**: sequential data with a hidden state; LSTMs use gates
  to combat vanishing gradients.
- **Transformer**: self-attention over all positions, parallelizable,
  dominant for text and increasingly vision.

## Transfer learning

Reuse a model pretrained on a large dataset; fine-tune on a small target
dataset. Freeze early layers (generic features), retrain later layers.
