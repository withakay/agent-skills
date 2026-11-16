---
name: principle-avoid-shared-mutable-state
description: "Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first. Serialize structurally only when one shared writer is a real invariant."
disable-model-invocation: true
---

# Avoid shared mutable state

When concurrent actors might share mutable state, first ask whether they need the same mutable object. If they don't, eliminate the sharing. When sharing is real, enforce serialization structurally with lock files, sequential phases, or exclusive ownership. Instructions and conventions aren't concurrency control.

Concurrent writes to shared state create race conditions that are intermittent, hard to reproduce, and expensive to debug. Telling agents or goroutines to take turns doesn't work.

## Pattern

1. Identify shared mutable state, such as files both actors read and write, branches both push to, or APIs both define and consume.
2. Default to eliminating the shared write target. Ask whether these actors need one canonical object, or whether they're publishing independent facts. Give each actor its own owned file, key, branch, or state directory, and merge only at the read or reporting boundary. Two workers writing their own `lastX` field into one `state.json` file is still shared mutation. `indexer-state.json` plus `metrics-state.json` isn't.
3. Serialize access structurally only when one shared write target is a real invariant. Use lock files, sequential phases, a single-writer actor, or atomic compare-and-swap. Treat "we need a lock" as a design smell to check, not as the default answer.
