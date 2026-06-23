Title: From Static Graphs to Thinking Systems: Agentic GraphRAG for COBOL Codebases
Date: 2026-06-22
Category: Knowledge Graphs
Tags: GraphRAG, COBOL, LangGraph, Neo4j, Agentic AI, Legacy Modernization
Slug: agentic-graphrag-cobol-codebases
Status: published

Disclaimer:
This is a shadow article of https://medium.com/@vineetchachondia/from-static-graphs-to-thinking-systems-agentic-graphrag-for-cobol-codebases-fcea6d1b62a6
as Medium is paywalled

Part-3 of the Knowledge Graph Series

What if your legacy COBOL codebase could explain itself — collaboratively, intelligently, and on demand?

For decades, COBOL systems have quietly powered banks, insurance firms, and governments. And for decades, teams have struggled with the same questions:

- "Which programs read this file?"
- "What breaks if we touch this batch job?"
- "Who really understands this code?"

In the previous parts of this series, we explored Knowledge Graphs as a way to bring structure and relationships to legacy systems. But structure alone isn't enough anymore. We need systems that reason. We need systems that collaborate. We need Agentic GraphRAG.

This article shows how a team of AI agents can analyze a COBOL codebase, construct a Neo4j knowledge graph, enrich it semantically using LLMs, and let you query it in natural language — all in a production-ready architecture.

## Why Traditional RAG Breaks Down for COBOL

**Classic RAG treats code like documents**
Chunk → Embed → Retrieve → Generate. That approach fails for COBOL because the language is highly structured and meaning lives in relationships, not text.

**Behavior spans files**
Program behavior spreads across multiple files, and impact analysis requires graph traversal, not cosine similarity. This is exactly where GraphRAG shines — but even GraphRAG has a ceiling.

## The Missing Piece: Agency

**Static pipelines fall short**
Most GraphRAG systems parse everything, build the graph, then query it. Real systems don't work that way.

**Real analysis is dynamic**
It is incremental, multi-step, collaborative, and context-aware. That's where Agentic Architectures change the game.

## The COBOL Agentic Knowledge Graph System

This system treats code understanding as a team sport. Instead of one monolithic pipeline, we introduce 7 specialized agents, each with a clear responsibility, coordinated via LangGraph. Think of it as a virtual COBOL analysis team.

```
Ingestion Agent     → "What files do we have?"
Validation Agent    → "Is this valid COBOL?"
Parsing Agent       → "What entities and relations exist?"
Enrichment Agent    → "What does this code mean?"
Graph Builder Agent → "How do we model this in Neo4j?"
Cypher Agent        → "How do we query this?"
Retrieval Agent     → "What's the answer?"
```

Each agent does one thing well — and collaborates through shared state.

## Architecture at a Glance

```
cobol_agentic_kg/
├── agents/                 # Specialized AI agents
├── workflows/              # LangGraph orchestration
├── utils/                  # State, Neo4j, logging
├── ui/                     # Streamlit dashboard
└── tests/                  # Production-grade tests
```

**Tech Stack**
Python as the language, LangGraph for AI agents, OpenAI for the LLM, Neo4j for the knowledge graph, and Streamlit for the UI.

## How the Agents Collaborate

**Ingestion Agent**
Pulls COBOL files from upload or Git repositories. Tracks metadata, version, and progress.

