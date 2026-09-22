# Distributed Systems Guidance

Status: **provisional**

This module provides routing and engineering-quality guidance for distributed boundaries.

It is **not** a substitute for full distributed-systems correctness analysis. The mandatory modern DDIA 2nd Edition research is still open.

## Core principle

Do not make distributed behavior look local when network semantics affect correctness.

Remote operations differ from local calls because they can involve:

- partial failure;
- timeout ambiguity;
- retry duplication;
- latency;
- reordering;
- version skew;
- partitions;
- independent deployment;
- stale state.

## Failure model first

Before reviewing structure, identify:

- what can fail independently;
- what the caller observes on timeout;
- whether operations are idempotent;
- whether duplicates are possible;
- ordering requirements;
- consistency requirements;
- retry ownership;
- recovery behavior.

If these are unknown, do not approve generic retry/failover abstractions blindly.

## Retries

A retry is safe only relative to operation semantics.

Review:

- idempotency;
- idempotency keys;
- deduplication;
- retry budget;
- timeout;
- backoff/jitter;
- retryable error classification;
- retry amplification;
- terminal failure.

Exponential backoff does not make a non-idempotent operation safe.

## Timeouts

A timeout means the caller did not receive a result in time.

It does **not** necessarily mean:

- the remote operation did not run;
- the remote operation failed;
- retrying is safe.

Preserve this ambiguity in API and error handling.

## Ordering

Clarify whether the system requires:

- no ordering;
- per-key ordering;
- per-stream ordering;
- causal ordering;
- total ordering.

Do not rely on incidental current ordering unless it is guaranteed.

## Idempotency and deduplication

Choose where duplicate protection belongs:

- client;
- server;
- durable store;
- broker;
- protocol.

Do not duplicate ownership ambiguously across layers.

## Consistency

Use explicit terms.

Do not say "consistent" without specifying the property that matters.

Examples:

- read-your-writes;
- monotonic reads;
- linearizability;
- eventual convergence;
- transaction isolation.

If exact consistency semantics decide correctness, require specialist analysis.

## Version skew

Rolling deploys create temporary mixed-version systems.

Review:

- old/new request compatibility;
- schema compatibility;
- capability negotiation;
- fallback behavior;
- partial rollout;
- rollback.

A system that only works when all nodes upgrade atomically is fragile unless atomic deployment is guaranteed.

## Queues/streams

Review:

- at-most-once / at-least-once / effectively-once semantics;
- duplicate delivery;
- consumer restart;
- poison messages;
- dead-letter handling;
- backpressure;
- lag;
- ordering;
- replay.

Do not claim "exactly once" without identifying the mechanism and scope.

## Centralization vs decentralization

Central coordination can simplify invariants but introduce:

- bottlenecks;
- availability dependence;
- scale ceilings.

Decentralization can improve resilience but adds:

- reconciliation;
- propagation delay;
- conflict handling;
- more complex observability.

Neither is universally better.

## Remote API granularity

Round trips are architectural cost.

Consider:

- batching;
- streaming;
- coarse operations;
- metadata included with object creation/announcement.

Do not mirror local fine-grained object APIs across the network without measuring the effect.

## Observability

Distributed correctness often requires provenance.

Preserve:

- request IDs/correlation IDs;
- retries/attempts;
- version/build info;
- timestamps with known semantics;
- causal or sequence identifiers where needed.

## Verification

Use relevant tests:

- timeout-after-success;
- duplicate delivery;
- retry storms;
- node restart;
- version skew;
- partial rollout;
- partition simulation;
- stale-state behavior;
- idempotency;
- replay.

## Specialist boundary

Require deeper distributed-systems review when deciding:

- consensus;
- quorum rules;
- replication guarantees;
- transactional consistency;
- conflict-resolution semantics;
- ordering proofs;
- exactly-once claims;
- partition behavior.
