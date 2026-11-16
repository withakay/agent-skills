---
name: tdd
description: Use when changing observable software behavior and an executable test harness can provide useful red-green evidence.
---

# Test-Driven Development

<!-- toc -->
## Contents

- [Route By Risk](#route-by-risk)
- [Choose The Boundary](#choose-the-boundary)
- [Cycle](#cycle)
  - [RED](#red)
  - [GREEN](#green)
  - [REFACTOR](#refactor)
- [Test Quality](#test-quality)
  - [No tautologies](#no-tautologies)
  - [Lean suites](#lean-suites)
  - [Integration over abstraction](#integration-over-abstraction)
  - [Containers and expensive fixtures](#containers-and-expensive-fixtures)
- [.NET Example](#net-example)
- [Evidence](#evidence)
<!-- tocstop -->

Specify one observable behavior, prove the test can fail for the intended reason, implement the minimum change, and keep the suite green.

Test important guarantees at the smallest trustworthy boundary, at the lowest sustainable feedback and maintenance cost. Test count and line coverage are not the goal: coverage exposes gaps, but it does not show that an assertion means anything or that a test is worth its upkeep.

## Route By Risk

Use normal red-green-refactor for features, bug fixes, behavior changes, and refactors that can regress behavior.

Use an explicit exception when test-first has lower value than direct proof. Record the reason and replacement verification. Common cases:

- Generated code: test or validate the generator and generated contract; do not hand-edit output.
- Configuration, manifests, and policy files: use schema validation, parser/load tests, plan/dry-run output, or a focused integration check. When configuration is the behavior (an authentication requirement, a tenant filter, a rounding rule), test its runtime effect, not the declared value: an unauthenticated request is rejected, not `requireAuthentication == true`.
- Documentation or static data: validate links, structure, examples, or the consuming tool.
- Inherited implementation written before the test: do not delete working code. Add a characterization or regression test, demonstrate that it detects the defect when practical, then change the code.
- Throwaway probes: label them disposable and do not treat them as production evidence.
- Mechanical changes already covered by a deterministic compiler, analyzer, or existing test: use that check when adding a new test would only duplicate it.

Do not use an exception for security boundaries, data-loss risks, public behavior, concurrency, or a reproduced bug merely because testing is inconvenient. If the user requests an exception, state the risk and run the strongest proportionate replacement check.

## Choose The Boundary

A unit is a coherent capability exercised through a meaningful interface: a function, parser, policy, state machine, or a few collaborating objects. It does not map to one file or class, and "public" means the capability's interface, not every method with a `public` modifier. Pick a boundary that lets the internal decomposition change without rewriting the tests: test that cancelling an eligible order releases its reservation, not that the handler calls three helpers.

Pick the smallest scope that still contains the failure mechanism:

- A calculation: the function.
- Query translation: the real query provider and database.
- HTTP authorization: through the middleware where the protection lives, not the handler alone.

Judge scope (how much behavior the test covers) separately from cost (which resources it uses). A fast database test is still a small test.

## Cycle

### RED

Write the smallest test at a public or stable behavior seam. Name the behavior and the production change that would make the test fail.

Run only the focused test first. Confirm:

- It fails, rather than crashing during setup.
- The failure message matches the missing or incorrect behavior.
- It does not fail because of a typo, stale fixture, or unrelated environment problem.

A test that passes immediately may describe existing behavior. Change it only if it does not exercise the intended gap.

### GREEN

Write the smallest production change that satisfies the behavior. Do not add speculative options or unrelated refactors.

Run the focused test and confirm a pass. Then run affected neighboring tests.

### REFACTOR

Improve names, duplication, and structure while tests remain green. Do not add behavior during refactoring.

Repeat for the next independent behavior.

## Test Quality

- Assert externally observable results or stable contracts, not mock call choreography. Assert an interaction only when the interaction is the guarantee: a notification must be sent, an expensive call must not repeat, a forbidden side effect must not occur.
- Use real collaborators when fast and deterministic; fake only boundaries that are slow, unsafe, or nondeterministic.
- Choose inputs that distinguish plausible mistakes: the boundary and its neighbours, matching and deliberately non-matching records, non-default values in mappings so a swapped or omitted field shows.
- One behavior per test, not one assertion per test. A transfer test checks both balances; a rejection test checks the error and the absence of a write. Do not split a coherent story to satisfy a rule, and do not merge unrelated scenarios into one test.
- Keep each test focused enough that its failure identifies the broken contract.
- Cover errors and edge cases in proportion to impact and likelihood. Do not manufacture impossible inputs for defensive branches an upstream guarantee already excludes; do validate untrusted external input.
- Put test helpers in test code, not production APIs.

### No tautologies

A tautological test cannot fail while the code is wrong: it asserts the test's own setup, re-implements the production logic and compares the two, pins mock choreography that merely restates the implementation, or passes vacuously (`every result belongs to tenant A` holds for an empty result). Derive the expectation from the requirement, not from the code: `shippingCost(49) == 5` and `shippingCost(50) == 0`, not `total >= threshold ? 0 : cost`. Assert the observable contract, and prove the test detects a break by seeing it red (the RED phase) or by mutating the production code once. A test that survives its contract being broken is deleted or rewritten, never kept for coverage numbers.

Review an important test with two questions: which plausible defect must make it fail, and which harmless implementation change must leave it passing. A test needs both answers.

### Lean suites

Tests are code to maintain; every one must earn its place, per the **less-is-more** principle skill. One test per behavior, not per code path permutation. Do not duplicate coverage a compiler, type system, or existing test already provides. Judge a test by its marginal fault detection: what does it catch that the existing tests do not? Prefer deleting a redundant test over keeping it green; repair a weak security or regression test before deleting it. Use the **test-simplifier** skill to prune a suite after the work.

### Integration over abstraction

Prefer an integration test through the real seam over introducing an interface whose only consumer is a mock. Layers of test doubles verify choreography, not behavior, and they silently diverge from real persistence, serialization, and transaction semantics. Mock only boundaries that are genuinely slow, unsafe, or nondeterministic after containerization has been considered.

### Containers and expensive fixtures

For databases, brokers, and other backing services, use real instances in containers (Testcontainers or the repository's equivalent) instead of in-memory fakes; dialects, constraints, and transaction behavior are exactly what fakes get wrong.

Separate fixture lifetime from state lifetime. The server lives for the session; the mutable state a test sees lives for one test. Sharing a resource does not mean sharing its unreset state.

- Server or container, migrated template, immutable reference data: once per session (for example an xUnit collection fixture), never per test.
- Working database: per test, per test group, or per exclusively owned parallel worker.
- Connection, unit of work, scenario data: per test.

Default design: warm servers, a cloned database per concurrently running group, a deterministic reset between tests inside a group. Parallelise across databases, not inside one. Restarting the container is the last resort. Keep the one-command wiring (`make test` or equivalent) working locally and in CI, per the feedback-loop expectations in **verification-before-completion**.

Read [references/test-isolation.md](references/test-isolation.md) before designing database or host fixtures; it covers the isolation strategies, their limits (rollback is not a reset, caches and workers outlive a truncate), and the reset-safety rules.

Read [references/writing-good-tests.md](references/writing-good-tests.md) when adding or changing tests; its mutation check is the standing anti-tautology gate.

## .NET Example

```csharp
[Fact]
public async Task Rejects_empty_email()
{
    var result = await handler.Handle(new RegisterUser(""), CancellationToken.None);

    result.Error.Code.Should().Be("email_required");
}
```

Focused RED/GREEN command:

```bash
dotnet test tests/Users.Tests/Users.Tests.csproj --filter FullyQualifiedName~Rejects_empty_email
```

Use xUnit or the repository's existing framework. For database behavior, prefer the project's integration-test pattern, such as Testcontainers, over mocks that bypass persistence semantics.

## Evidence

Record:

- RED command, relevant failing output, and why the failure was expected.
- GREEN command, exit status, and relevant passing output.
- Broader affected-test command and result.
- Any exception, its risk rationale, and replacement proof.

Fresh red-green evidence is required only for behavior changed since that evidence. Re-run after any relevant implementation or test change.
