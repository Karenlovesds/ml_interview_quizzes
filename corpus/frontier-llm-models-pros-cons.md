# Frontier LLM Models: Pros & Cons

## OpenAI (GPT series)
- **Pros**: strong general reasoning, function/tool calling, broad ecosystem, evals
- **Cons**: rate/price, some features gated, less control
- **Use**: agents, coding, general Qs

## Anthropic (Claude)
- **Pros**: long context, strong reasoning, safety-focused, good at long docs/summarization
- **Cons**: tool use nuances, availability varies
- **Use**: document analysis, RAG over long docs

## Google (Gemini)
- **Pros**: large context, multimodal, integrated search, competitive price
- **Cons**: can be verbose, ecosystem less mature in some tools
- **Use**: multimodal, search-grounded

## Meta (Llama)
- **Pros**: open weights, local/self-host, fine-tunable, cost control
- **Cons**: needs infra, evals depend on variant, less turnkey
- **Use**: private/on-prem, fine-tuning

## Mistral
- **Pros**: efficient, strong open models, good price/perf, flexible
- **Cons**: smaller ecosystem vs OpenAI/Anthropic
- **Use**: cost-sensitive, edge/local

## DeepSeek
- **Pros**: competitive reasoning/coding, open weights, often cost-efficient
- **Cons**: availability/geo considerations, tooling maturity
- **Use**: coding/reasoning-heavy tasks

## xAI (Grok)
- **Pros**: real-time info, less filtered in some cases
- **Cons**: safety/reliability varies, narrower enterprise adoption
- **Use**: real-time/current events

## Comparison notes (pragmatic)
- **RAG over long docs**: Claude/Gemini strong
- **Agents/tool use**: OpenAI/Claude solid
- **Privacy/on-prem**: Llama/Mistral/DeepSeek (self-host)
- **Cost at scale**: open/self-host or smaller models + routing
