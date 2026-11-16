---
name: technical-writing
description: Use when writing technical documentation, RFCs, READMEs, or engineering explanations, or when explicitly asked to review technical prose; use writing-pull-requests for PR titles and bodies, and create-commits for commit operations or messages.
---

# Technical Writing

Write for a tired engineer who must understand the text on the first read. Preserve facts, logic, uncertainty, and exact technical names before improving style.

## Workflow

For language-only reviews of existing documentation, read [`references/language-review.md`](references/language-review.md) before editing.

1. Identify the audience, decision or task, source of truth, and primary document mode.
   When the document must show structure, flow, or ownership, load **create-ascii-diagram** and place a verified fenced `text` diagram next to the prose it explains.
2. Verify symbols, paths, commands, versions, counts, and claims against current evidence.
3. Put the conclusion, result, or required action where the reader needs it.
4. Rewrite with direct sentences, stable terms, explicit actors, and visible conditions.
5. Apply the factual cleanup pass. Do not add personality or opinions to compensate for weak source material.
6. Read [`references/style-guide.md`](references/style-guide.md) when sentence structure, procedures, headings, or ambiguity need a detailed review.
7. Compare the result with the source for facts, modality, logic, scope, ownership, and uncertainty.

## Pick One Primary Mode

- **Tutorial:** guide a learner through a complete task with visible results.
- **How-to:** give a competent reader the actions needed to reach one goal.
- **Reference:** organize verified facts, options, limits, and errors for lookup.
- **Explanation:** answer one bounded why question with decisions, constraints, history, and alternatives.

Split material when modes compete. Do not bury reference tables in a tutorial or arguments in a procedure.

## Core Rules

- Use the codebase's real symbol, file, flag, command, and component names.
- Cut words that do no work, but keep articles, conjunctions, qualifiers, and repeated nouns when they prevent a misread.
- Prefer plain words and precise domain terms. Do not replace a technical term with a vague synonym.
- Give one instruction per sentence. Keep a longer sentence when it expresses one condition and consequence more clearly than fragments would.
- Name the actor when known and relevant. Do not invent one to avoid passive voice.
- Put a condition or warning before the instruction it governs.
- Keep modal meaning, `and`/`or`/`not` logic, approximation, and uncertainty unchanged.
- Use numbered lists for order and bullets for unordered items. Keep list grammar parallel.
- Use descriptive sentence-case headings, meaningful link text, code formatting for code, and bold for UI labels.
- Never call a procedure simple, easy, or quick.

## Factual Cleanup

Apply only when the source contains the defect:

- Cut unsupported puffery, promotional claims, formulaic conclusions, and generic statements that could describe any project.
- Replace vague attribution with a named source, or remove the claim.
- Replace invented or unverified metrics, testimonials, logos, and comparisons with verified facts or labeled placeholders.
- Expand an `-ing` phrase when it hides an actor or result; otherwise remove it.
- Remove forced groups, false ranges, and synonym cycling. Use the natural count and one stable term.
- Replace filler and stacked hedges with the shortest wording that preserves uncertainty.
- Use punctuation that makes the sentence easiest to parse. Do not impose a universal punctuation or voice preference.

## Boundaries

Use Microsoft style or Simplified Technical English only when explicitly requested or when that specialist mode fits the document's risk and audience. Product UI strings follow the product's copy system, not this documentation workflow.

PR titles and bodies belong to `writing-pull-requests`. Commit operations and messages belong to `create-commits`. Do not claim a test, result, count, or generated artifact without current evidence.

## Review

Check that the reader can identify the purpose, actor, action, condition, result, and next step without guessing. Confirm every pronoun has one referent, each thing has one name, link text names its destination, and all code or path references are current.
