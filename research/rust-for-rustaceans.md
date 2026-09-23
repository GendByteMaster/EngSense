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
- [x] Chapter 1 — Foundations
- [x] Chapter 2 — Types
- [x] Chapter 3 — Designing Interfaces
- [x] Chapter 4 — Error Handling
- [x] Chapter 5 — Project Structure
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

# Chapter 1 — Foundations

## Source thesis

The chapter builds two complementary mental models for Rust:

- a high-level **value/data-flow** model for ownership, borrowing, and lifetimes;
- a low-level **memory/place** model for raw memory and unsafe reasoning.

The source treats both as useful simplifications rather than one universally correct way to think.

## Ownership is design, not syntax

Rust assigns every value an owner, and moving a value transfers that responsibility.

For EngSense this means ownership choices affect:

- lifetime of resources;
- who may mutate;
- whether data can cross threads/tasks;
- whether APIs require allocation or cloning;
- how cleanup occurs.

A refactor that changes ownership is therefore not cosmetic.

## Borrowing is controlled aliasing

Shared and mutable references represent different access guarantees.

The important source-level idea is that Rust's compiler reasons about **flows of access**, not simply variable scopes.

### EngSense extraction

When a proposed abstraction creates difficult borrow-checker interactions, inspect the design before mechanically adding:

- clones;
- `Arc`;
- `Mutex`;
- extra lifetime parameters;
- unsafe code.

The compiler error may be evidence that ownership boundaries are unclear.

Conversely, a small intentional clone of cheap data may be the simpler and safer design when borrowing would spread lifetime coupling across an API.

## Lifetimes are not lexical scopes

The chapter's examples emphasize that a lifetime follows actual use/flow and can end before lexical scope ends.

This matters for review because "reference is still in scope" is not sufficient reasoning about borrow validity.

## Lifetime parameter count is a complexity trade-off

The source explicitly says multiple lifetime parameters should be introduced when they preserve semantically distinct relationships, but not merely because the language permits them.

Candidate EngSense rule:

> Encode independent lifetime relationships only when callers benefit from the distinction; otherwise avoid unnecessary generic lifetime complexity.

## Variance matters at advanced boundaries

Covariance, invariance, and contravariance affect whether lifetimes/types can be safely substituted.

The source recommends weighing:

- ergonomic cost of invariance;
- cognitive cost of additional lifetime parameters.

EngSense should not invent variance findings for ordinary code. Route this only when generic/reference API behavior actually depends on it.

---

# Chapter 2 — Types

## Layout and representation are contracts only when promised

Rust's default representation deliberately gives the compiler freedom to optimize layout.

Explicit representations such as `repr(C)`, `repr(transparent)`, packing, or alignment establish stronger representation constraints.

### EngSense extraction

Do not rely on layout accidentally.

Treat representation as a public/unsafe/FFI contract only when:

- the language attribute promises it;
- external ABI/data format relies on it;
- unsafe code requires it;
- persisted/network bytes intentionally use it.

A performance refactor that changes representation is not necessarily behavior-neutral in these contexts.

## Static vs dynamic dispatch is a trade-off

The source explains both mechanisms rather than ranking one universally.

Static dispatch / monomorphization can provide:

- specialization and inlining;
- no virtual dispatch cost;

but may increase:

- compile time;
- binary size;
- instruction-cache pressure.

Dynamic dispatch can reduce code duplication and compile pressure, but limits optimization and adds runtime indirection.

### EngSense rule

Choose dispatch from actual requirements:

~~~text
compile-time generic capability
→ static dispatch is often natural

runtime heterogeneity / erased concrete type
→ dynamic dispatch may be justified
~~~

Do not flag `dyn Trait` merely for existing, and do not introduce it solely because "interfaces are cleaner."

## Generic traits vs associated types

The source presents a real design trade:

- generic trait parameters permit multiple implementations for different type arguments;
- associated types simplify use and create one associated mapping per implementation.

EngSense should ask whether multiple relationships per implementing type are actually required.

## Coherence/orphan rule constrains API evolution

Trait extensibility is not symmetric in Rust.

Who owns the trait and who owns the type determines what downstream/upstream code can legally implement.

This means interface design cannot be copied from languages where extension is unrestricted.

## Marker traits and typestate

Marker traits can encode semantic properties such as thread safety without runtime methods.

Marker types can encode states such as authenticated/unauthenticated so invalid operations are unavailable at compile time.

### EngSense qualification

