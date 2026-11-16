---
name: root-cause-debugging
description: Use when encountering a bug, test failure, performance problem, build failure, or other unexpected technical behavior, before proposing a fix.
---

# Root-Cause Debugging

Find the root cause before changing production behavior. A containment action can reduce immediate harm; it is not a diagnosis or a completed fix.

## Contain vs Diagnose

When impact is active or safety is at risk, first use the smallest reversible containment: disable a feature, isolate a component, roll back, or stop a destructive operation. Record what containment changes and what evidence it may hide. Then continue the diagnostic workflow. Do not present a retry, guard, fallback, or symptom suppression as the root-cause fix.

## Workflow

Complete each phase in order.

### 1. Reproduce

- Read the complete error, stack trace, warning, path, line, and error code.
- Record exact inputs, environment, steps, expected behavior, and actual behavior.
- Reproduce with the smallest reliable case. If it is intermittent, measure frequency and gather more data instead of guessing.
- Check recent code, dependency, configuration, and environment changes.

### 2. Gather Evidence

- Trace bad data or state backward from the symptom to its origin.
- In multi-component flows, observe each boundary: input, output, configuration, environment, and state. Run once to locate the failing boundary before inspecting that component.
- Compare the broken path with a working example in the same codebase. List all relevant differences and dependencies.
- Separate observed facts from assumptions. Add temporary instrumentation only where it can distinguish causes.

### 3. Test One Hypothesis

- State one falsifiable claim: "X is the root cause because Y; evidence Z would confirm it."
- Make the smallest experiment that changes one variable. Do not bundle fixes or refactors.
- If disproved, remove the experimental change, record the result, and form a new hypothesis from the new evidence.
- After three failed hypotheses or fixes, stop before attempt four. Reassess shared state, coupling, ownership, and architectural assumptions with the human partner.

### 4. Fix the Source

- Create the smallest failing automated test or reproducible script before the fix when feasible.
- Change only the root cause. Do not add unrelated cleanup.
- Add validation or defense in depth only where the data flow shows it prevents recurrence; do not use guards to hide an unknown cause.

### 5. Verify

- Run the original reproduction and confirm the observed failure is gone for the expected reason.
- Run the focused regression test and the relevant broader suite; inspect failures and warnings.
- Verify adjacent behavior and containment removal or intentional retention.
- Remove temporary diagnostics unless they provide deliberate operational value.
- Report the cause, evidence, change, and fresh verification. Do not claim success from code inspection alone.

## References

Read the reference that matches the situation before applying its technique:

- [Root-cause tracing](references/root-cause-tracing.md)
- [Defense in depth](references/defense-in-depth.md)
- [Condition-based waiting](references/condition-based-waiting.md), with a [worked implementation](condition-based-waiting-example.ts)
- [Polluter bisection script](find-polluter.sh) for test-order pollution. It runs each matching file with `npm test <file>`; change that line for another test runner.

This skill is the diagnostic engine behind the `bug-fix` playbook. The fix itself follows the **principle-fix-root-causes** skill: change the cause, not the symptom.
