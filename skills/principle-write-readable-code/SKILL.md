---
name: principle-write-readable-code
description: "Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head. Collapse one-caller wrappers and shrink mutable scope."
disable-model-invocation: true
---

# Write readable code

Maintainability is the work a reader must do to understand code. Track two axes:

1. Layers to trace. How many indirections sit between the question and the answer.
2. State to hold. How much hidden or mutable context the reader must keep in their head.

Code is read far more than it is written. Line count, cyclomatic complexity, and "clean architecture" are proxies. Reader load is the thing that matters. The two axes are independent. A flat file with 50 globals can be as hard to reason about as a six-layer adapter stack. Guard both. This is the human analog of [Guard the context window](../principle-guard-the-context-window/SKILL.md): working memory is finite for readers too.

## Pattern

- Collapse layers that don't earn their keep: pass-through wrappers and indirection introduced for a future that never came. A single-consumer adapter can earn its place by translating between domain models; judge its meaning, not its consumer count.
- Make adjacent layers change the abstraction. A layer that repeats the same methods and arguments adds reader load without compression. Collapse pass-through layers.
- Demand interface compression. A broad interface that hides little complexity makes readers learn both the surface and the implementation. Prefer boundaries that hide meaningful decisions.
- Shrink state scope. Prefer pure functions that return instead of mutating, locals over fields, fields over module state, and module state over globals. Derive instead of sync.
- Name the invariant at the boundary, not in every consumer, so the reader learns it once.
- Before adding a layer or a piece of state, ask whether this reduces reader load somewhere else by at least as much.

## Check

Can a new reader answer "Where does X come from?" and "What can change X?" in under 30 seconds? If not, cut layers or cut state.