Use typestate when it materially eliminates invalid transitions or security/safety misuse.

Do not encode every ordinary boolean state as a generic type parameter if runtime state is simpler and sufficiently safe.

## `impl Trait` can hide implementation at zero runtime cost

Existential return types let an API promise capabilities without exposing the concrete type.

This can reduce public compatibility surface while retaining static dispatch.

However, hidden auto-traits such as `Send`/`Sync` may still be observable contracts.

---

# Chapter 3 — Designing Interfaces

## Four source principles

The chapter's explicit interface criteria are:

- **unsurprising**;
- **flexible**;
- **obvious**;
- **constrained**.

These principles can conflict, so EngSense should use them as lenses rather than a checklist score.

## Unsurprising means ecosystem-consistent semantics

Rust users infer behavior from conventional names and standard traits.

A familiar name with unfamiliar semantics creates more friction than a novel but precise name.

The source also encourages common trait implementations where their semantics genuinely hold.

### Important exception: `Copy`

The source treats `Copy` as a stronger public commitment because it changes move semantics and may become impossible to preserve as the type evolves.

EngSense should therefore distinguish:

~~~text
ergonomic trait implementation
from
semantic commitment that constrains future representation
~~~

## Interface contracts = requirements + promises

This is one of the strongest EngSense ideas in the book.

Arguments/bounds impose requirements on callers.

Return types/trait implementations/documented behavior make promises.

Good API design avoids:

- unnecessary requirements;
- promises the implementation may later regret.

### Candidate decision model

~~~text
caller flexibility
+ implementation evolution
+ semantic clarity
-
generic complexity
- compatibility commitment
- runtime/compile cost
~~~

## Generic inputs are not always better

The source explicitly warns against making every parameter generic.

Use generics when callers reasonably and frequently need multiple compatible input types.

Do not genericize merely for theoretical flexibility.

Changing a concrete argument to a generic one can itself break inference-dependent callers, so "more flexible" does not automatically mean backward compatible.

## Object safety is part of the public contract

A trait that is object-safe enables runtime trait objects; losing object safety can be a breaking change.

The source says there is **no single answer** for how much ergonomics should be sacrificed to preserve object safety.

EngSense should base this on likely usage.

## Borrowed vs owned APIs

Source guidance:

- if implementation needs ownership, usually require ownership explicitly rather than borrowing and cloning internally;
- if ownership is not needed, prefer borrowing;
- cheap small values may be copied directly;
- when lifetime complexity makes an interface painful, intentionally owning/cloning cheap data can be a better API.

This directly supports a contextual, not zero-copy-at-all-costs, Rust lens.

## Fallible/blocking destruction

`Drop` cannot cleanly report errors or await async cleanup.

The source recommends best-effort `Drop` plus an explicit consuming cleanup API when callers need reliable completion.

EngSense extraction:

Resource-lifecycle APIs must make failure/asynchrony visible when ignoring it could matter.

Do not rely on destructors to communicate guarantees they cannot express.

## Make misuse obvious and difficult

Use:

- types;
- names;
- documentation;
- module organization;
- examples;

to communicate contracts.

Rust-specific docs should explicitly surface:

- panic conditions;
- error conditions;
- unsafe caller obligations;
- important lifecycle requirements.

This is a useful counterweight to an oversimplified "comments are failures" reading of Clean Code.

## Public API evolution has hidden contracts

The source identifies several non-obvious compatibility surfaces:

- public struct construction/pattern matching;
- object safety;
- trait implementations;
- re-exported foreign types;
- `Send`/`Sync`/other auto-traits;
- downstream coherence interactions.

### EngSense rule

When reviewing public Rust API changes, do not inspect signatures alone.

Check compile-time behavior that downstream code may rely on.

## `#[non_exhaustive]` and sealed traits are trade-offs

They preserve future evolution by restricting what downstream callers/implementers may do today.

Use them when extension uncertainty is material.

Do not add them mechanically to every public type/trait.

---

# Chapter 4 — Error Handling

## Source thesis

The book explicitly says Rust error-handling practice was still evolving and therefore focuses on principles rather than one blessed crate/pattern.

The central question is:

> Does the caller need to distinguish failure categories in order to behave differently?

## Enumerated errors

Use distinct variants when callers have actionable recovery/handling differences.

Examples of useful distinctions include different sources of failure that require different responses.

## Opaque/erased errors

Use opaque representation when the caller can only:

- report;
- log;
- propagate;
- abort the operation;

