Title: Agentic AI Roadmap
Date: 2026-11-11
Category: AI Engineering
Tags: Agentic AI, RAG, Context Engineering, Harness Engineering, Loop Engineering, MCP, Memory, Fine-Tuning, Evaluation, Observability, Guardrails
Slug: agentic-ai-roadmap
Status: Published
Cover: image/2026-11-09-agentic-roadmap/1794411004084-opt.jpg

![1794411004084](image/2026-11-09-agentic-roadmap/1794411004084.png)

Are you interested to start your career or switch your career into GenAI? After working 3 years in GenAI, I came up with this AgenticAI Roadmap.

This is good enough to make your strong career in GenAI.

# Phase 1: Retrieval Foundations

## 1. RAG Fundamentals

**1.1 Simple RAG**
Embed the query, retrieve the top matching chunks, and pass them to the LLM as context.

**1.2 Chunking Strategies**
Fixed, recursive, semantic, document-aware and hierarchical splitting. How you chunk often matters more than which model you use.

**1.3 Embeddings**
Turn text into vectors so the system can search by meaning rather than exact keywords.

**1.4 Vector Databases**
pgvector, Qdrant, FAISS and Elasticsearch store vectors and serve fast similarity search.

**1.5 Metadata Filtering**
Narrow retrieval by source, date, owner or type before similarity ranking.

## 2. Advanced RAG

**2.1 Hybrid RAG**
Combine dense retrieval with sparse BM25 and merge the two result lists using Reciprocal Rank Fusion.

**2.2 Reranking**
Re-score the retrieved candidates with a cross-encoder so the best chunks reach the prompt.

**2.3 Multi-Query RAG**
Rewrite one question into several queries to widen recall.

**2.4 HyDE**
Generate a hypothetical answer first, then retrieve using that answer's embedding.

**2.5 Parent-Child RAG**
Match on small chunks but return their larger parent sections for fuller context.

**2.6 Multi-Hop RAG**
Chain retrievals so each step's answer feeds the next query.

**2.7 Adaptive RAG**
Route each query to no retrieval, single-step or multi-step retrieval based on its difficulty.

**2.8 Corrective RAG (CRAG)**
Grade the retrieved documents and fall back to rewriting or web search when they are weak.

**2.9 Self-RAG**
The model decides when to retrieve and critiques its own output against the sources.

**2.10 GraphRAG**
Build a knowledge graph of entities and relations, then retrieve across it.

**2.11 Agentic RAG**
An agent plans, picks retrieval tools and iterates until it can answer.

**2.12 Multimodal RAG**
Retrieve over images, tables, charts and audio as well as text.

# Phase 2: Engineering the System

## 3. Context Engineering

**3.1 System Instructions**
The fixed role, rules and output format the model works under.

**3.2 Dynamic Context**
Information injected at runtime, such as the user, time, state or task.

**3.3 Retrieved Context**
Documents pulled in by RAG for the current query.

**3.4 Conversation Context**
The prior turns kept, trimmed or summarized.

**3.5 Memory**
Facts carried across sessions and recalled when relevant.

**3.6 Tool Context**
Tool definitions plus the results returned by tool calls.

**3.7 Context Compression**
Summarize or prune content so more signal fits in fewer tokens.

**3.8 Context Selection**
Choose which candidate pieces of context make it into the prompt.

**3.9 Context Prioritization**
Order and place content so the most important parts get the model's attention.

**3.10 Context Window Management**
Budget tokens across all sources and stay within the model's limit.

## 4. Harness Engineering

**4.1 Model**
The LLM at the core, along with its settings.

**4.2 Context**
What the harness feeds the model on each step.

**4.3 Memory**
State the harness persists between steps and sessions.

**4.4 Tools**
The actions the model can call.

**4.5 Permissions**
What each tool or agent is allowed to touch.

**4.6 Guardrails**
Input and output checks that block unsafe or off-policy behaviour.

**4.7 Execution**
Running tool calls safely, with sandboxing and timeouts.

**4.8 Verification**
Checking outputs and results before they are accepted.

**4.9 Retry / Recovery**
Handling failures, timeouts and bad outputs gracefully.

**4.10 Audit**
Logging every decision and action for review.

## 5. Loop Engineering

**5.1 Generate → Evaluate → Regenerate**
Produce a draft, score it, and improve it until it passes.

**5.2 Retrieve → Evaluate → Retrieve Again**
Check retrieval quality and search again when the context is insufficient.

