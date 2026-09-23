# Rust for Rustaceans — EngSense Research Notes

Source: *Rust for Rustaceans: Idiomatic Programming for Experienced Developers*  
Author: Jon Gjengset  
Publisher: No Starch Press  
Research basis: user-provided full-text PDF available in the EngSense research session

Research status: **IN PROGRESS — full-text study started**

This note intentionally separates:

- what the source argues;
- EngSense interpretation;
- candidate EngSense rules;
- failure modes and limits;
- tensions with general design advice;
- changes that may eventually replace provisional guidance in `languages/rust.md`.

No source is treated as absolute authority.

The copyrighted source text is not copied into this repository. These notes are original summaries and source references only.

---

## Progress

- [x] Foreword
- [x] Preface
- [x] Introduction
- [ ] Chapter 1 — Foundations
- [ ] Chapter 2 — Types
- [ ] Chapter 3 — Designing Interfaces
- [ ] Chapter 4 — Error Handling
- [ ] Chapter 5 — Project Structure
- [ ] Chapter 6 — Testing
- [ ] Chapter 7 — Macros
- [ ] Chapter 8 — Asynchronous Programming
- [ ] Chapter 9 — Unsafe Code
- [ ] Chapter 10 — Concurrency (and Parallelism)
- [ ] Chapter 11 — Foreign Function Interfaces
- [ ] Chapter 12 — Rust Without the Standard Library
- [ ] Chapter 13 — The Rust Ecosystem
- [ ] Index/reference cross-check

---

# Source scope

This is explicitly an intermediate-to-advanced Rust book rather than an introductory language manual.

The source assumes the reader already knows basic Rust and focuses on the gap between:

```text
knowing Rust syntax and basic concepts
!=
designing robust, ergonomic, idiomatic Rust systems
```

The book covers:

- memory, ownership, borrowing, and lifetimes;
- types, traits, layout, dispatch, and trait bounds;
- API/interface design;
- typed and opaque errors;
- crate/project structure;
- testing and linting;
- declarative and procedural macros;
- async/await, `Future`, `Pin`, waking, and task execution;
- unsafe Rust and validity;
- concurrency and atomics;
- FFI;
- `no_std` and low-level runtime concerns;
- ecosystem patterns and tooling.

## EngSense routing implication

This source should have high priority whenever generic code-quality advice collides with Rust-specific semantics.

It should not become a replacement for the core decision framework. It is a **language lens** that changes how general principles are implemented.

Candidate routing categories:

```text
rust.memory-model
rust.ownership-borrowing
rust.types-traits
rust.interface-design
rust.error-modeling
rust.project-structure
rust.testing
rust.macros
rust.async
rust.unsafe
rust.concurrency
rust.ffi
rust.no-std
rust.ecosystem
```

---

# Foreword / Preface / Introduction

## Source thesis

The opening material frames expert Rust development as a combination of:

- theory;
- mechanisms;
- idioms;
- trade-offs;
- practice;
- engineering taste.

The book does not present advanced Rust as a catalogue of features to use whenever possible.

A repeated theme is that understanding mechanisms enables better judgment about when **not** to use them.

The foreword explicitly treats nuance and trade-offs as part of the target skill level, and encourages readers to challenge even current guidance when experience produces a better result.

## EngSense interpretation

This aligns strongly with EngSense's central philosophy.

The Rust lens should not ask:

> Which Rust feature is most advanced or most idiomatic in isolation?

It should ask:

> Which Rust mechanism best expresses the actual ownership, capability, cost, safety, and evolution constraints here?

## Candidate rule

Prefer the Rust construct that makes the relevant contract visible with the least unnecessary semantic machinery.

Examples of costs that must remain visible:

- ownership transfer;
- borrowing/lifetime coupling;
- allocation;
- dynamic dispatch;
- synchronization;
- blocking;
- pinning;
- unsafe obligations;
- FFI invariants.

---

# Why this source matters more than generic OOP guidance in Rust

The book's chapter structure makes several Rust-specific design dimensions first-class:

- layout and representation;
- static vs dynamic dispatch;
- trait coherence;
- borrowed vs owned APIs;
- object safety;
- hidden contracts;
- typed error representation;
- async polling contracts;
- validity and unsafe boundaries;
- memory ordering;
- FFI type and allocation boundaries.

These concerns do not map cleanly onto Java-style class/interface heuristics.

## EngSense priority rule

When a general design lens recommends an abstraction that changes:

- ownership;
- lifetime relationships;
- dispatch;
- allocation;
- thread-safety;
- pinning;
- unsafe boundaries;
- representation guarantees;

load the Rust lens before finalizing the decision.

A general principle may still win, but it must survive the Rust-specific cost model.

---

# Existing provisional Rust module — validation targets

The current `languages/rust.md` is explicitly provisional.

This research should validate, revise, or delete its current claims rather than merely confirm them.

The main hypotheses to test against the full book are:

## Traits

Current provisional claim:

- traits should represent real capability/substitution boundaries;
- avoid interface-per-type architecture;
- choose static vs dynamic dispatch intentionally.

Research questions:

- how does the source distinguish generic traits from trait objects?
- when do ergonomic trait implementations improve APIs?
- what hidden compatibility contracts do public trait implementations create?
- how should coherence/orphan-rule constraints affect API boundaries?
- when does a wrapper type provide a better boundary than a trait?

---

## Ownership and borrowing

Current provisional claim:

