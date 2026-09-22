# EngSense Decision Framework

Status: **implemented core framework — source-specific coverage remains intentionally incomplete while the mandatory research corpus is open**

Use this framework for non-trivial engineering decisions. Skip unnecessary ceremony for small, obvious changes.

---

## 1. Define the real problem

State the actual behavior, quality risk, or decision.

Reject vague prompts such as:

- "make it cleaner";
- "apply best practices";
- "use SOLID";
- "split this function";
- "add an interface".

Translate them into a concrete problem when evidence supports one.

Examples:

- one function combines persistence, retry policy, and parsing;
- a public API leaks an unstable internal representation;
- a queue can grow without bound under storage slowdown;
- a second provider now exists and the current concrete coupling blocks substitution.

If there is only stylistic discomfort, say so.

---

## 2. Classify scope

Choose the smallest scope that actually contains the problem:

```text
local expression/function
module
package
repository
service/application
platform
organization
public ecosystem
```

Do not import organization-scale practices into local code without evidence that scale matters.

Do not keep analysis local when the behavior crosses process, network, persistence, or public compatibility boundaries.

---

## 3. Capture architecture drivers

Identify only relevant drivers:

```text
language/runtime
workload
lifetime
current scale
expected scale
variation axes
consumer/provider population
compatibility surface
performance constraints
failure model
trust model
concurrency model
persistence model
deployment model
operational model
contributor/organization model
migration/removal expectations
```

Separate known facts from assumptions.

---

## 4. Preserve invariants

List behavior that must not accidentally change.

Possible invariants include:

- externally observable behavior;
- wire/protocol compatibility;
- persisted data compatibility;
- transaction atomicity/durability;
- ordering;
- idempotency;
- retry semantics;
- security properties;
- concurrency guarantees;
- resource bounds;
- user-visible workflows;
- command/replay semantics.

For specialist-sensitive invariants, defer to specialized guidance rather than guessing.

---

## 5. Gather evidence

Classify evidence:

### Strong direct evidence

- executable tests;
- measured benchmark/profile data;
- production traces/incident evidence;
- actual callers/implementations;
- explicit public contract;
- observed failure;
- repository dependency graph.

### Contextual evidence

- repository conventions;
- historical migrations;
- architecture docs;
- stable recurring code patterns;
- operational practices;
- contributor/user feedback.

### Weak evidence

- estimate;
- analogy;
- hypothetical future use;
- generic pattern preference;
- unsupported "best practice".

Recommendations should weaken as evidence weakens.

---

## 6. Select affected quality dimensions

Choose only what matters.

Common dimensions:

```text
correctness
comprehension
cognitive_complexity
cohesion
coupling
locality
discoverability
maintainability
evolvability
compatibility
testability
reliability
operability
reproducibility
deployability
human_scalability
knowledge_resilience
provenance
contributor_accessibility
migration_cost
removal_cost
reversibility
extension_safety
coordination_cost
user_impact
end_to_end_latency
throughput
resource_efficiency
overload_resilience
performance_observability
```

Do not produce a universal numeric score.

---

## 7. Locate complexity

For every alternative, ask where its complexity lives.

Possible locations:

```text
core
callers
providers/adapters
public API
build/deploy
runtime operations
migration
support/compatibility
contributors
users
```

Record both:

- amount of complexity;
- multiplicity of complexity.

A central complex implementation may be cheaper than simple logic duplicated across hundreds of clients.

A centralized abstraction may also become an expensive bottleneck.

---

## 8. Identify conflicts

Load `references/conflicts.md`.

Do not resolve tensions by slogan.

Examples:

```text
abstraction vs locality
standardization vs specialization
compatibility vs architectural freedom
DRY vs local clarity
isolation vs fidelity
centralization vs scale
extensibility vs compatibility burden
portability vs native capability
reversibility vs speculative abstraction
```

Name the conflict explicitly.

---

## 9. Generate viable alternatives

For a meaningful design decision, compare at least two plausible options when available.

Do not include obviously bad strawmen.

A useful option comparison contains:

- what changes;
- benefit;
- new complexity;
- where complexity moves;
- new coupling;
- compatibility impact;
- migration cost;
- failure modes;
- scale ceiling;
- reversibility;
- verification path.

---

## 10. Evaluate abstraction pressure

An abstraction is supported by stronger evidence when one or more exist:

- multiple real implementations;
- stable repeated variation;
- external/provider/platform boundary;
- repeated invariant;
- independently changing lifecycle;
- volatile dependency;
- substantial combinatorial duplication;
- focused testability;
- stable domain representation.

Negative signals:

- one implementation;
- no substitution requirement;
- hypothetical reuse only;
- consumers need implementation details anyway;
- abstraction adds more concepts than it removes;
- framework exists only to satisfy a test/mocking style.

---

## 11. Evaluate representation leverage

