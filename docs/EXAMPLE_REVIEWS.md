# EngSense Example Reviews

These examples show the expected **shape of engineering judgment**. They are not universal answers.

The important properties are:

- evidence before doctrine;
- explicit trade-offs;
- authority proportional to confidence;
- the smallest useful change;
- verification matched to the risk;
- a revisit trigger when assumptions may change.

## Example 1 — Premature interface

### Scenario

A repository has one payment provider implementation.

The proposed refactor introduces:

- `PaymentProvider` interface;
- `PaymentProviderFactory`;
- one adapter;
- dependency injection wiring.

All callers use the same provider. No external substitution boundary exists. Tests can use the concrete implementation directly.

### Review

**[Medium] The new interface does not protect a demonstrated variation boundary**

**Problem**

The proposed interface/factory layer adds concepts and navigation, but current evidence shows one implementation and no independent substitution requirement.

**Why it matters**

The change increases indirection and maintenance surface without reducing an existing coupling or enforcing a new invariant.

**Context/evidence**

- one production implementation;
- factory always returns the same type;
- no caller selects a provider;
- tests do not require a substitute;
- consumers still depend on provider-specific behavior.

**Trade-off**

Dependency inversion can be valuable when a stable capability boundary or provider variation exists. Here, concrete simplicity dominates because the variation is hypothetical.

**Recommended change**

Keep the concrete implementation. Extract a boundary only if there is another concrete reason, such as a second provider, external platform boundary, or volatile SDK behavior that must be isolated.

**Verification**

Run current behavior tests and inspect callers to confirm no existing substitution requirement has been missed.

**Authority**

Guidance.

**Revisit when**

A second real provider, external provider contract, or independent substitution requirement appears.

---

## Example 2 — Large but cohesive parser

### Scenario

A parser function is 190 lines long.

It:

- implements one grammar production;
- uses shared parser state;
- performs a sequential parse;
- has several branches belonging to the same grammar rule.

A proposed cleanup extracts twelve helpers, most of which are fewer than ten lines and require passing the same parser state through several calls.

### Review

**No material issue from line count alone**

The current function is long, but the evidence does not show multiple independent responsibilities.

Splitting it into many shallow helpers would trade local line count for:

- more navigation;
- repeated state threading;
- additional names that do not introduce new concepts;
- weaker visibility of the sequential algorithm.

Keep the cohesive parsing flow together.

Extract only a helper that represents a genuine semantic sub-operation with its own invariant or reason to change.

**Trade-off**

Small decomposition vs locality/deep cohesive behavior.

**Verification**

Parser regression tests should remain unchanged. If an extraction is attempted, compare whether the resulting control flow is easier to follow rather than measuring success by function length.

**Authority**

Note / Guidance, depending on the strength of the proposed refactor.

**Revisit when**

Persistence, retry policy, I/O, caching, or another independently changing responsibility enters the function.

---

## Example 3 — Stable duplicated invariant

### Scenario

Three modules independently implement the same normalization rule.

Every time the business rule changes, all three files must be updated. Two previous changes updated only two modules and caused inconsistent behavior.

### Review

**[Medium] The duplicated rule is now a stable shared invariant**

**Problem**

The duplication is no longer merely similar-looking code. The same invariant is maintained in three places and has already drifted.

**Why it matters**

The cost is multiplicative: every rule change requires synchronized updates, and missed updates create inconsistent behavior.

**Context/evidence**

- the semantic rule is the same in all three modules;
- changes repeatedly move together;
- historical defects came from incomplete synchronized edits.

**Trade-off**

DRY vs local duplication.

Earlier duplication may have been appropriate while requirements were unstable. Current evidence now favors centralization because the invariant has stabilized.

**Recommended change**

Introduce one narrow shared normalization function/module that owns the rule. Do not build a generic framework beyond the demonstrated invariant.

**Verification**

- preserve all current normalization cases;
- add shared tests for the invariant;
- verify all three call sites use the same behavior.

**Authority**

Strong recommendation.

**Revisit when**

The modules develop genuinely different normalization semantics.

---

## Example 4 — Bounded performance escape hatch

### Scenario

A generic conversion layer supports many source and destination formats.

Profiling under a representative production workload shows one native-to-native conversion consumes a dominant fraction of CPU. A specialized path can bypass intermediate serialization when both endpoints advertise the same native capability.

The generic path remains correct and available as fallback.

### Review

**[Guidance] A bounded fast path is justified by measured evidence**

**Decision**

Add the specialized path behind an explicit capability check while keeping the generic path as the default/fallback.

**Evidence**