and fine-grained categories would enlarge the public API without useful behavior.

### EngSense rule

Expose **actionable semantics**, not maximum internal detail.

## Error types are API commitments

Concrete error variants become downstream matchable contract surface.

Type-erased errors preserve more implementation freedom but reduce caller introspection.

Downcasting can create an informal hidden dependency if users rely on undocumented concrete types behind an erased error.

EngSense should flag such hidden contract reliance when public stability matters.

## Failure is not absence

The source explicitly distinguishes:

- `Result<T, E>` / `Result<T, ()>` — operation failed and deserves failure handling;
- `Option<T>` — value may simply be absent.

Do not simplify one into the other merely because both can encode two states.

## Rust overrides exception-centric general advice

The book treats `Result`, `?`, typed errors, erasure, and propagation as idiomatic mechanisms.

Therefore Clean Code's language-specific "prefer exceptions to error codes" recommendation does not become "panic/throw instead of Result" in Rust.

## Cleanup and early return

The source highlights how `?` can bypass later cleanup if lifecycle is manually sequenced.

EngSense should inspect whether resources rely on:

- RAII/`Drop`;
- explicit cleanup;
- transaction guards;
- scope guards;
- async teardown.

The happy path must not silently skip required cleanup on error paths.

---

# Chapter 5 — Project Structure

## Feature flags are composition contracts

The source strongly prefers **additive features**.

Cargo unifies features across dependents, so mutually exclusive features can create dependency-graph breakage.

### EngSense rule

For reusable crates, a healthy default invariant is:

~~~text
if individual feature sets compile,
their union should also compile
~~~

unless the crate explicitly documents a different architecture and accepts the ecosystem cost.

Feature-combination CI is valuable when the feature surface is material.

## Project structure should respond to actual scale

The chapter frames workspaces/subcrates/configuration as tools that become useful when project growth creates concrete needs such as:

- compile-time pressure;
- conditional dependencies;
- CI complexity;
- organizational separation.

This supports EngSense's anti-rule:

> Do not split crates merely to look modular.

A crate boundary has build, dependency, versioning, and API consequences.

## Build profiles encode explicit trade-offs

Optimization, codegen units, LTO, debug assertions, and overflow checks trade:

- compile time;
- binary size;
- runtime performance;
- diagnostic power.

EngSense should not recommend "maximum optimization" or "fastest compile" without workload context.

## Panic strategy is a system decision

Unwinding allows cleanup and may isolate a panic to one thread, but can leave shared state partially updated and requires recovery semantics.

Abort gives a stronger whole-process fail-stop behavior but skips cleanup.

The correct policy depends on:

- state consistency;
- platform capability;
- recovery model;
- observability;
- embedded/system constraints.

## Conditional compilation is part of supported-platform complexity

`cfg` is legitimate for platform, architecture, compiler, test, and tool differences.

But every conditional dimension adds a configuration state that may require validation.

EngSense should ask whether CI actually covers the supported combinations that matter.

## Dependency health belongs to project quality

The source recommends automated dependency auditing.

EngSense should route actual vulnerability/license policy to security/compliance tooling, but it can identify missing automated dependency hygiene as an operability/maintenance concern when relevant.

## MSRV is a compatibility policy, not a universal number

The source explicitly says there is no perfect MSRV strategy.

Supporting older compilers can help downstream consumers but may delay language/library/security/performance updates.

Candidate EngSense context:

~~~text
consumer_constraints
release_policy
security_update_pressure
language_feature_value
maintenance_cost
~~~

## Dependency version floors are promises

For libraries, declaring the newest dependency version when older ones would work can unnecessarily constrain downstream resolution.

Conversely, declaring a too-low floor that does not actually build creates a false compatibility promise.

## Changelog/versioning guidance is consumer-oriented

The durable principle is to make compatibility/release changes discoverable and machine/user interpretable.

The exact prerelease version workflow in the book is one practical recommendation, not an EngSense requirement.

---

# Cross-source conflicts established by Chapters 1–5

## Clean Code DIP vs Rust traits

Generic Clean Code pressure:

~~~text
depend on abstractions
→ interface
~~~

Rust-specific questions now required:

- Is runtime substitution needed?
- Would a generic parameter be clearer?
- Would `impl Trait` hide concrete representation without dynamic dispatch?
- Would an enum better represent a closed set?
- Does a public trait create coherence/object-safety/semver commitments?
- Does `dyn Trait` impose runtime/optimization constraints that matter?

