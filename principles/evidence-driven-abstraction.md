# Evidence-Driven Abstraction Lens

Source basis: completed Google SWE and AOSA Volume 1 research plus EngSense synthesis.

## Question this lens answers

> Is this abstraction protecting a real boundary/invariant, or only anticipating hypothetical reuse?

## Positive evidence

An abstraction is more justified when it represents one or more of:

- multiple real implementations;
- stable repeated behavior;
- independently varying concern;
- external/provider/platform boundary;
- public capability contract;
- repeated invariant;
- volatile dependency;
- combinatorial duplication;
- stable intermediate representation;
- reusable execution policy;
- focused testability.

## Negative evidence

Challenge the abstraction when:

- one implementation exists;
- no caller requires substitution;
- the interface mirrors concrete methods one-for-one;
- a factory always returns one type;
- the abstraction needs mode flags to represent divergent concepts;
- consumers still reach through it for implementation details;
- it exists mainly to satisfy a mocking framework;
- hypothetical future reuse is the only justification.

## Stable variation axes

Strong abstractions often form around real dimensions of change:

- protocol;
- platform;
- storage engine;
- provider;
- renderer;
- language binding;
- capability;
- ruleset.

Do not create abstractions around arbitrary nouns merely because they exist in the domain.

## Representation as abstraction

A representation can be a powerful boundary when it is self-contained.

Examples of useful properties:

- producers/consumers can evolve independently;
- focused tests are possible;
- replay/audit becomes possible;
- transformation/tooling can operate without hidden context.

A boundary is weak if downstream code must reach behind it to recover missing semantics.

## Extensibility power

Use the least powerful extension mechanism that meets the need.

Rough spectrum:

```text
configuration
→ bounded callback/interface
→ plugin module
→ process boundary
→ arbitrary runtime patching
```

More power generally increases compatibility, security, and reasoning cost.

## Escape hatches

A strong abstraction may still need a bounded escape hatch.

Accept one when:

- a real capability cannot be expressed otherwise;
- measured performance requires it;
- platform/protocol semantics require it;
- compatibility migration requires it.

Keep it explicit, narrow, observable, and owned.

## Revisit triggers

A concrete design may deserve abstraction when:

- the second real implementation appears;
- duplicated changes start moving together;
- a stable invariant repeats;
- an external boundary appears;
- maintenance cost becomes multiplicative.

An abstraction may deserve removal when:

- variation disappeared;
- every implementation became identical;
- users constantly bypass it;
- it adds more concepts than it protects.

## Anti-rules

Do not abstract because:

- "we may need it someday";
- a design pattern exists;
- interfaces look cleaner;
- tests are easier to mock;
- two code blocks happen to look similar.
