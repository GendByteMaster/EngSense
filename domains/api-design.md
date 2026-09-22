# API Design Guidance

Status: **provisional**

Use this module when a decision affects a public, shared, remote, plugin, protocol, or persisted interface.

This module is grounded in the completed *Software Engineering at Google* and *AOSA Volume 1* research plus EngSense synthesis. It does not replace a dedicated API-security or protocol-correctness review.

## Core principle

An API is not only a type signature.

Its effective contract can include:

- observable behavior;
- ordering;
- timing;
- error shape;
- mutability;
- capability availability;
- versioning;
- transport cost;
- persistence/wire representation;
- extension semantics.

The design threshold should rise with **surface inertia**.

## Surface classes

Think in terms of:

```text
private implementation
module-local
repository-internal
organization-shared
external API
plugin/extension contract
protocol
persisted format
public ecosystem standard
```

Higher-inertia surfaces require stronger compatibility and migration reasoning.

## Observable behavior

Do not assume undocumented behavior is unused.

Check:

- callers;
- integration tests;
- examples;
- generated clients;
- support/docs;
- persisted data;
- downstream snapshots.

If behavior has been stable and externally visible, treat a change as a compatibility risk until consumer evidence says otherwise.

## Capability modeling

Do not force every implementation into a single interface when capabilities genuinely differ.

Prefer:

- capability-specific interfaces;
- explicit feature discovery;
- optional capabilities;
- tagged/discriminated metadata;
- separate adapters where semantics diverge.

Avoid APIs where unsupported operations are normal control flow.

## Remote API granularity

For RPC/IPC/network boundaries, include round-trip cost in API design.

Fine-grained APIs can create:

- latency multiplication;
- extra failure points;
- ordering complexity;
- repeated serialization/deserialization.

Consider:

- batching;
- coarser operations;
- immutable metadata snapshots;
- explicit streaming;
- command/event payloads.

Do not optimize remote calls as if they were local method calls.

## Compatibility policy

Define compatibility intentionally per surface.

Possible policies:

- internal unstable;
- source compatible;
- wire compatible;
- read-old/write-new;
- stable public;
- versioned breaking changes.

Avoid one global compatibility policy for every surface.

## Versioning and migration

When a breaking change is justified, include:

- consumer discovery;
- migration path;
- old/new coexistence rules;
- adapters or compatibility bridge where needed;
- backsliding prevention;
- deprecation timeline/trigger;
- rollback;
- removal condition.

A breaking change without a migration path is often an incomplete design.

## API size

Every public operation increases:

- compatibility burden;
- test matrix;
- documentation cost;
- security/trust surface;
- future change constraints.

Prefer the smallest public surface that satisfies real use cases.

Do not expose internals merely because they are convenient to expose.

## Generality

Challenge general-purpose APIs when:

- only one narrow workflow exists;
- generality introduces flags/modes;
- callers need implementation-specific escape hatches anyway;
- capabilities differ too much for one clean contract.

General APIs are more justified when multiple real consumers share stable semantics.

## Protocols and persisted formats

Treat these as high-inertia surfaces.

Review:

- canonical representation;
- forward/backward compatibility;
- version skew;
- unknown-field behavior;
- migration;
- replay;
- debuggability;
- provenance;
- partial rollout.

Binary compactness, human readability, and debuggability are trade-offs, not absolutes.

## Extension APIs

Use the least powerful extension mechanism that meets the requirement.

Rough risk spectrum:

```text
declarative configuration
< bounded callback/interface
< plugin module
< process boundary
< arbitrary in-process patching
```

More power can increase:

- compatibility burden;
- crash/failure blast radius;
- security surface;
- reasoning cost;
- migration cost.

## API findings

A useful API finding should name the affected property, such as:

- compatibility;
- discoverability;
- round-trip cost;
- unsupported-capability ambiguity;
- migration cost;
- observability;
- extension safety.

Do not report "this API is not clean" without concrete evidence.

## Revisit triggers

Revisit an API design when:

- consumer count materially changes;
- a second real implementation appears;
- a formerly internal surface becomes external;
- version skew appears;
- transport cost becomes material;
- migration becomes necessary;
- optional capabilities become common enough to reshape the contract.
