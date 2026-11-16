# Evaluate routing

<!-- toc -->
## Contents

- [Prepare the run](#prepare-the-run)
- [Run two passes](#run-two-passes)
  - [Discovery pass](#discovery-pass)
  - [Workflow pass](#workflow-pass)
  - [Principle planning pass](#principle-planning-pass)
- [Score and record](#score-and-record)
<!-- tocstop -->

These prompt-based evaluations test discovery and workflow decisions. They
do not prove that an implementation, UI, or tracker integration works.

## Prepare the run

1. Read the current Subspace skill, the request examples in its route table,
   `workflow-scenarios.md`, and **check-change-readiness**. Treat the examples'
   interpretations and each scenario's Pass section as the answer key.
2. Use fresh subagent contexts. Prefer an available smaller, fast, or
   low-reasoning agent over the agent that wrote the instructions. Name the
   actual agent selected; don't claim a model size that the harness doesn't
   expose. If no suitable subagent is available, report the evaluation as not
   run rather than substituting your own judgment and calling it a pass.
3. Keep tested agents read-only. Don't permit edits, commits, publication,
   deployments, or commands that change application state. Run independent
   batches in parallel when supported. Never reuse a context between a
   no-guidance control and a guided test.
4. Keep expected answers out of test prompts. Don't let tested agents read
   this reference, the scenario file, or the request-example answer table.
   For guided tests, supply the skill body with its request-example table and
   evaluation section removed, plus only the required playbooks. Give a
   scoped copy when a harness cannot restrict file reads.

## Run two passes

### Discovery pass

Give a fresh agent the current descriptions of `subspace`,
`check-change-readiness`, `brainstorm`, `how`, and
`verification-before-completion`, and only the request text and context.
Ask it to select the first skill and classify the request as read-only, fast
path, full workflow, resume, or evaluation. It should recognize Subspace as the
router for work requests. A post-implementation check belongs to verification.

Run every request example from the skill, with enough context to resolve
pronouns and the specified small-change boundaries. Include the scenario's
post-implementation verification request as an exclusion case. No skill body
or answer key is supplied in this pass.

### Workflow pass

Give another fresh agent the filtered skill instructions and each scenario's
input and context, but not its Pass section. Ask for:

```text
Case ID:
Selected route:
Next action:
Required artifacts, if any:
Readiness outcome, if applicable:
What must happen before implementation:
Stop condition:
```

Run every case and subcase in `workflow-scenarios.md`. Include a no-guidance
control for the scenario that motivated a routing change when no earlier
baseline exists. Don't teach the expected behavior in the test prompt.

### Principle planning pass

When changing planning-principle routes, also use the input portions of
`evals/principle-planning/cases.json`. Keep its expected behavior, required loads,
and forbidden loads out of tested contexts. The cases cover all 24 principles
across the four stages, plus fast-path and read-only controls.

Observe actual skill calls or fixture-scoped body reads before the affected
decision. Source-body read simulations are not native installed-skill calls;
label them separately. Inspect the artifact or next action to establish the
guidance's effect, including a justified confirmation that an existing decision
already complies. A principle-name list is not evidence.

Test approval, compatibility, wrong-stage and fresh-worker boundaries. Every
required assertion must pass; do not hide a safety failure in an average score.
Preserve baseline outcomes even when they already retrieve useful principles.
Never assume a baseline fails before observing it.

## Score and record

Compare each response with its expected behavior. Evaluate meaning, not keyword
counts. Quoting a prohibition is not evidence that the agent followed it.

- **Pass:** The route, artifact requirement, authorization boundary, and next
  action match the scenario. Required evidence is distinguished from assumed
  results. Different wording is acceptable.
- **Fail:** A material decision is wrong, such as forcing artifacts for a
  button-color edit, treating tenant isolation as low risk, skipping an approval
  in the full workflow, duplicating tracker items, or using readiness to claim
  a completed implementation is correct.
- **Not run:** The test was unavailable, interrupted, contaminated by its
  answer key, or lacked enough output to assess. Don't count it as passing.

Save a short Markdown report in the repository's temporary agent-docs location,
normally `.local/docs/agents/subspace-evals/`. Record the tested revision or
working-diff identity, agent names, provided inputs/context, observed responses,
per-case verdicts, and material failures. Keep expected answers separate from
the inputs that were sent. Don't put transcripts or generated reports in the
skill bundle; the reusable scenarios and this procedure belong here.

For a failure, make the smallest instruction change that fixes it. Rerun that
case in a fresh context and the directly affected near-miss cases. Preserve
the original failure in the report. Stop when the requested behavior and its
boundaries pass; report unrun or unresolved cases explicitly.
