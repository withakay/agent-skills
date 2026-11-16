---
name: principle-migrate-and-delete
description: "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers."
disable-model-invocation: true
---

# Migrate and delete

When a new API is the right design, migrate callers and remove the old API in the same refactor wave. Don't preserve compatibility layers.

## Rules

- Don't keep legacy API paths alive only because internal callers still exist.
- Inventory callers, migrate them, and delete the old API immediately.
- Treat temporary adapters as exceptional and time-boxed, not as default architecture.
- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details.

## When this applies

- No external users depend on backward compatibility.
- The project can absorb coordinated breaking changes.
- The new API is part of a simplification or refactor initiative.

One repository does not imply one model or change authority. Confirm that
affected contexts can coordinate the migration. Keep translation between
different models; it is not an obsolete compatibility path.

Keeping both old and new APIs creates dual-path complexity, slows cleanup, and makes the codebase feel append-only.
