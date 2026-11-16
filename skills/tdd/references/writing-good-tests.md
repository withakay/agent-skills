# Writing Good Tests

<!-- toc -->
## Contents

- [Overview](#overview)
- [Principle 1: Name the Break](#principle-1-name-the-break)
  - [Gate Function](#gate-function)
- [Principle 2: Exercise the Real Thing](#principle-2-exercise-the-real-thing)
  - [Gate Function](#gate-function-1)
- [Keep Each Test Obvious](#keep-each-test-obvious)
- [Tests Ship With the Implementation](#tests-ship-with-the-implementation)
- [The Mutation Check](#the-mutation-check)
- [Review Questions](#review-questions)
- [Quick Reference](#quick-reference)
- [Warning Signs](#warning-signs)
<!-- tocstop -->

**Load this reference when:** writing or changing tests, adding mocks, or
adding cleanup/helper methods for tests.

## Overview

A test exists to catch a specific break. Two principles govern everything
here:

```
1. Every test names the break it catches
2. Every test exercises the real thing
```

Strict TDD produces both naturally: a test written first and watched
failing against real code has already proven it can fail, and only earns
a mock when the real dependency proves slow or external.

## Principle 1: Name the Break

Before writing the test body, answer: **what production change should
make this test fail — and is that change a bug or a decision?** A test
earns its place by catching a wrong branch, missing side effect, wrong
argument, boundary case, or broken contract.

**Derive expectations independently.** Use literals and hand-checked
fixtures; table-driven tests with literal `want` values are the preferred
shape. An expectation computed by the code under test — or its helpers —
passes no matter what that code does:

```typescript
// ❌ Mirror assertion: the same builder computes both sides — always true
const expected = buildSearchQuery({ tag: 'urgent' });
expect(buildSearchQuery({ tag: 'urgent' })).toBe(expected);

// ✅ Hand-derived literal
expect(buildSearchQuery({ tag: 'urgent' })).toBe('tag:"urgent"');
```

**Choose values that distinguish plausible mistakes.** For a rule that
changes at a threshold, test the boundary and its neighbours
(`49`, `50`, `51`), not three ordinary values on the same side. For a
query, arrange matching and deliberately non-matching records so the
missing filter shows. Use distinct, non-default values in mapping tests
so an omitted or swapped field cannot pass by coincidence.

**No vacuous passes.** `every order in result belongs to tenant A` is
true of an empty result. Assert that the expected result exists:
`result contains exactly A1`, given `A1` (tenant A, pending),
`A2` (tenant A, completed), and `B1` (tenant B, pending). That one
assertion distinguishes returning nothing, dropping the tenant filter,
dropping the status filter, and returning too much.

**Properties need anchors.** "Transfer preserves the combined balance"
also passes for a transfer that does nothing; "serialise then deserialise
returns the original" passes when both sides agree on the wrong wire
format. Pair a property with a concrete check that the effect happened
or a known-format example.

**No change detectors.** If only intentional decisions can fail a test —
a constant's value, exact message wording, private structure — it fires
on redesign and sleeps through bugs. Test the behavior that depends on
the decision: not `expect(MAX_RETRIES).toBe(5)` but "a failing call is
retried 5 times and the 6th attempt never happens."

**Behavior, not text.** Asserting that a script, skill, or config
contains an exact line proves only that the source is the source. Run
scripts against controlled inputs and assert outputs, side effects, or
exit codes. Documents that instruct agents are tested by the consuming
agent behavior through `skill-creator/references/behavior-testing.md`;
prose for humans needs no behavior test.

**Your code, not the framework.** Test the contract your code makes at
its boundaries — the route you register, the query you emit, the payload
you produce. Upstream mechanics are their maintainers' tests to write
(the classic: asserting your router invokes a registered handler — that
is the framework's test, not yours). When upstream behavior genuinely
surprised you, write one narrow characterization test naming the
assumption. The same boundary applies inside your code: constructors,
getters, constants, and trivial forwarding earn tests only when they
validate, normalize, default, derive, enforce, or cause side effects —
otherwise assert the first consumer-visible result that depends on them.

### Gate Function

```
BEFORE writing the test body:
  Name the production change that would make this test fail.

  Cannot name one            → redesign around an observable behavior
  "The source text changed"  → run the artifact and assert its effects
  Only intentional decisions → change detector; test the behavior
                               that depends on the decision

  Confirm the expected value is derived without the code under test.
  IF it reuses the code's logic or helpers:
    Replace it with a literal or hand-checked fixture
```

## Principle 2: Exercise the Real Thing

**The mock earns no assertions.** A mock assertion passes when the mock
is present and fails when it is absent — it says nothing about the
component. Assert the real component's behavior; if the mock is what you
are checking, unmock it or delete the assertion.

```typescript
// ✅ Real behavior
expect(screen.getByRole('navigation')).toBeInTheDocument();

// ❌ Mock existence
expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
```

Ask: "Are we testing the behavior of a mock?"

**Mock at the right level.** Learn every side effect of the real method
before replacing it; mock the slow or external operation and keep what
the test depends on real. When unsure, run the test against the real
implementation first and observe what actually needs to happen.

```typescript
// ❌ The mock swallows the config write that duplicate detection reads
vi.mock('ToolCatalog', () => ({
  discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
}));

// ✅ Mock only the slow server startup; the config write stays real
vi.mock('MCPServerManager');
```

**Make doubles specific.** When arguments, call counts, or ordering are
part of the contract, assert them — a fake that accepts anything verifies
nothing. Give each branch (success, error, malformed) its own fixture or
spy, so the wrong branch cannot satisfy the expectation.

**Mirror real data completely.** Mock the complete structure as it exists
in reality — all documented fields — not just the ones your test reads.
Partial mocks fail silently when downstream code reads an omitted field:
the test passes while integration breaks.

**Production classes carry production methods only.** Cleanup that only
tests need lives in test utilities, never as a `destroy()` on the
production class. Ask: is this method called only from tests? Does this
class own this resource's lifecycle? Wrong answers → test utility.

**Prefer real components over complex mocks.** When mock setup outgrows
the test logic, mocks miss methods the real components have, or tests
break when the mock changes, switch to an integration test with real
components. Ask: "Do we need to be using a mock here?"

### Gate Function

```
BEFORE adding a mock or test helper:
  List the real method's side effects; keep the ones the test
  depends on real — mock the slow/external level below them.

  Mock responses mirror the complete real structure.

  A method only tests call lives in test utilities, not production.

  About to assert on the mock itself?
    Unmock it or delete the assertion.
```

## Keep Each Test Obvious

**One behaviour, not one assertion.** A test tells one coherent story,
which may need several assertions: both sides of a transfer, a returned
result and its persisted effect, a rejection and the absence of a write.
Do not split those mechanically. Do not merge unrelated scenarios into
one test either.

**Share mechanics; keep meaning visible.** Some duplication is better
than hiding what a test means (DAMP over DRY in tests). Put irrelevant
construction behind small factories and keep the scenario-defining values
and expectations in the test body: `customer(overdueDays = 31)` says more
than `createCustomer(ScenarioType.ThirdCase)`. Return fresh mutable
objects, not a shared "standard customer". Avoid deep base-class
hierarchies, boolean-heavy helpers, and universal scenario runners.

**Parameterise only same-shaped cases.** Use parameterised tests when
cases share the arrangement, operation, and assertion structure. Name
each case. If the body needs a conditional to handle a row, the rows are
different behaviours and belong in separate tests.

**Test infrastructure is code.** A database allocator or a custom
comparison helper may deserve tests of its own. "Tests should be simple"
does not exempt complex fixture code.

## Tests Ship With the Implementation

The TDD cycle — failing test, minimal implementation, refactor — is what
"complete" means. Ship the tests the behavior needs and only those:
trivial code and human prose earn none, and a test written to satisfy
process costs maintenance forever.

## The Mutation Check

Before finishing, mentally mutate the production code; at least one test
should fail for each realistic mutation:

- Wrong constant or argument
- Wrong branch handler
- Missing state change or side effect
- Empty or default return
- Missing validation for zero, empty, nil, unauthorized, or malformed input

A mutation nothing catches marks the behavior as unprotected — or the
test as tautological.

Run a mutation tool (Stryker or the repository's equivalent) selectively
on important or recently changed logic, or when a test's value is in
doubt. Do not treat the mutation score as a percentage to maximise: some
mutants are behaviourally equivalent and cannot be killed, and killing
others would add tests that make the suite worse.

## Review Questions

Ask these when reviewing an important test or deciding whether to keep
one. Do not attach them as boilerplate to every test.

1. What important guarantee does this test protect?
2. What plausible defect would make it fail?
3. Is the expectation independent of the implementation?
4. Does it survive a harmless internal refactor?
5. Does it run on its own, with controlled state?
6. Is its added protection or diagnostic value worth its cost?

Two tests that execute the same lines are not necessarily redundant; they
may check different boundaries or consequences. Two differently named
tests may supply identical evidence. When removing a weak test, decide
whether its guarantee is already protected, needs a better replacement,
or was never a requirement.

## Quick Reference

| When you... | Do |
|-------------|-----|
| Write any test | Name the break it catches — a bug, not a decision |
| Build an expected value | Derive it by hand; never with the code under test |
| Pick input values | Boundary and neighbours; matching and non-matching; non-default |
| Assert on a collection | Require the expected items to exist, not just that none are wrong |
| Test a script or document | Run it / pressure-test its consumer; never grep its text |
| Reach for a dependency test | Test your boundary contract, not their documented mechanics |
| Want to assert on a mocked element | Test the real component, or unmock it |
| Are about to mock a method | Learn its side effects; mock the slow/external level |
| Build a mock response | Mirror the real structure completely |
| Need cleanup only tests use | Put it in test utilities |
| Watch mock setup balloon | Switch to an integration test with real components |
| Finish a test file | Run the mutation check |

## Warning Signs

- Setup and assertion share the same object, guaranteeing equality
- The assertion still passes when the result is empty
- Every input sits on the same side of the boundary the rule is about
- The test can fail only through a panic, crash, or missing selector
- The test fails on every intentional change, never on accidental breakage
- Expected values are hidden behind loops, builders, or helpers
- The test greps source text, or asserts a removed symbol stays removed
- The test would still matter if only the framework remained
- The test exists for coverage, checking no side effect or outcome
- An assertion checks a `*-mock` test ID, or fails if you remove the mock
- A method is called only from test files
- Mock setup is more than half the test, or you can't explain why the mock is needed
- Mocking "just to be safe"
