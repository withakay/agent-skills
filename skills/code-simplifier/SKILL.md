---
name: code-simplifier
description: Use when asked to simplify, reduce, or clean up recently changed code while preserving its observable behaviour. Not for adding features, fixing bugs, reviewing a diff for defects, or removing AI slop, which uses `deslop`.
---

# Simplify code

Make recently changed code easier to understand, maintain, and modify without changing its observable behaviour.

Prefer the simplest implementation that clearly expresses the intent.

## Look for

- unnecessary abstractions, indirection, wrappers, and layers
- duplicated or repeated logic
- excessive nesting and branching
- unnecessary state or intermediate values
- overly defensive code for impossible or already-constrained cases
- comments that merely restate the code
- clever or compressed code that is harder to understand than an explicit alternative
- abstractions used only once that make the code harder to follow
- complexity introduced for hypothetical future requirements

## Guardrails

- Follow the project's existing conventions and instructions. Do not introduce personal style preferences where the project already has an established approach.
- Do not optimise for line count. Optimise for comprehension and changeability.
- Preserve useful abstractions where they clarify responsibilities, isolate meaningful complexity, or represent genuine domain concepts.
- Prefer deleting complexity over reorganising it.
- Keep the scope focused on code changed by the current work unless asked to review more broadly.

## After simplifying

1. Verify observable behaviour has not changed.
2. Run the relevant existing checks where practical.
3. Remove anything made obsolete by the simplification.
4. Report only changes significant enough to help someone understand the result.

A successful simplification leaves less code, fewer concepts, or less cognitive overhead without hiding complexity somewhere else.
