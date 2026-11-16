---
name: principle-evolve-a-shared-domain-language
description: "Apply when domain terms conflict or scenarios reveal a different meaning. Scope shared language to its model; not for cosmetic renames with established meaning."
---

# Evolve a shared domain language

Use a model-based language consistently in discussion, requirements, examples,
and implementation within a bounded context. Refine it as domain knowledge
improves. A glossary records the language; it does not establish agreement.

- Test a term with concrete scenarios, exceptions, and counterexamples.
- Treat conflicting definitions as possible model discoveries. Different
  contexts can legitimately use the same word differently.
- Use domain expertise when available. Otherwise use contracts, examples,
  existing records, and observed behavior; label inferred meaning.
- Ask only when an unresolved meaning materially changes the work. Missing
  access to experts is not itself a blocker or permission to invent policy.
- When meaning changes, revise affected decisions, examples, and code together.
  Integrate those changes with other work in the same context.
- Record an agreed term in the project's glossary, anchored to the identifier
  that carries it in code. See the
  [glossary location reference](../domain-modeling/references/glossary.md).

For example, Sales may use "Order" for agreed commercial terms while Shipping
uses it for delivery instructions. Renaming both to one shared type does not
resolve that difference. Follow [Domain modeling](../domain-modeling/SKILL.md)
to decide whether the models need separate contexts.
