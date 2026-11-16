# Test Isolation For Expensive Fixtures

<!-- toc -->
## Contents

- [Lifetimes](#lifetimes)
- [Isolation strategies](#isolation-strategies)
- [Default design](#default-design)
- [Traps](#traps)
- [Feedback loop](#feedback-loop)
- [Sources](#sources)
<!-- tocstop -->

**Load this reference when:** designing database, broker, or application-host
fixtures for integration tests, choosing a reset strategy, or diagnosing
cross-test contamination or flaky integration runs.

## Lifetimes

Give each resource the longest lifetime that keeps test-visible state
controlled. Use the fixture scopes your runner provides (session, module,
class, function, or the xUnit collection fixture equivalent).

| Resource | Default lifetime |
|----------|------------------|
| Database server or container | Session, or a bounded pool for the session |
| Migrated template and immutable reference data | Session, tied to a schema or configuration version |
| Working database | Test, test group, or exclusively owned worker |
| Application host | As long as its configuration and mutable state stay isolated |
| Connection, unit of work, scenario data | Test |

## Isolation strategies

These are trade-offs, not a ranking.

| Strategy | Where it fits | Main limitation |
|----------|---------------|-----------------|
| Server per test | Server configuration, restart, crash, or infrastructure tests | Repeated startup, high resource use |
| Cloned database per test | Tests that need independent commits and strong data isolation | Clone/drop cost, connection lifecycle |
| Database per group, reset between tests | Default for application integration tests | Tests in the group run serially |
| Database per worker, reset between tests | Bounded parallel suite with stable resource use | Every lease must start from a verified clean baseline |
| Transaction per test, rolled back | Tests whose relevant writes join that transaction | Does not exercise real commit behaviour |
| Shared database, unique tenant or namespace IDs | Workloads whose reads, writes, and background work are scoped | Unique IDs do not isolate global queries or operations |

## Default design

1. Start a small, bounded server pool once. Wait for readiness. Assign
   explicit ownership of cleanup.
2. Build a template on each server with the real migrations and only the
   baseline reference data.
3. Allocate a clone to each concurrently running group. Bind its host and
   connection configuration to that database.
4. Run tests serially inside a database and restore the baseline between
   them. Parallelise across independently owned databases.
5. Dispose or recycle safely: stop related work, close resources, reset or
   recreate, and only then return the database to the pool.

Pre-create a pool for the expected concurrency; do not create a database for
every discovered test. Measure clone-per-group against reset-per-lease on the
real schema before committing to one. For PostgreSQL, clone with
`CREATE DATABASE test_orders_01 TEMPLATE test_template;`. The template must
have no connected sessions during the copy, `CREATE DATABASE` cannot run inside
a transaction block, and database-level settings and grants are not all
inherited from the template.

## Traps

**Rollback is not a universal reset.** A test-owned transaction covers only
operations that join it. Independent application connections, background
workers, and external side effects do not. PostgreSQL sequences advance even
when the calling transaction rolls back. Use committed-state isolation when the
behaviour under test includes commit visibility, transaction boundaries, or
concurrency.

**Verify persistence, not an in-memory echo.** Read back through a fresh
context or connection so a change tracker or identity map cannot satisfy the
assertion with the object the test just wrote.

**Reset the whole relevant environment.** Truncating tables is insufficient
when a host caches entities, a worker is still processing, or a queue holds
messages from the previous test. Do not return a database or environment to
the pool until its previous owner can no longer mutate it. When cleanup is
uncertain, discard the resource instead of handing contamination to the next
test.

**Register cleanup as you acquire.** Pair each successful acquisition with its
cleanup immediately. One teardown block reached only after every setup step
succeeds leaks resources on partial failure.

**A cloned current schema does not prove upgrades work.** Keep dedicated
migration tests for the supported upgrade paths with representative old data.
Ordinary tests consume the migrated template; upgrade tests exercise the
transition.

**Separate databases share the cluster.** PostgreSQL roles and other
cluster-level resources are shared across databases. Tests that mutate shared
infrastructure need coordination or a stronger boundary.

**Reuse across runs is a separate decision.** Sharing a container inside one
run is not the same as keeping it between developer runs. Cross-run reuse
needs schema and configuration invalidation plus a clean-state check;
Testcontainers' reuse feature is experimental and not for CI.

**Guard destructive resets.** Use test-only credentials, identifiable
disposable database names, and refuse to clean an unexpected target.

## Feedback loop

Measure the whole loop: provisioning, schema preparation, fixture setup,
execution, cleanup, diagnosis, and reruns. Tuning assertions while rebuilding
the host per test misses the larger cost.

- One command bootstraps the dependencies.
- A single test runs without a predecessor.
- Worker counts fit an ordinary development machine.
- Failures carry enough evidence to reproduce.
- Use controllable clocks for time-dependent logic and explicit completion
  signals for asynchronous work. Bound any polling and report the last
  observed state. Do not use fixed sleeps as the normal synchronisation.
- Do not make blanket retries the definition of success. Record first-attempt
  failures and fix recurring causes.
- Provide a fast focused command, a complete required pre-merge suite, and
  separate expensive stress or fuzz runs. Splitting execution must not remove
  guarantees from the merge gate.

## Sources

- Testcontainers, manual container lifecycle control and reusable containers.
- pytest, fixture scopes and flaky tests.
- Microsoft Learn, EF Core testing strategy and testing against the production database system.
- PostgreSQL, `CREATE DATABASE`, sequence functions, database overview.
- Martin Fowler, *Eradicating Non-Determinism in Tests*.
