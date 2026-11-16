---
name: principle-make-operations-idempotent
description: "Apply when designing commands, installers, setup or refresh flows, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs."
disable-model-invocation: true
---

# Make operations idempotent

Design operations so they converge to the correct state regardless of how many times they run or where they start from. Every state-mutating operation should answer two questions: What happens if this runs twice? What happens if the previous run crashed halfway?

Commands, lifecycle operations, and processing loops run where crashes, restarts, and retries are normal. If partial state changes the next run's outcome, every restart becomes a debugging session.

## Pattern

- Convergent startup: scan for existing state, clean stale artifacts, and adopt live sessions.
- Content-based cleanup: compare by content equivalence, not creation order.
- Self-healing locks: use PID-based stale lock detection.
- Idempotent scheduling: failed work respawns cleanly, and fresh input is regenerated after each cycle.

## Managed-file setup and refresh

Before writing, inventory the complete destination set and classify each file:

- Absent: create it.
- Content-identical: leave it untouched.
- Tool-owned stale: refresh it only when an ownership marker or canonical source proves ownership.
- User-divergent: report the conflict and don't modify it.

Report all user-divergent files together and resolve them before any write. Apply the approved set as one coherent operation so a failed preflight can't leave a partial mixture of old and new managed content. Use the general reconciliation pattern, not this file inventory, for runtime state.

## Checks

1. What happens if this runs twice in a row?
2. What happens if the previous run crashed at every possible point?
3. Does re-execution converge to the same end state?

If any answer is "it depends on what state was left behind," the operation needs a reconciliation step.
