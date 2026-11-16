### Feature

Implement an approved full-workflow delivery and verify its outcome. Small,
low-risk edits use Subspace's fast path instead of this playbook. Delegate
implementation where useful and retain responsibility for review.

1. Read the change folder's `intent.md`, `spec.md`, approved `delivery.md`, and ready `task-NN-<desc>.md` files per [`change-artifacts.md`](../references/change-artifacts.md). If any stage is missing or unapproved, return to that stage before implementation. Read linked existing plans and `ext-refs.md` when present. Confirm linked-tracker publication is reconciled or explicitly deferred by the owner. Start only tasks whose dependencies are satisfied. Keep artifact metadata, task evidence, and tracker links aligned as work proceeds.
2. Use **check-change-readiness** before implementation. Use **how** when you
   need more context about the affected subsystem, rather than repeating
   completed research.
3. Follow the implementation approach in `delivery.md`. If a material design question remains, return to `refine-delivery.md`. For domain discoveries, use [domain-modeling](../../domain-modeling/SKILL.md) to revise affected decisions and downstream work. Renew approval only when the revision changes scope, behavior, or another decision governed by the existing approval. Do not choose a competing design inside task execution.
4. Check how work will be assigned. Mark irrelevant items `n/a: <reason>`:
   - **Blocking first steps.** Resolve prerequisites before starting parallel work.
   - **Independent workstreams.** Parallel work needs disjoint writes and independent domain decisions. Shared meaning or unresolved contracts create dependencies even across separate files. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (**principle-avoid-shared-mutable-state**). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
5. When delegating, use a subagent the harness provides; where it provides none, implement the task directly. Supply
   the task's file scope, approved data model, approach, and acceptance criteria.
   Include only relevant context-scoped terms, ownership, and integration or
   translation decisions, with links to their source records.
   Apply **principle-model-the-domain-in-data** to keep state and structure
   explicit. Review the diff yourself. If implementation reveals a material
   design choice, return to delivery planning before selecting a new approach.
   Keep edits within the approved scope and verify affected consumers of shared
   code. Commit coherent units when authorized.
6. Verify each task's acceptance and the delivery's end-to-end criteria on the matching surface. Record evidence and task status in the task files; all tasks passing is not a substitute for delivery acceptance. If the surface has no project-local verification skill, run **create-verification-skill** before relying on repeated live checks. If an existing verification skill or feature map is stale, run **maintain-verification-skill** before using it. "Inconclusive" or wrong-surface is not a pass; flag it.
7. Rebase into small, ordered commits; stack follow-ups.
   Use **principle-sequence-verifiable-units-of-work**, building, verifying, and committing each small unit before the next.
8. If the design is contested, run an independent decision review before shipping.
9. Run **Opening a PR**.

Assign tightly coupled work to one owner. Delegate independent tasks in
parallel when their file scopes and domain decisions permit it. Reassess ownership at phase
boundaries and preserve the approved task boundaries.

**Reply:** what you built, what you chose and why, open decisions. Tables for design alternatives.