- representative profiling identifies the hotspot;
- end-to-end benchmark shows material improvement;
- eligibility can be determined explicitly;
- public semantics can remain equivalent.

**Trade-off**

Strict layering and one-path simplicity vs measured performance and data-movement reduction.

**Why this option**

Rejecting every escape hatch would preserve conceptual uniformity at a measurable runtime cost. Removing the generic abstraction entirely would overgeneralize evidence from one workload.

A contained specialization keeps the exception local.

**Verification**

- benchmark both paths under the same workload;
- verify semantic equivalence for eligible inputs;
- verify fallback when native compatibility is absent;
- keep path selection observable.

**Revisit when**

The fast path becomes the dominant architecture or dual-path maintenance cost exceeds the measured benefit.

---

## Example 5 — Rewrite with weak evidence

### Scenario

A long-lived subsystem is difficult to navigate.

A team proposes a rewrite because:

- the old code does not follow the preferred layering;
- a newer framework is available;
- the replacement architecture appears cleaner.

However:

- regression coverage is incomplete;
- persisted state must survive;
- no migration plan exists;
- no rollback strategy exists;
- recent incidents were not caused by the layering.

### Review

**[High] Rewrite readiness is below the risk level of the subsystem**

**Problem**

The replacement proposal is stronger on target architecture than on behavioral understanding and transition safety.

**Why it matters**

A rewrite can replace visible structural complexity with compatibility, migration, and correctness failures that are harder to detect.

**Context/evidence**

- current behavior is only partially characterized;
- persisted data creates high surface inertia;
- migration/cutover is undefined;
- rollback is not demonstrated;
- architectural cleanliness is the main stated benefit.

**Trade-off**

Architectural correction vs behavioral/migration risk.

**Recommended change**

Do not approve the full replacement yet.

First:

- characterize critical behavior;
- identify the material current cost;
- define persisted-data migration;
- define old/new comparison or other behavioral oracle;
- define rollback/cutover;
- identify removal criteria.

Targeted independently verifiable refactors can continue in parallel if they reduce current cost.

**Verification**

- regression/contract tests for critical workflows;
- representative persisted-data migration test;
- rollback rehearsal;
- old/new behavior comparison where practical.

**Authority**

Strong recommendation.

**Revisit when**

Behavioral understanding, migration tooling, and rollback become strong enough that replacement risk is bounded.

---

## Example 6 — Public API chatty over a high-latency boundary

### Scenario

A mobile client needs four sequential API calls to render one screen.

End-to-end traces show network round trips dominate latency. Server CPU is low. A proposal suggests rewriting one handler in a faster language.

### Review

**[High] The proposed CPU rewrite does not address the measured latency source**

**Problem**

The evidence shows coordination distance dominates, not local handler CPU.

**Context/evidence**

- four sequential remote calls;
- representative RTT is high;
- server handler CPU is a small portion of total time;
- no end-to-end evidence shows a language rewrite materially improves user latency.

**Trade-off**

Local implementation speed vs network round-trip cost and API granularity.

**Recommended change**

Investigate whether the screen's required data can be fetched with fewer dependent round trips while preserving API semantics and compatibility.

Do not rewrite the handler solely from language-level performance assumptions.

**Verification**

Measure end-to-end screen latency under the representative network after any protocol/API change.

**Specialist boundary**

Specific transport tuning should be reviewed with current networking expertise rather than inferred by EngSense.

---

## Example 7 — Provider normalization hides a correctness capability

### Scenario

Two storage providers are normalized behind one generic `write()` operation.

Provider A supports a strong conditional write.

Provider B does not.

Callers rely on the conditional semantics to prevent lost updates, but the common model hides this difference.

### Review

**[High] The normalization erases a capability that affects correctness**

**Problem**

The provider difference is not incidental. It changes the concurrency guarantee callers receive.

**Trade-off**

Uniform API vs semantic truth.

**Recommended change**

Keep normalization for incidental differences, but expose the conditional-write capability explicitly. Prevent callers from assuming the guarantee when the selected provider cannot provide it.

Do not silently emulate semantics unless a correct implementation is actually available.

**Verification**

- capability-aware contract tests;
- concurrent lost-update scenarios;
- tests that unsupported providers cannot enter the stronger path.

**Specialist boundary**

The exact provider consistency guarantees must be verified against provider/database-specific semantics.

---

## What these examples are not

They are not templates that should be copied mechanically.

For a real repository:

- evidence can change the conclusion;
- severity can change;
- the same principle can lose to another principle;
- an omitted specialist invariant can invalidate the entire recommendation.

EngSense should reproduce the **reasoning discipline**, not the wording.
