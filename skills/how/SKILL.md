---
name: how
description: Use when the user asks for a codebase walkthrough, runtime-flow explanation, ownership analysis, or architecture critique.
---

# How

Explain how a codebase or subsystem works from current evidence. Prefer a working mental model over annotated source.

## Route

- Simple question: explore directly and answer in the parent session.
- Complex cross-file or cross-service question: optionally partition 2-4 independent read-only exploration angles, then synthesize them.
- Rationale or prior-decision question: invoke `agentsview-finding-history` for recorded agent history and `ask-second-brain` for broader synthesized knowledge. An empty search means no result, not proof that no rationale exists.
- Explicit visual request: invoke `show-me`. Use `archify` for a durable diagram artifact.
- Architecture critique: explain the current flow first, then review it against the stated constraints.

When in doubt, start direct. Add agents only when separate contexts reduce a genuinely broad search.

## Direct Exploration

1. When lean-ctx is available, call `ctx_compose` for task-ranked context.
2. Trace definitions, callers, data, and dependencies with `ctx_read`, `ctx_search`, `ctx_callgraph`, and `ctx_graph`, or with the harness's file, text, symbol, and reference search when lean-ctx is not available.
3. Read implementation, tests, configuration, and entry points. Do not infer behavior from file names.
4. Stop when the trigger-to-effect path is supported by file and symbol evidence.

Use tool-side filters for paths, symbols, and result counts before expanding context.

## Optional Agent Exploration

For a complex question, give each read-only agent one angle, such as request flow, state ownership, configuration, or external integration. Use the runtime's available agent type and select capability for the task; do not hard-code a provider or model. Prompts may use `references/explorer-prompt.md`. Synthesis may use `references/explainer-prompt.md`.

The parent verifies contradictions against source before presenting the explanation.

## Output

Adapt these sections to the question:

- Overview: what the subsystem does and its boundary.
- Key concepts: only the types and abstractions needed for the flow.
- Flow: trigger, steps, decisions, state changes, external effects, and result.
- Ownership: relevant files, packages, services, and interfaces.
- Gotchas: non-obvious behavior, failure modes, compatibility, or unresolved rationale.

Cite file and symbol locations. Include code only when the exact shape is necessary.

## Critique

Evaluate correctness, coupling, data ownership, boundary clarity, failure handling, security, operability, and testability. Categorize observations as:

- Act on: demonstrated issue worth fixing now.
- Consider: credible concern with uncertain trade-off.
- Noted: valid but low priority.
- Dismissed: unsupported, incorrect, or preference-only.

Use `references/critic-prompt.md` and `references/critique-rubric.md` when an independent critique adds value. Keep the explanation usable without the critique.
