# EngSense Review Workflow

Status: **implemented core review workflow — source-specific lenses remain gated by research status**

Use this workflow for focused code review, refactoring review, and architecture-quality review.

---

## Review modes

### Focused review

Use for:

- a function;
- module;
- PR/change;
- one requested engineering concern.

Stay inside the requested scope unless a directly connected issue materially affects correctness or the requested decision.

### Refactoring review

Use when the question is whether structure should change.

Determine:

- whether there is a real problem;
- whether the proposed refactor addresses it;
- the smallest safe transformation;
- whether tests/verification are sufficient.

Do not recommend a rewrite merely because the current code is aesthetically imperfect.

### Architecture-quality review

Use for:

- subsystem boundaries;
- public APIs;
- platform/service decomposition;
- dependency direction;
- large migrations;
- cross-process/distributed boundaries;
- major extensibility models.

Do not automatically escalate small code changes into this mode.

---

## Review order

Review in this order:

1. correctness/invariant risk;
2. compatibility/migration risk;
3. failure/reliability risk;
4. meaningful structural complexity;
5. testability/verification gaps;
6. operability/discoverability when relevant;
7. low-impact maintainability issues;
8. optional notes.

Style-only preferences are normally omitted.

---

## Inspect before judging

Read enough nearby evidence to understand:

- the change goal;
- affected callers;
- existing abstractions;
- tests;
- public interfaces;
- repository conventions;
- dependency direction;
- relevant history/documentation when available.

Repository consistency is evidence, not proof.

Do not recommend a different architecture without understanding why the current one exists.

---

## Finding acceptance gate

Emit a finding only when most of the following are true:

- materially relevant;
- concrete;
- actionable;
- supported by evidence;
- tied to an invariant or named quality dimension;
- confidence matches severity;
- not better delegated to formatter/linter/typechecker;
- not merely a personal preference.

For uncertainty that matters, downgrade authority or state the missing evidence.

---

## Finding severity

### Critical

Use only when the structural decision plausibly creates severe:

- correctness loss;
- data loss/corruption;
- security-boundary break;
- reliability failure;
- irreversible compatibility/migration problem.

### High

Substantial:

- broken invariant;
- unsafe evolution path;
- severe coupling;
- major reliability/operational cost;
- public compatibility risk.

### Medium

Material:

- complexity;
- cohesion;
- coupling;
- locality;
- testability;
- migration;
- discoverability

problem with a clear improvement path.

### Low

Small concrete improvement with limited impact.

### Note

Trade-off, future trigger, or optional contextual observation.

Do not inflate severity because a pattern is unfashionable.

---

## Finding format

Prefer:

```text
[Severity] Short title

Problem:
<what is wrong>

Why it matters:
<affected invariant/quality dimension>

Context/evidence:
<what in this repository/change supports the finding>

Trade-off:
<what competing concern matters>

Recommended change:
<smallest useful change>

Why this option:
<why it fits this context better than alternatives>

Verification:
<how to prove the change is safe>
```

For small findings, compress the format while keeping evidence and action clear.

---

## Bad review behavior

Do not report:

- "this function is too long" without identifying mixed responsibilities or comprehension cost;
- "use an interface" when there is no real variation/substitution boundary;
- "make it DRY" when duplication preserves local clarity or requirements are unstable;
- "use DDD" for simple CRUD/data movement without domain complexity;
- "use microservices" because the project may scale someday;
- "add comments" for obvious syntax;
- "remove comments" when they preserve non-obvious rationale/invariants;
- "mock this dependency" when the real dependency is cheap and deterministic;
- "increase coverage" without identifying uncovered risk;
- "rewrite in a faster language" without evidence of the bottleneck;
- "split this module" based only on line count;
- "this is not clean" as a reason.

---

## Preference noise rule

If two implementations are both:

- correct;
- idiomatic for the language/repository;
- similarly understandable;
- similarly maintainable;

do not emit a finding solely because one reviewer would write it differently.

Human attention is a scarce resource.

---

## Refactoring decision test

Before recommending a refactor, answer:

1. What current cost is being paid?
2. What evidence demonstrates it?
3. What quality dimension improves?
4. What new concepts/indirection appear?
5. What behavior/compatibility can break?
6. Is there a smaller safe step?
7. How will the change be verified?
8. What happens if we do nothing?

If these questions cannot be answered, the refactor may be premature.

---

## Long/cohesive code

Do not split code by line count.

A long function/module may be acceptable when:

- behavior is strongly sequential;
- shared state makes extraction harder to understand;
- branches belong to one cohesive algorithm;
- decomposition would create shallow wrappers/jumping.

Recommend decomposition when there are real independent reasons to change, such as:

- parsing + persistence + retry policy;
- business rules + network transport;
- protocol framing + storage;
- unrelated lifecycle ownership.

Preserve locality where it reduces cognitive load.

---

## Duplication review

