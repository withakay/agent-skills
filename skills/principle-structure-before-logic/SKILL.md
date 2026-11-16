---
name: principle-structure-before-logic
description: "Apply before writing logic: choosing core types and data structures, and sequencing scaffold versus feature work. Get the data structures right so downstream code becomes obvious."
disable-model-invocation: true
---

# Structure before logic

Structural decisions keep later choices open. Code-level decisions protect simplicity. Over-engineering is often a premature decision that closes doors. The right foundational data structure keeps later choices open.

## Data structures first

Get the data shape right before writing logic. The right shape makes downstream code obvious. Define core types early, trace every access pattern, and choose structures that match the dominant paths. A data-structure change late is a rewrite. Early, it is often a one-line diff.

At the code level, share the structure, not every line. Converge types only where their meaning is shared within a model. Across contexts, follow [Make model boundaries explicit](../principle-make-model-boundaries-explicit/SKILL.md) before sharing types. Three similar statements still beat a premature abstraction. Prefer explicit over clever. Test behavior and edge cases, not line counts.

Before sharing state between actors, follow [Avoid shared mutable state](../principle-avoid-shared-mutable-state/SKILL.md).

## Scaffold first

If something helps every later phase, do it first. Ask whether every subsequent phase benefits from this existing. CI, linting, test infrastructure, and shared types are scaffold. Sequence so later work can reuse the foundation: setup before features, tests before fixes. Keep commits small and single-purpose.

Each increment should land a coherent abstraction or deepen one that exists. Don't spread a new capability across callers as special-case coordination.

Remove dead weight first, then lay foundations. Follow [Tidy first](../principle-tidy-first/SKILL.md) for that order.
