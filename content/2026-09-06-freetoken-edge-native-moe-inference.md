Title: UC Berkeley Open-Sources FreeToken: Frontier-Scale MoE on Consumer Hardware
Date: 2026-09-05
Category: AI Infrastructure
Tags: MoE, Inference, Edge AI, Open Source, LLM
Slug: freetoken-edge-native-moe-inference
Status: Published

UC Berkeley has open-sourced **FreeToken**, an edge-native inference engine that runs frontier-scale Mixture-of-Experts (MoE) models on consumer hardware. It treats GPU, CPU, host memory, and PCIe interconnects as a single unified inference platform.

The approach works because of how MoE models are structured. A model like DeepSeek-V4-Flash carries 284B total parameters but activates only 13B per token — 6 of 256 routed experts at each layer. The per-token computation is feasible; the real problem is that the full expert pool must stay accessible in memory, far exceeding GPU VRAM.

FreeToken resolves this with a two-level hierarchy. Non-expert weights stay resident on the GPU, the full expert pool lives in host RAM, and only the experts needed for each token are fetched over PCIe. A bandwidth-adaptive policy continuously decides whether to fetch experts to the GPU or compute them on CPU, based on the machine's actual measured PCIe bandwidth.

The results span a wide hardware range: an 8GB-VRAM laptop runs Qwen3.6-35B, a single RTX 5090 runs DeepSeek-V4-Flash at 284B, and a workstation GPU runs GLM-5.2 at 753B. No GGUF conversion is required — it loads HuggingFace safetensors directly, is OpenAI- and Anthropic-API compatible on localhost, and ships with a native GUI, one-click install on Windows and Linux, and built-in agent harnesses.

## Key Capabilities

**Two-Level Expert Hierarchy** GPU holds non-expert weights while the full expert pool resides in host RAM. This keeps the always-needed weights fast and the large expert pool addressable.

**Bandwidth-Adaptive Co-Execution** CPU-GPU execution is calibrated to your machine. The engine measures real PCIe bandwidth and routes expert work accordingly.

**Global LRU Expert Caching** Least-recently-used caching operates across all MoE layers. Frequently used experts stay hot rather than being refetched.

**Semantic-Aware KV Caching** KV caching is tuned for agentic workflows. It preserves reusable context across multi-step agent runs.

**Direct Safetensors Loading** HuggingFace safetensors load directly with no GGUF conversion. This removes a conversion step from the deployment path.

**Local API Compatibility** OpenAI and Anthropic APIs are supported on localhost. Existing clients can point at the local endpoint unchanged.

**Native GUI with Agent Harnesses** A native interface ships with agent harnesses built in. One-click install is available on Windows and Linux.

FreeToken is 100% open source.

Links:

- Paper: [https://arxiv.org/pdf/2608.16157](https://arxiv.org/pdf/2608.16157)
- Repo: [https://github.com/FlashML-org/FreeToken](https://github.com/FlashML-org/FreeToken)
