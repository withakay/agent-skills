---
name: principle-boundary-discipline
description: "Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries such as CLI, config, network, and external APIs. Trust internal types, and keep business logic in pure functions."
disable-model-invocation: true
---

# Boundary discipline

Place validation, type narrowing, and error handling at system boundaries. Trust internal types after they have been parsed at a boundary. Business logic lives in pure functions. The shell is thin and mechanical.

Scattered validation is noisy, redundant, and gives a false sense of safety. Validate data once at the boundary. Keep logic out of framework wiring so you can test it without the framework.

## Pattern

- At boundaries such as CLI arguments, config files, external APIs, and network protocols, validate, return errors, and handle defensively.
- Inside the system, use typed data and error propagation. Don't re-validate. Trust the types.
- Across the boundary, expose domain concepts, not the boundary's private representation. Keep general-purpose mechanism inside and special-purpose policy at the edge.
- Distinguish input validation from model translation. A valid payload can mean something different in another context, even within one process. Follow [Make model boundaries explicit](../principle-make-model-boundaries-explicit/SKILL.md).

## Applications

Validation and error handling:

- Validate config at parse time, which is the boundary, not inside business logic.
- Parse, don't validate. Construct a valid domain value at the boundary or return an error. Don't return raw input plus a Boolean or proof token that callers must remember to check.
- Don't re-export transport, storage, framework, or wire types through the public surface.
- Don't add redundant nil checks deep in call chains if the boundary already validated.

Code organization:

- Put business logic in pure functions with no framework dependencies.
- Make parse functions pure transforms from raw bytes to typed state.
- Make prompt construction structured state in, string out.
- Make scoring and assessment pure transforms from state to results.

## Checks

- Is data entering a trust boundary or crossing a model boundary? Validate untrusted input and translate different meanings; avoid repeating checks within the same trusted model.
- Can this be a pure function that the shell just calls? If yes, extract it.
