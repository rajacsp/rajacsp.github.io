Title: 50 Basic GenAI Engineer Interview Questions
Date: 2026-06-02
Category: GenAI
Tags: genai, interview, llm, rag, fine-tuning, mlops
Slug: 50-basic-genai-engineer-interview-questions

A starter question bank for screening entry-level GenAI engineers. Grouped by theme, covering fundamentals through production concerns.

## Fundamentals

1. **What is generative AI vs discriminative AI?** — Generative models learn to produce new data; discriminative models learn decision boundaries to classify or predict.

2. **What is a large language model (LLM)?** — A neural network trained on large text corpora to predict tokens, capable of broad language tasks.

3. **Transformer architecture** — Asks for a high-level grasp of attention-based sequence modeling without recurrence.

4. **Attention mechanism** — How a model weighs the relevance of different tokens when producing a representation.

5. **Self-attention vs cross-attention** — Self-attention relates tokens within one sequence; cross-attention relates one sequence to another.

6. **Tokens and tokenization** — How raw text is split into model-readable units and why the scheme matters.

7. **Context window** — The maximum number of tokens a model can attend to at once.

8. **Embeddings** — Dense vector representations of meaning, used for search, clustering, and retrieval.

9. **Encoder vs decoder vs encoder-decoder** — Architectural families and the task types each suits.

10. **Pretraining vs fine-tuning** — Broad foundational training vs targeted adaptation to a task or domain.

## Prompting & Inference

11. **Prompt engineering** — Designing inputs to reliably steer model behavior.

12. **Zero-shot vs few-shot prompting** — No examples vs in-context examples to guide the output.

13. **Chain-of-thought prompting** — Eliciting intermediate reasoning steps to improve answers.

14. **Temperature and top-p** — Controls over randomness and the sampling distribution of generated tokens.

15. **Greedy decoding vs sampling** — Always taking the top token vs probabilistic selection for diversity.

16. **System prompt** — Instructions that set persistent behavior and role for the model.

17. **Hallucinations** — Why models invent plausible-but-false content and how to mitigate it.

18. **Max tokens parameter** — Caps output length and affects cost and truncation.

19. **In-context learning** — Learning a task purely from examples in the prompt, no weight updates.

20. **Prompt injection** — Adversarial inputs that hijack instructions and defenses against them.

## RAG (Retrieval-Augmented Generation)

21. **What is RAG and why use it?** — Grounding generation in retrieved documents to reduce hallucination and add fresh knowledge.

22. **Vector database** — Storage and similarity search over embeddings.

23. **Semantic vs keyword search** — Meaning-based retrieval vs literal term matching.

24. **Chunking and chunk size** — Splitting documents for retrieval and the tradeoffs of granularity.

25. **Cosine similarity** — A measure of vector closeness used to rank retrieved items.

26. **Embedding model in RAG** — Converts queries and documents into the shared vector space.

27. **Re-ranking** — A second-stage scoring pass to refine retrieved candidates.

28. **Evaluating a RAG system** — Measuring retrieval relevance and answer faithfulness.

29. **Hybrid search** — Combining sparse (keyword) and dense (vector) retrieval.

30. **Handling context overflow** — Strategies when retrieved content exceeds the window.

## Fine-tuning & Training

31. **Full vs parameter-efficient fine-tuning** — Updating all weights vs a small subset for cost savings.

32. **LoRA** — Low-rank adapters that fine-tune efficiently with few trainable parameters.

33. **Quantization** — Reducing numerical precision to shrink models and speed inference.

34. **RLHF** — Aligning models to human preferences via a reward signal.

35. **Instruction tuning** — Training on instruction-response pairs to improve task following.

36. **Catastrophic forgetting** — Loss of prior capabilities after further training.

37. **SFT vs RLHF** — Supervised fine-tuning vs preference-based reinforcement.

38. **Fine-tune vs RAG vs prompting** — When each approach is the right tool.

39. **Data needed to fine-tune** — Quantity, quality, and format requirements.

40. **Overfitting** — Memorizing training data and how to detect it.

## Evaluation & Production

41. **Evaluating LLM output quality** — Approaches to judging open-ended generation.

42. **Generative text metrics** — BLEU, ROUGE, perplexity and their limits.

43. **LLM-as-a-judge** — Using a model to score outputs and its biases.

44. **Reducing latency** — Techniques like streaming, caching, and smaller models.

45. **Controlling inference cost** — Token budgeting, model selection, and caching.

46. **Model distillation** — Training a smaller model to mimic a larger one.

47. **Guardrails** — Constraints on inputs and outputs for safety and compliance.

48. **Monitoring in production** — Tracking quality, drift, cost, and failures.

49. **Safety and ethical risks** — Bias, misuse, privacy, and misinformation concerns.

50. **Agent vs simple LLM call** — Multi-step tool-using systems vs single-shot generation.