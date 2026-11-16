---
name: principle-make-model-boundaries-explicit
description: "Apply when sharing domain models, changing ownership, or integrating systems with different meanings. Not for transport validation alone."
---

# Make model boundaries explicit

State where a model applies before sharing or merging it. A bounded context
defines the scope of a language and model. It need not match a service,
repository, team, or deployment unit.

- Map actual contexts and relationships before proposing a target arrangement.
  Use known rule and contract ownership; mark unknown ownership explicitly.
- Within a context, maintain coherent meaning. Across contexts, choose sharing,
  translation, conformity, or separation based on purpose and ability to
  coordinate changes.
- Shared names and schemas do not prove shared meaning. A Shared Kernel needs
  an explicit scope and a workable joint change agreement.
- Keep translation that protects a model, even with one supplier or consumer.
  Validate the translated meaning, not only the payload shape.
- Consider Separate Ways when integration costs exceed its domain value.

Use [Domain modeling](../domain-modeling/SKILL.md) for the context map and
relationship choices. Share code only after the model decision supports it.
