# Technical Writing Style Guide

Use this reference for detailed sentence, procedure, and structure review. The canonical workflow remains in `../SKILL.md`.

## Sentences

- Address the reader as "you" when appropriate and use present tense for current behavior.
- Write instructions as commands. State facts directly.
- Put the common case first and exceptions after it.
- Split an instruction longer than about 20 words or another sentence longer than about 25 words when the split preserves logic. These are review thresholds, not hard limits.
- Replace an unclear pronoun with the correct noun. Do not use "this" or "which" for a whole clause when the referent can be read two ways.
- Keep "only" and "not" next to the word they modify.
- Give every coordinated clause a verb. Make the grouping of `and` and `or` explicit when two readings are possible.
- Keep articles when they distinguish one item from two: "the client and the host."
- Replace long noun strings with a clause: "the script that checks the proto-import budget."
- Replace an `-ing` form when it hides the actor or action.
- Use active voice when the actor matters. Passive voice is valid when the actor is unknown or irrelevant.
- Preserve negative wording for security, safety, legal, and data-loss prohibitions.

## Terms and Tone

- Use one term for one meaning. Do not cycle synonyms for variety.
- Prefer "use" to "utilize," "help" to "facilitate," and "do" to "perform" when no precision is lost.
- Avoid invented engineering metaphors. Name the mechanism: "a limit that only decreases," not "a ratchet."
- Avoid buzzwords, idioms, decorative jargon, and claims about future support.
- Vary sentence length naturally. Do not force every sentence to be short or every list to contain three items.
- In explanations, evaluate tradeoffs with evidence. Keep reference material factual.
- Do not add first-person reaction, deliberate messiness, or an opinion merely to make prose sound human.

## Procedures and Lists

- Start with prerequisites and conditions that affect whether the reader should continue.
- Give one action per numbered step and state its observable result when verification matters.
- Put warnings immediately before the action they constrain.
- Use direct commands, not narration or "should be done."
- Introduce a list with a complete sentence and keep items grammatically parallel.
- Use a partial-list signal such as "including" instead of ending with "etc."
- Preserve exact commands and quoted errors. Do not silently correct command syntax without verifying it.

## Headings and Links

- Use one `h1`, do not skip heading levels, and use sentence case.
- Make task headings bare verb phrases and concept headings noun phrases.
- Put the point in the heading when practical: "Pick the mode first," not "Modes."
- Use the page title or destination description as link text. Do not use "click here."
- Prefer enough local context to let the reader decide whether to follow a link.

## Ambiguity Review

Ask these questions:

1. Does every action have the correct actor?
2. Does every condition have a clear result and scope?
3. Can `only`, `not`, `and`, or `or` attach to the wrong phrase?
4. Does every pronoun refer to one noun?
5. Are requirement, recommendation, permission, and possibility distinct?
6. Are values, units, dates, paths, commands, and limits complete?
7. Does each object have one stable name across the document set?
8. Could two competent readers take different actions from the text?

Ask a focused question when source evidence cannot resolve a consequential ambiguity.

## Sources

These rules synthesize Diataxis, the Google developer documentation style guide, ASD-STE100 Issue 9 principles, and Kohl's *The Global English Style Guide*. Use the current source standard when formal compliance or a disputed rule matters.
