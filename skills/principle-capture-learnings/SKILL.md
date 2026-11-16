---
name: principle-capture-learnings
description: "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text."
disable-model-invocation: true
---

# Capture learnings

Encode recurring fixes in mechanisms such as tools, code, metadata, and automation instead of textual instructions. Every error, human correction, and unexpected outcome is a learning signal. Capture it, route it, and close the loop.

Textual instructions are easy to miss. They require the reader to notice, remember, and comply. Structural mechanisms such as lint rules, metadata flags, runtime checks, and automation scripts enforce the rule without cooperation.

## Pattern

When you catch yourself writing the same instruction a second time:

1. Ask whether this can be a lint rule, a metadata flag, a runtime check, or a script.
2. If yes, encode it and delete the instruction.
3. If no, because it genuinely requires judgment, make the instruction more prominent and add an example of the failure mode.

## Pick the strongest rung

When more than one mechanism would work, choose the strongest the situation allows: an unrepresentable state that cannot compile, then a lint or banned API that fails CI, then a canonical helper, then a runtime check. Agents copy whatever the surrounding code already does, and a weaker guard becomes the next template.

If the fix is structural, use only the structural fix. The instruction is the symptom.

## Feedback loop

- Capture every correction. When the human intervenes or tests fail, decide whether it's a one-off or a pattern.
- Route to the right layer. One-off goes to a brain note. A recurring fix goes to a skill or lint rule. A systemic issue goes to a principle.
- Close the loop. Don't only record. Apply now or create a concrete todo.

## Anti-patterns

- Acknowledging without recording. "I'll keep that in mind" doesn't persist.
- Recording without routing. A brain note about a lint rule that should exist is wasted unless the lint rule gets implemented.
- Fixing without generalizing. Fixing one instance while leaving the recurring pattern intact.
