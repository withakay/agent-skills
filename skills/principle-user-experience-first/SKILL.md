---
name: principle-user-experience-first
description: "Apply when product, UX, or feature-scope tradeoffs come up. Prefer the consumer's experience over implementation convenience. Ship fewer polished features over more rough ones."
disable-model-invocation: true
---

# User experience first

The product is the experience. Every technical decision either helps or hurts it. When implementation convenience conflicts with the consumer's experience, choose the experience.

- Every feature, control, and option must earn its place.
- A polished experience with three features beats a rough one with ten.
- Prototype before committing. Design decisions are cheaper in throwaway HTML than in production code.
- Check transitions, alignment, spacing, feedback, and error states.
- Tighten the core loop. Every feature should serve the central workflow or be removed.

The user is whoever consumes the work. For a UI, that is the end user. For a library or an internal API, it is the colleague who imports it. The engineer who maintains the code next is a user too. Weigh their experience the same way, and explain impact from their seat.

Foundations should serve the experience, not the other way around. [Structure before logic](../principle-structure-before-logic/SKILL.md) governs the sequence of work. This principle governs the target.
