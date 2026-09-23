# Domain Modeling Guidance

Status: **provisional routing guidance**

Use this module when the main engineering question is whether business/domain rules deserve a richer explicit model, or whether the problem should remain simple data flow / CRUD.

This module is **not** the future source-specific Domain-Driven Design lens. The mandatory full-text Eric Evans research gate in Issue #2 is still open. Do not attribute this guidance to Evans or claim full DDD coverage.

## Core question

Do not ask:

> Should this project use DDD?

Ask:

> Is domain complexity high enough that explicit domain concepts, ownership, invariants, and lifecycle boundaries reduce total complexity compared with straightforward application/data-flow code?

The default is not "rich domain model."

The default is the simplest model that preserves the real invariants.

---

## Load this module when

Relevant signals include:

- multiple business rules interact around the same concept;
- valid state transitions matter;
- invariants span several fields/entities/operations;
- language used by domain experts has precise meaning that code currently obscures;
- lifecycle ownership matters;
- consistency boundaries are non-trivial;
- the same business rule is duplicated across handlers/services/jobs;
- orchestration is becoming a hidden state machine;
- changes frequently require touching unrelated transport/persistence layers because business policy has no explicit home.

Do not load this module merely because the code has:

- database entities;
- HTTP routes;
- DTOs;
- repositories;
- services;
- CRUD operations;
- validation schemas.

Those are technical structures, not evidence of a complex domain.

---

## Prefer simple data/application flow when

Simple modules/functions/data structures are usually enough when:

- operations are straightforward CRUD;
- validation is mostly syntactic or boundary-level;
- there are few cross-field/domain invariants;
- state transitions are trivial;
- persistence shape closely matches the application need;
- most logic is transport, authorization, mapping, or data movement;
- introducing aggregates/value objects/services would mostly rename existing pass-through layers.

A simple CRUD application is not "missing DDD."

Do not create:

```text
route
→ use case
→ domain service
→ repository interface
→ repository implementation
→ adapter
→ database
```

when most layers forward the same data unchanged and no invariant boundary is gained.

---

## Prefer a richer domain model when

A richer model becomes more credible when it centralizes real business semantics.

Useful signals:

### Stable domain language

Important concepts have precise meaning and those concepts recur across workflows.

Examples:

- reservation;
- entitlement;
- credit;
- settlement;
- subscription state;
- evidence;
- reputation;
- capability.

The exact names depend on the repository. Do not invent domain terminology from generic architecture advice.

### Non-trivial invariants

Examples of the shape of an invariant:

```text
A transition is valid only when several conditions hold.
Two fields cannot vary independently.
A business operation must update multiple related values atomically.
Only one object owns permission to perform a transition.
```

If a rule must remain true regardless of which API/job/UI triggers the operation, it needs an authoritative home.

### Meaningful lifecycle/state machine

Explicit state transitions are often better than scattered booleans and handler-specific conditionals when:

- transition legality matters;
- transitions carry side effects;
- retries/replay matter;
- invalid intermediate states are costly.

### Repeated policy across delivery mechanisms

If the same rule appears in:

- HTTP handler;
- worker;
- CLI;
- scheduled job;
- admin UI backend;

extract the **policy**, not necessarily an enterprise layer stack.

---

## Invariant ownership before layering

Before introducing entities, services, aggregates, repositories, or use cases, identify:

```text
Invariant:
Owner:
Mutation boundary:
Persistence/transaction boundary:
External side effects:
Verification:
```

If no clear invariant can be named, a richer domain abstraction may be premature.

Layer count is not a quality metric.

---

## Data model vs domain model

A database record is not automatically a domain object.

A transport DTO is not automatically an anemic-domain smell.

Transparent data is appropriate when:

- the representation itself is the contract;
- consumers need direct data access;
- there is little protected behavior;
- operations vary more than data types.

Encapsulated/domain behavior is more useful when:

- representation must be protected to preserve invariants;
- invalid operations must be prevented;
- state transitions are meaningful;
- behavior and data evolve together.

Load `principles/representation-design.md` when the dominant question is data shape rather than domain policy.

---

## Repositories and persistence boundaries

