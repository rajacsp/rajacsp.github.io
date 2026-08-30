Title: Requirements or Technical Design? Choosing Where a Kiro Spec Begins
Date: 2026-08-29
Category: Agentic Engineering
Tags: kiro, spec-driven-development, requirements, technical-design, ai-ides
Slug: kiro-requirements-vs-technical-design
Status: Published

Every Kiro spec opens with a small but consequential fork: what do you author first? The IDE offers two starting points — Requirements or Technical Design — and treats Requirements as the recommended default. The choice isn't cosmetic. It decides which artifact is the source of truth and which is derived, and that ordering shapes how traceable, defensible, and maintainable the resulting spec turns out to be. Get it right and the spec reads like a clean argument from need to implementation. Get it wrong and you spend the rest of the project reverse-justifying decisions no one can quite explain.

## The Two Entry Points

**Requirements-first**
You begin by gathering and documenting requirements, typically as user stories paired with EARS-style acceptance criteria. Kiro then generates the technical design from those requirements, and implementation tasks flow from the design. The chain runs requirements → design → tasks, so every architectural decision can be traced back to an explicit, agreed-upon need.

**Design-first**
You begin with the technical design — architecture, components, data models, interfaces — and requirements are reverse-derived from that design. The spec becomes documentation of what is being built rather than a driver of what should be built.

## The Underlying Model: Spec-Driven Development

Both paths sit inside the same three-artifact structure that defines how Kiro works. A spec is not a single document; it's a `requirements` file, a `design` file, and a `tasks` file that stay linked. The entry-point question is really about which of those three you seed by hand and which you let Kiro generate. Understanding this makes the choice less about preference and more about causality: whatever you author first becomes the thing everything else must stay consistent with.

**Requirements artifact**
The contract. It states what the system must do in terms a stakeholder can verify, independent of how it's built.

**Design artifact**
The bridge. It translates the contract into architecture — the components, boundaries, and data flows that will satisfy each requirement.

**Tasks artifact**
The execution plan. It breaks the design into discrete, ordered units of work an agent or engineer can pick up one at a time.

## Why Requirements Is the Default

**Traceability**
When requirements come first, the design exists to satisfy them. Anyone reviewing the spec can ask "why does this component exist?" and follow the thread back to a stated need. Design-first inverts this, and the "why" is easier to lose.

**Scope discipline**
Writing requirements before architecture forces you to agree on the problem before committing to a solution. It reduces the classic failure mode of shipping something well-engineered that doesn't map to what anyone actually asked for.

**Reviewability**
Requirements written as user stories with acceptance criteria are legible to non-engineers. Stakeholders can sign off on intent before a single interface is drawn.

**Better inputs for the agent**
An AI agent generating a design produces sharper output when it's constrained by concrete acceptance criteria than when it's asked to invent both the goal and the means. Clear requirements narrow the search space and reduce the wandering, speculative design that comes from an underspecified prompt.

## When Design-First Earns Its Place

The recommendation is a default, not a rule. Design-first fits a handful of real situations:

**Back-filling existing code**
You already have a working system and want a spec that documents it. Here the design genuinely came first in reality, so deriving requirements from it is honest bookkeeping rather than a shortcut.

**Hard technical constraints drive the product**
Sometimes the architecture isn't a choice — a latency budget, a hardware target, a protocol you must speak. When the technical envelope is the binding constraint, starting from design and deriving what it can deliver reflects how the decisions actually flow.

**Exploratory or spike work**
When you're proving a technical approach is even feasible, formal requirements can be premature. Sketch the design, see if it holds, and let requirements crystallize once you know what's possible.

## A Common Failure Mode

The trap isn't picking the "wrong" entry point — it's picking design-first out of impatience and then pretending requirements were the source of truth. You end up with requirements written to match a design you'd already committed to, which quietly launders architectural decisions into "needs." The result looks traceable but isn't; the requirements can't actually constrain the design because they were derived from it. If you go design-first, be honest that you did, and treat the derived requirements as documentation rather than as an independent check.

## A Working Rule

Reach for Requirements on greenfield or ambiguous work, where you want the design justified by needs and the scope pinned down before you build. Reach for Technical Design when the architecture is settled and the spec's job is to record and rationalize it.

The question to ask yourself is simple: in this project, did the need or the architecture actually come first? Author in that order, and the spec will tell the truth about how the work happened. A spec that matches reality is one you can trust six months later; a spec that inverts it is one you'll spend those six months quietly working around.

## Takeaways

**Order encodes causality**
Whatever you author first becomes the source of truth. Choose it to match how the decisions really flowed.

**Requirements-first is the safe default**
It maximizes traceability, scope discipline, and reviewability, and it gives the agent sharper constraints to design against.

**Design-first is a deliberate tool, not a shortcut**
Use it for back-filling, hard technical constraints, or spikes — and stay honest that the design led.
