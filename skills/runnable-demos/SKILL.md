---
name: runnable-demos
description: Use when the user asks to create, update, validate, list, run, or continue a repository Markdown demo or runnable demo, including requests such as "list the demos I can run" or "run foo demo"; not for product demo copy or ordinary automated test implementation.
---

# Runnable demos

Treat a demo as an executable runbook and a Markdown acceptance test. Store each
demo at `<repo>/demos/<demo-name>/DEMO.md`. Search only that repository-level
`demos/` directory unless the user gives another path.

## Route the request

- **List:** run `demo.py list` and report each demo's name, description, kind,
  path, and validity.
- **Create:** read [`references/demo-format.md`](references/demo-format.md),
  copy [`assets/DEMO.template.md`](assets/DEMO.template.md), and replace every
  placeholder with content based on the repository.
- **Update:** resolve `this demo` or `that demo` from the named path or most
  recent demo in the conversation; ask only when multiple demos fit. Read the
  complete bundle before editing. Preserve its kind unless the user asks to
  convert it. Update commands, checks, expected results, acceptance criteria,
  and cleanup together.
- **Validate:** run `demo.py validate [name]`. Fix structural errors, broken
  local links, and incomplete runnable steps.
- **Run or continue:** read
  [`references/running-demos.md`](references/running-demos.md) and follow the
  demo from its preconditions through cleanup.
- **Terminal evidence:** when the demo or user requests images or an HTML run
  report, read [`references/terminal-evidence.md`](references/terminal-evidence.md).
  Execute one annotated block at a time through the skill-owned Python runner.
  Keep each fence body as the exact plain command a human can copy and paste.

Resolve this skill's directory as `SKILL_DIR`, then invoke its helper from the
target repository root:

```bash
python3 "$SKILL_DIR/scripts/demo.py" list
python3 "$SKILL_DIR/scripts/demo.py" validate
python3 "$SKILL_DIR/scripts/demo.py" validate foo
python3 "$SKILL_DIR/scripts/demo.py" plan foo
python3 "$SKILL_DIR/scripts/demo.py" run foo BLOCK_ID --run-dir EVIDENCE_DIR
```

## Authoring rules

1. `DEMO.md` is the only required file. Use `references/` for on-demand
   instructions, `scripts/` for executable helpers, and `assets/` for inputs,
   fixtures, or expected data. Do not create empty optional directories.
2. Keep a plain Markdown demo plain unless runnable steps add value. A runnable
   demo has `## Steps`; each step has `Action`, `Verify`, and `Accept` fields.
3. Make each acceptance criterion observable and binary. Verify actual state;
   do not treat a successful setup command as proof of its side effect.
4. Use commands that run from the repository root, or state a working
   directory. Never put credentials, tokens, or copied secrets in a demo.
   Prefer Bash 5 for command-oriented macOS/Linux demos and Python 3.10 for
   structured helpers. Reuse the project's language for non-trivial domain
   logic. Use PowerShell only when an existing dependency or target platform
   gives it a concrete advantage.
5. Mark external writes, cost, destructive actions, and required permissions
   before the first affected step. Include cleanup for resources the demo
   creates and guarded restoration for explicitly authorized temporary changes
   to existing resources. Follow the restoration and ownership rules in
   `references/running-demos.md`, including after a failed step.
6. Test safe commands and bundled scripts when authoring. Do not provision,
   delete, publish, or incur cost merely to validate Markdown; run those steps
   only when the user asks to run the demo and has authorized the effect.
7. Mark runner-owned fences with execution metadata. Require explicit effects
   and stable block IDs. The runner reserves external writes before execution,
   never retries them, and requires exact per-block approval.

Do not add a parser or test framework to the target repository. The demo is the
test contract; existing project tools remain the execution mechanism.
