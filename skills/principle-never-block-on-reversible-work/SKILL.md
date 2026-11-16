---
name: principle-never-block-on-reversible-work
description: "Apply when considering confirmation for reversible work. Proceed with authorized work within the request; keep approval gates, permissions, and irreversible actions."
disable-model-invocation: true
---

# Never block on reversible work

The human supervises asynchronously. Within authorized work, make reasonable decisions, proceed, and let the human course-correct after the fact. Code is cheap. Waiting is expensive.

An unnecessary confirmation stalls the pipeline and makes the human the bottleneck. Because authorized code changes are reversible and reviewable, a wrong decision usually costs less than blocking.

## Pattern

- Proceed, then present. For work the request already covers, such as research, drafting, and reversible edits, show the result. Don't ask "Should I do X?" Do X, and explain why.
- Reserve questions for genuine ambiguity. Ask only when you truly can't infer intent from context.
- Make the system self-healing. When you notice a problem, log it and fix it in the next round.
- Supervision is asynchronous. The human reviews plans, diffs, and changes on their own schedule. Design workflows for review after the fact.
- Code is cheap. Attention is scarce. A blocked agent costs the human's attention to unblock.

## Boundaries

- Irreversible actions such as force-push, deleting production data, or sending external messages still require confirmation.
- Reversible actions such as writing code, editing notes, or splitting tasks proceed without blocking only when the request authorizes them.
- Reversibility does not extend authority. Keep accepted intent, Spec and Delivery approvals, task readiness, and user permissions in force. Do not implement before the required approval.
- Product direction comes from the human. Execution within approved scope shouldn't block.
