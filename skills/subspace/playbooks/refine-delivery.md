### Plan delivery and refine tasks

Turn the approved specification into one shippable delivery plan, then divide
it into bounded work. Planning produces `delivery.md`, also called a product
backlog item (PBI). This playbook applies to the full workflow, not small edits.
There is no separate `plan.md` for new changes. Read the accepted intent and
approved spec. Use templates in
[`change-artifacts.md`](../references/change-artifacts.md).

#### Delivery stage: delivery.md

1. Inspect relevant modules, contracts, helpers, tests, and project commands.
   Consider the Delivery principles in
   [`principle-routing.md`](../references/principle-routing.md) before choosing
   the approach. Compare triggers with the evidence, explicitly load those that
   apply, and apply each as a concrete decision or a short confirmation that the
   plan complies. Record a material effect or override in the owning delivery
   section; recorded approvals and accepted requirements outrank a principle.
   Do not defer guidance needed for an approach choice until implementation.
   Choosing a type or state representation is already a design decision.
   Choose the smallest implementation approach that satisfies the spec. Use
   **architect**, scoped to design only, for a non-trivial or contested shape.
   Use a bounded prototype only for a material implementation uncertainty.
   When domain boundaries are involved, use [domain-modeling](../../domain-modeling/SKILL.md)
   and **principle-make-model-boundaries-explicit**: establish context ownership
   before shared types, record actual integration relationships, and decide where
   meanings need translation. Use **principle-focus-on-the-core-domain** to
   direct investment toward known differentiating capabilities. For large work,
   state the few boundary rules that guide evolution rather than fixing every module.
   When the approach has components, sequence, or ownership, load **create-ascii-diagram** and include a verified text diagram in `delivery.md`.
2. Define the shippable outcome, affected users, included requirement IDs,
   implementation approach and rationale, bounded files or interfaces,
   dependencies, sequence, and exclusions. Include migration, rollout,
   rollback, and operational effects when applicable. Reuse decisions from an
   existing plan rather than copying a competing source of truth.
3. Map delivery acceptance criteria to `REQ-*` IDs and direct verification.
   Name exact available checks and the integration evidence that proves the
   unit can ship. Passing task checks alone does not establish that outcome.
4. Keep a small delivery short. For multi-phase or multi-PR work, expand its
   body using `multi-phase-plan.md`; keep the result in this `delivery.md`.
   If the outcome cannot ship as one unit, propose a split and obtain a scope
   decision before creating more change folders or tracker items.
5. Check requirement coverage, contradictory scope, undefined interfaces,
   and unresolved implementation decisions. If required behavior changes,
   amend and reapprove the spec first. Do not add product requirements through
   technical planning.
6. Write `delivery.md`, `status: draft`. Obtain approval of outcome, approach,
   scope, acceptance, and dependencies; record approval before refining tasks.

#### Tasks stage: task-NN-<desc>.md

1. Consider the Tasks principles in
   [`principle-routing.md`](../references/principle-routing.md) before
   decomposing, and load those that apply. Split the approved delivery into work
   a human or agent can complete and verify independently. Use stable filenames such as `task-01-add-export.md`;
   the number is a local identifier, not a tracker ID or an implicit dependency.
   Parallel tasks need independent domain decisions as well as disjoint writes;
   unresolved shared meaning or contracts are dependencies.
2. Each task names its parent `delivery.md`, covered requirements, objective,
   bounded files or interfaces, prerequisites, explicit dependencies, work
   steps, acceptance criteria, and verification evidence. State exclusions
   where needed to prevent overlap or unintended edits.
   Link only the domain terms, context ownership, and integration decisions the
   worker needs; reuse their existing records. A fresh worker does not share
   this context: state the decision constraints it needs and name the
   principles it must load for its own work.
3. Reuse approved scope and decisions. A task must not invent behavior or
   choose between unresolved designs. Return such questions to the stage that
   owns them. Separate implementation, tests, or documentation only when that
   creates useful bounded work; do not force a fixed task count or taxonomy.
4. List task links and requirement coverage in `delivery.md`. Check complete
   scope coverage, missing integration work, duplicated ownership, circular
   dependencies, and whether each task has a direct completion check.
5. Refine the task set with the owner and mark approved tasks `status: ready`.
   If a project tracker is linked, route to `publish-work-items.md` before
   implementation. Otherwise retain `work-items: []`. Use
   **check-change-readiness**, then hand the local task set to the matching
   execution playbook when the owner authorizes implementation.

When scope changes, update the affected upstream artifact and descendants
together. Preserve task filenames and tracker identity; record obsolete tasks
explicitly rather than recycling their numbers or silently deleting tickets.

**Reply:** delivery and task paths, approach, coverage, dependencies, pending
decisions, and tracker publication status. Commit only when authorized.
