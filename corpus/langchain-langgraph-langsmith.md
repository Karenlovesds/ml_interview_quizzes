# LangChain, LangGraph, LangSmith

## LangChain
- **Chains**: composable LLM workflows (LCEL)
- **Prompts/Output parsers**: structure outputs (JSON/schema)
- **Retrievers/Vectorstores**: FAISS, Weaviate, pgvector, OpenSearch
- **Memory/Callbacks**: conversation history, tracing hooks

## LangGraph
- **Stateful graphs**: nodes/edges with shared state (TypedDict)
- **Human-in-the-loop**: interrupts for approval/editing
- **Subgraphs/multi-agent**: supervisor + workers, handoffs
- **Conditional routing**: dynamic control flow
- **Persistence/checkpoints**: resume long-running flows

## LangSmith
- **Tracing**: step-by-step traces (inputs/outputs, tokens, latency)
- **Evaluations**: run experiments, compare prompts/models
- **Datasets**: golden sets, few-shot examples
- **Feedback**: user ratings, corrections
- **Monitoring**: dashboards, regressions on prompts

## When to use
- **LangChain**: quick prototyping, rich integrations
- **LangGraph**: complex, stateful, multi-step/agentic flows
- **LangSmith**: evals, debugging, production observability
