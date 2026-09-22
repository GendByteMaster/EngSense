# Persistence Guidance

Status: **provisional**

This module covers engineering-quality concerns around persisted state, schema evolution, transactions, replay, and migration.

It does not replace database-engine-specific correctness review.

## Core principle

Persisted state creates **time-coupling**.

A code change can affect data written:

- by older versions;
- by other services;
- before a deployment;
- during a rolling migration;
- after partial failure.

Persistence refactors must therefore be reviewed as compatibility and lifecycle decisions, not only local code cleanup.

## Invariants

Identify which matter:

- atomicity;
- durability;
- uniqueness;
- ordering;
- idempotency;
- referential integrity;
- version compatibility;
- replay correctness;
- restore behavior;
- transaction boundaries.

Do not move code across persistence boundaries without preserving the relevant invariants.

## Schema evolution

For schema/format changes, define:

- current version;
- target version;
- migration direction;
- compatibility window;
- backfill;
- rollback;
- partial-migration behavior;
- old-reader/new-writer compatibility where relevant.

Do not assume deployment is atomic unless the system guarantees it.

## Persisted formats as APIs

Treat on-disk records, event logs, serialized objects, and snapshots as high-inertia surfaces.

Changing field names/types/order/meaning can be equivalent to breaking a public API.

Use explicit versioning or migration where required.

## Transactions

Keep transaction boundaries aligned with real invariants.

Avoid:

- transactions that are so large they create unnecessary contention;
- fragmented transactions that break atomic domain behavior;
- hidden network calls inside critical transaction sections without intent.

If transaction semantics are database-specific, defer to specialist review.

## Event/replay systems

For event logs or replayable systems, preserve:

- deterministic interpretation where required;
- event identity;
- ordering guarantees;
- versioned event semantics;
- deduplication/idempotency;
- migration/upcasting strategy.

Do not rewrite history casually.

## Caches and persistence

A cache is not authoritative storage unless explicitly designed as such.

Review:

- source of truth;
- invalidation;
- stale reads;
- reconstruction;
- write-through/write-back semantics;
- data loss on eviction/restart.

## Migrations

A safe migration should consider:

- consumer discovery;
- old/new coexistence;
- verification;
- restart after partial progress;
- rollback;
- backsliding prevention;
- cleanup/removal of obsolete schema/code.

Migration tooling is part of reversibility.

## Complexity placement

Removing database features can move complexity into application code.

Examples:

- removing transactions → application compensation logic;
- removing joins → manual consistency/query logic;
- denormalization → update synchronization;
- weak consistency → conflict resolution.

Do not call the result simpler without accounting for displaced complexity.

## Verification

Depending on risk:

- migration tests;
- round-trip serialization tests;
- restart/reopen tests;
- rollback tests;
- transaction failure tests;
- replay tests;
- compatibility tests across versions;
- backup/restore tests.

## Specialist boundary

Escalate when correctness depends on:

- isolation levels;
- write anomalies;
- consensus/replication semantics;
- database-specific durability behavior;
- distributed transactions;
- subtle recovery guarantees.