Do not introduce repository abstractions only because a project has a database.

A repository-like boundary is more credible when:

- domain logic should not depend on storage representation;
- multiple persistence mechanisms are real;
- persistence querying/mapping is materially complex;
- aggregate loading/saving has meaningful semantics;
- the storage model is volatile relative to stable policy.

Prefer direct persistence access in simple application code when a repository would only mirror the database client one-for-one.

Load `domains/persistence.md` when correctness depends on:

- transactions;
- atomicity;
- durability;
- migrations;
- replay;
- isolation;
- persisted compatibility.

---

## Domain service vs ordinary function

Use a domain-oriented service/function when behavior:

- belongs to the domain;
- spans multiple domain concepts;
- does not naturally belong to one object/state owner;
- represents stable business policy.

Do not create a "service" merely because frameworks commonly use a service layer.

A plain function or module can be the better domain mechanism.

Language idioms have priority over class-oriented terminology.

---

## Application orchestration vs domain policy

Keep orchestration distinct when useful.

Application orchestration often owns:

- load dependencies/state;
- call domain policy;
- persist;
- publish/send side effects;
- coordinate retries/idempotency;
- translate external errors.

Domain policy owns:

- whether an action is valid;
- state transition semantics;
- calculations/business rules;
- domain-specific failure reasons.

Do not push network/database/framework concerns into the domain merely to make the outer layer thinner.

Do not push business policy into controllers/jobs merely to avoid abstractions.

---

## Bounded-context-style routing without claiming DDD

When one word means materially different things in different subsystems, or two parts of the system evolve under different rules, investigate whether a boundary is needed.

Signals:

- conflicting definitions for the same concept;
- independent data ownership;
- independent lifecycle/change cadence;
- translation is already occurring informally;
- teams/components cannot agree on one model without flags/optional fields.

A boundary can be:

- module/package;
- schema;
- service/process;
- adapter/translation layer.

Do not create a network service just to obtain conceptual separation.

This module may identify that a future source-specific DDD lens would be relevant, but it must not manufacture Evans terminology as authority before that research is complete.

---

## Distributed-domain intersection

Domain complexity and distributed-systems complexity are separate axes.

A rich domain model does not make retries, timeouts, replication, or consistency disappear.

A distributed system does not automatically need DDD.

Load `domains/distributed-systems.md` when the decision crosses:

- process/network boundaries;
- partial failure;
- timeout ambiguity;
- retry/deduplication;
- independent deployment/version skew;
- replication/consistency;
- queues/streams with delivery semantics.

Keep domain invariants explicit across those boundaries.

If a business invariant depends on consensus, replication guarantees, isolation, or distributed ordering, require specialist distributed-systems review.

---

## Decision test

Before recommending richer domain modeling, answer:

1. What business invariant is difficult to preserve today?
2. Where is that rule currently duplicated or hidden?
3. What concept would become authoritative?
4. What invalid state/transition becomes harder to represent?
5. What new abstraction/layer is introduced?
6. Does the abstraction reduce total change cost?
7. Does it fit the target language?
8. Can the same result be achieved by a smaller module/function/type?
9. How will behavior be verified?
10. What evidence would justify further modeling later?

If these cannot be answered, do not recommend DDD-like structure from aesthetics alone.

---

## Revisit triggers

Revisit a simple CRUD/data-flow design when:

- business invariants multiply;
- state transitions become error-prone;
- policy is duplicated across entry points;
- persistence concerns repeatedly leak into business decisions;
- one concept develops a distinct lifecycle/ownership boundary;
- changes require synchronized edits across many technical layers.

Revisit a rich model and simplify when:

- abstractions mostly delegate;
- domain types mirror database/DTOs one-for-one without protecting invariants;
- language/serialization friction dominates;
- the expected domain complexity never appeared;
- new contributors must traverse many layers to make trivial changes.

---

## Specialist boundary

Require deeper domain/product expertise when correctness depends on business rules not represented in repository evidence.

EngSense must not invent domain truth.

When domain meaning is ambiguous, state the missing rule or seek authoritative product/domain documentation rather than choosing an architecture around a guess.
