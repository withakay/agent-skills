---
name: principle-less-is-more
description: "Apply when refactoring, reviewing code or tests, evaluating a diff, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the least new structure that solves the problem."
disable-model-invocation: true
---

# Less is more

Writing code is cheap for you, which makes over-engineering likely. Aim for the most result with the least code and complexity.

- **Prefer deletion.** When asked to refactor or improve, look for removals before additions.
- **Review by subtraction.** For each changed file, try to delete one-use abstractions, duplicated capability, speculative extension points, unnecessary dependencies, unrelated edits, and explanation required only by newly introduced complexity. Name the smaller implementation, and show that the same acceptance checks still pass.
- **Make tests earn their cost.** Keep tests that can catch a plausible behavior regression at a stable boundary. Delete tests that mirror source text, reproduce the implementation's formula, assert mock choreography, duplicate stronger coverage, or change whenever an internal representation changes.
- **Delete test-only seams.** After you remove a low-value test, remove production wrappers, flags, injectable functions, and visibility changes that existed only for that test. A useful test adapts to the production design. Production code shouldn't adapt to the test.
- **Consolidate decisions.** Don't repeat the same choice in several places. Put it behind one source of truth, and pass the result as a flag. If answering a question requires tracing through more than three files or layers, follow [Write readable code](../principle-write-readable-code/SKILL.md).
- **Minimize structure, not line count.** Choose the fewest new concepts, states, files, and ownership boundaries that make the behavior true. A longer direct implementation can be clearer than a short abstraction stack.
- **Preserve distinct meanings.** Similar shapes in different contexts need not share one model. Keep distinctions and translation that express different domain rules; follow [Make model boundaries explicit](../principle-make-model-boundaries-explicit/SKILL.md).
- **Question the threading.** If a task asks you to pass a new signal through types, schemas, pipelines, or similar layers, stop and look for a more direct path.
- **Remove tiny leaks.** Remove tiny pass-throughs, representation leaks, and duplicated choices before they spread. Small leaks compound into permanent coordination costs.

If a human developer would find the code exhausting to maintain, it is a bad solution.