Before recommending abstraction, classify duplication.

### Tolerate temporarily when

- requirements are still diverging;
- examples look similar but represent different concepts;
- abstraction would require flags/conditionals to hide differences;
- there are only a few cases and change pressure is low.

### Abstract when

- duplicated behavior encodes the same invariant;
- changes repeatedly need to be synchronized;
- the concept is stable;
- multiple real users/implementations exist;
- centralization materially reduces inconsistency.

DRY is a heuristic, not an invariant.

---

## Interface/trait review

A new interface/trait is more credible when:

- multiple real implementations exist;
- external/provider substitution is required;
- volatility must be isolated;
- a stable capability boundary exists;
- callers need to depend on a smaller contract;
- testing requires a real substitution boundary and no cheaper design exists.

Challenge it when:

- one implementation exists;
- factory/adapter/DI layers only wrap the same concrete type;
- consumers still need implementation-specific behavior;
- the abstraction mirrors implementation methods instead of defining a stable capability.

---

## Public API/protocol review

Raise scrutiny for:

- external APIs;
- protocols;
- serialized/persisted formats;
- plugin contracts;
- extension points.

Review:

- observable behavior;
- capability discovery;
- optional features;
- compatibility tiers;
- migration path;
- versioning;
- round-trip cost across IPC/network;
- debugging/provenance;
- deprecation/removal.

Do not design remote APIs as though calls are local.

---

## Testing review

Ask:

- Which failure mode is the test protecting?
- Is this the cheapest sufficient level of fidelity?
- Would a harmless implementation refactor break it?
- Is a real dependency cheap/deterministic enough to use?
- Is a fake more faithful than a pile of stubs?
- Is interaction testing necessary?
- Are larger tests covering integration/emergent behavior?
- Is the suite trusted, deterministic, and diagnostic?

Do not use one fixed test pyramid as a universal rule.

---

## Performance review

Load `principles/performance-engineering.md` when performance materially affects the decision.

Do not recommend performance-oriented structural changes without scoped evidence.

Ask:

- What metric matters: latency, throughput, memory, startup, power, fairness, durability cost, or another resource?
- Is the workload representative, and what is the evidence scope?
- Is the benchmark/profiler itself trustworthy for this conclusion?
- What resource or coordination cost is actually constrained?
- Can work be removed, reused, precomputed, coalesced, or moved out of the critical path before adding machinery?
- What data movement, serialization, copies, syscalls, locks, or round trips dominate?
- What happens at and beyond saturation?
- Does the optimization change caching, durability, freshness, retries, queue bounds, shutdown, or security semantics?
- How will the same workload verify the claimed improvement?

If the evidence is missing, recommend measurement rather than speculative architecture churn.

Escalate specialist-sensitive conclusions such as lock-free memory ordering, formal performance statistics, database-engine internals, modern transport tuning, side-channel behavior, or hardware-specific memory semantics.

---

## Representation review

Load `principles/representation-design.md` when correctness, performance, compatibility, or evolvability is dominated by the shape of data/state rather than code organization.

Ask:

- Does the representation encode the real relationship/invariant directly?
- Is state duplicated or reconstructed through conventions?
- Are incidental external differences normalized without erasing needed semantics?
- Is a human-facing representation being misused as a machine contract?
- Is an internal runtime object leaking into durable storage or protocol form?
- Can the representation be versioned, migrated, replayed, validated, and debugged?
- Does a physical optimization remain behind a stable logical model?
- Is provenance needed for automated transformations or decisions?

Do not recommend representation changes from elegance alone; identify the operation/invariant they improve and the migration cost they create.

## Rewrite/refactoring strategy

Load `principles/change-strategy.md` when the question is whether to leave, refactor, stage, coordinate, or replace a subsystem.

Before recommending a rewrite or broad migration, identify:

- current material cost;
- target benefit;
- behavioral oracle/verification strength;
- public/persisted/content compatibility surfaces;
- mixed old/new coexistence cost;
- cutover path;
- rollback/reversal;
- removal condition.

Do not treat "never rewrite" or "rewrite it cleanly" as useful review rules.

Raise the evidence threshold for high-consequence systems.

## Migration/deprecation review

Evaluate the full transition:

- discover consumers/state;
- add compatible target capability where needed;
- support old/new coexistence only as long as required;
- migrate/backfill;
- prevent backsliding;
- test conversion and mixed-version behavior;
- move consumers/traffic;
- define rollback;
- remove old dependency and temporary bridge.

A new implementation is not automatically better if migration/coexistence cost dominates its benefit.

A coordinated cross-cutting transition can be preferable to a long mixed architecture when the transition state itself is the greater risk and verification/rollback are strong.

---

## Final review summary

When useful, finish with:

- highest-risk findings first;
- unresolved assumptions;
- recommended verification;
- explicit statement when no meaningful issues were found.

Do not manufacture low-value issues to fill a review.
