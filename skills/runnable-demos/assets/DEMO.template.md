---
name: demo-name
description: Demonstrate one observable behavior and state its important requirements.
---

# Demo title

## Goal

State the user-visible outcome.

## Preconditions

- State required tools, access, initial state, permissions, cost, and safety
  constraints.
- If images are required, name the evidence directory and require Python 3.10+
  with `tui-test==0.1.0b3`. The runnable-demos skill executes annotated plain
  commands through the in-process binding.

## Steps

### 1. Perform one action

**Action**

State the action and whether the actor is a human, an agent, or either.

**Run**

```bash demo id=perform-action effect=local
command --with explicit-arguments
```

**Verify**

```bash demo id=verify-result effect=read
independent-read-only-check
```

**Accept**

- [ ] State one observable, binary result.

**Evidence**

State the output or artifact to retain. If terminal images are required, run
each named fence once and retain its SVG, text, JSON receipt, and refreshed HTML
report. Keep the fence body directly copy/pasteable.

**Pause**

Continue automatically, or wait for human confirmation.

## Completion

- [ ] State the end-to-end observable result.

## Cleanup

State exact teardown commands and how to verify cleanup. Remove this section
only when the demo creates no state.
When terminal capture is enabled, mark cleanup with a stable ID and
`effect=cleanup`. Execute it only with exact approval and retain its receipt.
