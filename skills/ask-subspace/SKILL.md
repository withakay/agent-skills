---
name: ask-subspace
description: Ask which subspace skill, playbook, or flow fits your situation. A conversational router over this collection.
disable-model-invocation: true
---

# Ask Subspace

Answer the user's "what should I use for this?" with the route below, then
stop. Don't start implementation from a routing question.

A workflow is a path through the skills. The `subspace` skill's route table is
the authoritative index; this skill explains the available paths.

## Small changes

For a clear, local, low-risk, reversible change such as "Change button from
green to blue," use Subspace's fast path: inspect the target, run
**check-change-readiness**, implement, and verify. No change package, interview,
tracker item, or additional process approval is required. Reassess the route
if inspection reveals wider impact or a material unresolved decision.

## Full delivery workflow

1. **Intent:** `capture-intent` writes `intent.md`, answering why the work is needed. Research, **brainstorm**, and **interrogate** help clarify the user's goals before acceptance.
2. **Specification:** `design-spec` writes `spec.md`, defining precise observable behavior or functional requirements, with explicit pass-or-fail criteria. Implementation choices follow later.
3. **Delivery:** `refine-delivery` plans implementation scope, approach, and acceptance as one shippable `delivery.md`, also called a product backlog item (PBI) or delivery plan. Use **architect** for non-trivial implementation design and `multi-phase-plan` for a detailed multi-PR body. Do not create a separate `plan.md` for new changes.
4. **Tasks:** the same playbook produces bounded `task-NN-<desc>.md` files with dependencies and verification. Each file uses frontmatter for status, approval, and tracker metadata.
5. If a tracker is linked to the project, `publish-work-items` previews and publishes the delivery as a parent and the tasks as children, then reads them back and records IDs and links in their source files. Otherwise the artifacts remain local.
6. Use **check-change-readiness**, then run approved, ready tasks with the matching playbook, such as **`feature`** or **`refactoring`**. Verify task acceptance and the delivery outcome. Use **`opening-a-pr`** when authorized, and **`verification-before-completion`** before any completion claim.

Not sure what is wanted yet? Start at **`capture-intent`**; brainstorming and
interrogation support that stage. Resume existing artifacts at the first
incomplete or unapproved stage.

## Other routes

- **Something's broken** → **`bug-fix`** (playbook) with **`root-cause-debugging`** as the diagnostic engine: reproduce, gather evidence, one hypothesis at a time, fix the cause, verify. Live-system diagnosis without a known bug → **`runtime-forensics`**.
- **Slow or resource-heavy** → **`perf-issue`**. Evidence is the trace.
- **"Explain or recommend, don't change anything"** → **`investigation`**, or **`how`** for a walkthrough and **`why`** for rationale archaeology.
- **A production incident or monitoring finding** → diagnose first, then classify the proposed change through Subspace.

## Supporting skills

- The **`principle-*`** skills are stage inputs for the full workflow: Intent, Specification, Delivery, and Tasks each consider the principles mapped to them in the [principle routing reference](../subspace/references/principle-routing.md) and explicitly load those whose triggers the evidence meets. They add no stage, artifact, or approval, and the fast path and read-only work skip the full matrix. Reach for one directly when the question is about the discipline, not the task.
- **`interrogate`** is the questioning primitive: elicit mode for wants, pressure-test mode for artifacts. `capture-intent`, `brainstorm`, and `architect` all drive it.

## Standalone

- **`prototype`** answers one design question with throwaway code.
- **`show-me`** for a visual explanation; **`teach`** to learn a concept.
- **`create-ascii-diagram`** for architecture, flow, or ownership as a text diagram.
- **`fix-merge-conflicts`** mid-conflict; **`extract-workflow`** to turn a repeated chat pattern into a skill; **`create-skill`** to author one; **`reflect`** to mine a session for lessons.
- **`code-simplifier`**, **`test-simplifier`**, **`deslop`**, and **`unslop`** before review; **`technical-writing`** for prose.
- **`session-pickup`** and **`pause-safely`** at session boundaries; **`orchestrate`** for long-running coordination.

## Answer format

Name the one skill or playbook that owns the situation, the flow position it sits at, and what it hands off to next. If two could apply, say which wins and why in one sentence.
