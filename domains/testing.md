# Testing Guidance

Status: **provisional**

This module is grounded primarily in the completed *Software Engineering at Google* research plus supporting AOSA case studies.

## Core principle

Testing is risk allocation, not ritual.

Do not ask:

> Which test type is best?

Ask:

> Which failure mode must be detected, what fidelity is required, and what is the cheapest trustworthy verification that provides that confidence?

## Test-quality dimensions

Evaluate:

```text
speed
determinism
hermeticity
fidelity
scope
diagnosticity
maintainability
trust
risk coverage
```

Do not collapse these into one score.

## Unit/narrow tests

Prefer smaller tests when they can detect the target failure reliably.

Good narrow tests are usually:

- fast;
- deterministic;
- focused;
- easy to diagnose;
- behavior-oriented.

Do not structure tests around method count.

Prefer behavior over implementation structure.

## Refactor resilience

Ask:

- Would a semantics-preserving refactor break this test?
- Does the test assert user/domain behavior or internal call order?
- Is setup hiding essential scenario information?

Brittle tests create change cost without adding confidence.

## DAMP vs DRY

In tests, local readability can outweigh deduplication.

Do not extract every repeated setup line if the helper makes each scenario harder to understand.

Abstract test helpers when they preserve clarity and remove genuinely repetitive mechanics.

## Real dependencies, fakes, stubs, mocks

Default preference:

1. real implementation when cheap, deterministic, and practical;
2. maintained high-fidelity fake when real use is too costly;
3. targeted stubbing for specific outputs/error paths;
4. interaction testing only when interaction itself is the behavior.

Do not add production abstraction solely to satisfy a mocking framework.

## Larger tests

Use larger tests when the failure mode requires higher fidelity, such as:

- real database behavior;
- service contracts;
- deployment/configuration;
- browser/device behavior;
- load/performance;
- distributed/emergent behavior;
- migrations;
- production-like routing;
- rollback/recovery.

Do not replace the only meaningful system-level coverage with narrower tests merely to make the suite faster.

## Suite portfolio

A healthy suite normally mixes scopes.

Do not enforce one universal test pyramid ratio.

Choose placement by:

- failure risk;
- cost;
- speed;
- determinism;
- diagnosability;
- workflow latency.

## Coverage

Code coverage is a proxy.

Useful questions:

- Which important behaviors remain untested?
- Are branches executed but not meaningfully asserted?
- Is a coverage target distorting test design?

Do not equate high coverage with high confidence.

## Flakiness

Treat flaky tests as reliability debt.

A test that developers do not trust loses most of its value.

Investigate:

- shared state;
- timing;
- nondeterminism;
- external dependencies;
- ordering;
- environment leakage.

## Test infrastructure

Shared test helpers/frameworks with many consumers should be treated as product-like infrastructure.

They need:

- stable behavior;
- tests;
- compatibility awareness;
- maintainable APIs.

## Verification selection

Examples:

- pure parser behavior → narrow regression tests;
- external provider contract → contract/integration tests;
- schema migration → migration + rollback tests;
- retry/idempotency → failure-path integration tests;
- load collapse → performance/load test;
- public compatibility → downstream/consumer tests.

## Anti-rules

Do not say:

- more tests are always better;
- unit tests are always best;
- E2E is always the most valuable;
- mocks are always necessary;
- 100% coverage proves correctness.

## Revisit triggers

Revisit test strategy when:

- failure modes change;
- system boundaries change;
- runtime/deployment topology changes;
- flakiness reduces trust;
- CI latency becomes unacceptable;
- a critical bug class escapes existing tests.
