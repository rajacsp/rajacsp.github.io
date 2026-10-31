Title: Beyond the Persona: Adding Skill and Goal Layers to TencentDB Agent Memory
Date: 2026-10-31
Category: GenAI Engineering
Tags: agent memory, TencentDB, RAG, LLM, Python, memory layering
Slug: tencentdb-agent-memory-l4-skill-l5-goal
Status: Published
Cover: image/2026-10-31-tencentdb-agent-memory-l4-skill-l5-goal/1793461927972-opt.jpg

![1793461927972](image/2026-10-31-tencentdb-agent-memory-l4-skill-l5-goal/1793461927972-opt.jpg)

Most RAG applications retrieve the right documents, generate a good answer, and then forget the person who asked. Every session starts from zero, and the user repeats their preferences all over again.

TencentDB Agent Memory tackles this with a layered design it calls a semantic pyramid. It stops at four layers. In this article, we extend it with two more: a Skill layer that learns how to help, and a Goal layer that remembers why the user is here.

## The Four Layers TencentDB Gives You

TencentDB organizes memory by meaning, not by time. Each layer is built from the one below it, and each one is smaller and denser than the last.

**L0 Conversation**
The raw dialogue, stored exactly as it happened. This is the ground truth that every higher layer traces back to.

**L1 Atom**
Single facts about the user, extracted by an LLM every few turns. One atom holds one fact, such as "owns a 2019 Honda Civic."

**L2 Scenario**
Related atoms grouped into topic blocks, stored as plain Markdown. A scenario might read "car maintenance on a budget."

**L3 Persona**
A short profile synthesized from many scenarios. It captures stable habits, communication style, and preferences.

The strength of this design is traceability. When the agent needs evidence, it drills down from persona to scenario to atom to the original message. Nothing is lost to an irreversible summary.

## What the Pyramid Is Missing

The four layers answer three questions well: what was said, what is true, and who the user is. They do not answer two questions that matter just as much in a real product.

The first is how to help. If a user has twice approved a price comparison laid out as a table, the agent should learn that procedure and reuse it without being asked. That is procedural memory, and it is different from a fact.

The second is why the user is here. A persona might say "cost-conscious car owner." A goal says "keep this car running ten years at the lowest total cost." The goal changes which answer is most useful, not just how it is phrased.

## Introducing L4 and L5

**L4 Skill**
A reusable procedure learned from conversations that succeeded. It records the task, the steps, when to use it, and the sessions it came from.

**L5 Goal**
The user's one to three long-term objectives, rebuilt periodically from the persona. It is short enough to inject into every prompt.

The full pyramid now reads: Conversation, Atom, Scenario, Persona, Skill, Goal. In plain terms, that is what was said, what is true, what is happening, who they are, how to help, and why it matters.

## Implementation Strategy

TencentDB's gateway exposes routes for L0 through L3 only. So we keep TencentDB in charge of the first four layers and build L4 and L5 as a thin extension beside it. Since TencentDB is still in beta, keeping your extension outside its storage means an upgrade will not break your custom layers.

Skills live in a small SQLite database with full-text search. Goals live in one Markdown file per user.

```python
class Pyramid:
    def learn_skill(self, session_id):          # L4, on a thumbs-up
        convo = self.tdai.query_conversation(session_id=session_id, limit=6)
        skill = llm_json("Extract a reusable procedure as "
                         "{task, steps, when_to_use}, or null:\n" + str(convo))
        if skill:
            self.save_or_merge(skill, source=session_id)

    def rebuild_goals(self):                    # L5, weekly
        persona = self.read_persona()
        goals = llm("List this user's 1-3 long-term goals:\n" + persona)
        (self.dir / "goals.md").write_text(goals)

    def context_for(self, query):
        return {"goals": self.read_goals(),                       # L5
                "persona": self.read_persona(),                   # L3
                "skills": self.find_skills(query),                # L4
                "facts": self.tdai.search_atomic(query=query)}    # L1
```

The flow inside a RAG application is simple. Record every turn into TencentDB. When the user gives a thumbs-up, try to learn a skill from that session. Once a week, rebuild the goals. Before answering any question, assemble goals, persona, matching skills, and relevant facts into the system prompt, next to your retrieved documents.

## Design Rules That Matter

**Require a success signal**
Skills should only be learned from conversations that worked. Without a thumbs-up or a "no correction" signal, the system learns bad procedures as eagerly as good ones.

**Merge, do not pile up**
When a new skill resembles an existing one, let the LLM merge them and append the new session reference. Otherwise you end up with ten versions of the same procedure.

**Let goals steer, not override**
Tell the model to use goals for prioritizing, while still answering the question asked. Without this, every reply drifts toward the goal.

**Keep the drill-down path**
Every skill stores the sessions it came from. That preserves TencentDB's core promise: any memory can be traced back to the conversation that produced it.

## A Short Example

A Toronto car owner asks over several weeks about snow tires and oil changes, approving two price comparisons laid out as tables. Later, they mention wanting to keep the car for ten years. In week five they type only: "Brakes are squeaking. What now?"

The Goal layer frames the answer around long-term cost. The Skill layer runs the price-comparison procedure automatically. The Persona keeps the reply short, and the Atoms supply the car model and neighbourhood. The user typed one sentence; the memory supplied the rest.

## Closing Thoughts

Memory layering works because each layer has one job. Adding Skill and Goal layers turns a system that remembers the user into one that learns how to serve them. Automatic skill generation is on TencentDB's roadmap; when it arrives, swap in the native L4 and keep L5 as it is.