# Strategic design reference

Use these choices only for the affected domain decision. They are not a
checklist of patterns to implement.

## Context relationships

A context map describes actual model boundaries and how they interact,
including organizational constraints. Distinguish the current map from a
proposed change. Record upstream/downstream direction where it applies, each
side's ability to influence changes, and responsibility for translation.

| Pattern | Use and consequence |
| --- | --- |
| Shared Kernel | Share a small, explicit part of the model and implementation. Changes require coordination and joint integration checks. |
| Customer/Supplier | The downstream team's needs influence upstream planning. Record the actual agreement; dependency alone does not establish this relationship. |
| Conformist | Adopt the upstream model when influencing it is impractical and conformity is acceptable. Accept the resulting dependency deliberately. |
| Anticorruption Layer | Translate another context's model to protect the local model. Preserve semantic differences even when wire formats are compatible. |
| Open Host Service | Offer a defined integration protocol for multiple consumers rather than separate integrations for each. |
| Published Language | Use a documented interchange language that both sides can interpret. It can accompany an Open Host Service; it need not become either side's internal model. |
| Separate Ways | Keep contexts independent when integration offers insufficient value. Accept local duplication where it preserves useful independence. |

These choices can combine. Do not force every relationship into one exclusive
label or invent agreements to complete the map. Review changes with the
relevant collaborators when available; record assumptions otherwise.

## Distillation

- **Core Domain:** identify distinctive domain knowledge and concentrate design
  effort there. Other necessary work still needs appropriate quality.
- **Generic Subdomains:** separate capabilities that do not carry the system's
  distinctive knowledge; consider established solutions.
- **Domain Vision Statement:** state the domain's valuable purpose and how the
  core serves it. Reuse the existing product or domain record.
- **Highlighted Core:** point readers to the parts of the model that express
  the core, using a brief description or annotations in existing documents.
- **Cohesive Mechanisms:** separate general mechanisms when they obscure domain
  concepts. Do not turn this into a framework-building requirement.
- **Segregated Core / Abstract Core:** consider isolating the core or its key
  relationships when that makes the model clearer. Do not require a separate
  service, package, or inheritance hierarchy.

"Supporting" can describe necessary, non-distinctive work. Subspace uses it as
a planning description, not as an additional named Blue Book pattern.

## Large-scale structure

Apply **Evolving Order**: use a large-scale organizing rule only while it helps
people understand and change the domain. Revise it as knowledge improves;
leave local design freedom where global consistency adds no value.

| Option | Consider when |
| --- | --- |
| System Metaphor | A shared analogy clarifies responsibilities. Drop it where it misleads the model. |
| Responsibility Layers | Broad domain responsibilities and their dependencies clarify the system. These are not automatically presentation, application, and persistence layers. |
| Knowledge Level | The domain needs explicit knowledge that governs another part of the model. Avoid speculative configurability. |
| Pluggable Component Framework | Established domain abstractions support meaningful interchangeable components. Do not generalize before those abstractions are understood. |

## Source and scope

Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of
Software*, Part IV: Maintaining Model Integrity, Distillation, and Large-Scale
Structure. Ubiquitous Language and collaborative model discovery support
these strategic decisions.

Evans's [DDD Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
provides pattern summaries and marks later additions. This guidance uses the
Blue Book's strategic patterns; it does not prescribe tactical building blocks,
microservices, CQRS, or event sourcing.
