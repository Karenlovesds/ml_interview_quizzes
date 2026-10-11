# Transformers & Large Language Models

## Self-attention

Each token forms Query, Key, Value vectors. Attention weights are
`softmax(QKᵀ / √d_k) V`. The `√d_k` scaling keeps logits from saturating the
softmax. Attention lets every position attend to every other position in
parallel (unlike RNNs).

- **Multi-head attention**: several attention heads in parallel capture
  different relationships.
- **Causal masking**: prevents attending to future tokens (decoder / GPT).
- **Positional encoding**: injects order information since attention is
  permutation-invariant.

## Transformer blocks

`LayerNorm → Multi-Head Attention → residual → LayerNorm → Feed-Forward →
residual`. Encoder-only (BERT) for understanding, decoder-only (GPT) for
generation, encoder-decoder (T5) for seq2seq.

## Pretraining objectives

- **Masked LM (BERT)**: predict randomly masked tokens.
- **Causal LM (GPT)**: predict the next token.
- **Seq2seq denoising (T5)**: reconstruct corrupted spans.

## Scaling & fine-tuning

- **Scaling laws**: loss falls as a power law with parameters, data, compute.
- **LoRA**: freeze base weights, train low-rank adapter matrices — cheap
  fine-tuning.
- **RLHF**: train a reward model on human preferences, then optimize the
  policy (e.g., PPO) to maximize reward while staying close to the SFT model.

## Inference

- **Temperature**: scales logits; lower = more deterministic.
- **Top-k / nucleus (top-p) sampling**: truncate the distribution.
- **KV cache**: reuse past keys/values to speed up autoregressive decoding.
