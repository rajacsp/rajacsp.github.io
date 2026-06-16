Title: GraphRAG for Mainframe Abend Troubleshooting with AgentScope
Date: 2026-06-12
Category: GenAI
Tags: GenAI, RAG, KnowledgeGraph, AgentScope, Mainframe, GraphRAG, Python, COBOL
Slug: graphrag-mainframe-abend-troubleshooting-agentscope

Most mainframe troubleshooting RAGs fail at the same place: retrieval. An abend code like S0C7 is a near-exact lookup, not a fuzzy semantic match — but vector search happily returns the S0C4 chunk because the embeddings sit close together. And job dependencies are graph-shaped: an abend in step 3 cascades to downstream jobs, and plain RAG flattens that structure into disconnected paragraphs. The fix is a knowledge graph that traverses real relationships instead of guessing with cosine similarity.

## The Core Idea

**Structure over similarity** — Mainframe docs encode jobs, steps, abend codes, and fixes with strict relationships. Model those as typed nodes and edges so the agent traverses known paths instead of hoping a vector match lands on the right text.

**Schema is the boundary** — Every md file gets parsed into one fixed node/edge structure. The LLM never reasons over raw document shape; it queries known types. This is where accuracy comes from.

## Step 1 — Define the Schema

Five node types and a handful of edge types cover most batch environments:

```
Node types:    JOB, STEP, ABEND, DATASET, REMEDIATION

Edge types:    JOB   -HAS_STEP->     STEP
               STEP  -RAISES->       ABEND
               ABEND -RESOLVED_BY->  REMEDIATION
               JOB   -TRIGGERS->     JOB        (downstream dependency)
               STEP  -READS/WRITES-> DATASET
```

## Step 2 — Parse the MD Files into the Graph

Codes follow strict formats, so regex handles the deterministic bits. Prose remediation text may need an LLM extraction pass for messier docs.

```python
# build_graph.py
import re
import networkx as nx

ABEND_RE = re.compile(r'\b([SU]\d{3,4}|U\d{4})\b')   # S0C7, U4038
JOB_RE   = re.compile(r'\bJOB[_A-Z0-9]+\b')

def parse_md_to_graph(md_text: str) -> nx.DiGraph:
    g = nx.DiGraph()
    current_job = current_step = None

    for line in md_text.splitlines():
        if line.startswith("## "):                       # ## JOB_PAYROLL
            jobs = JOB_RE.findall(line)
            if jobs:
                current_job = jobs[0]
                g.add_node(current_job, type="JOB")

        elif line.startswith("### ") and current_job:     # ### STEP04
            current_step = line.replace("###", "").strip()
            g.add_node(current_step, type="STEP")
            g.add_edge(current_job, current_step, rel="HAS_STEP")

        elif current_step:
            for ab in ABEND_RE.findall(line):
                g.add_node(ab, type="ABEND")
                g.add_edge(current_step, ab, rel="RAISES")
                rem = line.split(ab, 1)[-1].strip(" :-")
                if rem:
                    rem_id = f"FIX::{ab}::{hash(rem) & 0xffff}"
                    g.add_node(rem_id, type="REMEDIATION", text=rem)
                    g.add_edge(ab, rem_id, rel="RESOLVED_BY")

        if current_job and "trigger" in line.lower():
            for dep in JOB_RE.findall(line):
                if dep != current_job:
                    g.add_edge(current_job, dep, rel="TRIGGERS")

    return g
```

Tune the section markers and regex to your actual md conventions — the principle holds regardless.

## Step 3 — Query Functions (the Agent's Tools)

Deterministic traversals. No embeddings, no LLM, no similarity error on the code lookup.

```python
# graph_tools.py
import json
import networkx as nx

g = nx.read_gml("abend_graph.gml")

def query_abend(abend_code: str) -> str:
    """Remediations + which steps/jobs raise a given abend code."""
    if abend_code not in g:
        return json.dumps({"found": False, "abend": abend_code})

    remediations = [g.nodes[n].get("text", n)
                    for n in g.successors(abend_code)
                    if g.edges[abend_code, n].get("rel") == "RESOLVED_BY"]

    raised_by = [s for s in g.predecessors(abend_code)
                 if g.edges[s, abend_code].get("rel") == "RAISES"]

    jobs = []
    for step in raised_by:
        jobs += [j for j in g.predecessors(step)
                 if g.edges[j, step].get("rel") == "HAS_STEP"]

    return json.dumps({
        "found": True, "abend": abend_code,
        "remediations": remediations,
        "raised_by_steps": raised_by,
        "jobs": list(set(jobs)),
    })

def downstream_impact(job: str) -> str:
    """Jobs that fail or delay if this job abends — the cascade."""
    if job not in g:
        return json.dumps({"found": False, "job": job})
    affected = [v for u, v in nx.edge_dfs(g, job)
                if g.edges[u, v].get("rel") == "TRIGGERS"]
    return json.dumps({"job": job, "downstream_jobs": affected})
```

## Step 4 — Wire into AgentScope

The graph handles structure; vector RAG stays as the fallback for open-ended prose questions. The agent picks the right tool.

```python
# agent.py
import asyncio
from agentscope.agent import ReActAgent
from agentscope.tool import Toolkit
from agentscope.message import Msg
from graph_tools import query_abend, downstream_impact
from rag_tools import retrieve_docs   # your existing vector RAG

toolkit = Toolkit()
toolkit.register_tool_function(query_abend)        # exact structured lookup
toolkit.register_tool_function(downstream_impact)  # dependency cascade
toolkit.register_tool_function(retrieve_docs)      # semantic fallback

agent = ReActAgent(
    name="mainframe_ops",
    sys_prompt=(
        "You troubleshoot mainframe batch jobs. For a specific abend code, "
        "ALWAYS call query_abend first. To assess the blast radius of a failed "
        "job, call downstream_impact. Use retrieve_docs only for open-ended "
        "questions the graph cannot answer. Never invent abend semantics."
    ),
    model=...,           # your model wrapper
    toolkit=toolkit,
)

async def main():
    q = Msg("user",
            "JOB_PAYROLL step 4 hit S0C7. What do I do, and what breaks downstream?",
            role="user")
    print((await agent(q)).content)

asyncio.run(main())
```

## Why This Lifts Accuracy

**No similarity error on codes** — `query_abend("S0C7")` walks ABEND -> RESOLVED_BY directly. S0C7 and S0C4 can no longer be confused because there is no embedding step in the lookup path.

**Real cascade reasoning** — `downstream_impact` traverses TRIGGERS edges to return the actual blast radius — something flat vector RAG structurally cannot do.

**Graceful fallback** — Vector retrieval stays for "how do I..." prose questions, so you lose nothing and gain structured precision.

## The Honest Order of Operations

Build hybrid retrieval (exact code match + vector) first, then this graph layer. Most mainframe abend RAGs become good enough right here at Step 4 — the probabilistic layer (PKG + MCMC) is worth adding only if you have genuine multi-cause, cross-job causal uncertainty left to resolve after the graph is in place.

One thing to confirm: verify the AgentScope import paths against your installed version — the `agentscope.agent` and `agentscope.tool` namespaces have moved across releases.