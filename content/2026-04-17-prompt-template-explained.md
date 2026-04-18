Title: PromptTemplate Explained for 10 year old
Date: 2026-04-17
Category: GenAI Basics
Tags: langchain, prompt-engineering, beginner, kactii
Slug: prompttemplate-explained-for-10-year-old

PromptTemplate is one of those ideas that sounds technical but is actually something you already understand from everyday life. Here are three ways to see it clearly.

## Cookie Cutter 🍪

**The Shape** — A star-shaped cookie cutter that never changes. You press it into any dough and get the same star, every time.

**The Dough** — Chocolate today, vanilla tomorrow, strawberry next week. The filling is what you swap out each time you use the cutter.

## Teacher's Board 📝

**The Sentence on the Board** — "Today we will learn about ___ and it matters because ___." The teacher wrote it once and never rewrites it from scratch.

**The Daily Swap** — Every morning she just fills in the two blanks with whatever today's topic is. Same structure, new content.

## McDonald's Script 🍔

**The Greeting** — "Hi! Can I take your order? Would you like ___ with that?" Every cashier at every counter says this same line.

**Your Order** — The only thing that changes is what goes into the blank. The script stays untouched.

## The Big Idea 💡

**PromptTemplate is a reusable sentence with blanks** — You write the shape of your question once, and then just swap the blanks as many times as you need. One template, infinite questions, zero repetition.

---

## Now Let's See It in Code 🧑‍💻

If you're curious what this looks like when a developer actually writes it, here it is — still simple, still just blanks.

### Step 1 — Create the Cookie Cutter

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["animal", "color"],
    template="Tell me a fun fact about a {color} {animal}!"
)
```

`{color}` and `{animal}` are the blanks. That's it.

### Step 2 — Fill in the Blanks

```python
prompt = template.format(animal="elephant", color="pink")
print(prompt)
# → "Tell me a fun fact about a pink elephant!"
```

You hand this finished sentence to the AI and it answers.

### Step 3 — Reuse It Forever

```python
template.format(animal="dog",    color="blue")   # → blue dog
template.format(animal="cat",    color="green")  # → green cat
template.format(animal="parrot", color="red")    # → red parrot
```

One cutter. Infinite cookies. No copy-pasting.

---

## Everything Side by Side

| Everyday Life | Code Version |
|---|---|
| 🍪 The cookie cutter shape | `template="Tell me about {topic}"` |
| ✏️ The blanks to fill | `input_variables=["topic"]` |
| 🖊️ Filling in the blanks | `.format(topic="elephants")` |
| 🍪 The finished cookie | The prompt sent to the AI |

---

**One reusable shape. Infinite possibilities. That's PromptTemplate.**