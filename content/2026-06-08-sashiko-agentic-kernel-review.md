Title: Sashiko — The AI That Catches Kernel Bugs Humans Already Missed
Date: 2026-06-08
Category: GenAI Engineering
Tags: agentic-ai, linux-kernel, code-review, rust, llm, sashiko
Slug: sashiko-agentic-kernel-review

Sashiko (刺し子, "little stabs") borrows its name from a Japanese reinforcement-stitching technique — fabric repaired and strengthened at its points of wear. The metaphor is the whole pitch: an agentic system that stitches over the weak spots in proposed Linux kernel patches before they land. It's written in Rust (~85% of the repo), Apache-2.0 licensed under the Linux Foundation, and self-contained — no external agentic CLI tools, just patches in and structured reviews out.

What makes it interesting isn't "LLM reviews code" — that's commodity now. It's that someone built a vertical, domain-locked review agent for the hardest possible target and then published numbers.

## The Numbers Worth Pausing On

**53.6% bug-catch rate** — Against the last 1000 upstream commits carrying `Fixes:` tags (using Gemini 3.1 Pro), Sashiko surfaced more than half the bugs. The kicker: 100% of those bugs already passed human review and made it into the mainline tree. So on this sample, the tool is operating *above* the human bar that already failed.

**~20% false positive ceiling** — Measured loosely via manual review, with the maintainers candidly noting most of it lives in a "gray zone" rather than being flatly wrong. Honest framing — they also flag that output is probabilistic, so the same patch can yield different findings run to run.

## The Nine-Stage Protocol

This is the part I'd steal for my own agent work. Sashiko doesn't do one monolithic "review this" prompt — it runs a multi-stage protocol mimicking a team of specialists, each with a narrow mandate:

**Stage 1 — Main goal analysis** — Big-picture architectural flaws, UAPI breakages, conceptual correctness.

**Stage 2 — Implementation verification** — Does the code actually do what the commit message claims? Missing pieces, undocumented side-effects, API contract violations.

**Stage 3 — Execution flow** — Traces C execution paths for logic errors, unchecked returns, unhandled error paths, off-by-ones.

**Stage 4 — Resource management** — Memory leaks, use-after-free, double frees, object lifecycles across queues, timers, workqueues.

**Stage 5 — Locking and synchronization** — Concurrency bugs, deadlocks, RCU rule violations, thread-safety.

**Stage 6 — Security audit** — Buffer overflows, OOB reads/writes, TOCTOU races, uninitialized-memory leaks.

**Stage 7 — Hardware engineer's review** — Driver-specific: register accesses, DMA mapping, memory barriers, state machine constraints.

**Stage 8 — Verification and severity** — Consolidates stages 1–7, deduplicates, and tries to logically prove/disprove findings to kill false positives.

**Stage 9 — Report generation** — Converts confirmed findings into a polite, inline-commented LKML email reply.

The architecture lesson here maps directly onto what I keep arguing with AgentLegatus — agents fail at boundaries, and schemas are boundaries. Sashiko draws hard boundaries between review concerns instead of asking one prompt to hold the entire kernel's failure surface in its head at once. Stage 8 as an adversarial consolidation layer is the move: separate finding from confirmation.

## How It Actually Runs

**Ingestion** — Two paths: automated monitoring of mailing lists via `lore.kernel.org`, or manual ingestion from a local git repo.

**Providers** — Gemini and Claude both supported. Claude setup uses `claude-sonnet-4-5` with a 200K context window, prompt caching (5-min TTL) to cut repeated-context cost, and full tool calling for git operations.

**Interfaces** — Web UI and a CLI today; email support is on the roadmap.

**Prompts** — Per-subsystem and generic prompts, building on the review-prompts work originally developed by Chris Mason.

## The Disclaimers Are the Honest Part

Two warnings the README doesn't bury, and shouldn't:

**Data privacy** — Sashiko ships patches *and* potentially large slices of kernel git history to your configured LLM provider to give it enough context. For kernel work that's all public, but the pattern — "we send way more than the diff" — is the thing to internalize before you point a tool like this at anything proprietary.

**Cost** — Reviewing at volume against a 200K-context model is not cheap, and the authors explicitly disclaim responsibility for surprise API bills. Token monitoring is on you.

## Why This Matters for Practitioners

The hype read is "AI beats human kernel reviewers." The useful read is narrower and more durable: a focused agent, a staged protocol with explicit separation of concerns, a self-disproving verification stage, and published metrics with stated error bars beats a general-purpose "review my code" wrapper every time. The 53.6% figure is impressive precisely *because* the bar was bugs humans already missed — not a synthetic benchmark.

For anyone building agentic review systems: the takeaway isn't the kernel domain, it's the decomposition. Nine bounded reviewers and a skeptic at the end will outperform one omniscient prompt, and the cost/privacy footprint is a first-class design constraint, not a footnote.

## Repos

- [https://github.com/sashiko-dev/sashiko](https://github.com/sashiko-dev/sashiko) (upstream)
- [https://github.com/rajacsp/sashiko](https://github.com/rajacsp/sashiko) (fork)
