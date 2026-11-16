---
name: principle-tidy-first
description: "Apply when sequencing an addition, refactor, or rewrite. Remove dead weight, redundant validators, stale code, and stubbed references first, then build on the cleaner base."
disable-model-invocation: true
---

# Tidy first

When you evolve a system, clean up and remove complexity before you build. Removing mess gives you a cleaner base, which makes the next addition smaller and less brittle.

Adding to a complex system compounds complexity. Removing first cuts the surface area, reveals the essential structure, and usually makes the next design obvious. Default to subtraction.

Make simplification a continual investment. Leave the design more capable behind the same or smaller surface than you found.

## Pattern

- Sequence removal before construction.
- Cut before you polish. Reach the minimum before you invest in quality.
- Design for observed usage, not speculative edge cases.
- Don't add speculative validators, parsers, or guards beyond what the spec demands.
- Out-of-spec features drag validators behind them. Persistence, retry-on-startup, and schema migration each need guards to defend their inputs.
- Simplify prompts. Remove redundant instructions and excessive templates.
- When a reference has no novel content, delete it rather than leaving a stub.
