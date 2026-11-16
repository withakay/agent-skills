### Bug fix

**You own this task. Plan, review, verify.** Delegate investigation and the fix to subagents when the harness provides them, and stay in the lead; otherwise do both directly.

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix; it does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more. Same discipline for Perf, where the evidence is the trace.

1. Reproduce it yourself on the matching surface with the host's available terminal, browser, simulator, or service controls. Don't hand the repro to the user. Ask the user only when the available controls cannot reach the target, and state the exact limitation. If it will not reproduce directly, synthesize the trigger, tighten conditions, or add temporary instrumentation until it fires. A bug you can't reproduce, you can't prove fixed.
2. Binary-search the cause under the **root-cause-debugging** skill's phase discipline (reproduce, gather evidence, one falsifiable hypothesis at a time; stop and reassess with the human partner after three failed hypotheses). Form candidate hypotheses, then rule them out until one survives. Seed them with the **how** skill for the affected subsystem and the **why** skill for regression history. At each pass, take the split that cuts the most remaining problem space, get runtime evidence, and eliminate a hypothesis. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. For a long or stubborn hunt, use the host's bounded repeat or scheduled-run mechanism when available. Confirm the surviving mechanism with runtime evidence before designing the fix.
3. Plan the fix. For a cross-boundary change, run **architect** before implementation. Delegate implementation with a specific scope to a subagent when the harness provides one, otherwise implement it directly; review the diff yourself.
4. Verify on the same surface; the original repro now passes. If the surface has no project-local verification skill, run **create-verification-skill** before relying on repeated live checks. If an existing verification skill or feature map is stale, run **maintain-verification-skill** before using it. "Inconclusive" or wrong-surface is not a pass; flag it. Unit tests show branch behavior, not bug absence.
5. Stage the commits so the failing repro lands before the fix in git history; the diff tells the story. See the **tdd** skill for the failing-test-first cadence when the bug has a cheap local test path; skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical **principle-sequence-verifiable-units-of-work**, the failing test first and the fix on top.
6. Run **Opening a PR**.

Investigation fans out `how` + `why` as parallel subagents.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
