# LLMs: Training, Fine-tuning & Using Them

## Tokens & context

Text is split into **tokens** (subwords) before feeding a model. The
**context window** is the max tokens the model can attend to at once
(input + output). Costs scale with tokens, not words.

## Pretraining → alignment stack

1. **Pretraining (causal LM)**: next-token prediction over internet-scale
   text. Produces a strong base model.
2. **Supervised fine-tuning (SFT)**: train on high-quality
   instruction/response pairs so the model follows instructions.
3. **Alignment**: RLHF or preference optimization so outputs match human
   preferences.

## Aligning with humans

- **RLHF**: train a reward model on human preference comparisons, then
  optimize the policy (PPO) against it while staying close to the SFT model.
- **DPO / KTO**: directly optimize on preference data with a closed-form
  loss — simpler than RLHF, no reward model or PPO needed.
- **RLAIF**: uses an AI (e.g., a stronger model) to generate the preference
  labels instead of humans.

## Efficient fine-tuning

- **PEFT**: freeze the base model, train only a small set of parameters.
- **LoRA**: trains low-rank weight updates (`W + BA`). A 1-2% parameter
  footprint, cheap to train and swap between tasks.
- **QLoRA**: quantizes base weights (4-bit) + LoRA adapters → fine-tune on
  a single GPU.
- **Full fine-tuning**: updates everything; best quality if you have compute
  and data, but risks "catastrophic forgetting".

## Prompting & context engineering

- **Few-shot**: give examples in the prompt, no weight updates.
- **Chain-of-thought (CoT)**: ask the model to reason step by step; improves
  math/logic. **Self-consistency**: sample CoT multiple times, vote.
- **RAG** (retrieval-augmented generation): fetch relevant documents and
  insert them in the prompt — updates knowledge and reduces hallucination
  without retraining.
- **In-context learning / context caching**: reuse the same prefix across
  requests to cut latency and cost.

## Agents & tools

LLMs can call **tools / functions** (search, APIs, calculators, code),
plan steps, and iterate — turning the model into an agent. Add **guardrails**
to keep the loop safe and within policy.

## Common failure modes

- **Hallucination**: fluent but false output. Mitigate with grounding, RAG,
  citations, and evaluation.
- **Leaking / prompt injection**: untrusted text hijacking the model —
  sanitize inputs, isolate system instructions.
- **Reasoning shortcuts** and **instruction drift**: keep evaluations on
  every prompt template change.