---
name: check-change-readiness
description: Use before implementing a change, when asked to validate a change or delivery plan before coding, or to check whether work is ready to build. Use for small edits and full delivery work; not for post-implementation code review or proof that a completed change works.
---

# Check change readiness

Check whether implementation can start without guessing about a material
decision. Use this as a short checklist, not a scoring system, new artifact,
or additional approval stage. Return the result to the calling workflow;
don't implement the change as part of this check.

## Check the relevant items

Read the request and enough current evidence to assess the change. Reuse
existing answers and decisions. For a small edit, the request and source
context can be sufficient; missing change files are not a defect. For full
delivery work, read the spec, delivery, and selected tasks. If the route is
unclear, consult the fast-path criteria in
[`Subspace`](../subspace/SKILL.md) without restarting its workflow.

- **Outcome:** Is the expected behavior or visible result clear? Can you tell
  what passes and what fails?
- **Scope:** Is the affected element, file, interface, or task bounded? Does
  the approach follow existing patterns and preserve unrelated behavior?
- **Decisions and dependencies:** Are implementation-changing questions
  resolved and prerequisites available? For full work, are the relevant
  artifacts consistent, approved, and mapped to ready tasks?
- **Impact:** Have relevant permissions, public contracts, data integrity,
  accessibility, and external effects been considered? Check only what the
  change touches. A small diff is not evidence of low risk.
- **Verification:** Is there a direct, practical check for the expected result?
  An existing check, visual inspection, or focused command may be enough.
- **Domain meaning, when affected:** Are context-scoped terms, ownership, and
  cross-context contract meanings clear enough to implement? Can supposedly
  independent tasks proceed without conflicting domain decisions? Use
  [domain-modeling](../domain-modeling/SKILL.md) for material gaps. Available
  evidence and labeled assumptions can suffice; expert access is not required.

For full work with a linked tracker, confirm publication is reconciled or
explicitly deferred. Don't require a board or new artifacts for a small edit.
Mark irrelevant items as not applicable without inventing work to satisfy them.

## Return the next action

- **Ready:** No material gap remains. Give the scope and intended check in one
  or two sentences. The caller can proceed under the existing authorization.
- **Needs clarification:** Name the specific decision and ask one focused
  question, or identify the smallest investigation that can answer it.
- **Blocked:** Name the missing prerequisite, conflicting requirement, or
  authorization and the action needed to resolve it.

For full work, direct a gap to its owner: intent for purpose, spec for required
behavior, delivery for implementation approach, or task for bounded execution.
For a small edit, a focused answer can resolve the gap without a full workflow.
Recheck only the affected item after it is resolved. Don't repeat completed
reviews or request a separate readiness approval.

Example: "Ready. Change the identified button's local color token to the
existing blue variant. Verify its rendered default and focus states and text
contrast." The request supplies the acceptance criteria; no change package is
needed unless inspection reveals wider impact.
