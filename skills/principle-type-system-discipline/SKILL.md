---
name: principle-type-system-discipline
description: "Apply when designing types, reviewing a function signature, or writing code in a statically typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, refuse to lie to the compiler, exhaust variants, and derive types from authoritative schemas."
disable-model-invocation: true
---

# Type system discipline

Use the type checker to reject impossible states, mismatched primitives, and unhandled variants at compile time. A case the types let you ignore becomes a runtime failure the compiler could have stopped. Prefer types that make errors unrepresentable over extra handlers.

This principle applies to any typed language. Language-specific skills such as `typescript-best-practices` cover syntax.

## Patterns

- **Make illegal states unrepresentable.** Model variants as sum types: discriminated unions in TypeScript, enums with payloads in Rust, Swift, or Kotlin, sealed classes in Scala, and algebraic data types in Haskell or OCaml. Don't model state as a bag of optional fields where contradictory combinations compile. `{ completed: boolean; completedAt?: Date }` admits `completed: true; completedAt: undefined`, which is meaningless. Derive the boolean from one source such as `completedAt !== null`, or model `{ kind: 'open' } | { kind: 'done'; at: Date }`. If a bug forces the question "Can this combination happen?", the type is too loose.
- **Build types from the values you want.** Don't carve a looser type down with checks. The invariant that seems to need a refinement type is usually a construction. A non-empty list is a head plus a rest, not a list with a length check. A valid time range is a start plus a duration, not two timestamps you must keep ordered. Choose the shape that cannot build the illegal value, then expose the interface callers need.
- **Brand semantic primitives.** `UserId` and `OrderId` are strings underneath, but they shouldn't be interchangeable. Use newtypes in Rust, opaque types in Swift, value classes in Kotlin, phantom types in Haskell, or branded intersections in TypeScript. Validate once at creation, then trust the type downstream.
- **Treat external data as untyped until you parse it.** RPC payloads, JSON, IPC messages, CLI arguments, config files, environment variables, and database rows all need a parse function at the boundary that turns unstructured input into the typed model. See [Boundary discipline](../principle-boundary-discipline/SKILL.md) for where to put that work.
- **Don't lie to the type system.** Casts, unsafe coercions, and assertion functions that bypass the compiler are runtime crashes waiting to happen. If the compiler can't prove a fact, prove it by validating, narrowing, or refining the model, or accept that the cast is a hazard.
- **Let the compiler exhaust matches.** When you match on a sum type, compilation must fail if a new variant is added without a case. Use the idiom your language provides: a `never`-typed binding in TypeScript, unannotated `match` in Rust, `-Wincomplete-patterns` in Haskell, or sealed-class exhaustiveness in Kotlin.
- **Derive contract types from authoritative schemas.** Generate a protocol's types from its schema instead of hand-rolling the same contract. A schema owns the interchange shape, not every context's internal model. Translate when domain meanings differ.
- **Strengthen a type only where partiality appears.** A runtime assertion, null check, or "this should never happen" throw marks a type that is too weak. Push that check into the type, then stop. The type system's job is to track the cases each use site must handle, not to describe the data as precisely as possible. Prefer total functions. `sum` of an empty list is 0, so it takes a plain list. `head` of an empty list has no answer, so it demands a non-empty list. Extra precision costs reuse and ceremony and buys no safety.

## Checks

- Can you write a comment that explains when this combination of fields is valid? If yes, the type is too loose. Split it into a sum type.
- Do two function arguments share a primitive type but mean different things? Brand them.
- Where did this `any`, `as`, or `assertNotNull` come from? Trace it to the boundary and parse there instead.
- If a new variant is added next month, will the compiler tell the next agent where to add a case? If no, the match isn't exhaustive.
- Is this type duplicating the same contract another file owns? Derive it. If it expresses a different domain meaning, keep that distinction explicit.
- Are you strengthening this type to keep an operation total, or only to be more precise? If nothing would otherwise panic, keep the plain type.
