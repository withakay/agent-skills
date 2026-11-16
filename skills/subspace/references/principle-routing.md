# Principle routing

The full workflow (**Intent → Specification → Delivery → Tasks**) treats the
`principle-*` skills as stage inputs. Each stage considers the principles
listed for it below, loads those whose trigger the evidence meets, and applies
them before the decision they affect. This reference adds no stage, artifact,
or approval.

## Consider, load, apply

- **Consider.** Compare the table's observable triggers with the request,
  repository evidence, and recorded decisions. Do not load all 24 skills. A
  principle whose trigger is not met needs no mention.
- **Load.** Call the host's skill tool with the principle ID before the
  decision it affects. Read its known installed `SKILL.md` only where no
  loader exists. Never bypass a permission denial. Reuse a body already in the
  current context.
- **Apply.** Make a concrete decision or check, or confirm with a short reason
  that the current plan already complies. Do not add work just to show a
  principle was used.
- **Record.** Write a material effect or override in the artifact section that
  owns the decision (see the table). Do not add a principles section or a
  per-principle checklist.
- **Revisit.** Only when new evidence changes whether a principle applies or
  what it decides.

## Stage ownership

A principle informs the stage; it does not move a decision to another stage.

- **Intent** owns purpose, reason to act, and constraints. It chooses no implementation.
- **Spec** owns observable behavior only. It adds no technology or structure choice.
- **Delivery** owns the implementation approach and scope. It adds no product requirement.
- **Tasks** own decomposition of approved work. They settle no open design question.

## Conflicts

1. Security, data integrity, and user authority come first.
2. Recorded approvals and accepted requirements outrank a principle.
3. Internal migration does not waive an external compatibility or deployment
   commitment.
4. Do not write a script when an existing tool does the work.
5. Do not remove the only meaningful test for minimality.
6. Do not tidy unrelated code or invent product requirements from a principle.

`principle-never-block-on-reversible-work` permits authorized, reversible
preparation. It never replaces an approval in the chain.

## Handoff to workers

A fresh worker does not share the parent's context. Give it the relevant
decisions and constraints from the artifacts, and name the principles it must
load for its own task. Do not assume it has read the parent's principle bodies.

## Fast path and read-only work

Fast-path changes and read-only work skip the full matrix. A single principle
may still be loaded when it helps the work.

## Inventory

Artifact effect names where a material effect is recorded.