When the decision changes how state, relationships, commands, history, or dependencies are represented, ask:

- What invariant/relationship does the representation make explicit?
- Does it remove duplicated or convention-based state?
- Can producers/consumers operate without hidden context?
- Is it transient, internal, persisted, or public?
- Does it improve replay, scheduling, validation, provenance, or migration?
- Does normalization remove incidental variance without erasing required domain semantics?
- Does physical optimization remain separable from the logical model?

Load `principles/representation-design.md` when representation is a primary architecture lever.

---

## 12. Evaluate public-surface inertia

Classify the surface:

```text
private
module-local
repository-internal
organization-shared
external API
protocol
persisted format
public ecosystem standard
```

As inertia rises, increase attention to:

- observable behavior;
- compatibility;
- versioning;
- migration;
- deprecation;
- rollout;
- downstream testing;
- consumer discovery.

Do not assume undocumented behavior is unused.

---

## 13. Evaluate scale honestly

Capture:

```text
current_scale
expected_scale
known_ceiling
ceiling_probability
crossing_cost
migration_trigger
```

A known future ceiling does not make a simple present design wrong.

It becomes a current problem when:

- expected growth approaches it;
- crossing it is expensive;
- failure at the ceiling is severe;
- migration must begin early.

Watch for nonlinear knees.

---

## 14. Evaluate failure and overload

When relevant, test reasoning beyond the happy path:

- dependency slowdown;
- retry amplification;
- queue growth;
- memory/disk exhaustion;
- partial failure;
- stale replicas/state;
- worker loss;
- version skew;
- malformed/adversarial input;
- restart/recovery;
- rollback failure.

For distributed/security/concurrency semantics, engage specialized guidance.

---

## 15. Evaluate reversibility

Classify actual reversal support:

```text
theoretical
manual
tested
automated
staged
```

Consider:

- tests;
- schema/protocol adapters;
- feature flags;
- data backfill;
- rollback;
- version control;
- migration tooling;
- large-scale refactoring capability.

Do not count "we can rewrite it later" as meaningful reversibility.

---

## 16. Select the decision

Prefer the option that best satisfies the relevant goals under the current constraints.

Do not choose based on:

- most patterns;
- fewest lines;
- most abstractions;
- maximum DRY;
- maximum genericity;
- maximum compatibility;
- maximum future flexibility.

A good decision may deliberately accept a weakness because another constraint dominates.

State that trade-off.

---

## 17. Assign authority

Classify the conclusion:

### Invariant / hard gate
Use only for very high-confidence correctness, safety, compatibility, or explicit project constraints.

### Rule
Use for strongly scoped project/platform policy.

### Strong recommendation
Use for high-confidence material quality issues.

### Guidance
Use when alternatives are valid but one better fits current constraints.

### Heuristic
Use for a useful default that should be reconsidered with contrary evidence.

### Note
Use for non-blocking context.

### Preference
Normally do not emit.

---

## 18. Select change strategy

When the decision requires restructuring, choose the transition strategy explicitly:

```text
leave in place
incremental refactor
staged migration
coordinated cross-cutting change
replacement / rewrite
```

Use `principles/change-strategy.md` when this choice is material.

For broad change, account for:

- behavioral oracle;
- coexistence cost;
- cutover;
- rollback;
- removal of temporary compatibility code.

Do not assume smaller steps are always safer when mixed old/new states create the larger risk.

---

## 19. Implement minimally

When changing code:

- fix the identified problem;
- preserve unrelated behavior;
- avoid opportunistic rewrites;
- keep migration steps safe;
- do not introduce adjacent architecture without justification.

If a larger redesign is genuinely required, explain why a local change cannot preserve the required invariants.

---

## 20. Verify

Choose checks that match the risk:

- formatter;
- linter;
- typechecker;
- unit tests;
- integration/contract tests;
- build;
- benchmark/profile under a representative workload;
- load/saturation or memory/trace verification when performance is material;
- migration test;
- compatibility test;
- failure/recovery test;
- project-specific checks.

Prefer the cheapest verification that provides sufficient confidence.

Do not treat code coverage alone as proof of quality.

---

## 21. Re-evaluate after the change

Ask:

- Did complexity decrease or move elsewhere?
- Did the change introduce a new public surface?
- Did coupling become explicit or merely relocate?
- Did testability improve for meaningful behavior?
- Did the scale ceiling change?
- Did migration/removal become harder?
- Did a local optimization weaken global consistency?
- Did the implementation preserve the stated invariants?

---

## Compact decision record

Use when the decision is non-trivial and worth preserving.

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

"Revisit when" should name a concrete trigger where possible, such as:

- a second real provider appears;
- consumer count becomes external/public;
- p95 latency exceeds a measured threshold;
- data volume approaches a known storage ceiling;
- migration tooling becomes available;
- a security/trust assumption changes.
