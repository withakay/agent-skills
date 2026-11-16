---
name: principle-prioritize-end-state
description: "Apply during planned rewrites or migrations with explicit phases. Prefer the target architecture over temporary compatibility code in isolated development states; keep release, contract, data, and security boundaries."
disable-model-invocation: true
---

# Prioritize the end state

Optimize for the intended, verifiable end state. Don't preserve smooth intermediate states.

Keeping every intermediate step fully stable often creates temporary compatibility code that becomes long-lived debt. Converge on the target architecture, and prove correctness at explicit verification boundaries.

## Rules

- Prioritize end-state integrity over transitional stability.
- Intermediate breakage is acceptable only in planned, scoped, isolated development states, and when it is reversible.
- Run final verification at the relevant boundary before you declare the work done.

## Guardrails

- Use this principle for planned rewrites and migrations with explicit phase boundaries.
- Declare where temporary breakage is acceptable.
- Never break the default branch, released systems, public contracts, data safety, security, or approved rollout commitments. Do not waive external compatibility.
- Keep high-signal checks for actively touched areas while you migrate.
- At plan completion, run direct checks of the relevant boundary. Do not require a full build or audit for an unrelated change.
- For internal API replacement, follow [Migrate and delete](../principle-migrate-and-delete/SKILL.md). Don't keep dual internal APIs as transitional compatibility.
