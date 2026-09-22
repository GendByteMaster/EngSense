# TypeScript Guidance

Status: **provisional**

Use TypeScript's structural type system and JavaScript runtime semantics directly. Avoid importing nominal/class-heavy architecture unless it solves a real problem.

## Data and state modeling

Prefer discriminated unions for closed variant/state models when consumers need exhaustive narrowing.

Good fits include:

- request states;
- command/event variants;
- reducer actions;
- protocol results;
- finite lifecycle states.

Use classes when they provide real value such as:

- lifecycle;
- encapsulated mutable invariants;
- identity;
- behavior-rich instances;
- framework requirements.

Do not introduce inheritance solely because several objects share fields.

## Structural typing

Remember that TypeScript interfaces/types are structural.

An interface can document a capability without requiring explicit implementation inheritance.

Do not introduce factories/adapters just to make a type "implement" an interface when structural compatibility already provides the desired contract.

## Runtime validation

Static TypeScript types do not validate untrusted runtime data.

At external boundaries such as:

- HTTP;
- files;
- environment variables;
- message queues;
- local storage;
- third-party SDK responses;

perform runtime validation when malformed data has meaningful consequences.

Do not duplicate runtime validation deeply inside trusted internal code unless the boundary requires it.

## Async behavior

Make async/error behavior explicit.

Do not hide network/process latency behind synchronous-looking abstractions.

Review:

- cancellation;
- timeout;
- retry semantics;
- Promise rejection behavior;
- concurrency limits;
- stale-result races.

Use specialist distributed/concurrency guidance when network ordering/idempotency matters.

## Modules vs classes

Prefer modules/functions for stateless capabilities when object identity/lifecycle adds no value.

Use classes when instance state/lifecycle is meaningful.

Avoid "service classes" whose only purpose is grouping unrelated functions under `new Service()`.

## Public API design

Because JavaScript objects are highly observable, public callers can depend on:

- property presence;
- property ordering in some contexts;
- thrown error shapes;
- timing/async behavior;
- mutation behavior.

Treat externally consumed shapes as compatibility surfaces even when TypeScript declarations are not the only observable contract.

## Optional capability

Do not force every implementation into a single interface with methods that some implementations can only throw as unsupported.

Prefer:

- capability interfaces;
- discriminated capability metadata;
- separate adapters;
- explicit feature discovery.

## Framework boundaries

Framework conventions are evidence.

Do not fight a framework's dataflow/lifecycle model unless the local convention creates a material engineering problem.

Do not elevate framework conventions into universal TypeScript rules.

## Common traps

Challenge:

- abstract base classes for closed data variants;
- Java-style getters/setters with no invariant;
- deep inheritance trees;
- repository/service/use-case layers that only forward calls;
- generic wrappers around `fetch`/SDKs that erase useful error/capability semantics;
- type-only safety assumptions at untrusted runtime boundaries.
