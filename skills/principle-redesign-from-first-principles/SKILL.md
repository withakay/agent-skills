---
name: principle-redesign-from-first-principles
description: "Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on."
disable-model-invocation: true
---

# Redesign from first principles

When integrating a change, don't bolt it onto the existing design. Redesign as if the requirement had been there from the start. The result should look like what you would have built if you'd known on day one.

- Read all affected files and understand the current design holistically.
- Ask: if you were writing this from scratch with this new requirement, what would you build?
- Propagate the change through every reference: types, docs, examples, and rationale sections.
- Think about the redesign holistically, then deliver it incrementally.
- Let large-scale structure evolve with domain knowledge. Keep organizing rules only while they clarify responsibilities and support local design.

## Check

The result should look like a design that had the requirement from the start. An extra flag or parallel path can indicate a workaround. Check its purpose before redesigning. Preserve adapters that translate between valid domain models; follow [Make model boundaries explicit](../principle-make-model-boundaries-explicit/SKILL.md).
