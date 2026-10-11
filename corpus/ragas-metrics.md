# RAGAS Metrics

RAGAS evaluates RAG systems (retrieval + generation) with reference-free metrics.

## Retrieval metrics
- **Context Precision**: how much relevant info is in top contexts
- **Context Recall**: covers all claims needed to answer
- **Context Entities Recall**: important entities present
- **Context Utilization**: used vs available context

## Generation metrics
- **Faithfulness**: claims grounded in context (hallucination check)
- **Answer Relevancy**: answers question directly
- **Answer Correctness**: factual correctness vs ground truth
- **Answer Similarity**: semantic similarity to reference
- **Answer Completeness**: covers all aspects
- **Coherence/Fluency**: readability

## End-to-end / others
- **Factual Correctness**, **Semantic Similarity**, **BLEU/ROUGE** (lexical)
- **Noise Sensitivity**, **Response Consistency**

## Usage tips
- Use **faithfulness + context precision/recall** as core
- Pair with **human eval** on golden set
- Track per-query + aggregates; watch regressions
- Calibrate thresholds per domain (healthcare stricter)
