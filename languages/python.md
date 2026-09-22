# Python Guidance

Status: **provisional**

Prefer simple, explicit, idiomatic Python unless stronger structure protects a real invariant or boundary.

## Simplicity

Python makes small modules, functions, protocols, dataclasses, and plain objects cheap.

Do not introduce enterprise-style layering merely to make a small service resemble a large Java system.

Challenge layers that only forward arguments unchanged.

## Functions vs classes

Prefer functions/modules when:

- behavior is stateless;
- construction/lifecycle adds no value;
- one namespace is sufficient.

Use classes when:

- state/identity matters;
- lifecycle/resource ownership matters;
- invariants belong with data;
- polymorphism is real.

Do not create classes solely to hold static-like methods.

## Protocols and abstraction

Use `typing.Protocol` or abstract interfaces when callers genuinely need a capability boundary.

Do not create one protocol per concrete implementation by default.

Structural typing can keep contracts lightweight when substitution is real.

## Data models

Use dataclasses/Pydantic/plain mappings according to the boundary and validation need.

Runtime validation is especially valuable for:

- external HTTP input;
- configuration;
- persisted/external data;
- third-party responses.

Do not repeatedly validate already-trusted internal objects without a reason.

## Typing

Typing should improve:

- comprehension;
- refactoring safety;
- API clarity;
- tooling.

Do not pursue maximum type sophistication when annotations become harder to understand than the behavior.

Avoid `Any` at important boundaries when a stable useful type can be expressed.

## Exceptions and errors

Use exceptions where the surrounding Python ecosystem expects them.

Preserve meaningful error categories when callers need different recovery behavior.

Do not wrap every exception in a custom exception layer if it adds no context or contract value.

## Async and I/O

Treat async as a concurrency model, not a syntax preference.

Review:

- blocking calls inside async code;
- cancellation;
- timeouts;
- task ownership;
- resource cleanup;
- connection/session lifecycle.

Do not introduce async to CPU-bound or purely synchronous flows without a concurrency need.

## FastAPI/service layering

A small FastAPI application does not automatically require:

`route → use-case → service → repository → adapter`

Keep a layer when it has a real responsibility such as:

- external schema/boundary handling;
- authorization policy;
- domain invariant;
- transaction boundary;
- provider/persistence isolation;
- independent lifecycle/testing need.

Collapse pass-through layers.

## Dynamic features

Metaprogramming, monkeypatching, decorators, import-time registration, and dynamic attribute access are powerful escape hatches.

Use them when they materially reduce repeated machinery or are ecosystem-standard.

Avoid them when explicit code would be easier to inspect, type, test, and migrate.

## Common traps

Challenge:

- unnecessary base classes;
- generic factories for one concrete type;
- excessive dependency injection containers;
- Java-style DTO/entity/service duplication;
- hidden import-time side effects;
- monkeypatching where a bounded extension seam would suffice.
