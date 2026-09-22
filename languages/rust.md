# Rust Guidance

Status: **provisional**

This module is based on current EngSense research plus language/ecosystem reasoning. The mandatory *Rust for Rustaceans* full-book research is still open, so do not attribute these rules to that source.

## Core orientation

Prefer designs that make invalid or ambiguous states harder to represent while keeping ownership, lifetimes, and dispatch costs visible.

Do not transplant class-heavy or interface-per-type architecture into Rust automatically.

## Traits

Use a trait when it represents a real capability or substitution boundary, such as:

- multiple real implementations;
- external/provider boundary;
- runtime polymorphism is required;
- generic algorithms need shared behavior;
- callers should depend on a smaller stable contract.

Challenge a trait when:

- one implementation exists;
- it mirrors the concrete type one-for-one;
- it exists only to satisfy a mocking style;
- it forces `Box<dyn Trait>` without a runtime-polymorphism need;
- consumers still need implementation-specific behavior.

Prefer static dispatch/generics when polymorphism is compile-time and monomorphization cost is acceptable.

Prefer dynamic dispatch only when runtime heterogeneity/substitution is part of the requirement.

## Enums and state

Prefer enums and exhaustive matching for:

- closed state machines;
- protocol variants;
- lifecycle states;
- result categories;
- mutually exclusive modes.

Do not replace a closed enum with trait-object hierarchies solely for "extensibility."

If the state space is intentionally open to external implementations, a trait/plugin boundary may be more appropriate.

## Ownership and borrowing

Treat ownership as architecture, not syntax.

When reviewing a refactor, ask whether it:

- clarifies who owns data;
- reduces unnecessary cloning;
- avoids lifetime complexity that exceeds the value of borrowing;
- prevents shared mutable aliasing;
- keeps synchronization ownership explicit.

Do not force zero-copy/borrowing when cloning a small value would greatly simplify code without material cost.

Do not clone reflexively to silence borrow-checker design problems when ownership is genuinely wrong.

## Error modeling

Prefer typed errors when callers need to distinguish recovery/handling behavior.

Avoid large error enums containing unrelated implementation details when only one layer needs them.

Do not erase actionable error semantics into generic strings at important boundaries.

At public boundaries, decide intentionally which implementation details are stable enough to expose.

## Concurrency

Do not refactor synchronization based on readability alone.

Preserve:

- ownership;
- Send/Sync expectations;
- lock ordering;
- atomicity;
- task cancellation;
- channel backpressure;
- shutdown semantics.

Use specialist concurrency review when correctness depends on memory ordering or subtle synchronization.

## Allocation and indirection

Treat:

- `Box`;
- `Arc`;
- trait objects;
- heap allocation;
- cloning;
- reference counting

as trade-offs, not smells.

Report them only when they materially affect:

- performance;
- ownership clarity;
- API design;
- lifecycle complexity.

## APIs

Prefer APIs that make ownership/cost semantics understandable.

Be cautious with APIs that:

- require unnecessary cloning;
- hide blocking work;
- hide allocation;
- return opaque trait objects without substitution value;
- expose implementation lifetimes accidentally.

## Anti-pattern transfer examples

Usually challenge:

- interface + implementation + factory for every type;
- service locator;
- runtime DI container for simple construction;
- class-hierarchy emulation using trait objects where enums are closed and sufficient;
- getters/setters around plain data without invariants.

## Revisit triggers

A concrete implementation can become a trait boundary when:

- a second real implementation appears;
- plugins/providers must be selected at runtime;
- the implementation becomes volatile behind a stable capability;
- consumers need a narrower contract than the concrete type.