- ownership is an architectural concern;
- unnecessary cloning and unnecessary lifetime complexity are both costs.

Research questions:

- what ownership/lifetime relationships should public APIs expose?
- when is borrowing beneficial versus constraining?
- when does interior mutability improve a design versus hide ownership?
- which ownership decisions affect concurrency and API stability?

---

## Error modeling

Current provisional claim:

- preserve typed distinctions when callers need different behavior;
- do not expose implementation details accidentally.

Research questions:

- when should errors be enumerated?
- when should they be opaque?
- how should library/application boundaries influence that choice?
- when does propagation preserve useful semantics versus leaking layers?

---

## Concurrency

Current provisional claim:

- concurrency correctness outranks readability cleanup;
- ownership, ordering, atomics, cancellation, backpressure, and shutdown semantics are invariants.

Research questions:

- how does the source separate concurrency from parallelism?
- when are shared memory, worker pools, or actors appropriate?
- what guidance does it give on atomics and memory ordering?
- what testing practices are recommended for concurrent code?

---

## Allocation and indirection

Current provisional claim:

- `Box`, `Arc`, trait objects, cloning, and heap allocation are trade-offs, not smells.

Research questions:

- how should layout and wide pointers affect abstraction review?
- when does dynamic dispatch buy meaningful flexibility?
- when does representation cost become part of API design?

---

# Initial conflict inventory

These conflicts should become explicit eval material after the relevant chapters are read in full.

## Dependency inversion vs trait cost

General advice may suggest:

```text
depend on abstraction
→ introduce trait
```

Rust may impose additional costs:

- generic propagation;
- monomorphization;
- object-safety restrictions;
- lifetime coupling;
- `dyn Trait` allocation/indirection;
- coherence constraints;
- larger public API commitment.

Expected EngSense behavior:

Do not introduce a trait merely to satisfy an abstract design slogan. Require a concrete capability or substitution benefit.

---

## Encapsulation vs type transparency

General advice may push toward hiding representation behind methods.

Rust may instead benefit from:

- plain structs;
- enums;
- exhaustive matching;
- newtypes/wrappers;
- public data where no invariant requires hiding it.

Research must determine where the source draws these lines rather than assuming an OOP default.

---

## "Small functions" vs ownership locality

Extracting a helper can improve naming but may also:

- expand lifetime parameters;
- force awkward borrowing;
- require cloning;
- scatter state transitions;
- obscure ownership flow.

Expected EngSense behavior:

Evaluate decomposition using Rust ownership/locality costs, not line count.

---

## Flexibility vs misuse resistance

Chapter 3 explicitly centers interface design around several dimensions, including being unsurprising, flexible, obvious, and constrained.

This is likely one of the most important source areas for EngSense.

The tension to preserve:

```text
more flexible API
vs
smaller valid state space / harder misuse
```

Do not assume maximum generic flexibility is always superior.

---

## Abstraction vs hidden contracts

Public traits, type behavior, destructors, error types, and other interface details may create compatibility promises even when not documented as such.

This should later be compared with EngSense's existing evolution/compatibility lens and Hyrum's Law material from *Software Engineering at Google*.

---

# Candidate evals from the opening pass

## Eval: Java-style service abstraction in Rust

Context:

A Rust module has one concrete implementation. A reviewer proposes:

```text
trait Service
ServiceImpl
ServiceFactory
Box<dyn Service>
```

with no runtime substitution requirement.

Expected EngSense behavior:

- challenge the abstraction;
- identify dispatch/allocation/API costs;
- prefer the concrete implementation unless a real capability boundary exists;
- define a revisit trigger such as a second implementation or plugin/provider boundary.

---

## Eval: split function causes borrow complexity

Context:

A cohesive function owns mutable state and performs a short state transition. Splitting it into helpers requires extra lifetime parameters or cloning.

Expected EngSense behavior:

- do not split by function length alone;
- compare readability benefit against ownership complexity;
- keep the cohesive unit together when extraction does not reveal a real abstraction.

---

## Eval: error enum vs opaque error

Context:

A library has several failures, but callers can recover differently from only two of them.

Expected EngSense behavior:

- route to the Rust error-modeling lens;
- preserve actionable distinctions;
- avoid exposing every internal failure as permanent public API;
- evaluate enumerated versus opaque boundaries contextually.

---

## Eval: trait-object flexibility is not free

Context:

An API returns `Box<dyn Trait>` because "we may have more implementations later."

Expected EngSense behavior:

- identify whether runtime heterogeneity actually exists;
- compare a concrete type, generic parameter, enum, and trait object;
- make dispatch, allocation, object-safety, and compatibility trade-offs explicit.

---

# Research integrity notes

- Full-source completion is not claimed yet.
- Current findings come only from the fully reviewed opening material and the source's explicit chapter structure.
- Existing `languages/rust.md` remains provisional.
- No claim should be attributed to Gjengset unless the completed chapter supports it.
- The final Rust lens must be cross-checked against the complete source, not only familiar Rust conventions.
- The source's guidance should be allowed to contradict current EngSense assumptions.

---

# Next research pass

Continue in source order:

1. Chapter 1 — Foundations
2. Chapter 2 — Types
3. Chapter 3 — Designing Interfaces
4. Chapter 4 — Error Handling

These chapters should establish the core language/design model before EngSense changes `languages/rust.md`.

Do not mark the mandatory Rust source complete or finalize Rust-specific evals until all 13 chapters have been reviewed.
