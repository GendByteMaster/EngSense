# Evolution and Compatibility Lens

Source basis: completed Google SWE and AOSA Volume 1 research.

## Question this lens answers

> How much future change freedom should be traded for compatibility with existing consumers, data, protocols, and behavior?

## Surface inertia

Classify the surface:

```text
private
module
repository
organization
external API
plugin/extension contract
protocol
persisted format
public ecosystem standard
```

As inertia increases, raise the evidence threshold for breaking changes.

## Observable behavior

Formal documentation is not the entire effective contract.

Consumers may depend on:

- ordering;
- timing;
- error shapes;
- side effects;
- default values;
- performance characteristics;
- undocumented-but-stable behavior.

Investigate before declaring a behavior "implementation detail."

## Compatibility is not absolute

Do not preserve all behavior forever.

A compatibility promise should reflect:

- consumer count;
- maturity;
- lifetime;
- ecosystem reach;
- migration feasibility;
- severity of current defect;
- ability to version.

Early broken behavior may be cheaper to fix than permanent support.

## Migration is part of design

For meaningful change, consider:

- consumer discovery;
- compatibility bridge;
- dual-read/dual-write or adapters when relevant;
- staged rollout;
- backfill;
- backsliding prevention;
- rollback;
- deprecation;
- final removal.

A new design is incomplete if the transition is ignored.

## Tiered compatibility

Different surfaces can rationally have different policies.

Example:

```text
internal implementation → fast evolution
stable internal API → scoped compatibility
public protocol → strict versioning/migration
persisted data → explicit schema evolution
```

Do not apply one global rule.

## Revisit triggers

Reconsider compatibility policy when:

- a private surface becomes shared/public;
- consumer count grows;
- a migration path becomes available;
- current behavior causes material correctness/security harm;
- versioning can isolate change;
- maintenance burden exceeds compatibility value.

## Anti-rules

Do not:

- equate undocumented with unused;
- treat compatibility as automatically virtuous;
- break high-inertia surfaces for local cleanup;
- preserve severely broken immature behavior merely because it exists;
- ignore rollback and partial rollout.
