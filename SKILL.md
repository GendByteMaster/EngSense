---
name: engsense
description: Context-aware software engineering judgment for code review, refactoring, architecture, API design, maintainability, testability, and engineering trade-offs. Use when a task requires deciding between competing software-design principles or evaluating whether a structural change is justified. Do not use for purely mechanical formatting, trivial renames, or as a replacement for specialist security, performance, database, distributed-systems, concurrency, or UI review.
---

# EngSense

EngSense is an engineering-judgment router, not a style checklist.

Its goal is to choose context-appropriate trade-offs while preserving behavior, compatibility, and specialist invariants.

## Core question

Do not ask:

> Which software-engineering rule should I apply?

Ask:

> Given this language, architecture, invariants, evidence, risks, lifecycle, and change scope, which option gives the best total engineering trade-off?

Do not collapse quality into one numeric score.

## Activate when

Use EngSense for non-trivial decisions involving:

- code structure or maintainability;
- refactoring;
- abstraction boundaries;
- API/protocol shape or compatibility;
- coupling, cohesion, locality, discoverability, or modularity;
- duplication versus abstraction;
- interface/trait extraction;
- testability and test-strategy trade-offs;
- migration/deprecation/change cost;
- architecture quality;
- over-engineering or under-engineering;
- conflicts between reasonable engineering principles.

Do not escalate formatting, syntax, simple renames, obvious lint fixes, or other deterministic mechanical work into architecture review.

## Always preserve

Before recommending structural change, identify relevant invariants:

- externally observable behavior;
- public/protocol/persisted compatibility;
- correctness and failure semantics;
- security boundaries;
- concurrency/ordering/atomicity;
- persistence/migration/replay;
- distributed retry/idempotency/consistency semantics;
- user-visible workflows.

If correctness depends on specialist semantics, use the matching EngSense domain guidance for routing and require deeper specialist review rather than guessing.

## Loading order

Start with the smallest useful set:

1. `decision-framework.md` for non-trivial decisions.
2. `review-workflow.md` for code/change review.
3. A language module when language idioms materially affect the choice.
4. A domain module when the change crosses that boundary.
5. One or more principle lenses only when their question matters.
6. `references/conflicts.md` when valid principles pull in different directions.

Do not load every module for every task.

### Language modules

- `languages/general.md`
- `languages/rust.md`
- `languages/typescript.md`
- `languages/python.md`

### Domain modules

- `domains/api-design.md`
- `domains/testing.md`
- `domains/concurrency.md`
- `domains/persistence.md`
- `domains/distributed-systems.md`

### Research-grounded principle lenses

- `principles/sustainable-engineering.md`
- `principles/empirical-architecture.md`
- `principles/complexity-placement.md`
- `principles/evolution-and-compatibility.md`
- `principles/evidence-driven-abstraction.md`
- `principles/performance-engineering.md`

### References

- `references/conflicts.md`
- `references/smells.md`
- `references/decision-examples.md`
- `references/source-status.md`

Source-specific Clean Code, Ousterhout, Fowler, DDD, DDIA, Release It!, Code Complete, Legacy Code, and related lenses remain blocked until their required full-book research is complete.

## Evidence rule

Prefer repository/task evidence over doctrine.

Useful evidence includes:

- tests and executable behavior;
- actual callers/providers;
- measured benchmark/profile data;
- production/incident evidence;
- explicit contracts;
- repository history and dependency structure;
- migration history;
- documented product requirements;
- qualitative user/contributor evidence.

Label estimates and assumptions.

Do not justify a non-trivial recommendation solely with "best practice", a pattern name, an author's authority, style preference, or hypothetical future reuse.

## Review finding gate

Emit a finding only when it is:

- materially relevant;
- concrete and understandable;
- actionable;
- supported by evidence;
- tied to an invariant or named quality dimension;
- assigned authority/severity appropriate to confidence;
- not better handled by a deterministic tool;
- not merely a preference.

Suppress low-value preference noise.

## Guidance authority

Use the weakest level that matches the evidence:

- **Invariant / hard gate** — correctness, safety, compatibility, or explicit project constraint with very high confidence.
- **Rule** — strongly scoped project/platform requirement.
- **Strong recommendation** — high-confidence material engineering risk.
- **Guidance** — contextual preference with real trade-offs.
- **Heuristic** — useful but defeasible default.
- **Note** — non-blocking observation.

## Decision output

For a non-trivial decision, use a compact record when useful:

```text
Context:
Goal:
Invariants:
Evidence:
Alternatives:
Trade-offs:
Decision:
Assumptions:
Verification:
Revisit when:
```

Do not create ceremony for trivial changes.

## Specialist routing

Use or consult:

- persistence concerns → `domains/persistence.md`;
- distributed semantics → `domains/distributed-systems.md`;
- concurrency semantics → `domains/concurrency.md`;
- API/protocol compatibility → `domains/api-design.md`;
- test fidelity/strategy → `domains/testing.md`;
- performance trade-off/evidence quality → `principles/performance-engineering.md`.

Require deeper specialist review when correctness depends on:

- cryptography/authentication/authorization;
- low-level or unmeasured performance claims after the performance lens identifies a material concern;
- database-engine isolation/durability behavior;
- consensus/quorum/replication guarantees;
- memory ordering/lock-free synchronization;
- legal/compliance requirements;
- specialized UI/UX constraints.

## Research integrity

EngSense is research-informed, but no source is an authority.

Current source-specific coverage is intentionally incomplete. Do not attribute a rule to a book or author unless the repository research note supports it.

Preserve unresolved disagreement instead of inventing consensus.
