# Running demos

## Select a mode

- **One-shot:** default when the user says `run <name> demo`. Run all eligible
  steps in order. Stop at failure or any explicit human pause.
- **Guided:** use when the user asks for step-by-step execution, asks to run the
  next step, or wants human verification. Run one step, report it, and stop.
- **Human-led:** use when a step says `Actor: human`. Present the exact action
  and command. Do not claim it ran. Wait for the person's result before
  verification.

An explicit `Pause` always overrides one-shot mode.

## Preflight

1. Read all of `DEMO.md` and only the linked resources needed for the next
   step.
2. Validate the demo with `demo.py validate <name>`.
3. Resolve tools, working directory, access, environment, expected cost, and
   existing resources. Prefer the demo's read-only preflight commands.
4. Identify every external write or destructive command. Obtain required user
   authorization before that boundary; a request to run the demo authorizes
   its stated ordinary effects, but not unstated or broader effects. Before an
   authorized temporary change to an existing resource, capture its original
   state and define guarded restoration and verification.
5. Establish the current step. In the same conversation, use the prior step
   report. In a new conversation, inspect durable evidence or ask which step
   completed. Never infer completion from expected output.
6. If the demo or user requests terminal images, follow the terminal-evidence
   reference linked from `SKILL.md`. Use `demo.py plan` and run one named fence
   at a time. The Python runner executes the exact body with Bash 5 or its
   explicitly declared PowerShell dependency. Use separate terminal names and
   evidence subdirectories for separate terminal processes.

## Run a step

1. State `Step N/T: <title>` and the actor.
2. Show the exact command before execution.
3. Run the action when the actor and permissions allow it.
4. Run the independent verifier after the action. Capture the command, exit
   status, and relevant output. A successful action is not its own verifier.
5. Evaluate every `Accept` item as pass or fail from observed evidence.
6. Save evidence at the demo's named path when requested. With terminal capture,
   save a receipt and image immediately after each action and verifier, and at
   each human checkpoint. Refresh the HTML report each time, including failure.
   Keep the demo's commands unchanged; capture is the runner's responsibility.
7. Stop on a failed criterion. Report the smallest useful diagnosis; do not
   continue into dependent steps. Perform already-authorized restoration as
   described under "Complete and clean up"; failure does not cancel it.
8. In guided mode or at `Pause`, report and wait. Otherwise continue.

Use this report shape:

```text
Step 2/10: Create cluster — PASS
Action: agent
Command: <exact command>
Exit: 0
Observed: <relevant output or artifact path>
Acceptance:
- PASS: <criterion and evidence>
Next: Step 3 — <title>
Pause: waiting for human confirmation
```

Use `BLOCKED` when the action awaits a human or permission. Use `FAIL` when a
command or acceptance criterion fails. Do not label expected output as
observed output.

## Complete and clean up

After the last step, evaluate `Completion` criteria. Run cleanup when the demo
requires it or the user requests it. Distinguish these operations:

- Restore explicitly authorized temporary changes to existing resources to the
  captured baseline, including after a failed step. Verify the restoration and
  report any failure immediately. If guards no longer match, report the conflict
  rather than overwrite unrelated changes.
- Delete only resources created and owned by this run.
- Leave other borrowed resources untouched.

Retain evidence unless the demo explicitly says to remove it.
Report final status as `PASS`, `FAIL`, or `BLOCKED`, failed criteria, evidence
paths, and cleanup status.

Finalize terminal evidence after criteria review and cleanup. Close only the
run's own session, including after a timeout or failure. Retain partial images,
failed receipts, unresolved checkpoints, and cleanup results. Never repeat an
external write to obtain a better screenshot. A screenshot supports the observed
state checks; it does not replace them.
