Title: AgentLegatus — Terraform for AI Agents
Date: 2026-04-15
Category: Engineering, Agents
Tags: agentlegatus, multi-agent, llm, open-source, orchestration, python, langgraph, vendor-agnostic
Slug: agentlegatus-terraform-for-ai-agents

The multi-agent space is fracturing fast. Teams pick LangGraph one quarter, switch to CrewAI the next, then discover Google ADK or AWS Strands and wonder if they should migrate again. Every switch costs weeks — ripping out abstractions, rewriting orchestration logic, re-testing state management. This is the exact problem Terraform solved for infrastructure: you shouldn't be locked into a provider. You should declare *what* you want, and swap *where* it runs.

AgentLegatus applies that same philosophy to AI agents. It is a vendor-agnostic agent framework abstraction layer — a unified API that sits above LangGraph, AutoGen, CrewAI, Google ADK, AWS Strands, and Microsoft Agent Framework, letting you switch providers with a config change rather than a codebase rewrite.

## What Makes It Different

**Provider Abstraction via BaseProvider** — Every backend (LangGraph, AutoGen, mock) implements a single `BaseProvider` interface. Your workflow code never calls a provider SDK directly. Swap the backend, keep the logic.

**Roman Military Hierarchy** — The orchestration model maps to four command tiers: `Legatus` (top-level orchestrator managing the workflow lifecycle), `Centurion` (workflow controller handling topological sorting and execution strategies), `Cohort` (agent group coordinator), and `Agent` (the atomic task execution unit with tools and memory). This hierarchy makes large multi-agent systems readable and governable by design.

**Portable Execution Graph (PEG)** — The PEG is the core mechanism for provider switching at runtime. It serialises the current workflow state and execution graph, then reconstitutes it on a new provider without losing progress. Switching mid-workflow from mock to LangGraph — or back — is a first-class operation.

**EventBus** — A unified event system with subscription, history, correlation IDs, and trace propagation. Every state transition, tool call, and step completion emits an event. This makes observability a built-in concern, not an afterthought bolted on later.

**State Management** — State is scoped at four levels: workflow, step, agent, and global. Backends include in-memory (zero dependencies), Redis, and Postgres. Snapshots and restore are supported natively, enabling checkpoint-and-resume after failures or timeouts.

**ToolRegistry** — Define a tool once. The registry auto-converts it to OpenAI or Anthropic format, with per-provider caching. No more writing the same tool schema twice.

**Memory Abstraction** — Four memory types are supported out of the box: short-term (TTL-based), long-term, episodic, and semantic. Backends cover Redis and vector stores (ChromaDB). The MemoryManager handles routing between types transparently.

**Benchmark Engine** — Run the same workflow across multiple providers and get back a side-by-side comparison of latency (p50/p95/p99), cost, token usage, and success rate. For teams that need to justify a framework choice with data, this is significant.

**Security Layer** — Input sanitization, path traversal prevention, PII detection and redaction, rate limiting, audit logging, and HTTPS with certificate validation are included in core. Security is not an optional plugin.

**Retry and Resilience** — Configurable exponential backoff with max delay capping is built into the executor. Workflows recover from transient failures without custom retry scaffolding.

## The CLI

The `legatus` CLI brings Terraform-like commands to agent workflows.

```
legatus init --provider mock
legatus apply workflow.yaml
legatus apply workflow.yaml --dry-run
legatus plan workflow.yaml
legatus benchmark workflow.yaml --providers mock,langgraph --iterations 5
legatus switch langgraph
legatus providers
legatus status <workflow-id>
legatus cancel <workflow-id>
```

`legatus plan` shows what *would* happen before execution. `legatus benchmark` is the comparison engine. `legatus switch` migrates a running workflow to a different provider. These aren't experimental — they're in the 0.1.0 release.

## Architecture at a Glance

```
CLI (legatus)
    └── Legatus (Orchestrator)
            ├── EventBus ──► Observability (OpenTelemetry, Prometheus)
            ├── StateManager (in-memory / Redis / Postgres)
            └── Centurion (Workflow Controller)
                    ├── Sequential / Parallel / Conditional execution
                    └── Cohort (Agent Group)
                            └── Agent (Worker)
                                    ├── ToolRegistry
                                    └── MemoryManager
```

The layering is intentional. Each tier has a single responsibility. EventBus threads through the entire stack, connecting observability to every component without coupling them.

## Test Coverage

936 tests. 88% coverage. The test suite spans unit, integration, and property-based tests (via Hypothesis). For a 0.1.0 release, that is a serious signal about engineering intent.

## Why This Matters Now

The agentic AI ecosystem is still sorting itself out. LangGraph and CrewAI are not going to be the last frameworks. New ones will emerge. Teams building production systems today cannot afford to be structurally coupled to any single provider's API surface. AgentLegatus treats that coupling as the core problem and attacks it directly — not with a thin wrapper, but with a full abstraction stack including state migration, event-driven observability, benchmarking, and a CLI that mirrors how infrastructure engineers already think.

If you are building multi-agent systems in Python and you want optionality as the ecosystem evolves, this is worth watching closely.

**GitHub** — `pip install agentlegatus` or explore at [github.com/rajacsp/agentlegatus](https://github.com/rajacsp/agentlegatus)