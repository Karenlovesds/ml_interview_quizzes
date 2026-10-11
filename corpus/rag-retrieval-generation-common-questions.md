# RAG: Retrieval, Generation & Common Q&A

## Retrieval issues & fixes
- **Low recall**: hybrid (BM25+dense), query rewrite, multi-hop, larger k + rerank
- **Low precision/noisy**: reranker (cross-encoder), chunking strategy, metadata filters
- **Ambiguous queries**: query clarification, HyDE
- **Out-of-scope**: "I don't know" policy, confidence threshold

## Generation issues & fixes
- **Hallucinations**: strict grounding, citations, reduce temperature
- **Over-reliance on param knowledge**: force cite-only, system prompt
- **Truncation/verbosity**: max tokens, structured output
- **Lost in long context**: place relevant chunks first, use long-context models carefully

## Common interview questions
1. **Vanilla RAG vs Advanced?** Single-pass vs adaptive/agentic with routing/verification
2. **Chunking best practice?** Semantic/recursive; avoid fixed 500 blindly; preserve tables/sections
3. **When to use reranker?** After retrieval (top 50->top 10) to improve precision cheaply
4. **How to detect hallucinations?** Faithfulness checks, claim extraction + grounding
5. **Multi-hop approach?** Decompose question -> iterative retrieve -> synthesize
6. **Evaluation strategy?** Golden set + RAGAS (faithfulness/context recall) + human review

## Solutions checklist
- [ ] Clear chunking + metadata
- [ ] Hybrid search + reranking
- [ ] Query rewriting/decomposition
- [ ] Citations + refusal for OOS
- [ ] Tracing + golden-set regression