Conclusion:

> "Use an abstraction" does not mechanically mean "introduce a trait object."

## Small-function extraction vs ownership locality

An extraction that looks cleaner structurally may force:

- longer borrow relationships;
- extra clones;
- additional generic lifetimes;
- interior mutability;
- `Arc<Mutex<_>>`;
- ownership transfer merely to satisfy helper boundaries.

Rust ownership cost must be part of the decomposition trade-off.

## Clean Code comments skepticism vs Rust public contracts

Rust interfaces may require documentation for behavior the type system cannot enforce, especially:

- panic conditions;
- error behavior;
- unsafe preconditions;
- lifecycle/cleanup semantics.

Therefore "remove comments by making code self-documenting" has a hard limit at API contracts.

## Generic flexibility vs simplicity

Rust makes powerful generic interfaces possible, but the source explicitly warns that maximal genericity can damage readability and may create compile/binary costs.

EngSense should not reward generic abstraction merely because it is zero-cost at runtime.

## Hidden implementation vs hidden compatibility contracts

Even when concrete types are hidden, public behavior may expose:

- auto-traits;
- object safety;
- trait impls;
- downstream inference;
- foreign type identity.

Rust API review must include these compile-time contracts.

---

# Additional eval candidates from Chapters 1–5

## Eval: borrow complexity introduced by cleanup

Context:

A readability refactor splits a cohesive state transition into helpers, forcing cloned values and a new `Arc<Mutex<_>>` solely to satisfy ownership across helper boundaries.

Expected:

- reject the refactor unless the new boundaries have independent semantic value;
- preserve simpler ownership/locality;
- do not "fix" borrow checker friction by adding synchronization without a concurrency requirement.

## Eval: generic API overreach

Context:

A public function accepts one common concrete input in all known consumers. A proposed rewrite gives every parameter a separate generic type and trait bounds.

Expected:

- ask whether callers realistically need alternate input types;
- consider readability, inference, monomorphization, compile time, and semver effects;
- keep concrete API when genericity has no user value.

## Eval: public trait gains method

Context:

A public unsealed trait implemented downstream needs a new required method.

Expected:

- recognize this as a breaking API change;
- consider default method, new trait/version, or sealed design only if semantics support it;
- do not treat source compatibility as internal implementation detail.

## Eval: hidden Send contract regression

Context:

A private implementation field changes from `Arc<T>` to `Rc<T>`, causing the public type to stop implementing `Send`.

Expected:

- detect hidden public compatibility break;
- add compile-time contract test if Send is intended;
- do not dismiss because the field is private.

## Eval: Result vs Option

Context:

A parser currently returns `Result<T, ParseFailure>`. A cleanup proposes `Option<T>` because the caller only checks success today.

Expected:

- preserve failure-vs-absence semantics unless the domain truly says failure carries no exceptional meaning;
- consider future/error reporting contract;
- do not optimize only for type brevity.

## Eval: feature union failure

Context:

Crate features `sqlite` and `postgres` compile separately but enabling both makes the crate fail.

Expected:

- identify conflict with Cargo feature unification/composability;
- prefer additive feature design or an explicit higher-level backend selection mechanism;
- add feature-combination CI when these are public features.

## Eval: MSRV pressure

Context:

A library supports enterprise consumers on an older Rust release; a new convenience API requires the newest compiler but brings little maintenance benefit.

Expected:

- treat MSRV as a compatibility trade-off;
- compare downstream breakage with actual feature value;
- avoid universal "always latest Rust" guidance.

# Research integrity notes

- Full-source completion is not claimed yet.
- Current findings come only from the fully reviewed opening material and the source's explicit chapter structure.
- Existing `languages/rust.md` remains provisional.
- No claim should be attributed to Gjengset unless the completed chapter supports it.
- The final Rust lens must be cross-checked against the complete source, not only familiar Rust conventions.
- The source's guidance should be allowed to contradict current EngSense assumptions.

---

# Next research pass

Chapters 1–5 are complete.

Continue in source order:

1. Chapter 6 — Testing
2. Chapter 7 — Macros
3. Chapter 8 — Asynchronous Programming
4. Chapter 9 — Unsafe Code
5. Chapter 10 — Concurrency (and Parallelism)

Then continue through FFI, `no_std`, and ecosystem guidance before revising `languages/rust.md`.

Do not mark the mandatory Rust source complete or finalize Rust-specific evals until all 13 chapters have been reviewed.
