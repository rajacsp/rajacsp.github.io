Title: Claude Code Project Structure — Every File and Folder Explained
Date: 2026-04-18
Category: Engineering
Tags: claude-code, agentic-engineering, llm-tooling, project-structure
Slug: claude-code-project-structure-explained


Most Claude Code projects start with a `CLAUDE.md` and nothing else. Here is the full structure that turns Claude from a coding assistant into an engineering partner.

## The complete directory

```
your-project/
├── CLAUDE.md
├── CLAUDE.local.md
├── mcp.json
└── claude/
    ├── settings.json
    ├── rules/
    │   ├── code-style.md
    │   ├── testing.md
    │   └── api-conventions.md
    ├── commands/
    │   ├── review.md
    │   └── fix-issue.md
    ├── skills/
    │   └── deploy/
    │       ├── SKILL.md
    │       └── deploy-config.md
    ├── agents/
    │   ├── code-reviewer.md
    │   └── security-auditor.md
    └── hooks/
        └── validate-bash.sh
```

## File and folder breakdown

**`CLAUDE.md`** — Loaded at session start. Defines project overview, tech stack, and run commands. Contains coding conventions and architecture decisions. This is the onboarding doc for the agent — invest in it once, benefit every session.

**`CLAUDE.local.md`** — Personal overrides that stay out of git. Keeps individual preferences (editor, aliases, local flags) separate from shared project context.

**`mcp.json`** — MCP integration manifest committed to the repo. Connects Claude to GitHub, JIRA, Slack, and databases. One file controls every external tool the agent can reach — shared so the whole team gets the same integrations.

**`claude/settings.json`** — Controls permissions, tool access, model selection, and hook configuration. Override per-developer with `settings.local.json`.

**`claude/rules/`** — Modular `.md` files organized by concern. Claude loads them contextually: `code-style.md` when writing code, `testing.md` when generating tests, `api-conventions.md` for API work.

**`claude/commands/`** — Custom slash commands (`/project:name`) for repeatable workflows. Type `/project:review` and Claude runs your entire review process end-to-end. Supports shell execution.

**`claude/skills/`** — Auto-triggered context folders. Load only when Claude detects a relevant task type. Keeps the context window lean between unrelated tasks.

**`claude/agents/`** — Specialized sub-agents with defined roles, isolated context windows, and custom model preferences. A security audit runs in its own context — no pollution of the main conversation.

**`claude/hooks/`** — Event-driven scripts that run before or after tool use. Automates validation, linting, and formatting. Blocks unsafe operations without any prompting needed.

---

The quality of Claude Code output is directly proportional to the quality of your project structure. Structure it once — every session compounds.