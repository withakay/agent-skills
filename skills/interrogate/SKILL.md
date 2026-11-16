---
name: interrogate
description: Use when the user asks to be interviewed about what they want (grill me, interview me, elicit requirements) or to pressure-test a plan, proposal, or design sketch, through one decision-focused question at a time.
---

# Interrogate

Resolve the highest-impact unknowns through relentless, disciplined questioning. Two modes share one core: **elicit** questions the user about what they want; **pressure-test** questions an existing plan, proposal, or design sketch.

## Pick the mode

| Signal | Mode |
| --- | --- |
| "Grill me", "interview me", vague wants, `capture-intent` step 2 | Elicit |
| "Pressure-test this", an existing plan, spec, or `architect` sketch | Pressure-test |

An artifact to attack means pressure-test. No artifact yet means elicit.

## Core rules, both modes

- Inspect repository evidence before asking for facts the code can answer.
- Ask exactly one concise question per message.
- Resolve prerequisite decisions before dependent ones.
- Stay on the current question until the answer is clear enough to proceed.
- Do not turn the exchange into a fixed questionnaire. Each question follows from the last answer or the next-largest unknown.
- Vague answers get a sharper follow-up, not silent acceptance. "Users want it faster" is not an answer; "which users, doing what, how slow is it now" is the follow-up.

## Elicit mode

Target: the user's intent. Do not propose solutions, shapes, or technology choices; naming an option the user already implied is fine, designing is not.

Hunt the unknowns an analyst would: the problem in concrete terms, who is affected, why now, what better looks like, constraints, what is explicitly out of scope, and how success is measured. Challenge contradictions between answers directly.

Stop when you could write an `intent.md` (per `skills/subspace/references/change-artifacts.md`) that the user would accept with at most one correction pass. Then offer to write it via the `capture-intent` playbook.

```text
Question: <one unknown about what is wanted>
Why it matters: <what changes downstream depending on the answer>
```

## Pressure-test mode

Target: the artifact. Attack what could break, the riskiest step, hidden coupling, unstated assumptions, and the alternatives not taken.

Include a recommended answer and its main trade-off with each question.

Stop when the proposal is coherent, implementable, and has explicit remaining unknowns. Report the unknowns; do not silently absorb them.

```text
Question: <one decision>
Recommended: <best current answer and why>
```
