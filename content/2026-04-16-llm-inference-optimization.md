Title: LLM Inference Optimization: What Actually Makes Your Model Fast
Date: 2026-04-18
Category: GenAI
Tags: LLM, Inference, Optimization, Quantization, KV Cache, Speculative Decoding, Flash Attention
Slug: llm-inference-optimization-techniques

When you send a prompt to an LLM, three layers shape how fast you get a response: the hardware (GPUs, TPUs, LPUs), the model size and architecture, and the inference engine strategies sitting on top. Most of the latency battle is fought at that third layer — and the core problem is this: token generation is memory-bound. Loading model weights to produce a single token is expensive. Once those weights are loaded, the compute itself costs almost nothing. Every technique below attacks that bottleneck from a different angle.

## The Optimization Techniques

**Quantization**
Store model weights in lower precision — 4-bit or 8-bit instead of 32-bit floats. Smaller weights mean less memory to load per token. Result: 4–8× memory reduction, 2–4× faster token generation. This is the lowest-effort, highest-leverage starting point for local inference (yes, this is exactly why llama.cpp runs well on consumer hardware).

**Speculative Decoding**
A small, fast draft model predicts the next K tokens. The large model then evaluates those predictions in parallel and accepts or rejects them based on probability alignment. Accepted tokens are kept; rejected ones fall back to the large model for correction. Result: 2–3× faster generation because the large model validates in bulk rather than generating token-by-token.

**KV Cache**
Transformer decoders are autoregressive — they recompute key-value pairs for every input token at every step. KV Cache stores those computed values and reuses them across steps instead of recalculating. Result: 10–100× faster generation for long contexts, since you stop paying for redundant math.

**PagedAttention (KV Cache Memory Management)**
Standard KV Cache reserves a fixed memory block upfront — leading to fragmentation and waste. PagedAttention breaks the cache into small pages and allocates new ones only as needed, borrowing the idea from OS virtual memory management. Result: 2–4× higher throughput across concurrent users because memory is used dynamically, not hoarded.

**Flash Attention**
Attention computation is dominated by matrix multiplications, but the actual bottleneck is data movement between HBM and compute units — not the math itself. Flash Attention tiles the attention matrix into chunks that fit inside the chip's fast SRAM, minimizing round trips to slower memory. Result: 2–4× faster attention compute and headroom for much longer context windows.

**Continuous Batching**
Traditional batching pads sequences to a fixed length and waits for a full batch. Continuous batching packs sequences back-to-back without padding, slots new requests in the moment a slot opens, and handles long prompts via chunked prefill — breaking them into smaller pieces processed incrementally. Result: 10–20× higher throughput under real-world load because the GPU is never idling on padding tokens.

**Model Pruning**
Removes weights and entire layers that contribute little to output quality — essentially trimming the network down to its load-bearing structure. Result: ~25% size reduction, 1.3–3× faster generation depending on pruning aggressiveness and task type.

**Smaller Models**
The obvious one, but worth saying plainly: if a smaller model is good enough for your task, use it. No engineering trick beats the latency win of simply loading fewer parameters. Task-model fit is an inference strategy.

## The Mental Model

Think of inference optimization as a stack. Quantization shrinks what you load. KV Cache and PagedAttention cut what you recompute and how you manage that memory. Flash Attention speeds up the compute path itself. Speculative Decoding parallelizes the generation loop. Continuous Batching maximizes GPU utilization across the request queue. Pruning and model selection reduce the problem size before any of the above even kicks in.

Stack them right, and you go from a sluggish 70B model on shared hardware to a production-grade inference pipeline that feels fast for every user in the queue.