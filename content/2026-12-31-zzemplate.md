Title: Your Title Here
Date: 2026-01-01
Category: GenAI
Tags: GenAI, LLM, tag1, tag2
Slug: your-slug-here
Status: draft

Write your intro paragraph here. Keep it short and punchy — set the stage for what follows.

## Section Heading

**Term or Concept** — One or two line explanation of what it is and why it matters. Keep it concise and useful.

**Another Term** — Another brief explanation. Link to sources if needed.

## Another Section

Content goes here. Use markdown formatting as needed.

- Bullet point one
- Bullet point two

> Optional blockquote for emphasis or callouts.
> ![1775918663065]({static}/image/2026-04-04-zzemplate/1775918663065.png)

Title: WeeLLM — Running 20B Diffusion Models on a 4GB GPU
Date: 2026-08-21
Category: Inference
Tags: diffusion, low-vram, layer-streaming, flux, local-inference
Slug: weellm-layer-streaming-inference
Status: Draft

WeeLLM is a layer-streaming inference engine for large diffusion models. Its
one claim is unusual: run a ~12B FLUX model, or even a ~20B Qwen-Image model,
in under 4GB of VRAM — with no quantization. Full bfloat16 weights, degraded
only in speed, never in precision.

## The Core Idea

**Layer Streaming**
The whole model never sits in VRAM at once. One transformer layer is loaded
from disk, executed, evicted, and the next takes its place. Peak VRAM is
bounded by the largest single layer, not the total parameter count.

    Traditional:   [ load ALL layers into VRAM ] -> run
                   VRAM cost ~= full model size

    WeeLLM:        for step in denoising_steps:
                       for layer in model:
                           load(layer)  -> GPU
                           run(layer)
                           evict(layer)
                   VRAM cost ~= one layer

**The Payoff**
This decoupling of VRAM from parameter count is why the benchmarks invert
what you'd expect — a 20B model can cost less VRAM than a 6.6B one.

    FLUX.1-dev     ~12B params   ->  1.51 GB peak VRAM
    Qwen-Image     ~20B params   ->  2.47 GB peak VRAM
    SDXL           ~6.6B params  ->  2.98 GB peak VRAM

## Why It Works for Diffusion

**The Step Count Is the Trick**
Diffusion models denoise a latent over a handful of discrete steps, typically
4 to 20. The full weight set is streamed from disk only that many times per
image — costly, but finite.

    FLUX.1-schnell ->  4 steps ->  4 disk sweeps  -> ~159s
    SDXL           -> 20 steps -> 20 disk sweeps  -> ~120s

**Where It Breaks: Autoregressive Models**
Vision-language and autoregressive image models generate pixels as tokens,
sequentially. A 1024x1024 image is 1000+ tokens = 1000+ full forward passes.

    20GB model  x  1000 forward passes  =  ~20 TB streamed from disk
                                        =  several hours per image

The code runs, but the wall-clock time is impractical. WeeLLM is upfront about
this: for those models, use quantization instead.

## The Hard Dependency: Disk I/O

**Disk Is the Bottleneck**
Every layer is re-read from disk on every step, so the disk *is* the engine.
This architecture is built for local NVMe SSDs, not throttled cloud volumes.

    Fast local NVMe   ->  streaming keeps the GPU fed
    Cloud disk (T4)   ->  throttled I/O -> severe slowdown

**The bfloat16 Trap on Older GPUs**
On Turing cards (Kaggle/Colab T4), bfloat16 isn't natively supported. Forcing
it silently disables FlashAttention and falls back to the Math backend, which
materializes the full N x N attention matrix — blowing the VRAM budget you
came here to save.

    Symptom:  expected ~2 GB, saw 6 GB+
    Cause:    --dtype bfloat16 on non-supporting hardware
    Fix:      match dtype to what the GPU actually supports

## Using It

**CLI — Point It at a Hugging Face Repo ID**
No manual download step. Pass a repo ID and a prompt; it streams directly from
the HF safetensors.

    pip install -r requirements.txt

    python main.py
        --model black-forest-labs/FLUX.1-dev
        --prompt "A majestic lion at golden hour"

**Python API**
The same engine wrapped as a pipeline object, with RAM caching optional.

    from weellm import WeePipeline

    pipe = WeePipeline.from_pretrained(
        "Tongyi-MAI/Z-Image-Turbo",
        device="cuda",
        cache_to_ram=False,
    )
    image = pipe.generate(
        prompt="A serene Japanese zen garden at sunrise",
        height=512, width=512,
        num_inference_steps=4,
        seed=42,
    )
    image.save("output.png")

## The Verdict

**What It Buys You**
State-of-the-art image models on consumer hardware you'd normally be told is
far too weak — an RTX 3050 running full-precision FLUX and Qwen-Image.

**What It Costs**
Time. Generation runs into minutes for the biggest models. The trade is memory
for wall-clock, and it only holds on a fast local SSD with diffusion-style
models. Inside that envelope, it's a genuinely clever piece of engineering.