```python
"""Ingestion Agent - Handles file uploads and repository scanning"""
import os
from typing import Dict, Any
from utils.state import CobolProcessingState
from utils.logger import logger
import chardet


class IngestionAgent:
    """Agent responsible for ingesting COBOL files"""

    def __init__(self):
        self.supported_extensions = ['.cob', '.cbl', '.cobol', '.cpy']

    def process(self, state: CobolProcessingState) -> CobolProcessingState:
        """
        Ingest COBOL file and extract metadata

        Args:
            state: Current processing state

        Returns:
            Updated state with file content and metadata
        """
        logger.info(f"🔽 INGESTION AGENT: Processing {state['file_path']}")

        try:
            # Read file with encoding detection
            file_content = self._read_file(state['file_path'])

            # Create metadata
            metadata = self._create_metadata(state['file_path'], file_content)

            # Update state
            return {
                **state,
                "file_content": file_content,
                "file_metadata": metadata,
                "stage": "ingestion",
                "status": "completed"
            }
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            return {
                **state,
                "stage": "ingestion",
                "status": "failed",
                "errors": state.get('errors', []) + [f"Ingestion error: {str(e)}"]
            }

    def _read_file(self, file_path: str) -> str:
        """
        Read file with automatic encoding detection

        Args:
            file_path: Path to file

        Returns:
            File content as string
        """
        # Try UTF-8 first
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding'] or 'utf-8'
            # Read with detected encoding
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                return f.read()

    def _create_metadata(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        Create file metadata

        Args:
            file_path: Path to file
            content: File content

        Returns:
            Metadata dictionary
        """
        return {
            "filename": os.path.basename(file_path),
            "directory": os.path.dirname(file_path),
            "size_bytes": len(content.encode('utf-8')),
            "line_count": content.count('\n'),
            "char_count": len(content),
            "extension": os.path.splitext(file_path)[1]
        }

    def is_cobol_file(self, file_path: str) -> bool:
        """
        Check if file is a COBOL file by extension

        Args:
            file_path: Path to file

        Returns:
            True if COBOL file, False otherwise
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.supported_extensions


# Create singleton instance
ingestion_agent = IngestionAgent()


# Wrapper function for LangGraph
def ingestion_agent_node(state: CobolProcessingState) -> CobolProcessingState:
    """LangGraph node wrapper"""
    return ingestion_agent.process(state)
```

**Validation Agent**
Filters out invalid or unsupported COBOL syntax early — saving time and tokens. (GitHub repo link at the bottom for full code.)

**Parsing Agent**
Extracts programs, data files, COPYBOOKS, CALL relationships, and READ / WRITE / UPDATE operations. This is where structure is born.

**Enrichment Agent (The Intelligence Layer)**
Using LLMs, this agent explains what a program does, infers business intent, tags batch vs online behavior, and adds semantic labels to graph nodes. Now your graph isn't just connected — it's understandable.

**Graph Builder Agent**
Transforms raw entities into a Neo4j knowledge graph. The result is queryable system intelligence.

```
(:CobolProgram)-[:READS]->(:DataFile)
(:Program)-[:CALLS]->(:Program)
(:Program)-[:USES]->(:Copybook)
```

**Cypher Generation Agent**
Ask "Which programs read customer master files?" and the agent converts it to Cypher — accurately and safely.

**Retrieval Agent**
Executes the query, validates results, and returns grounded answers. No hallucinations, no guesswork — only graph-backed truth.

## Natural Language → Graph Insights

```python
cypher_chain.invoke({
  "query": "Which programs read from a file?"
})
```

Generated Cypher:

```cypher
MATCH (p:CobolProgram)-[:READS]->(:DataFile)
RETURN DISTINCT p.id AS program_id
```

Query:

```
List all programs in the Finance domain
```

Generated Cypher:

```cypher
MATCH (p:CobolProgram) WHERE toLower(p.domain) = toLower('finance') RETURN p.name, p.summary, p.loc ORDER BY p.name
```

Response from LLM:

```
In the Finance domain, we have identified 14 key programs that handle various
financial operations. Notable programs include CBACT01C, which processes account
records, and CBSTM03A, which generates account statements. Programs like COBIL00C
facilitate bill payments, while COPAUA0C and its related programs manage card
authorization processes.

These programs are crucial for maintaining financial transactions and customer
account management, meaning any changes or maintenance will directly impact
financial reporting and customer service. It's important to ensure that updates
are carefully managed to avoid disruptions in these critical functions.
```

This is GraphRAG done right: deterministic, explainable, and auditable.

## The UI: Making the System Observable

A Streamlit dashboard lets you upload repositories, monitor agent progress, inspect graph growth, and query the knowledge graph interactively. This makes the system usable not just for engineers but for architects, modernization teams, product owners, and risk & compliance teams.

## Tested, Scalable, Production-Ready

**Proven at scale**
5,000+ files processed, ~4–5 minutes end-to-end, with parallel workers. This is not a PoC — it's a foundation.

## Why This Is the Future of RAG

**A clear progression**
Classic RAG answers questions. GraphRAG explains systems. Agentic GraphRAG understands them.

**A breakthrough for modernization**
It delivers faster impact analysis, safer refactoring, knowledge retention, and AI-assisted decision-making.

GitHub Repo: https://github.com/rajacsp/legacy-cobol-insights
