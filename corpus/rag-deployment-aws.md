# RAG Deployment on AWS

## Architecture options
- **Serverless**: API Gateway + Lambda + OpenSearch Serverless + Bedrock
- **Containerized**: ECS/Fargate or EKS + ALB + RDS/pgvector/OpenSearch
- **App**: Streamlit/Next.js on ECS/Amplify

## Components
- **Vector store**: OpenSearch, Amazon Bedrock Knowledge Bases, Aurora pgvector
- **Embeddings/LLM**: Amazon Bedrock (Titan/Claude/Llama), or self-hosted
- **Orchestration**: LangGraph/LangChain in FastAPI
- **Auth**: Cognito/JWT
- **Storage**: S3 for docs
- **Cache**: ElastiCache/Redis (optional)

## Deployment steps (high level)
1. Ingest docs -> chunk -> embed -> index (S3 event -> Lambda or ECS task)
2. Build API (FastAPI) with retriever+agent
3. Containerize + push ECR
4. Deploy to ECS/Fargate behind ALB
5. Add WAF, CloudWatch logs/metrics, X-Ray tracing
6. CI/CD (CodePipeline/CodeBuild/GitHub Actions)

## Security & compliance
- VPC/private subnets, least privilege IAM
- Encryption at rest/in transit (KMS)
- Bedrock knowledge bases with access controls
- Avoid logging PII; use CloudWatch Logs filters
- Consider HIPAA if PHI (extra controls)

## Cost tips
- Use OpenSearch Serverless or right-size
- Cache frequent queries
- Bedrock provisioned throughput vs on-demand
- S3 lifecycle policies

## Pros/Cons
- **Bedrock KB**: fast start, managed; less custom routing/advanced agentic
- **Custom (LangGraph)**: full control, more complex ops
