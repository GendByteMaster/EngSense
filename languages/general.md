# General Language-Aware Guidance

Status: **provisional**

Use this module before applying language-specific guidance when a decision may be distorted by patterns imported from another ecosystem.

## Principle

Do not evaluate a design independently of the target language/runtime.

A pattern that is useful in one ecosystem can create unnecessary indirection, allocation, runtime coupling, or ceremony in another.

## Questions

Before recommending a language-neutral pattern, ask:

- Does the language already provide a simpler native mechanism?
- Is the pattern compensating for a limitation that does not exist here?
- Does the runtime make the abstraction expensive?
- Does the type system already encode the invariant?
- Does the ecosystem have a strong idiom for this problem?
- Is the repository already consistent with that idiom?
- Is the proposed pattern helping a real boundary or only making the code look familiar?

## Prefer native semantic tools

Examples of native mechanisms include:

- algebraic/enumerated state modeling;
- structural typing;
- traits/protocols/interfaces;
- modules;
- iterators;
- pattern matching;
- ownership/borrowing;
- exceptions/results;
- async/await;
- decorators/attributes;
- data classes/records.

Do not add an additional design-pattern layer when a native language feature already expresses the required invariant clearly.

## Avoid pattern transplantation

Common failure modes:

- Java-style interface/factory/DI layers copied into Rust;
- inheritance-heavy models copied into TypeScript where unions/modules are clearer;
- enterprise service/repository/use-case stacks copied into simple Python CRUD;
- dynamic-language patterns copied into static systems without using the type system;
- synchronous-looking APIs layered over inherently asynchronous/distributed behavior.

## Language idiom vs repository convention

Language idiom is evidence, not absolute authority.

Repository consistency can outweigh a local idiom when:

- the difference is low-value;
- migration cost is high;
- tooling depends on the existing convention;
- mixed styles materially harm discoverability.

Language idiom can outweigh repository precedent when the existing pattern:

- creates correctness risk;
- defeats the language's safety model;
- causes substantial accidental complexity;
- was copied from another ecosystem without a real constraint.

## Generic decision rule

Prefer the design that:

- expresses invariants in the language's strongest appropriate mechanism;
- minimizes unnecessary runtime indirection;
- remains understandable to maintainers in that ecosystem;
- respects actual repository constraints;
- does not introduce abstraction merely to imitate another language's conventions.