| Principle | Stages | Applicability trigger | Artifact effect |
| --- | --- | --- | --- |
| [principle-user-experience-first](../../principle-user-experience-first/SKILL.md) | Intent, Spec | Product, UX, or feature-scope tradeoff between user experience and implementation convenience | Intent desired outcome; spec requirement or exclusion |
| [principle-focus-on-the-core-domain](../../principle-focus-on-the-core-domain/SKILL.md) | Intent, Delivery | Work competes for investment between differentiating capabilities and reusable or supporting ones | Intent outcome; delivery approach and investment choice |
| [principle-never-block-on-reversible-work](../../principle-never-block-on-reversible-work/SKILL.md) | Intent, Spec, Delivery, Tasks | A confirmation is considered for reversible preparation inside the request | Stage notes; proceed with authorized preparation, never skip an approval |
| [principle-fix-root-causes](../../principle-fix-root-causes/SKILL.md) | Intent, Delivery | The change responds to a defect, and its origin may be a symptom | Intent evidence (supported cause or hypothesis); delivery approach |
| [principle-capture-learnings](../../principle-capture-learnings/SKILL.md) | Intent, Delivery | A correction or instruction has recurred | Intent evidence; delivery guard mechanism (lint, check, flag) |
| [principle-evolve-a-shared-domain-language](../../principle-evolve-a-shared-domain-language/SKILL.md) | Intent, Spec | A term conflicts or scenarios reveal a different meaning in one model | Intent constraints; spec terms and glossary link |
| [principle-make-model-boundaries-explicit](../../principle-make-model-boundaries-explicit/SKILL.md) | Spec, Delivery | Models with different meanings are shared, owned, or integrated | Spec contract meaning; delivery context ownership and translation |
| [principle-boundary-discipline](../../principle-boundary-discipline/SKILL.md) | Spec, Delivery | Input arrives from a CLI, configuration, network, or external API | Spec validation and failure behavior; delivery guard placement |
| [principle-make-operations-idempotent](../../principle-make-operations-idempotent/SKILL.md) | Spec, Delivery | An operation can be retried, restarted, or interrupted partway | Spec repeat and partial-run behavior; delivery lifecycle design |
| [principle-less-is-more](../../principle-less-is-more/SKILL.md) | Intent, Spec, Delivery | Scope, layers, wrappers, or abstractions grow beyond the stated need | Intent exclusions; spec exclusions; delivery smaller approach |
| [principle-explore-the-design-space](../../principle-explore-the-design-space/SKILL.md) | Delivery | A novel UI or architecture decision has no codebase precedent | Delivery compared options and rationale |
| [principle-redesign-from-first-principles](../../principle-redesign-from-first-principles/SKILL.md) | Delivery | A new requirement strains an existing design and would become an exception | Delivery approach treating it as a foundational assumption |
| [principle-structure-before-logic](../../principle-structure-before-logic/SKILL.md) | Delivery, Tasks | Core types or data structures must be chosen before logic or features | Delivery structure decision; task order, structure first |
| [principle-model-the-domain-in-data](../../principle-model-the-domain-in-data/SKILL.md) | Delivery | Stateful logic, many branches, or repeated data-shape assumptions | Delivery domain structures replacing scattered conditionals |
| [principle-type-system-discipline](../../principle-type-system-discipline/SKILL.md) | Delivery | A type, state representation, or function signature is chosen or designed in a statically typed language, before code is written | Delivery type invariants and boundary parsing choices |
| [principle-avoid-shared-mutable-state](../../principle-avoid-shared-mutable-state/SKILL.md) | Delivery, Tasks | Concurrent actors may write the same file, branch, key, or state object | Delivery ownership approach; task write scopes kept disjoint |
| [principle-guard-the-context-window](../../principle-guard-the-context-window/SKILL.md) | Intent, Delivery, Tasks | Context fills, outputs or files are large, reads repeat, or work fans out | Delivery approach for large inputs; task handoff size and scope |
| [principle-tidy-first](../../principle-tidy-first/SKILL.md) | Delivery, Tasks | An addition or refactor touches dead code, stale code, or redundant validators | Delivery cleanup scope; task ordering, cleanup before feature |
| [principle-migrate-and-delete](../../principle-migrate-and-delete/SKILL.md) | Delivery, Tasks | An internal API with callers is replaced | Delivery migration plan; task migrating callers and deleting the old API |
| [principle-prioritize-end-state](../../principle-prioritize-end-state/SKILL.md) | Delivery | A planned rewrite or migration has explicit intermediate phases | Delivery target architecture and phase sequence |
| [principle-sequence-verifiable-units-of-work](../../principle-sequence-verifiable-units-of-work/SKILL.md) | Delivery, Tasks | Multi-step work, sweeps, migrations, or stacked changes need ordering | Delivery sequence; task boundaries and dependencies |
| [principle-verify-results](../../principle-verify-results/SKILL.md) | Spec, Delivery, Tasks | A requirement or task needs proof beyond a proxy, self-report, or compile | Spec acceptance examples; delivery verification; task checks |
| [principle-build-bespoke-tools](../../principle-build-bespoke-tools/SKILL.md) | Delivery, Tasks | Concrete mechanical repetition or a rerunnable verification need is not covered by existing tools, including a one-off need | Delivery tooling approach; task tool deliverable only when justified |
| [principle-write-readable-code](../../principle-write-readable-code/SKILL.md) | Delivery, Tasks | Hard-to-trace code, hidden state, or one-caller wrappers are likely | Delivery structure constraints; task acceptance criteria |
