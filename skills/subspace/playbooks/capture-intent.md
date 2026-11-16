### Capture intent

Answer why the change is needed before deciding what to build. This is the
first stage of the full workflow. Small, low-risk edits use Subspace's fast
path instead. An informal request such as "what I'd like you to do next"
needs scope classification before choosing this playbook. Follow
[`change-artifacts.md`](../references/change-artifacts.md).

1. Find an existing change folder before creating one. Resume a draft intent;
   when an accepted intent still covers the request, route to its next
   incomplete stage. Amend the existing intent for a material scope change and
   obtain acceptance again. A separate problem gets a separate folder.
2. Research only what is needed to understand the problem: current behavior,
   affected users, constraints, repository evidence, or linked project records.
   Distinguish observed facts, user preferences, hypotheses, and open questions.
   When domain purpose is relevant, use [domain-modeling](../../domain-modeling/SKILL.md)
   to name the business capability and its relation to a known core domain or
   product vision. Use available evidence; label assumptions rather than inventing
   a strategy or making expert access a prerequisite.
3. Use **brainstorm** to explore uncertain goals or options and **interrogate**
   in elicit mode to ask the user about unresolved needs, one question at a
   time. Reuse answers already supplied. These are supporting activities inside
   intent capture, not routes around the artifact chain. A suggested solution
   is a hypothesis until its purpose and constraints are understood.
4. Before choosing scope or constraints, consider the Intent principles in
   [`principle-routing.md`](../references/principle-routing.md). Compare each
   trigger with the evidence, explicitly load the principles that apply, and
   apply them to purpose, scope, constraints, and evidence. For a defect,
   separate supported causes from hypotheses without blocking intent on
   unnecessary debugging. Record a material effect or override in the intent
   section that owns it; add no principles section.
5. Write `<home>/<slug>/intent.md`, `status: draft`, from the template. Capture
   the problem in the user's terms, the reason to act, affected users, desired
   outcome, constraints, exclusions, success measures, and remaining questions.
   Link material research evidence. Do not choose an implementation design here.
   When the problem has structure, flow, or ownership that prose hides, load **create-ascii-diagram** and include a verified text diagram in the intent.
6. Record existing tracker references if supplied. Do not create a delivery
   item or tasks at this stage; publication follows delivery refinement.
7. Ask the owner to accept or reject the intent. Record the decision;
   on acceptance set `status: accepted` and route to `design-spec.md`. On
   rejection record the reason and archive under the reference's rules.

**Reply:** intent path, captured outcome, unresolved questions, and pending
acceptance. Commit only when authorized.