**5.3 Plan → Execute → Observe → Replan**
The core agent loop, adjusted after each observation.

**5.4 Critic / Reviewer Loop**
A second model or prompt reviews the work before it is accepted.

**5.5 Reflection**
The model reasons about its own mistakes and how to fix them.

**5.6 Self-Correction**
The model revises its output using errors or feedback.

**5.7 Retry Strategy**
When to retry, how many times, and with what changes.

**5.8 Loop Termination**
Stop conditions such as a quality threshold, step limit or budget so loops never run forever.

# Phase 3: Agents

## 6. Agentic AI

**6.1 Tool Calling**
The model emits structured calls to functions and APIs.

**6.2 ReAct**
Interleave reasoning steps with actions and observations.

**6.3 Planning**
Break a goal into ordered sub-tasks before acting.

**6.4 Single Agent**
One agent with tools handles the whole task.

**6.5 Multi-Agent**
Several specialised agents collaborate on a task.

**6.6 Supervisor / Worker**
A supervisor delegates tasks to worker agents and merges their results.

**6.7 Planner / Executor**
One agent plans while another carries out the steps.

**6.8 Router Agent**
Sends each request to the right agent, tool or model.

**6.9 Critic Agent**
Reviews other agents' outputs and flags problems.

**6.10 Human-in-the-Loop**
A person approves or corrects the agent at key points.

**6.11 Durable Agents**
Long-running agents that survive restarts through checkpointed state.

**6.12 Agentic RAG**
Retrieval driven by an agent's own decisions.

## 7. MCP / Tool Ecosystem

**7.1 MCP Architecture**
Agent → MCP Client → MCP Server. The server exposes tools in a standard way.

**7.2 MCP Server Integrations**
Databases, REST APIs, search, files and enterprise systems.

**7.3 A2A**
Agent-to-agent protocols that let independent agents talk to each other.

## 8. Memory

**8.1 Working Memory**
Scratch state for the current task.

**8.2 Conversation Memory**
What was said in this session.

**8.3 Episodic Memory**
Records of past events and interactions.

**8.4 Semantic Memory**
Distilled facts and knowledge.

**8.5 Procedural Memory**
Learned how-tos and skills.

**8.6 User / Profile Memory**
Stable facts and preferences about the user.

**8.7 Long-Term Memory**
Persistent storage across sessions.

**8.8 Memory Tooling**
Mem0, TencentDB memory approaches, LangGraph persistence and checkpoints, Redis, vector DB memory and graph-based memory.

**8.9 Memory Lifecycle**
Write → extraction → consolidation → retrieval → forgetting / TTL → conflict resolution.

## 9. Prompt / Program Engineering

**9.1 Zero-Shot**
Instructions only, with no examples.

**9.2 Few-Shot**
Instructions plus a handful of worked examples.

**9.3 DSPy**
Treat prompts as programs and optimise them automatically against a metric.

# Phase 4: Model Adaptation and Evaluation

## 10. Fine-Tuning

**10.1 Prompt Engineering**
Adapt the model's behaviour without changing its weights.

**10.2 RAG**
Adapt through external knowledge instead of training.

**10.3 SFT**
Supervised fine-tuning on input-output pairs, including instruction tuning.

**10.4 PEFT**
Parameter-efficient tuning with LoRA and QLoRA: train small adapters instead of the full model.

**10.5 Preference Optimization**
Align the model to preferred answers using DPO.

**10.6 Reinforcement Fine-Tuning**
Train with reward signals from graders or verifiers.

**10.7 Distillation**
Teach a small model to imitate a larger one.

**10.8 Continued Pretraining**
Extend the model's knowledge with domain text.

**10.9 POC: RAG vs Fine-Tuning vs RAG + Fine-Tuning**
Compare the three approaches on the same task and dataset.

## 11. Evaluation

**11.1 RAG Evaluation**
RAGAS metrics: faithfulness, context precision, context recall and answer relevance.

**11.2 LLM-as-a-Judge**
An LLM scores outputs, using DeepEval or a custom judge.

**11.3 Custom Metrics**
Domain-specific scores that fit your use case.

**11.4 Golden Dataset**
A curated set of questions with expected answers.

**11.5 Regression Testing**
Re-run evals on every change to catch quality drops.

**11.6 Human Evaluation**
People rate outputs as the ground truth.

**11.7 Pairwise Evaluation**
Compare two outputs head to head.

**11.8 Agent Evaluation**
Score task success, number of steps and trajectory quality.

**11.9 Tool-Call Evaluation**
Check that the right tool was called with the right arguments.

