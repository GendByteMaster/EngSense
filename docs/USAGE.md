# Using EngSense

EngSense is most useful when a coding agent must make a **non-trivial engineering judgment**, not when it only needs to perform mechanical work.

## When to use it

Use EngSense for questions such as:

- Should this abstraction exist?
- Should this function/module be split?
- Should duplicated code be centralized?
- Is this API boundary too broad or too chatty?
- Is a provider interface justified?
- Should this migration be incremental or coordinated?
- Is a rewrite justified?
- Is a performance escape hatch supported by evidence?
- Is complexity being moved into callers or operations?
- Does this representation preserve the right semantics?
- Does a structural cleanup threaten compatibility, persistence, concurrency, or distributed-systems invariants?

Do not invoke a full EngSense analysis for:

- formatting;
- trivial renames;
- obvious lint fixes;
- syntax-only changes;
- deterministic mechanical edits.

## Three review modes

### Focused review

Use for one function, module, PR, or specific engineering concern.

Desired behavior:

- stay inside the requested scope;
- report only material findings;
- do not expand into unrelated architecture cleanup.

Example request:

~~~text
Review this PR with EngSense. Focus on whether the new provider abstraction is justified.
~~~

### Refactoring review

Use when deciding whether structure should change.

Example request:

~~~text
Use EngSense to review this module for refactoring. Identify the actual current cost,
the smallest safe structural improvement, and how to verify behavior remains unchanged.
~~~

### Architecture-quality review

Use for subsystem boundaries, public APIs, major migrations, representation changes, or cross-process design.

Example request:

~~~text
Use EngSense to compare these two service boundaries. Preserve current compatibility
and reliability invariants, identify where each option places complexity, and recommend
the better trade-off for the current scale.
~~~

## Useful request patterns

### Abstraction review

~~~text
Use EngSense to decide whether this interface/trait is justified.
Inspect actual implementations and callers. Do not keep it only because dependency
inversion is considered a best practice.
~~~

### Duplication review

~~~text
Use EngSense to review this duplication. Determine whether it represents one stable
invariant or only similar-looking code with different reasons to change.
~~~

### Function decomposition

~~~text
Use EngSense to review this long function. Do not split by line count.
Identify cohesive behavior, independent responsibilities, shared state, and whether
extraction improves or harms locality.
~~~

### Migration

~~~text
Use EngSense to review this migration plan. Compare staged migration, coordinated
change, and leaving the current design in place. Include coexistence cost, rollback,
compatibility, and removal conditions.
~~~

### Performance-oriented change

~~~text
Use EngSense to review this optimization. Start from the measured metric and workload,
identify the constrained resource, and reject speculative structural changes that are
not supported by evidence.
~~~

### API/protocol

~~~text
Use EngSense to review this API. Account for public-surface inertia, round-trip cost,
capability differences, compatibility, migration, and whether the API exposes a stable
semantic boundary.
~~~

## How EngSense reasons

For a non-trivial case, EngSense should approximately follow this sequence:

1. define the real problem;
2. classify scope;
3. identify relevant architecture drivers;
4. preserve invariants;
5. gather evidence;
6. select affected quality dimensions;
7. locate complexity;
8. identify conflicts;
9. compare viable alternatives;
10. evaluate abstraction pressure;
11. evaluate representation leverage when relevant;
12. evaluate public-surface inertia;
13. evaluate scale honestly;
14. evaluate failure and overload;
15. evaluate reversibility;
16. choose the decision;
17. assign authority;
18. select a change strategy;
19. implement minimally;
20. verify;
21. re-evaluate where complexity moved.

The full framework lives in [../decision-framework.md](../decision-framework.md).

## Compact decision format

For a non-trivial decision, a useful EngSense answer can look like:

~~~text
Context:
<relevant repository/task facts>

Goal:
<what must improve>

Invariants:
<what must not break>

Evidence:
<tests, callers, profiles, contracts, history, incidents, etc.>

Alternatives:
<plausible options>

Trade-offs:
<what each option gains and pays>

Decision:
<contextual choice>

Assumptions:
<what is not yet known>

Verification:
<how to prove the change is safe/useful>

Revisit when:
<concrete trigger that could change the decision>
~~~

Not every task needs the full record.

## Example: premature abstraction

Context:

- one repository-local implementation;
- no external provider;
- factory always returns the same type;
- tests can use the concrete implementation directly.

Bad reasoning:

> Add an interface now because dependency inversion is cleaner.

EngSense reasoning:

- no real variation axis is demonstrated;
- the interface adds navigation and concepts;
- substitution is hypothetical;
- the abstraction protects no current capability boundary.

Decision:

~~~text
Keep the concrete implementation.

Revisit when:
A second real provider, an external provider boundary, or an independent substitution
requirement appears.
~~~

## Example: justified abstraction

Context:

- two production providers exist;
- SDKs differ;
- provider-specific branches leak into callers;
- capabilities are not identical.

EngSense should **not** respond by forcing a false lowest-common-denominator interface.

A better decision is to create a provider boundary while preserving explicit capability differences.

## Example: long cohesive function

A 180-line parser function is not automatically a problem.

If it:

- implements one sequential grammar production;
- shares parser state;
- has branches belonging to one algorithm;
- would turn into shallow wrappers after extraction;

EngSense may recommend keeping it together.

If it also owns persistence, retry policy, metrics transport, or unrelated lifecycle responsibilities, decomposition becomes more credible.

## Example: duplication

Two similar workflows are evolving differently and a shared helper requires multiple mode flags.

EngSense may deliberately tolerate duplication.

When the duplicated logic later represents the same stable invariant and repeatedly changes in sync, centralization becomes more justified.

## Example: performance fast path

A generic path is correct, but profiling shows one conversion dominates CPU. A native compatible path materially improves end-to-end performance and can remain behind the same public API.

EngSense can accept a **bounded fast path** if:

- the hotspot is measured;
- eligibility is explicit;
- semantics remain correct;
- the generic fallback remains;
- maintenance cost is contained;
- the improvement is verified under the representative workload.

## Example: rewrite decision

A rewrite should not be approved because:

- code is old;
- architecture is ugly;
- a new framework is preferred.

A replacement becomes more credible when:

- current cost is material;
- behavior is understood;
- strong regression/characterization evidence exists;
- the replacement has a real advantage;
- migration/cutover is defined;
- rollback is credible;
- coexistence cost is bounded.

See [EXAMPLE_REVIEWS.md](EXAMPLE_REVIEWS.md) for fuller review examples.

## Specialist-sensitive tasks

EngSense can help frame a decision, but should defer specialist semantics for areas such as:

- cryptography/authentication;
- database-engine isolation and durability;
- lock-free memory ordering;
- consensus/quorum;
- transport-level performance;
- legal/compliance constraints;
- specialized UI/UX.

A strong EngSense result explicitly says where that boundary is instead of inventing confidence.

## Using EngSense with repository evidence

When a repository is available, ask the agent to inspect only the evidence necessary for the decision:

- affected callers;
- implementations;
- tests;
- public contracts;
- nearby architecture;
- migration history;
- benchmark/profile evidence;
- operational failure evidence.

Repository consistency is evidence, not proof.

The goal is not to preserve every existing pattern. The goal is to understand why a pattern exists before changing it.
