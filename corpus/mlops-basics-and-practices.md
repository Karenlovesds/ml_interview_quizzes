# MLOps Basics & Practices (for DS/AI)

## Lifecycle
Data -> Feature store -> Training -> Validation -> Registry -> Serving -> Monitoring -> Retraining

## Core pillars
- **Reproducibility**: data versioning (DVC), code/env pinning, seeds
- **Experiment tracking**: MLflow/W&B (params, metrics, artifacts)
- **Model registry**: versions, stages (dev/staging/prod), approvals
- **CI/CD**: tests, lint, typecheck, eval gates on golden set
- **Data validation**: schema/checks (Great Expectations)
- **Feature store**: consistent train/inference features
- **Infrastructure as code**: Docker, Terraform

## Deployment patterns
- **Batch**: scheduled jobs
- **Online REST/gRPC**: low-latency
- **Streaming**: event-driven
- **Canary/A-B/shadow**: safe rollouts

## Monitoring & drift
- **Data drift** (P(X)), **concept drift** (P(Y|X)), **label drift**
- **Prediction drift**, **latency/error/cost**
- Alerts + retraining triggers

## RAG-specific MLOps
- **Indexing pipeline**: chunking version, embedding model version, vector DB snapshots
- **Prompt/model config**: versioned in registry
- **Tracing**: per request (LangSmith)
- **Golden-set evals** on every change
- **Cost/latency dashboards**

## Interview Qs
- How to detect drift? (KS/PSI, embedding drift, performance drop)
- Why version embeddings? (re-embed + reindex on change)
- Safe rollout? (canary + rollback)
