Title: Using Free Cloud-Based LLMs via Ollama on Ubuntu
Date: 2026-04-19
Category: GenAI Engineering
Tags: ollama, llm, ubuntu, cloud-llm, local-ai, kactii, linux
Slug: using-free-cloud-llms-via-ollama-ubuntu

---

Ollama is a lightweight, open-source LLM runner. Its `:cloud` model suffix lets you route prompts to free-tier hosted models — no GPU, no paid API key required. Useful for learning, prototyping, and small projects on modest hardware.

This post covers the full Ubuntu setup: manual install, service startup, chatting with Kimi K2.5, fixing a common CLI error, and exposing the API to your local network.

---

## Why Manual Install?

**Official one-liner risk** — The `curl ... | sh` script fetches assets from GitHub at runtime. Unstable GitHub connectivity breaks it mid-install.

**Offline alternative** — Download `ollama-linux-amd64.tar.zst` (~1.9 GB) from the GitHub Releases page separately, transfer via USB or SCP, install without runtime dependency.

---

## Step 1 — Download and Transfer

**From a stable machine** — Visit `https://github.com/ollama/ollama/releases`, grab `ollama-linux-amd64.tar.zst` from the latest release, copy to USB or SCP to Ubuntu.

**VMware USB tip** — If Ubuntu inside VMware doesn't detect the USB drive, go to VM Settings → USB Controller → set compatibility to USB 3.2.

---

## Step 2 — Extract and Organize

**Create a local bin** — In your home directory, create `~/bin/ollama-install/` and paste the archive there.

**Extract** — Run `tar -xf ollama-linux-amd64.tar.zst`. You'll get `bin/` and `lib/` subfolders. The `ollama` executable lives inside `bin/`.

**No system install needed** — Run Ollama directly from this path. No `sudo`, no `/usr/local/bin` required.

---

## Step 3 — Start the Service

```bash
cd ~/bin/ollama-install/bin
./ollama serve
```

**Verify in browser** — Open `http://127.0.0.1:11434`. You should see `Ollama is running`.

**Verify in terminal** — Run `ps -ef | grep ollama` and confirm `./ollama serve` is listed.

---

## Step 4 — Chat With a Free Cloud Model

**Launch the interactive menu** — In a second terminal:

```bash
./ollama launch
```

**Select a cloud model** — Choose `chat with a model`, then pick any model with a `:cloud` suffix, e.g., `kimi-k2.5:cloud`.

**Authenticate** — Ollama opens a browser tab for login. If it doesn't open, copy the URL from terminal manually (remove any stray spaces).

**Example session:**

```
You:   What LLM are you using?
Model: I am Kimi, developed by Dark Side of the Moon Technology Co., Ltd.,
       part of the Kimi K2.5 series.
```

The model runs on Kimi's distributed cloud servers — not your local machine.

---

## Step 5 — Fix the `launch` Error

**Error you may see** — `error running model flag accessed but not defined verbose`

**Root cause** — The `launch` subcommand has parameter compatibility issues with certain cloud models.

**Fix** — Use `run` directly:

```bash
./ollama run kimi-k2.5:cloud
```

**Best practice** — Always prefer `ollama run <model>` for scripted or production use. Use `launch` for exploration only.

---

## Step 6 — Expose Ollama to Other Machines

**Find your Ubuntu IP:**

```bash
sudo apt install net-tools  # if ifconfig is missing
ifconfig
# e.g. 192.168.204.129
```

**Bind to all interfaces:**

```bash
export OLLAMA_HOST=0.0.0.0:11434
```

**Restart the service:**

```bash
pkill -9 ollama
./ollama serve
```

**Test locally first** — Hit `http://192.168.204.129:11434` from Ubuntu's browser. Then point any Ollama-compatible client (OpenClaw, Open WebUI, Continue) on another machine to the same URL.

**Security note** — This binds to your local network only. For internet-facing access, add firewall rules and authentication.

---

## What's Next

**Pull local models** — `ollama run llama3` runs fully offline once downloaded.

**Python integration** — Use the `requests` library against `http://localhost:11434/api/generate`.

**Connect AI clients** — Continue, OpenClaw, and Open WebUI all support Ollama as a backend out of the box.