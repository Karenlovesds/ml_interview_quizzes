# AI & AI-Engineer Terminology (Glossary)

## LLM & prompt basics

- **Token**: smallest unit of text a model works with (word fragments).
- **Context window**: max tokens the model can consider at once.
- **Temperature**: softmax temperature controlling randomness (low =
  deterministic).
- **Top-p / top-k**: samplers that restrict which tokens can be picked.
- **Logits**: raw, unnormalized model scores before softmax.
- **Embedding**: dense vector representation of text/image/ID, learned by
  the model.
- **Zero-shot / few-shot / in-context learning**: solving tasks with no
  examples / a few examples in the prompt / using prompt context only.

## Training & adaptation

- **SFT**: supervised fine-tuning on instruction/response pairs.
- **RLHF**: reward model trained on human preferences + PPO-style policy
  optimization.
- **DPO / KTO**: direct preference optimization without a separate reward
  model or RL loop.
- **RLAIF**: preferences labeled by an AI instead of humans.
- **PEFT**: parameter-efficient fine-tuning (few trainable params).
- **LoRA / QLoRA**: low-rank adapters (optionally on quantized base weights).
- **Checkpoint / adapter**: a saved model snapshot / a small trainable module
  applied on top of a frozen base model.
- **Catastrophic forgetting**: a model losing old skills when fine-tuned on
  new data.

## Reasoning & systems

- **CoT (chain-of-thought)**: prompting the model to reason step by step.
- **RAG**: retrieval-augmented generation — search then answer over documents.
- **Grounding**: tying model output to verifiable sources/retrieved context.
- **Agent**: model loop that plans, calls tools, and observes results.
- **Tool / function calling**: model emits structured calls to external APIs.
- **MCP (Model Context Protocol)**: a standard way for agents to connect to
  tools and data.
- **Guardrails**: input/output filters enforcing safety and policy.
- **Hallucination**: fluent but false content.
- **Prompt injection**: hidden instructions in input hijacking the model.

## Serving & performance

- **KV cache**: cached attention keys/values that enable fast decoding.
- **TTFT**: time to first token (perceived latency).
- **Throughput**: tokens generated per second (across requests/GPUs).
- **Quantization**: lowering weight precision (INT8/INT4) to save memory.
- **Distillation**: training a small student to copy a large teacher.
- **Speculative decoding**: draft model proposes, big model verifies faster.
- **PagedAttention** (vLLM): dynamic key-value memory for flexible batching.

## Classical ML — quick definitions

- **Underfitting / overfitting**: model too simple (high bias) / too tuned to
  training noise (high variance).
- **Bias-variance tradeoff**: test error = bias² + variance + noise.
- **Regularization (L1/L2/dropout)**: penalty or stochastic dropout to curb
  overfitting.
- **Cross-validation**: rotating train/validate splits to estimate
  generalization.
- **Data leakage**: test-set info reaching training — silently inflates scores.
- **Precision / Recall / F1**: correctness of positives / coverage of
  positives / harmonic mean.
- **ROC-AUC / PR-AUC**: threshold-independent performance measures.
- **Class imbalance**: skewed class distribution; fix with resampling, class
  weights, or metric choice.
- **Drift** (data, concept, label): input/target distributions changing over
  time.
- **Feature engineering / scaling**: building and normalizing predictors;
  fit scaling on train only.
- **Reproducibility**: pinned data, code, environment, seeds, logged
  experiments.

## Deployment & ops

- **MLOps**: practices to build, ship, and monitor ML reliably.
- **CI/CD for ML**: automated builds, tests, evaluation gates before rollout.
- **Canary / A-B / shadow**: low-risk rollout patterns for new models.
- **Model registry**: versioned store of models + metadata + lineage.
- **Online vs batch inference**: real-time request serving vs offline jobs.
- **Monitoring & drift alerts**: watch predictions, features, and outcomes.