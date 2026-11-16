# Change artifacts

<!-- toc -->
## Contents

- [Home and naming](#home-and-naming)
- [Frontmatter and ownership](#frontmatter-and-ownership)
- [Lifecycle and revisions](#lifecycle-and-revisions)
- [Archive](#archive)
- [Templates](#templates)
  - [intent.md](#intentmd)
  - [spec.md](#specmd)
  - [delivery.md](#deliverymd)
  - [task-NN-<desc>.md](#task-nn-md)
  - [ext-refs.md (optional)](#ext-refsmd-optional)
<!-- tocstop -->

For the full workflow, one change owns one folder. Small, clear, low-risk edits
use Subspace's fast path and don't require these files. Each full-workflow stage
reads its predecessor:
**Intent → Specification → Delivery → Tasks**.

| Artifact | Question it answers |
| --- | --- |
| `intent.md` | Why are we doing this? |
| `spec.md` | What behavior should exist? |
| `delivery.md` | What implementation scope and approach will satisfy the spec as a shippable unit? |
| `task-NN-<desc>.md` | What bounded piece of work needs doing? |

Planning produces `delivery.md`, also called a product backlog item (PBI) or
delivery plan. Don't create a separate `plan.md` for new full-workflow changes. For an
existing change, reuse its plan: either consolidate it with explicit approval
or link its technical decisions from `delivery.md` while retaining one owner
for each decision. Do not delete existing plans or duplicate mutable scope.

When domain decisions matter, link existing durable records for language,
context boundaries, integration, and core-domain priorities. Use
[domain-modeling](../../domain-modeling/SKILL.md) within the owning stage; record
change-specific decisions there without copying the durable records. No new
domain file, stage, or approval is required. Carry only relevant decisions into
tasks and revise affected records when new evidence changes their meaning. When
a change introduces or redefines a term, update the project's glossary at the
location described in the
[glossary location reference](../../domain-modeling/references/glossary.md) and
link that entry.

When a principle from [principle-routing](./principle-routing.md) materially
changes or overrides a decision, record that effect in the existing section that
owns the decision: intent constraints or evidence, spec requirements or
exclusions, delivery approach or verification, or task scope. Don't add a
principles section or a per-principle checklist. Tasks carry only the
constraints a worker needs and name the principles it must load.

## Home and naming

- Use `changes_home` from the repository's
  `.agents/config/subspace/config.json`, or an explicit operator path. Default
  to `docs/changes/`.
- Create `<home>/<slug>/`, with a kebab-case slug. Preserve an existing change
  folder's identity, including older date-prefixed names. Do not rename active
  folders to adopt this convention.
- Keep all artifacts flat in that folder. Use singular `task-01-<desc>.md`,
  `task-02-<desc>.md`, etc. Keep task numbers stable; dependencies are explicit,
  not inferred from numbering. Create at least one task for delivery work.
- Add supporting evidence only when useful. `ext-refs.md` is optional for a
  wider ledger of pull requests, branches, dashboards, or evidence links. Existing
  ledgers must stay synchronized with the artifact metadata.

```text
docs/changes/some-feature/
  intent.md
  spec.md
  delivery.md
  task-01-add-export.md
  task-02-verify-export.md
```

## Frontmatter and ownership

Use YAML frontmatter for metadata and the body for scope, requirements,
decisions, work instructions, and acceptance criteria. Quote dates and tracker
IDs as strings. Do not put secrets or copied API responses in frontmatter.

- `status`: artifact or change state, defined below.
- `created`: creation date.
- `from`: relative path to the preceding artifact (`intent.md` for spec,
  `spec.md` for delivery, `delivery.md` for a task).
- `approval`: approving person's name and decision date. Leave `by` and `date`
  null until approval is actually given. Record rejections or qualifications
  in the body. File existence, a commit, or an inferred preference is not approval.
- `depends-on`: task filenames for prerequisites, empty when there are none.
- `work-items`: tracker references, empty when unpublished or local-only.

Write the delivery item's reference in `delivery.md` and each child's reference
in its task file. Task `from` is the local parent; `parent-id` and `parent-url`
are the external parent. For example, after successful publication and read-back:

```yaml
work-items:
  - provider: azure-devops
    project: ExampleProject
    id: "1235"
    url: https://dev.azure.com/example/ExampleProject/_workitems/edit/1235
    parent-id: "1234"
    parent-url: https://dev.azure.com/example/ExampleProject/_workitems/edit/1234
    last-verified: "2026-09-08"
```

These are example values, not records to copy. Omit parent fields for the
delivery item. Record returned identities immediately after writes; keep
`last-verified: null` until read-back succeeds. Link the source artifact in the
tracker. Use the project's linked provider and actual hierarchy, not a default
board. Publication and partial-retry rules live in `publish-work-items.md`.

## Lifecycle and revisions

`intent.md` carries the overall change state:

| Status | Meaning |
| --- | --- |
| `draft` | Intent awaits owner acceptance |
| `accepted` | Intent accepted; specification and delivery refinement may proceed through their gates |
| `rejected` | Intent declined with a reason |
| `in-progress` | Delivery approved, tasks ready, implementation authorized and started |
| `shelved` | Work paused indefinitely with a reason |
| `completed` | Delivery acceptance met and integration verified |

`spec.md` and `delivery.md` use `draft` or `approved`. Task files
use `draft`, `ready`, `in-progress`, `blocked`, `completed`, or `cancelled`.
Task approval changes `draft` to `ready`. Record evidence before marking a task
completed. Complete delivery only when its own integration criteria pass.

Resume at the first missing or unapproved stage. For older artifacts without
approval metadata, consult the recorded decision or ask; do not infer approval.
Changing an upstream contract requires review of affected downstream artifacts
and renewed approval where their scope or acceptance changes. Preserve the
prior decision in history and explain the revision. Requirements changes
belong in spec, approach or packaging changes in delivery, and bounded work
changes in tasks. Do not silently add requirements through tasks.

Keep artifacts and tracker definitions aligned during authorized updates.
External systems own live state; the local artifacts hold the reviewed scope.
Keep artifact revisions with the implementation that requires them in version
control. Commit only when authorized; publication is a separate permission.

## Archive

On completion, rejection, or shelving, record the reason or final evidence and
`archived: "YYYY-MM-DD"` in `intent.md`. Move the folder to
`<home>/archive/<original-folder-name>_<COMPLETED|REJECTED|SHELVED>/` once its
final revision is saved. Preserve IDs and update source links or record the
archive destination. Do not modify archived contracts; follow-up work gets a
new folder.

## Templates

Use these templates only when the full workflow or an explicit request calls
for change artifacts. Replace placeholders with project facts. Keep each artifact as short as its
decision allows. Optional fields or inapplicable body sections can be omitted;
do not drop the artifact, its upstream link, approval state, or acceptance.

### intent.md

```markdown
---
status: draft
author: <name and role>
created: "YYYY-MM-DD"
approval:
  by: null
  date: null
work-items: []
---

# Intent: <title>

## Problem and reason to act

<Why this matters now, in the user's words.>

## Affected users and systems

<Who experiences the problem and where.>

## Desired outcome and success measures

<Desired capability and how the owner will recognize success; relation to a
known core domain or product vision when relevant.>

## Constraints and exclusions

<Known constraints with sources, and what this change will not address.>

## Evidence and open questions

<Research links, observed facts, hypotheses, and questions still to resolve.>
```

### spec.md

```markdown
---
from: intent.md
status: draft
created: "YYYY-MM-DD"
approval:
  by: null
  date: null
---

# Specification: <title>

## Scope, terms, and notation

<Behavioral or functional scope, context-scoped domain terms, chosen notation
and why; links to existing domain records when relevant.>

## Requirements

### REQ-01: <observable behavior>

<Actor, preconditions, input or trigger, observable outcome, and constraints.>

## Acceptance examples

<Normal, boundary, and failure cases mapped to REQ IDs with pass-or-fail conditions;
context and cross-context contract meaning where relevant.>

## Exclusions and unresolved decisions

<Excluded behavior, answered intent questions, and remaining decisions with
owners. Behavior-defining gaps block approval.>
```

### delivery.md

```markdown
---
from: spec.md
status: draft
created: "YYYY-MM-DD"
approval:
  by: null
  date: null
work-items: []
---

# Delivery: <shippable outcome>

## Outcome and scope

<Shippable user outcome, included REQ IDs, and explicit exclusions.>

## Implementation approach

<Chosen design and rationale, reuse, interfaces, data flow, bounded files,
sequence, and relevant migration or rollout work. When affected, context
ownership, integration relationships, translation, and core investment.>

## Acceptance criteria

- [ ] <End-to-end pass predicate, linked REQ IDs, and integration evidence.>

## Verification

<Exact checks or commands and expected results for each included requirement.>

## Dependencies, risks, and release conditions

<Prerequisites, implementation risks, integration boundary, release conditions,
and unresolved decisions.>

## Tasks

<Link every task file and its requirement coverage here during Tasks refinement.>
```

For multi-phase or multi-PR work, expand the body with the skeleton in
`multi-phase-plan.md`. Retain frontmatter, the outcome, requirement mapping,
acceptance, and task index. Delivery approval hands off to Tasks.

### task-NN-<desc>.md

```markdown
---
from: delivery.md
status: draft
created: "YYYY-MM-DD"
approval:
  by: null
  date: null
depends-on: []
work-items: []
---

# Task NN: <bounded objective>

## Objective and coverage

<One bounded objective within delivery scope and satisfied REQ IDs.>

## Scope and prerequisites

<Bounded files or interfaces, inputs, exclusions, and required prior state;
links to domain decisions needed for this task and semantic dependencies.>

## Work

- [ ] <Concrete work item within the approved approach.>

## Acceptance and verification

- [ ] <Binary completion predicate and exact check or command.>

## Evidence

<Observed result and artifact links when run; not expected output presented as
proof. Include remaining blockers or cancellation reasons when applicable.>
```

### ext-refs.md (optional)

Use a flat ledger for additional references. Link to delivery and task files
rather than copying their scope. Include system, type, stable ID and URL,
parent or dependency, source artifact or delivery section, state snapshot, and last
verification date. The source files retain their own tracker metadata even
when a ledger exists.
