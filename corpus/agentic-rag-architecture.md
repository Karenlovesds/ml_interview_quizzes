# Agentic RAG Architecture

## Vanilla RAG vs Agentic RAG
- **Vanilla RAG**: query -> retrieve top-k -> augment prompt -> generate (single pass)
- **Agentic RAG**: agent reasons, may rewrite query, choose retriever, iterate, call tools, verify, answer

## Core components
- **Query rewriting**: decompose/multi-hop, clarify ambiguous queries
- **Router/planner**: decides retrieval strategy (vector, hybrid, graph, web)
- **Retrievers**: dense/sparse/hybrid, rerankers, knowledge graphs
- **Memory**: short/long-term (conversation, user prefs)
- **Tools**: search, calculators, APIs, SQL
- **Critic/verifier**: checks grounding, citations, answer quality
- **Orchestrator**: ReAct, Plan-Act-Observe, Multi-Agent (router+executor)

## Patterns
- **Adaptive RAG**: classify query complexity -> choose strategy
- **Corrective RAG**: retrieve, grade relevance, self-correct
- **Multi-hop RAG**: iterative retrieval over sub-questions
- **GraphRAG**: use entity/relations for global queries

## Design tips
- Keep retrieval cheap; use reranker for precision
- Add citations + grounding checks
- Limit tool calls, add timeouts/guardrails
- Track traces (LangSmith) for debugging
