# Demo format

<!-- toc -->
## Contents

- [Bundle](#bundle)
- [Kinds](#kinds)
- [Executable fence metadata](#executable-fence-metadata)
- [Recommended sections](#recommended-sections)
- [Updating](#updating)
<!-- tocstop -->

## Bundle

Only `DEMO.md` is required:

```text
demos/<demo-name>/
|-- DEMO.md
|-- references/   # Extra instructions loaded only when needed
|-- scripts/      # Setup, exercise, verification, or cleanup helpers
`-- assets/       # Inputs, fixtures, schemas, snapshots, or expected data
```

Keep all optional resources specific to the demo. Link each resource directly
from `DEMO.md`. Do not make reference chains. A script must be executable or
have its exact interpreter command in `DEMO.md`.

`DEMO.md` starts with skill-style YAML frontmatter. `name` matches its parent
directory. `description` states the behavior demonstrated and important
requirements.

## Kinds

A **Markdown demo** is a prompt, scenario, or human runbook. It can use any
clear headings and need not contain commands.

A **runnable demo** contains `## Steps` and one or more numbered H3 steps. Use
this shape for each step:

````markdown
### 1. Create the sandbox

**Action**

Create an isolated sandbox named `demo-foo`.

**Run**

```bash
sandbox create demo-foo
```

**Verify**

```bash
sandbox show demo-foo --output json
```

**Accept**

- [ ] The command exits with status `0`.
- [ ] The JSON field `state` is `Ready`.

**Evidence**

Save the JSON output as `artifacts/demos/foo/sandbox.json`.

**Pause**

Wait for human confirmation.
````

`Action`, `Verify`, and `Accept` are required for every runnable step. `Run`,
`Evidence`, and `Pause` are optional. Put exact commands in fenced blocks.
When a person must perform an action, state `Actor: human` in `Action`. When
either actor can perform it, state `Actor: human or agent`.

Use `Pause` only for a real decision, visual judgment, permission boundary, or
explicit guided walkthrough. The user can request guided mode without `Pause`;
the runner then stops after every verified step.

## Executable fence metadata

Add `demo` and attributes after the shell language when the skill-owned runner
may execute a fence. The body remains the sole command source and stays directly
copy/pasteable:

````markdown
```bash demo id=show-ready effect=read timeout=60
sandbox show demo-foo --output json
```
````

Required attributes:

- `id`: stable lowercase hyphen-case block ID.
- `effect`: `read`, `local`, `write`, or `cleanup`.

Optional attributes:

- `terminal`: evidence/session group; default `main`.
- `mode`: `command`, `prompt`, `tui`, or `manual`.
- `capture`: `safe` or `none`; default `safe`.
- `timeout`: seconds greater than 0 and at most 3600; default 30.
- `expected-exit`: expected integer exit status; default 0.
- `wait-text`: required for `prompt` and `tui` modes.
- `before-capture` and `after-capture`: comma-separated TUI keys.
  `after-capture` is required for `tui` mode; it carries the keys that end the
  program.
- `observe-text`: capture and print a safe progress checkpoint while the
  original command continues.

`Verify` fences must use `effect=read`. `write` and `cleanup` require exact
per-block approval and are durably reserved before execution. `manual` prints
the source but is never run or captured. Use it for authentication and other
known secret-bearing interactions.

## Recommended sections

- `Goal`: user-visible behavior or outcome.
- `Preconditions`: tools, access, state, cost, and safety constraints.
- `Steps`: runnable work and step-level acceptance criteria.
- `Completion`: end-to-end acceptance criteria not owned by one step.
- `Cleanup`: exact teardown and cleanup verification.

Expected output must use stable fields or short fragments. Do not paste IDs,
timestamps, credentials, or a full volatile transcript as an expectation.

## Updating

Read the demo and every linked local resource before editing. Check commands
against repository documentation and installed tool help. If an action changes,
also change its verifier, acceptance criteria, evidence, and cleanup. Preserve
unknown bundle files. Convert a Markdown demo to runnable form only when the
user asks or agrees.
