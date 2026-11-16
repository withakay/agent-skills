---
name: synthesizer
description: "Spawn N parallel agents with the same task, pick the best, graft the strongest parts of the losers into it. Use for /synthesizer, 'synthesize this', 'run in parallel and merge the best ideas', or when one attempt at a non-trivial artifact would lock in the wrong shape."
---

# synthesizer

Run the same grounded task through independent candidates, select one base against an explicit rubric, then adapt only stronger parts that improve the base without making it incoherent.

## Phase A: Frame

Open a todolist with one entry per phase before launching anything. The synthesizer runs autonomously and the list keeps phases from silently disappearing.

1. Restate the task as a falsifiable done condition.
2. Read the source material and identify constraints candidates must share.
3. Define a short rubric before seeing candidates. Include correctness, fit to constraints, simplicity, and verifiability. Add domain criteria only when the task needs them.
4. Decide the candidate count. Use 3 by default. Use 2 for a narrow binary choice and 4 only when the design space has genuinely distinct families.

## Phase B: Generate

1. Give every candidate the same task, grounding artifacts, constraints, rubric, and output contract.
2. Ask for independent solutions, not reviews of an existing favorite.
3. Pick the runners. Use the host's configured agent pool when present. Otherwise use the available local agent runners and include different model families when possible. Use the same model N times when the work is generation-bound rather than judgment-sensitive.
4. Assign output paths. Each candidate writes to its own location (a git worktree where possible, otherwise a per-candidate directory such as `synth-<slug>/candidate-<n>/` under the host's temporary or scratch location). N candidates writing to the same path is shared mutable state and fails the **principle-avoid-shared-mutable-state** test.
5. Launch candidates concurrently when the host supports it. Do not start synthesis until every candidate has completed, failed, or timed out.

Each candidate returns:

- the artifact or concrete proposal;
- a rationale naming the alternatives it considered and rejected;
- verification performed;
- unresolved risks.

The rationale is mandatory. Without it, the parent cannot tell whether a candidate's structure is principled or accidental, which makes grafting unreliable. If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record.

## Phase C: Judge

After all Phase B candidates complete, choose a reviewer from the host's configured agent pool when present. Otherwise use an available runner from a different model family than the parent when the host supports it. Spawn one read-only reviewer. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with the parent's reading in Phase D, not with the candidates themselves. Starting it while candidates are still writing means it sees partial or empty outputs and reports them as dropouts.

The reviewer must identify:

- the strongest candidate and why;
- the strongest unique element in each non-winning candidate;
- contradictions that prevent grafting an element into the base;
- any candidate that fails a hard constraint.

## Phase D: Synthesize

Read every candidate end to end before picking; skimming N candidates surfaces only the one whose surface looks most familiar. Choose the base yourself; the reviewer advises but does not decide. Agreement with the reviewer confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous; read both rationales before deciding.

1. Score each candidate against the rubric criterion by criterion, not on holistic feel, then select the one that best satisfies the whole rubric, not the one with the most individually clever parts. When two feel tied, pick the base a future maintainer can extend without breaking invariants: the cleaner boundary or smaller surface, per the **less-is-more** principle skill.
2. List candidate contributions before editing the base.
3. Graft a losing candidate's element only when it is stronger, compatible with the base's assumptions, and worth the added complexity.
4. Prefer one coherent design over a union of all ideas. Reject additions that duplicate, contradict, or blur ownership.
5. Record what was accepted, adapted, and rejected with one reason each. The rejection notes are the highest-signal part of the record; future readers learn from what was considered and dropped.
6. When the candidates converge on the same shape, note the convergence and ship the consensus shape; no graft is needed. When they wildly diverge, Phase A was under-specified: re-frame and re-run rather than averaging the divergence.

## Phase E: Verify

Verify the synthesized artifact against the Phase A done condition and rubric. Re-run checks after every graft that can affect behavior.

The synthesized artifact has to hold up under the same scrutiny as any other output, per **principle-verify-results**. The synthesizer does not inherit evidence from candidates when the merged artifact differs from them.

If verification surfaces a problem the synthesizer did not catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the signal (return to Phase D). Do not patch around a failed premise.

## Output

Return:

1. The synthesized artifact or its path.
2. The selected base and rubric rationale.
3. Contributions adapted from each other candidate.
4. Rejected ideas and reasons.
5. Verification evidence and remaining risks.
