# LLM Evaluation & Human-in-the-Loop

## Why evaluation is different for LLMs

Open-ended generation can't be scored with a single accuracy number.
You need (1) automatic benchmarks, (2) human evaluation, and often
(3) an LLM acting as a judge — and a process that keeps people in the loop.

## Automatic benchmarks

- **MMLU**: broad knowledge, multi-task multiple choice.
- **GSM8K**: grade-school math (tests reasoning).
- **HumanEval**: code generation pass@k.
- **TruthfulQA / FactScore**: hallucination and factuality.
- **HELM / Open LLM Leaderboard**: batteries of benchmarks under one scaffold.
Benchmarks help compare models but can be **saturated or leaked** — they
don't tell you if *your* use case works.

## Metrics for generated text

- **BLEU / ROUGE**: overlap-based; cheap but reward surface similarity, not
  meaning. Suitable for translation/summarization, weak for dialogue.
- **Semantic similarity / embedding distance**: measures meaning more than
  n-grams.
- **Task metrics**: exact/partial match, tool-call correctness, answer
  grounded in retrieved docs.

## Human evaluation & human-in-the-loop

- **Golden sets**: a small curated set of prompts with reference answers;
  run it after every prompt or model change (regression testing).
- **Side-by-side comparison**: raters rank two outputs (A/B) — more reliable
  than absolute scores.
- **Rubrics**: score criteria (helpfulness, correctness, safety) per dimension
  instead of a single vague grade.
- **Inter-rater agreement** (Cohen's κ / Krippendorff's α) tells you whether
  the rubric is clear enough.
- **Red-teaming**: adversarial humans probing for harmful or misleading
  outputs before release.
- **In-the-loop workflows**: human review for high-stakes outputs
  (medical, finance, legal), with the model providing drafts + evidence.

## LLM-as-a-judge

A strong model scores/scans another model's output. Fast and scalable, but
has **biases**: prefers longer/self-style answers, position bias (A vs B
order), self-preference. Calibrate judges against a human-annotated set.

## Hallucination & groundedness

- **FActScore**: fact-check claims against a knowledge source.
- **Grounding checks**: verify each claim appears in the retrieved context.
- Mitigation: RAG, citations, "I don't know" training, conservative settings.

## Production evaluation loops

- **Online**: monitor user feedback (thumbs, ratings), answer quality QAs,
  and drift detectors.
- **Offline**: replay logged prompts against new candidates (prompt/model/code
  regression).
- **Feedback loop**: preference labels from production feed back into RLHF or
  future fine-tunes.