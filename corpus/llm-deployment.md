# LLM Deployment & Serving

## Serving fundamentals

- **Autoregressive decoding**: tokens are generated one at a time; each new
  token recomputes attention over previous tokens **unless** you cache them.
- **KV cache**: stores past keys/values to avoid recomputation.
  Memory ≈ `2 · layers · heads · dim · seq_len` — grows with context length.
- **Effective batching**: process many requests at once on a GPU to use it
  fully. **Continuous/in-flight batching** (e.g., vLLM's PagedAttention)
  packs active requests dynamically instead of waiting for whole batches.

## Key performance metrics

- **TTFT** (Time To First Token): perceived latency on streaming UIs.
- **Tokens/s / throughput**: output rate per request and per GPU.
- **Inter-token latency**: time between consecutive tokens.
- There is a classic **latency vs throughput** tradeoff shaped by batch size.

## Optimizing & reducing cost

- **Quantization**: reduce weight precision — INT8, or 4-bit (GPTQ, AWQ,
  GGUF). Big memory/dollar savings, small quality loss if calibrated.
- **Distillation**: train a smaller student model to mimic a large teacher.
- **Speculative decoding**: a small draft model proposes tokens; the big model
  verifies them in parallel — same quality, faster.
- **Caching**: cache user/system prefixes (prompt caching) and repeated
  answers.
- **Streaming** (token-by-token SSE) hides latency and feels responsive.

## GPU memory budget

Weights + KV cache + activations + CUDA overhead. For long contexts and many
concurrent users, the **KV cache often dominates** — plan for it, don't just
count model size.

## Serving stack

- **Inference servers**: vLLM, TensorRT-LLM, TGI, llama.cpp, ONNX Runtime.
- **Routing & orchestration**: an orchestrator selects model/route, adds
  guardrails, retries, and fallbacks.
- **API-first**: REST/gRPC with streaming, structured outputs (JSON schema).

## Production concerns

- **Guardrails**: block/rewrite harmful or off-topic inputs and outputs;
  enforce system prompts (prompt-injection resistance).
- **Monitoring**: tokens/s, latency percentiles, error rates, cost per
  request, and **output quality drift** (data/concept drift applies to
  prompts too).
- **Fallbacks & degradation**: hot standby for overload, timeouts, graceful
  "I can't answer" paths.
- **Evaluation gates in CD**: keep golden-set evals green before every
  prompt/model/code rollout.
- **Compliance & privacy**: no PII in prompts, encryption in transit/at rest,
  audit logging, regional hosting where mandated.