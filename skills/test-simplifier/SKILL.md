---
name: test-simplifier
description: Use when asked to prune, simplify, or reduce recently changed tests, remove low-value or redundant tests, or shrink a test suite while keeping meaningful behavioural coverage. Not for writing new tests, diagnosing failures, or simplifying production code, which uses `code-simplifier`.
---

# Simplify tests

The purpose of a test suite is to protect important behaviour and enable fast, confident change. More tests are not inherently better.

Review recently changed tests and remove or simplify tests that do not carry their own weight.

Prefer tests that exercise meaningful behaviour, logic, contracts, edge cases, and failure modes.

## Question tests that

- merely verify that a value was assigned or configuration was copied correctly
- restate implementation details rather than observable behaviour
- test framework, language, or library behaviour
- duplicate behaviour already covered by another test
- assert trivial getters, setters, constructors, mappings, or wiring
- mock everything and therefore prove little about the real behaviour
- exist primarily to increase coverage metrics
- repeat the same behaviour through many insignificant variations
- would almost never catch a realistic regression
- cost more to understand, maintain, or execute than the protection they provide

Do not preserve a test merely because it already exists.

For each test, ask:

> What realistic regression would this test catch?

If there is no convincing answer, consider deleting it.

Prefer a smaller number of high-value behavioural tests over exhaustive tests of trivial implementation details.

Consolidate repetitive cases when doing so improves readability. Delete redundant fixtures, helpers, mocks, setup, and test-only abstractions made unnecessary by the simplification.

## Do not remove tests that protect

- important business rules
- externally observable behaviour
- contracts between components or systems
- meaningful edge cases
- error and recovery behaviour
- security or permission boundaries
- regressions that have previously occurred
- complex logic where a failure would not be obvious

## Guardrails

- Do not optimise for coverage percentage. Coverage is evidence, not the objective.
- Optimise for confidence per unit of complexity and execution time.
- Keep the scope focused on tests changed by the current work unless asked to review more broadly.

## After simplifying

1. Run the relevant test suite.
2. Confirm the remaining tests still protect the important behaviour.
3. Remove obsolete test infrastructure.
4. Report significant removals and why they were considered redundant or low-value.

A successful test suite is fast, understandable, trustworthy, and proportionate to the risk of the code it protects.
