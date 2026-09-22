# EngSense Contextual Smells

These are **signals to investigate**, not automatic defects.

A smell becomes a finding only when repository/task evidence shows material impact.

## Abstraction smells

### Interface mirrors one concrete implementation

Investigate when:

- one implementation exists;
- method sets match one-for-one;
- factories always return one type;
- callers gain no smaller/stabler contract.

Possible conclusion:
- collapse abstraction now;
- revisit when a real variation boundary appears.

### Generic helper with many mode flags

Investigate when one abstraction requires:

- booleans;
- enum modes;
- callbacks;
- special-case branches

to keep unrelated workflows together.

Possible issue:
- superficial DRY has hidden conceptual divergence.

### Consumers reach through the abstraction

If callers repeatedly downcast, inspect internals, or require implementation-specific escape hatches, the boundary may not represent a real stable capability.

---

## Modularity smells

### Many modules, little independence

Module count is not evidence of decoupling.

Investigate:

- circular dependencies;
- shared mutable state;
- knowledge of concrete implementation location;
- synchronized deployment/change requirements.

### Long function

Length alone is not a finding.

Investigate whether the function combines independent responsibilities or remains one cohesive algorithm with high locality.

### Tiny pass-through layers

Investigate layers that only forward arguments and errors without adding:

- policy;
- invariants;
- translation;
- lifecycle ownership;
- substitution;
- observability.

---

## Complexity smells

### "Simplification" duplicates responsibility elsewhere

Ask where the removed complexity moved.

Common destinations:

- callers;
- deployment scripts;
- migration;
- operations;
- user workflow.

### Local cleanup creates global migration cost

A small implementation improvement can be expensive when it touches:

- public APIs;
- persisted data;
- protocols;
- plugin contracts.

### Future-proofing without trigger

Investigate architecture justified only by:

- "we might need";
- "it could scale";
- "maybe another provider";
- "possibly plugins later".

Require a real driver or revisit trigger.

---

## API smells

### Unsupported-operation interface

If many implementations expose methods that only throw unsupported errors, capability modeling may be wrong.

### Chatty remote object API

Local-style getters across RPC/IPC can cause multiplicative round trips.

### Undocumented stable behavior changed casually

Investigate consumer dependence before calling it a private implementation detail.

### Public surface grows for convenience

Every added public operation increases future compatibility cost.

---

## Testing smells

### Mock verifies implementation choreography

If harmless internal reordering breaks tests, the test may be coupled to implementation rather than behavior.

### Coverage target drives weak tests

High line execution with weak assertions is not strong confidence.

### Flaky test accepted as normal

Repeated nondeterministic failure erodes suite trust.

### Production abstraction exists only for mocking

Investigate whether testability is revealing a real boundary or whether the test tool is dictating architecture.

---

## Concurrency/distributed smells

### Unbounded queue

Investigate overload/backpressure/resource exhaustion semantics.

### Retry on timeout without idempotency story

Timeout does not prove remote failure.

### Sync-looking wrapper over async/distributed behavior

Investigate hidden ordering, deadlock, cancellation, and failure semantics.

### "Exactly once" without mechanism/scope

Require a concrete explanation of deduplication/transaction boundaries.

---

## Persistence smells

### Destructive migration during rolling deploy

Investigate mixed-version compatibility and rollback.

### Persisted shape treated as private implementation detail

Stored data often outlives the code version that wrote it.

### Cache accidentally becomes source of truth

Investigate restart/eviction/reconstruction semantics.

---

## Performance smells

### Rewrite before profiling

The assumed bottleneck may be wrong.

### Buffering added without overload model

Throughput can improve while memory pressure becomes catastrophic.

### Caching without semantic validity

Side effects/nondeterminism can make reuse incorrect.

---

## Historical smells

### "Ugly therefore obsolete"

Before removing old structure, recover the original constraint.

### "It has always been this way"

Historical consistency is evidence, not proof.

The original constraint may no longer exist.

---

## Review-noise smells

### Preference presented as defect

Examples:

- different but idiomatic control flow;
- naming preference without ambiguity;
- alternate folder layout with no structural impact.

### Finding without named impact

A finding should protect an invariant or improve a relevant quality dimension.

### Severity inflation

Do not make a style/maintainability observation sound like correctness or reliability risk.
