# Concurrency Guidance

Status: **provisional**

This module covers engineering-quality review around concurrency. It does **not** replace specialist reasoning about memory models, lock-free algorithms, atomics, or subtle synchronization correctness.

## Core principle

Concurrency semantics are invariants, not style.

A refactor that looks simpler can still be wrong if it changes:

- ownership;
- ordering;
- atomicity;
- cancellation;
- shutdown;
- backpressure;
- visibility;
- restart behavior.

## First questions

Identify:

- concurrency model: threads, async tasks, actors/processes, event loop, work queue;
- ownership of mutable state;
- synchronization primitives;
- blocking operations;
- cancellation semantics;
- shutdown/lifecycle behavior;
- failure propagation;
- queue/channel bounds.

If these are unclear, do not approve structural simplification based only on readability.

## Ownership

Prefer architectures where ownership is explicit.

Ask:

- Who can mutate this state?
- Who is responsible for cleanup?
- Who owns the task/process lifecycle?
- What happens when the owner fails or is cancelled?

Ambiguous ownership is often more dangerous than verbose synchronization.

## Shared mutable state

Reduce shared mutable state when that simplifies reasoning.

But do not copy or serialize everything blindly if it creates unacceptable allocation/latency cost.

The relevant trade-off is:

```text
reasoning simplicity
vs
copying/coordination/runtime cost
```

## Queues and channels

Any queue introduces resource semantics.

Review:

- bounded vs unbounded;
- producer/consumer mismatch;
- backpressure;
- memory growth;
- drop policy;
- fairness;
- shutdown behavior.

An unbounded queue can turn downstream slowdown into memory exhaustion.

## Async

Async improves concurrency for appropriate I/O-bound workloads.

It can also introduce:

- hidden task ownership;
- cancellation leaks;
- orphan tasks;
- stale results;
- unbounded fan-out;
- confusing error propagation.

Do not introduce async solely because the language/framework supports it.

## Locks

Do not recommend lock changes without understanding:

- lock ordering;
- critical sections;
- reentrancy;
- contention;
- blocking under lock;
- upgrade/downgrade semantics.

If correctness depends on subtle ordering or atomics, require specialist review.

## Actors/processes

Actor/process isolation can improve failure containment and ownership clarity.

"Let it crash" is valid only when:

- failure boundaries are explicit;
- supervisors/restart policy exist;
- state can recover safely;
- retries/restarts do not duplicate unsafe side effects.

Crashing without recovery architecture is not resilience.

## Concurrency abstractions

A wrapper is useful when it centralizes a real invariant such as:

- single-flight execution;
- serialization;
- bounded concurrency;
- cancellation propagation;
- ownership.

A wrapper that merely renames a lock/channel does not necessarily improve design.

## Verification

Choose tests that match the risk:

- deterministic unit tests for pure state transitions;
- stress tests;
- cancellation tests;
- shutdown/restart tests;
- bounded-queue/backpressure tests;
- race/concurrency tools where available;
- integration tests for ordering semantics.

## Specialist boundary

Escalate when the decision depends on:

- memory ordering;
- atomics;
- lock-free algorithms;
- cross-thread unsafety;
- happens-before proofs;
- runtime scheduler guarantees.

EngSense should preserve these semantics but not guess them.
