# EngSense Routing Map

Use this reference only when it is unclear which module should own the decision.

The goal is **minimal sufficient loading**. EngSense is a Skill, not an orchestration runtime: this file helps the active model choose the smallest useful set of static guidance.

## Routing rule

Start from the task's dominant engineering question.

Normally load:

```text
SKILL.md
+ decision-framework.md
+ language module when language semantics matter
+ domain module when domain semantics matter
+ one primary principle lens
+ one supporting lens only when a real second trade-off exists
+ conflicts.md only when valid principles pull in opposite directions
```

Do not load every lens because several could be relevant in theory.

A lens is justified when ignoring it could materially change the decision.

---

## Principle ownership

| Dominant question | Primary lens | Do not load merely because |
|---|---|---|
| Is local code understandable and safely changeable? | `principles/clean-code.md` | code exists or a function is long |
| Will this remain workable over lifetime/scale/organization change? | `principles/sustainable-engineering.md` | the project is expected to live for some time |
| Does the architecture fit real workload/product/ecosystem constraints? | `principles/empirical-architecture.md` | an architecture diagram exists |
| Was complexity removed or displaced to callers/ops/migration? | `principles/complexity-placement.md` | the design has several components |
| How much compatibility/change freedom should be preserved? | `principles/evolution-and-compatibility.md` | any refactor changes internal code |
| Is an abstraction justified by a real boundary/invariant? | `principles/evidence-driven-abstraction.md` | an interface/trait/class is present |
| Is a measured performance change justified? | `principles/performance-engineering.md` | code could theoretically be faster |
| Should we leave, refactor, migrate, coordinate, or replace? | `principles/change-strategy.md` | any cleanup is requested |
| Does the representation encode the right relationships/invariants? | `principles/representation-design.md` | data structures exist |
| Is reliability/operability the dominant production risk? | `principles/reliability-operability.md` | code runs in production |

---

## Domain ownership

| Semantic boundary | Domain module | Load when |
|---|---|---|
| Public/shared/remote/persisted contract | `domains/api-design.md` | compatibility, capability surface, versioning, migration, remote granularity |
| Business/domain invariants | `domains/domain-modeling.md` | state transitions, invariant ownership, domain policy, lifecycle semantics |
| Test strategy/fidelity | `domains/testing.md` | the decision depends on which evidence/test level is trustworthy |
| Concurrency lifecycle/ordering | `domains/concurrency.md` | tasks, threads, queues, cancellation, shutdown, backpressure |
| Persisted state | `domains/persistence.md` | transactions, durability, schema migration, replay, persisted compatibility |
| Remote/distributed semantics | `domains/distributed-systems.md` | partial failure, timeout ambiguity, retries/dedup, version skew, consistency, delivery semantics |

Domain modules can be co-loaded when boundaries genuinely intersect.

Examples:

```text
domain invariant + transaction
→ domain-modeling + persistence

background task + shutdown
→ concurrency

remote worker + at-least-once delivery + domain transition
→ domain-modeling + concurrency + distributed-systems

public protocol migration
→ api-design + evolution-and-compatibility
```

Do not turn co-loading into a fixed stack.

---

## Language precedence

Load a language module when the implementation mechanism can change the engineering decision.

Examples:

- Rust ownership, traits, lifetimes, async, unsafe, FFI → `languages/rust.md`
- TypeScript unions/structural typing/runtime boundaries → `languages/typescript.md`
- Python dynamic data modeling/simple module structure → `languages/python.md`

Use `languages/general.md` when checking whether a pattern is being transplanted from another ecosystem.

### Precedence rule

When a source-specific lens recommends a mechanism that is unnatural in the target language:

```text
preserve the engineering goal
→ choose the idiomatic language mechanism
```

Do not preserve the book's mechanism merely to preserve the book's terminology.

For example, a Clean Code dependency-boundary goal in Rust may use:

- concrete types;
- generics;
- traits;
- enums;
- modules;
- closures;

depending on the actual variation and ownership model.

---

## Overlap resolution

Some lenses intentionally overlap. Choose the primary lens from the question being decided.

### Clean Code vs Complexity Placement

Use Clean Code when the question is local comprehension/changeability.

Use Complexity Placement when local simplification may move burden into:

- callers;
- operations;
- migration;
- support;
- compatibility.

### Sustainable Engineering vs Evolution/Compatibility

Use Sustainable Engineering when the dominant concern is long-term human/system scalability.

Use Evolution/Compatibility when an existing observable surface constrains a specific change.

They can be combined for long-lived public APIs.

### Evidence-Driven Abstraction vs Representation Design

Use Evidence-Driven Abstraction for interface/provider/reuse boundaries.

Use Representation Design when the core decision is the shape of data/state/relationships.

Do not create an interface to compensate for a poor representation without considering the representation directly.

### Change Strategy vs Evolution/Compatibility

Use Change Strategy to choose **how to move** from current to target.

Use Evolution/Compatibility to determine **what must remain compatible during that move**.

Large migrations may need both.

### Performance vs Reliability/Operability

Use Performance Engineering when a measured metric/resource bottleneck drives the change.

Use Reliability/Operability when overload, recovery, availability, alerting, or operational burden dominates.

Do not optimize throughput in a way that silently weakens overload safety.

### Domain Modeling vs Representation Design

Use Domain Modeling when business meaning/invariant ownership is central.

Use Representation Design when data shape/state encoding is central.

A state machine may need both only if its business semantics and representation are independently difficult.

### Concurrency vs Distributed Systems

Concurrency does not imply distribution.

Use Distributed Systems only when a remote/process/broker boundary introduces its distinct failure/delivery semantics.

An in-memory local queue usually needs concurrency/lifecycle review, not retry/deduplication machinery.

---

## Source-specific lens gate

A source-specific lens can only be loaded if its repository research gate is complete.

Currently available source-specific coverage includes:

- `principles/clean-code.md`;
- research-grounded Rust guidance in `languages/rust.md`.

Do not invent source-specific Ousterhout, Fowler, Evans/DDD, DDIA, Nygard, McConnell, Feathers, or other blocked guidance from general model knowledge.

Use neutral EngSense principle/domain modules until that source's research is complete.

---

## Stop-loading test

Before adding another module, ask:

> What concrete decision could change if I load this module?

If no answer is available from the task/repository evidence, do not load it.

Before finalizing, ask:

> Did I load a lens because its question matters, or because its vocabulary appears in the code?

Prefer the former.
