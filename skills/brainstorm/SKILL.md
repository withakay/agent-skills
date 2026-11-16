---
name: brainstorm
description: Use when a proposed change needs design clarification, trade-off analysis, or risk-based approval before implementation. Routes by risk and composes interrogate, architect, capture-intent, and prototype.
---

# Brainstorm

Explore uncertain goals and decisions within the current Subspace route. For
full delivery work, brainstorming supports intent capture. A clear, low-risk
edit can use Subspace's fast path without a brainstorming session or artifacts.

## Classify

Use the lightest path that protects the decision:

| Path | Use when | Compose |
| --- | --- | --- |
| Bounded | The outcome and scope are clear, local, low-risk, reversible, and follow an existing pattern | Use Subspace's fast path and **check-change-readiness**. Don't require change artifacts or another approval for the stated edit. |
| Clarify | A material requirement, boundary, or acceptance condition has more than one plausible interpretation | Run **interrogate** on the unresolved decision only: elicit mode when the gap is what the user wants, pressure-test mode when the gap is in a stated approach. |
| Design | The change creates a subsystem, changes a public contract, migrates data, affects security or operations, or is costly to reverse | Research constraints and use **interrogate** to clarify intent or required behavior. Reserve implementation architecture for delivery planning after spec approval. |
| Spike | The user asks a feasibility question or throwaway experiment | Run the `prototype` playbook. State the probe and its limits, investigate cheaply, and report evidence. Keeping spike code requires a separate implementation decision. |

Reuse answers and approvals already supplied. For the fast path, the explicit
request authorizes the bounded edit. For full work, follow the artifact
approval sequence; a clear request doesn't approve unwritten artifacts.

Reassess the route when evidence reveals wider impact. State what changed and
ask only about the unresolved decision. Don't downgrade a change to avoid a
necessary approval.

## Process

1. Inspect current files, docs, tests, and relevant history before asking questions. Use the **how** skill for subsystem grounding and the **why** skill when prior decisions constrain the design.
2. Identify the outcome, constraints, success evidence, affected boundaries, and reversibility.
3. Remove speculative scope. Follow existing project patterns unless they cause the stated problem, per the **less-is-more** principle skill.
4. Compare options that resolve the current stage's question. Discuss desired outcomes during intent capture and required behavior during specification. Use **architect**, design only, for implementation choices during planning.
5. Cover data flow, failure handling, compatibility, security, operations, and testing only where relevant.
6. For full work, record findings in the owning artifact: `intent.md` for purpose and scope, `spec.md` for behavior, or `delivery.md` for implementation approach and shippable work. For a small edit, a short response is enough.
7. Return to the selected route. Use **check-change-readiness** before implementation. A completed brainstorming session doesn't authorize publication or replace full-workflow approvals.

Use **show-me** only when the user explicitly asks for a visual explanation.

## Approval boundaries

Follow the owning stage's approval boundary. Research can continue within the
requested scope; publishing, implementation, and irreversible actions require
their applicable authorization. Never infer approval from brainstorm completion.
