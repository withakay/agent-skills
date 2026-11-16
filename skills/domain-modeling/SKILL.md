---
name: domain-modeling
description: "Use when domain terms conflict, model boundaries or integration relationships are unclear, or a change needs core-domain prioritization. Not for routine data-structure selection, tactical DDD patterns, or local edits with established meaning."
---

# Domain modeling

Clarify domain meaning, model boundaries, and investment before choosing code
structure. Use this skill within the current Subspace stage or for read-only
analysis. It adds no approval stage or mandatory document.

## Ground the decision

Find existing domain documentation, glossaries, context maps, and decisions.
Follow their conventions. Compare them with current behavior, contracts,
examples, and code. Cite evidence; distinguish observed behavior, intended
behavior, and assumptions. Code shows the current implementation, not proof
that its model is correct.

Use domain expertise when available. Do not require named experts, interviews,
or an organization chart before proceeding. Use available evidence and label
inferred meanings. Ask a focused question only when an unresolved meaning
could materially change behavior, ownership, or integration. Continue work
that does not depend on that answer; do not invent business policy.

## Model the affected domain

1. **Language.** Test terms through concrete scenarios and counterexamples.
   Keep one meaning consistent within its context; investigate conflicts
   before normalizing names. Follow [Evolve a shared domain language](../principle-evolve-a-shared-domain-language/SKILL.md).
2. **Boundaries.** Identify where each model applies and who or what maintains
   its rules and contracts, as far as evidence supports. A bounded context is
   a language and model boundary, not necessarily a service, repository, team,
   or deployment. Follow [Make model boundaries explicit](../principle-make-model-boundaries-explicit/SKILL.md).
3. **Relationships.** Describe the actual context map before a proposed change.
   For affected integrations, record dependency direction, influence over
   changes, shared meaning, and translation responsibility. Use the
   [strategic design reference](references/strategic-design.md) to choose a
   relationship; do not infer agreement from a shared schema.
4. **Investment.** Identify how the capability contributes to the Core Domain.
   If its strategic value is unknown, say so. Follow [Focus on the core domain](../principle-focus-on-the-core-domain/SKILL.md).
5. **Learning.** Compare the model with scenarios and implementation feedback.
   Revise affected terms, boundaries, and decisions when evidence changes.
   Within a context, integrate model and language changes frequently; passing
   CI alone does not establish agreement on meaning.

## Keep the record small

Update the existing domain record when a decision becomes established. If none
exists and the knowledge must outlive the change, use one document in the
project's existing documentation structure. Include only the relevant vision,
core, context-scoped terms, relationships, evidence, and open questions.
Link that record from change artifacts rather than copying it into each one.
For a bounded analysis, a concise response can be sufficient.

Keep context-scoped terms, abbreviations, and preferred wording in the project's
Markdown glossary, and add or revise an entry in the change that introduces or
redefines a term. Use the
[glossary location reference](references/glossary.md) to find or choose that
file, its scope in a monorepo, and its idiomatic name.

Return the decision, supporting evidence, affected contexts, and material
unknowns. Revisit the owning workflow stage only when its decisions change.
Preserve Subspace's approval rules for changed scope or required behavior.

For integration options, distillation, and large-scale structure, consult the
[strategic design reference](references/strategic-design.md). Do not introduce
tactical patterns or services merely to make a context map look tidy.