**11.10 POC: RAGAS vs DeepEval vs Custom LLM-as-a-Judge vs Human Labels**
Measure how well each automated method agrees with human judgement.

# Phase 5: Production

## 12. Observability

**12.1 Tracing Tools**
Langfuse, Arize Phoenix, OpenTelemetry and LangSmith.

**12.2 What to Trace**
User query, retrieval, reranking, prompt, model, tool calls, tokens, cost, latency and evaluation score.

## 13. AI Safety / Guardrails

**13.1 Prompt Injection**
Detect instructions hidden in inputs or retrieved content.

**13.2 Jailbreak Detection**
Catch attempts to get around the model's rules.

**13.3 PII Detection**
Find and mask personal data.

**13.4 Data Leakage**
Prevent sensitive data from leaving through outputs or tools.

**13.5 Toxicity**
Filter harmful or abusive language.

**13.6 Hallucination Detection**
Flag claims the sources do not support.

**13.7 Grounding Verification**
Check each answer against the retrieved evidence.

**13.8 Tool Permissions**
Limit what tools and agents are allowed to do.

**13.9 Content Filtering**
Apply policy filters to inputs and outputs.

**13.10 Human Approval**
Require sign-off before high-risk actions.

## 14. Multimodal AI

**14.1 Text → Image Understanding**
Ask questions about images.

**14.2 PDF / Document Intelligence**
Extract structure and meaning from documents.

**14.3 OCR + LLM**
Read scanned text, then reason over it.

**14.4 Charts / Tables**
Interpret visual data and tabular data.

**14.5 Vision-Language Models**
Models that take images and text together.

**14.6 Audio → LLM**
Feed audio into the model.

**14.7 Speech → LLM**
Transcribe speech, then process it.

**14.8 Multimodal RAG**
Retrieve across several modalities.

## 15. Structured Generation / Constrained AI

**15.1 JSON Schema**
Define the exact output shape the model must produce.

**15.2 Pydantic Structured Output**
Typed Python models for LLM output, a natural fit with FastAPI.

**15.3 Function Calling**
Get arguments back that match a function's signature.

**15.4 Constrained Decoding**
Force tokens to follow a grammar or schema during generation.

**15.5 Validation / Retry**
Validate the output and re-prompt when it fails.

**15.6 Schema Repair**
Fix almost-valid output instead of discarding it.

**15.7 Example Flow**
User → LLM → Pydantic schema → validation → business API.

## 16. Production Model Engineering

**16.1 Model Routing**
Send each request to the best-fit model.

**16.2 Model Fallback**
Switch to a backup model when the primary fails.

**16.3 Small vs Large Models**
Use cheap models where they suffice and large ones where they are needed.

**16.4 Quantization**
Shrink model weights for faster, cheaper inference.

**16.5 Caching**
Reuse responses or prompt prefixes.

**16.6 Batching**
Group requests to increase throughput.

**16.7 Streaming**
Return tokens as they are generated.

**16.8 Rate Limits**
Handle provider limits and quotas.

**16.9 Token Optimization**
Cut tokens without losing quality.

**16.10 Cost / Latency / Quality Trade-offs**
Balance the three for each use case.

---

## POC Tracker

**01 RAG** (Fundamentals done)
Simple, Hybrid, Reranking, Multi-Hop, HyDE, GraphRAG, Adaptive / CRAG / Self-RAG, Agentic RAG.

**02 Context Engineering**
Selection, compression, prioritization and window management.

**03 Harness Engineering**
Tools, permissions, guardrails, verification, recovery and audit.

**04 Loop Engineering**
Evaluate-and-retry loops with clear termination.

**05 Agentic AI**
Tool calling, single agent, multi-agent, human-in-the-loop.

**06 MCP / A2A**
MCP servers and agent-to-agent communication.

**07 Memory**
Layered memory, Mem0, TencentDB.

**08 Prompt / Program Engineering**
DSPy.

**09 Fine-Tuning**
SFT, LoRA / QLoRA, DPO, distillation.

**10 Evaluation**
RAGAS, DeepEval, LLM-as-a-Judge, custom evaluation.

**11 Observability**
Langfuse, Phoenix, OpenTelemetry.

**12 Guardrails / AI Safety**
Injection, PII, hallucination and permission controls.

**13 Multimodal AI**
Documents, OCR, vision, audio and speech.

**14 Structured Generation**
Schema-validated output into business APIs.

**15 Production AI**
Routing, caching, cost, latency, security, monitoring.