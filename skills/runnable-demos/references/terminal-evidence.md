# Incremental terminal evidence

<!-- toc -->
## Contents

- [Requirements](#requirements)
- [Plan and execute](#plan-and-execute)
- [Effects and no-repeat execution](#effects-and-no-repeat-execution)
- [Commands, prompts and TUI screens](#commands-prompts-and-tui-screens)
- [Capture policy](#capture-policy)
- [Receipts and concurrency](#receipts-and-concurrency)
- [Verify the runner](#verify-the-runner)
<!-- tocstop -->

Use the skill-owned runner when a demo needs terminal SVGs or an HTML report.
The Markdown fence body is the only executable source. Humans copy that body;
the runner passes the same bytes to Bash or PowerShell without sourcing a
generated script or adding hidden shell options.

## Requirements

- Python 3.10 or later.
- `tui-test==0.1.0b3`, the Python binding for `tui-test 0.1.0-beta.3`.
- Bash 5 for Bash blocks. Install it with `brew install bash` on macOS, or set
  `DEMO_BASH` to an explicit Bash 5 executable.

Install the binding in the selected Python environment:

```bash
python3 -m pip install --pre 'tui-test==0.1.0b3'
```

The runner uses `tui_test` in-process. It does not require or communicate with
the standalone `tui-test` CLI. Library sessions are process-local.

## Plan and execute

From the target repository root:

```bash
python3 "$SKILL_DIR/scripts/demo.py" validate NAME
python3 "$SKILL_DIR/scripts/demo.py" plan NAME
python3 "$SKILL_DIR/scripts/demo.py" run NAME BLOCK_ID \
  --run-dir .local/demo-evidence/RUN_ID/NAME
```

`plan` performs no execution. `run` executes one block. This makes the runner
composable with human steps and prevents an unsafe "rerun all" operation. Use
the same fresh run directory for related block invocations.

The runner gives every block an isolated Bash 5 or PowerShell process. Blocks
must use explicit files or environment for cross-block state. `DEMO_WORK_DIR`
points to a private sibling of the evidence directory by default. Use
`--work-dir PATH` when related demos or terminal processes must share that
private state. The manifest binds the run to one repository, demo, and work
directory.

## Effects and no-repeat execution

Every runner-owned fence declares one effect:

- `read`: reads state and performs no intentional write.
- `local`: changes only the local checkout or private demo state.
- `write`: changes an external system or incurs the demo's stated effect.
- `cleanup`: removes or stops only a previously identified owned resource.

Run a write or cleanup only with matching approval:

```bash
python3 "$SKILL_DIR/scripts/demo.py" run NAME CREATE_BLOCK \
  --run-dir "$evidence" \
  --approve CREATE_BLOCK
```

The runner writes a `RESERVED` ledger entry before starting an external write.
Any later attempt with that block ID and run directory is refused, including
after a timeout or controller crash. Reconcile an unknown effect manually; do
not choose another directory merely to bypass the reservation. Cleanup needs
its own approval and never runs automatically or in `finally`.

## Commands, prompts and TUI screens

`mode=command` waits for direct process exit. Bash blocks run with an explicit
Bash 5 executable as `bash --noprofile --norc -c <exact-body>`. Therefore the
process exit is the fence body's real final status. Use visible subshell strict
mode where needed:

```bash
(
  set -euo pipefail
  command-one
  command-two
)
```

Do not end a block with an unrelated successful print that can hide an earlier
failure. Keep assertions in the snippet and non-trivial domain checks in the
project's existing helper.

`mode=prompt` waits for `wait-text`, captures a BLOCKED checkpoint, asks the
controller for a response, submits it to the same process, and resolves that
checkpoint only after process exit. The response is not added to runner command
arguments. It can still be echoed by the application, so never use prompt mode
for credentials or tokens. Use `mode=manual capture=none` for authentication.

`observe-text` records and prints a safe checkpoint while that same operation
continues. This lets a person open a second terminal after a submission ID is
visible without repeating the first command.

`mode=tui` waits for `wait-text` and visual idle, sends any `before-capture`
keys, saves a checkpoint SVG, sends `after-capture` keys such as `q`, waits for
the original process to exit, and appends a resolving receipt. `wait_idle` is
only visual stability; process completion always uses direct exit state.

## Capture policy

Automatic recording, shell history, verbose logs, and raw transcripts remain
disabled. `capture=safe` stores bounded visible text, an SVG, and a JSON receipt.
It is for commands with a reviewed safe-output contract. A secret-pattern match
suppresses output and SVG and leaves the receipt BLOCKED.

`capture=none` never reads terminal text or requests a screenshot. Use it for a
known sensitive command, normally with `mode=manual`. Redaction is not a reason
to execute a secret-bearing workflow in a captured terminal.

Never capture credentials, tokens, kubeconfig contents, SAS URLs, raw pod JSON,
authentication/device-code prompts, or model output bodies. Do not repeat an
external write to obtain a better image.

## Receipts and concurrency

The run directory is private and contains:

- `manifest.json` with source hashes, effects, ledger, status and resolution
  links;
- `evidence/<terminal>/...svg` for separate terminal groups;
- bounded text and metadata in the manifest;
- an incrementally rebuilt `report.html` with embedded SVG bytes.

Manifest and report updates use an exclusive short-lived lock and atomic file
replacement. Separate terminal runner processes can append to their own
evidence subdirectories while a long-running command remains active. Terminal
groups do not isolate shared credentials, files, ports, or cloud resources;
the demo defines those ownership boundaries.

A command PASS means its direct exit matched `expected-exit`. Images support
review but do not prove acceptance. A timeout, lost process, suppressed capture,
or unresolved checkpoint remains BLOCKED. The runner never retries.

## Verify the runner

Run pure tests without the binding, then harmless live binding checks:

```bash
python3 -m unittest discover -s "$SKILL_DIR/scripts" -p 'test_*.py' -v
uv run --python 3.10 --with 'tui-test==0.1.0b3' \
  python -m unittest discover \
  -s "$SKILL_DIR/scripts" -p 'test_evidence.py' -v
```

The live tests execute only local Bash snippets and a local one-key TUI. They
prove Bash 5 selection, direct exit status, SVG capture, prompt/TUI resolution,
safe capture suppression, and at-most-once write reservation without touching
any external service.
