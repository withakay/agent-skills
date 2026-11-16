---
name: verification-before-completion
description: Use before claiming work is complete, fixed, passing, or ready, and before an approved commit, push, or PR.
---

# Verification Before Completion

Make claims only as broad as fresh evidence.

## Freshness

Evidence is fresh when it was produced after the last relevant change to code, tests, configuration, dependencies, generated output, environment, or deployed state. A later unrelated edit does not stale focused evidence; a change that can affect the claim does.

Agent reports, earlier session output, and pre-change runs are leads, not completion proof.

## Choose The Claim And Proof

1. State the exact claim: focused behavior, affected package, integrated branch, release artifact, or deployed system.
2. Identify the closest direct artifact or observation that would prove it.
3. Run the smallest complete check for that claim.
4. Read exit status and relevant output. Count failures, warnings, skipped checks, and unverified requirements.
5. Report the evidence and scope. If it does not prove the claim, state the actual status and gap.

## Evidence Ladder

Prefer direct evidence over proxies:

1. Direct artifact or behavior: inspect the generated file, API response, UI state, database record, deployment resource, or reproduced symptom.
2. Focused executable check: regression test, contract test, parser, schema validator, dry run, or targeted query.
3. Integrated check: affected package tests, build, lint, type check, architecture tests, or end-to-end flow.
4. Release check: full required gates, packaged artifact inspection, deployment validation, smoke tests, and rollback evidence where applicable.

A direct artifact can prove an artifact claim without a test command. It does not prove unrelated build, regression, or release claims.

Avoid tautological tests: assert an observable contract, not duplicated production logic or the test's own setup. Confirm the test fails when that contract is broken.

## Focused Versus Release Checks

- During iteration, run focused checks for changed behavior and affected neighbors. Report them as focused evidence.
- Before claiming a task complete, verify every acceptance condition and the integrated effects of the change.
- Before claiming release or merge readiness, run the repository's required release gates. If they are too expensive, unavailable, or not requested, do not imply release readiness; list the unrun gates.
- A linter does not prove compilation. Tests do not prove every requirement. A successful build does not prove the original bug is fixed.

## Common Claims

| Claim | Minimum direct proof |
|---|---|
| Bug fixed | Reproduce the original symptom or run a regression test after the fix. |
| Regression test is meaningful | RED failure for the expected reason and GREEN pass, or an equivalent mutation/revert demonstration. |
| Tests pass | Fresh named test command with zero relevant failures. |
| Build succeeds | Fresh build command with exit 0. |
| Generated artifact is correct | Regenerate or parse it, then inspect the required fields and diff. |
| Requirements met | Requirement-by-requirement evidence, not only tests. |
| Agent task complete | Inspect actual changes and independently verify the task contract. |
| Deployment healthy | Query deployed state and exercise the relevant runtime path. |

Never hide skipped checks or warning-heavy output behind a success summary. Use qualified language when evidence is partial: name what passed, what was not run, and why.
