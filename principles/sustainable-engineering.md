# Sustainable Engineering Lens

Source basis: completed *Software Engineering at Google* research.

## Question this lens answers

> Will this decision remain workable across the expected lifetime, scale, and rate of change of the system?

Use this lens primarily for long-lived/shared code, public/internal APIs, infrastructure, repeated workflows, migration-heavy systems, and organization-scale engineering.

Do not apply it mechanically to disposable prototypes or tiny local changes.

## Core dimensions

Consider:

- expected lifetime;
- change frequency;
- consumer count;
- organization/repository scale;
- human scalability;
- compatibility;
- migration/removal cost;
- reversibility;
- feedback latency;
- knowledge concentration;
- operational cost.

## Time and change

A decision that is cheap today can become expensive when:

- dependencies evolve;
- consumers multiply;
- observable behavior becomes relied upon;
- platforms change;
- ownership changes;
- migration becomes unavoidable.

Do not compare:

```text
change now
vs
do nothing = free
```

Compare:

```text
change now
vs
current maintenance cost
+ future forced-change cost
+ migration constraints
```

## Human scalability

A workflow can be technically simple but organizationally unscalable.

Ask how human effort grows with:

- number of repositories;
- number of services;
- number of consumers;
- number of engineers;
- number of repeated executions.

Manual work that is reasonable at 3 instances may be unacceptable at 3,000.

## Evidence and feedback

Prefer earlier reliable feedback when its maintenance cost is justified.

Examples:

- static analysis;
- presubmit checks;
- tests;
- code review;
- automated migrations.

Do not add checks merely to increase process.

The value comes from catching recurring problems cheaply and early.

## Knowledge resilience

For critical systems, consider whether architecture depends on one person understanding:

- hidden constraints;
- deployment rituals;
- migration procedures;
- failure recovery;
- design rationale.

Knowledge concentration is a maintainability risk when the system outlives the individual owner.

## Reversibility

A choice is reversible only when a plausible reversal path exists.

Relevant capabilities include:

- tests;
- migration tooling;
- rollback;
- compatibility layers;
- version control;
- staged rollout;
- large-scale change tooling.

Do not call speculative abstraction "reversibility" if it adds complexity without creating a real reversal path.

## Standardization

Standardization can reduce:

- learning cost;
- tooling complexity;
- migration cost;
- review disagreement;
- operational variance.

But it is scale-dependent.

Do not override a material workload-specific need merely for consistency.

## Output pattern

When this lens matters, make the reasoning explicit:

```text
Current benefit:
Deferred cost:
Scale/lifetime assumption:
Human/operational impact:
Reversibility:
Revisit trigger:
```

## Anti-rules

Do not:

- apply Google-scale process to every repository;
- equate consistency with correctness;
- optimize only for present implementation cost;
- treat "leave it alone" as zero-cost;
- assume a decision remains good after its assumptions change.
