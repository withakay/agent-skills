---
name: principle-verify-results
description: "Apply when planning verification before implementation and after a task, before declaring it done, to check the real artifact and behavior rather than relying on a proxy, self-report, or successful compile."
disable-model-invocation: true
---

# Verify results

Verify every task output by checking the real thing directly. Don't infer from proxies, self-reports, or a successful compile.

Unverified work has unknown correctness. Indirect verification such as file modification times, output freshness, agent self-reports, and cached screenshots feels cheaper than direct observation. Acting on a wrong inference costs more than checking the source.

Plan the proof before implementation: at Spec, Delivery, and Tasks, record the minimum direct check at the relevant boundary. After execution, run it and report actual results. A planned check is not an executed check.

After you complete any task, ask how you prove this actually works.

## Check the real thing

- Check process liveness directly, not through derived state.
- Read the actual value, not a cached or derived representation.
- When verification fails, suspect the observation method before you suspect the system.

## Code and features

1. Build it when the change affects built output. Building is necessary but not sufficient.
2. Run it and exercise the actual feature path.
3. Check the chain the change touches. Confirm data flows from input to output.
4. For integrations, test the communication path end to end.

Choose the minimum direct proof. Do not force a build for documentation-only changes, or a full system run for unrelated risks.

## Delegation

Trust artifacts, not self-reports. When you verify delegated work, inspect the actual output artifact, such as a Git diff, file contents, or runtime behavior, not the delegate's summary. Agents report what they intended, not always what happened.

## Reuse checks before scripting

Reuse an existing check when it supplies the required direct proof. Add a small deterministic script only when existing checks do not cover the boundary and repeatability has concrete value. Run it and keep its output so a reviewer can repeat the comparison. Do not create another script merely because scripting is possible.

Completion claims stay owned by [Verification before completion](../verification-before-completion/SKILL.md). This principle adds no separate approval gate.

Keep the artifact visible for the human. Commit it only for large or complex work where the trail has to be auditable later, such as a large port or migration. Most work needs it visible, not committed.
