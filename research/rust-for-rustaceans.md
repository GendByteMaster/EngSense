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
- [x] Chapter 6 — Testing
- [x] Chapter 7 — Macros
- [x] Chapter 8 — Asynchronous Programming
- [x] Chapter 9 — Unsafe Code
- [x] Chapter 10 — Concurrency (and Parallelism)
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

# Chapter 6 — Testing

## Source thesis

The chapter treats testing as a layered evidence system rather than only a collection of `#[test]` functions.

It covers:

- the standard Rust test harness;
- unit versus integration-test compilation boundaries;
- `#[cfg(test)]` instrumentation;
- doctests as executable public examples;
- linting;
- fuzzing and property-based testing;
- Miri and Loom as test augmentation;
- performance testing.

## Unit and integration tests exercise different contracts

Unit tests can see private implementation details within their module/crate context, while integration tests under `tests/` compile as separate crates and therefore exercise the public interface.

### EngSense extraction

Do not ask one test layer to prove every property.

Use the narrowest evidence surface that matches the contract:

```text
private implementation invariant
→ unit/internal test

public crate contract
→ integration test

documented usage
→ doctest/example

compile-time negative contract
→ compile_fail / compile-time test
```

The existence of internal tests does not replace evidence at the public boundary.

## Test-only observability can be legitimate

The source shows `#[cfg(test)]` being used for:

- read-only test accessors;
- bookkeeping/counters;
- additional instrumentation.

This is a useful alternative to weakening production encapsulation just to make tests inspect internal state.

### Qualification

Test-only APIs should support meaningful invariants, not make tests mirror every implementation detail. If tests become coupled to incidental representation, refactoring cost rises.

## Doctests are contract tests for examples

Doctests are compiled like external use, which makes them valuable for validating that documentation examples remain real.

The source also warns that hidden lines can make examples misleading if copied code no longer works without invisible setup.

### EngSense rule

Documentation examples should optimize for truthful user experience, not merely short snippets.

## Testing technique should match the failure shape

The chapter distinguishes several tools:

- fuzzing for broad input-space exploration;
- property-based testing for semantic properties and differential comparison;
- Miri for runtime detection of certain Rust-specific undefined behavior;
- Loom for systematic exploration of concurrent interleavings;
- benchmarks/performance tests for regressions in non-functional behavior.

EngSense should therefore avoid the generic recommendation:

```text
add more unit tests
```

when the relevant defect class requires a different testing mechanism.

## Performance tests are noisy measurements

The source stresses:

- benchmark variance;
- compiler optimization eliminating the work being measured;
- accidental measurement of I/O/setup/random generation rather than the target operation.

### EngSense extraction

A benchmark is evidence only if its measurement boundary is credible.

Review:

- workload realism;
- warmup/repetition;
- distribution rather than one number;
- optimization artifacts;
- environmental noise;
- setup/I/O contamination.

This aligns with EngSense's existing performance-engineering lens.

---

# Chapter 7 — Macros

## Source thesis

Rust macros are legitimate language mechanisms, but the source consistently treats them as a trade-off rather than a sophistication badge.

## Declarative macros

`macro_rules!` is strongest for regular, mechanical repetition where ordinary functions/generics cannot express the source-level transformation.

The source gives a particularly strong rule of thumb:

```text
variation by type
→ prefer generics

source/code-shape repetition
→ macro may fit
```

### EngSense extraction

Before introducing a macro, ask whether the problem is actually:

- runtime behavior → function;
- type-level polymorphism → generics/traits;
- repetitive source structure → macro;
- complex compile-time parsing/transformation → procedural macro.

This prevents macros from becoming accidental abstraction machinery.

## Procedural macros have hidden project cost

The chapter calls out:

- heavy compile-time dependencies;
- code-generation volume;
- maintenance/debugging complexity;
- weaker hygiene than declarative macros.

A macro can reduce author typing while increasing compiler and maintainer work.

### Candidate rule

Do not evaluate code generation by source-line reduction alone.

Include:

```text
generated_code_volume
compile_time
diagnostic_quality
discoverability
IDE/tooling behavior
maintenance complexity
public DSL commitment
```

## Derives should match intuition

The source recommends derive macros when:

- the trait is implemented often;
- the derived implementation is obvious/predictable.

If the generated semantics are surprising, automation becomes a hidden policy.

## Attribute macros are justified by real leverage

Useful source cases include:

- test generation;
- framework annotations;
- transparent instrumentation;
- type transformation with safety checks.

EngSense should distinguish such leverage from decorative metaprogramming.

## Diagnostics are part of macro API quality

Spans and `compile_error!` allow generated-code errors to point back to user-authored source.

### EngSense rule

For public macros, diagnostics and failure locality are part of interface quality, not polish added after functionality.

---

# Chapter 8 — Asynchronous Programming

## Source thesis

The chapter explicitly warns that asynchronous design is not always the right solution.

The central trade-off is between:

- simple blocking/synchronous flow;
- threads with blocking APIs;
- futures/tasks multiplexed by an executor.

Async primarily helps when work spends substantial time waiting and many operations need to make progress concurrently.

## Async is not synonymous with parallelism

The source distinguishes:

- concurrency — multiple operations can make progress in an interleaved fashion;
- parallelism — operations execute simultaneously.

A single executor thread can run many futures concurrently without parallelism.

Parallel async execution requires explicit task boundaries and `Send` where work may move across threads.

### EngSense rule

Never justify async with the vague claim "it is faster."

Ask instead:

- Is the workload I/O/wait dominated?
- How many concurrent waits exist?
- Is thread-per-task cost material?
- Is parallel CPU execution required?
- What executor/runtime constraints are introduced?

## Async state machines move complexity rather than erase it

`async/await` makes code readable by letting the compiler generate the state machine that manual `Future` implementations would otherwise require.

This is a strong example of useful abstraction: substantial mechanical complexity is hidden behind a stable semantic model.

But the underlying contracts still matter for advanced code:

- polling;
- pinning;
- wakeups;
- executor ownership;
- task boundaries.

## Executor/runtime coupling is an architectural constraint

Leaf futures may integrate with a specific reactor/executor for timers, network, and file events.

A library that appears runtime-neutral at the syntax level can still be coupled through its resource/future types.

### EngSense extraction

When reviewing reusable async libraries, inspect runtime coupling explicitly rather than assuming `Future` alone guarantees portability.

## Blocking inside async is a scheduler-level defect

A blocking syscall, compute-heavy loop, or long section without yielding can stall unrelated tasks assigned to the same executor thread.

The source recommends moving such work to dedicated blocking/compute threads or otherwise yielding appropriately.

### Candidate rule

In async code, "does this call block?" is part of API correctness/performance, not merely an implementation detail.

## Spawning changes lifecycle and concurrency semantics

Spawning a future makes it an independently scheduled task.

That can enable concurrency/parallelism, but it also introduces lifecycle questions:

- who owns task completion?
- what happens if the executor stops?
- how are errors observed?
- can the task outlive caller state?
- is detached work intentional?

EngSense should not recommend `spawn` merely to avoid awaiting.

---

# Chapter 9 — Unsafe Code

## Source thesis

The chapter's central framing is precise:

> unsafe is a mechanism for manually upholding invariants the compiler cannot prove.

It is not a permission to ignore Rust's rules.

## `unsafe fn` and `unsafe {}` represent different responsibilities

The source distinguishes:

- `unsafe fn` — caller must uphold documented preconditions;
- `unsafe {}` — implementation author asserts that required invariants have been checked for the enclosed operations.

### EngSense extraction

An unsafe boundary is a contract boundary.

Review must identify:

```text
caller obligations
implementation proof
privacy boundary
failure/UB consequence
verification mechanism
```

## Safe wrappers are a primary design goal

The source repeatedly demonstrates unsafe internals exposed through safe APIs when the module can enforce all necessary invariants itself.

### Candidate rule

Prefer:

```text
small auditable unsafe core
→ safe narrow interface
```

over spreading unsafe obligations across callers.

But do not mark an API safe if its correctness still relies on undocumented caller behavior.

## Unsafe optimization requires evidence

Unchecked operations are sometimes available to remove runtime checks, but the source explicitly recommends measuring first because the safety/performance trade is rarely worthwhile by default.

EngSense should reject "unsafe for speed" without benchmark evidence tied to a real bottleneck.

## Validity is stronger than "I never read the bad value"

References and many Rust types must be valid whenever they exist, not only when later dereferenced/used.

Unsafe review must therefore reason about:

- alignment;
- lifetime/liveness;
- aliasing;
- valid bit patterns;
- initialization;
- ownership;
- layout guarantees.

## Panics and early returns are part of unsafe correctness

Unwinding can expose partially initialized or inconsistent states.

The source also calls out `?` as another early-exit path that can bypass later cleanup/repair logic.

### EngSense rule

For unsafe state transitions, verify safety at **every exit edge**, including panic/unwind where the configured panic strategy permits it.

## Layout assumptions require explicit guarantees

`repr(Rust)` does not give a stable field layout contract.

Casts/transmutes must be based on actual representation guarantees such as `repr(C)`, `repr(transparent)`, or otherwise proven constraints.

## Privacy boundary is the true audit scope

A local unsafe block may depend on safe code elsewhere preserving field, trait, or lifecycle invariants.

The source recommends shrinking the set of code capable of violating those invariants through encapsulation/module/crate boundaries.

This is deeper than simply "minimize unsafe line count."

### EngSense extraction

Measure unsafe surface by:

```text
code that can invalidate the safety proof
```

not just:

```text
number of lines inside unsafe {}
```

## Safety comments are mandatory evidence

This source directly conflicts with a mechanical anti-comment interpretation of Clean Code.

For unsafe operations, comments should document why the required invariants hold at the call/block/implementation site.

The act of writing that proof may itself expose missing reasoning.

## Verification must be augmented

The source recommends:

- ordinary tests;
- Miri;
- sanitizers;
- assertions/debug assertions;
- CI automation;
- regression tests for discovered failures.

Miri/sanitizers analyze only executed paths, so coverage/evidence still matters.

---

# Chapter 10 — Concurrency (and Parallelism)

## Source thesis

Concurrency is difficult along two independent axes:

1. correctness;
2. performance/scalability.

Adding concurrency can make both worse.

## Race condition is not the same as data race

The source distinguishes:

- data race — unsynchronized conflicting memory access; undefined behavior in Rust's model;
- race condition — result depends on relative timing; may be intentional or may be a logic bug.

EngSense should preserve this terminology in findings.

## More cores can make software slower

Contention, synchronization, shared-resource exhaustion, allocator/kernel limits, and false sharing can create sublinear or negative scaling.

### Candidate rule

Before adding concurrency for performance, establish:

```text
single-thread baseline
target workload
bottleneck
expected parallel fraction
contention points
measurement after change
```

"Uses all cores" is not evidence of improvement.

## Concurrency model should match ownership/work shape

The source describes three broad models:

### Shared memory

Best fit when threads truly need coordinated updates to shared state where operation ordering matters.

### Worker pools

Best fit when workers perform the same kind of independent work over different inputs/jobs.

### Actors

Best fit when independent resources/state can be exclusively owned and accessed through messages.

Actors can become bottlenecks when work is skewed or one actor owns too much.

### EngSense extraction

Do not select a concurrency pattern by fashion.

Choose based on:

- state ownership;
- commutativity;
- workload homogeneity;
- skew;
- coordination frequency;
- required parallelism.

## Async synchronization is not automatically superior

Async locks/channels avoid blocking executor threads but carry additional machinery.

The source allows synchronous primitives in async code when critical sections are demonstrably short/nonblocking, while warning about the footguns.

### EngSense rule

Default toward the safer composable primitive. Cross to a riskier optimization only with workload evidence.

## Atomics require explicit memory-model reasoning

The chapter covers:

- `Relaxed`;
- Acquire/Release;
- `SeqCst`;
- compare-exchange;
- fetch operations.

The key EngSense lesson is not to memorize an ordering table. It is that lower-level atomics move correctness obligations from library primitives into developer reasoning about permitted executions.

### Candidate rule

If code uses nontrivial atomic ordering, require an explicit invariant/happens-before explanation and specialist-level verification.

Do not "optimize" `SeqCst` to weaker orderings based solely on style or intuition.

## Start simple, then measure

The source gives a strong staged strategy:

```text
channels / locks / simple model
→ benchmark
→ identify concrete bottleneck
→ optimize locally
→ only then reach for fine-grained atomics/lock-free design
```

This maps directly to EngSense's evidence-driven complexity principle.

## Concurrent tests need adversarial scheduling evidence

The source recommends:

- stress tests;
- assertions;
- Loom for systematic small-model interleavings;
- ThreadSanitizer for larger runtime executions;
- other sanitizers where relevant.

It also explains Heisenbugs: instrumentation such as printing can change scheduling/synchronization and make the defect disappear.

### EngSense extraction

A concurrency review should not accept "tests passed once" as meaningful evidence for schedule-sensitive correctness.

---

# Cross-source conflicts established by Chapters 6–10

## Clean Code comments skepticism vs unsafe proof comments

Unsafe Rust requires prose that records invariants not mechanically evident in code.

Conclusion:

> For unsafe blocks/functions/impls, safety rationale is part of the contract and should not be removed merely to make code "self-documenting."

## DRY vs macro opacity

Macros can eliminate repetitive source code, but may add:

- compile cost;
- generated-code volume;
- debugging indirection;
- DSL maintenance.

Conclusion:

> Source duplication is not enough to justify metaprogramming. The repeated pattern must be mechanically stable enough that code generation reduces total complexity.

## Simplicity vs async adoption

Async can scale waiting-heavy workloads while increasing runtime/lifecycle complexity.

Conclusion:

> Prefer synchronous structure until concurrency/waiting requirements justify async machinery.

## Abstraction vs executor lock-in

`async fn` may look provider-neutral while concrete leaf futures bind a library to one runtime.

Conclusion:

> Evaluate architectural coupling below syntax-level abstractions.

## Readability cleanup vs unsafe invariants

Refactoring unsafe/concurrent code for local readability can invalidate nonlocal safety or ordering assumptions.

Conclusion:

> Preserve and re-prove invariants before applying ordinary structural-cleanup advice.

## Performance optimization vs concurrency complexity

Concurrency, atomics, unchecked operations, and macros can all make code faster in some context and slower overall in another.

Conclusion:

> Benchmark the actual bottleneck before paying correctness/complexity cost.

---

# Additional eval candidates from Chapters 6–10

## Eval: mock-driven trait pollution

Context:

Production code has one concrete dependency. Tests introduce a public trait and dynamic dispatch solely so a mocking library can replace it.

Expected:

- consider test-only seams, fake concrete types, integration tests, or narrower internal abstraction;
- require production abstraction to have production value;
- do not let mocking style dictate public architecture.

## Eval: macro replaces simple generic

Context:

A declarative macro dispatches behavior only by type, even though a generic function with trait bounds expresses the same contract.

Expected:

- prefer the generic solution;
- reserve macro for source-shape generation not expressible ergonomically through types.

## Eval: async for CPU-bound loop

Context:

A CPU-heavy transformation has no meaningful waiting but is rewritten as async to "make it faster."

Expected:

- reject async as a parallelism substitute;
- consider parallel workers/rayon only if measurement and data partitioning justify it.

## Eval: detached task lifecycle

Context:

A request handler calls `spawn` for important persistence work and ignores the task handle/error.

Expected:

- identify lifecycle/durability/error-observation risk;
- require explicit detached-work semantics or await/supervision.

## Eval: unsafe micro-optimization without benchmark

Context:

Bounds checks are replaced with `get_unchecked` in a non-hot path.

Expected:

- reject the safety cost without benchmark evidence;
- prefer safe indexing;
- if optimization is real, require documented invariants and dedicated verification.

## Eval: unsafe block with no safety rationale

Context:

Code is technically correct today but contains an unsafe pointer dereference with no explanation of why lifetime/alignment/aliasing invariants hold.

Expected:

- require a local safety proof/comment;
- inspect the full privacy boundary capable of invalidating the proof.

## Eval: lock-free rewrite before bottleneck evidence

Context:

A correct mutex-based queue is proposed for replacement with custom atomics because lock-free "scales better."

Expected:

- require workload benchmark and contention evidence;
- keep simple synchronization when it meets requirements;
- if lower-level rewrite proceeds, require ordering proof plus Loom/TSan/stress evidence.

## Eval: relaxed ordering used for security state

Context:

A flag guarding initialization/security state uses `Ordering::Relaxed` because atomic loads/stores are individually atomic.

Expected:

- reject the reasoning;
- require explicit cross-thread ordering semantics;
- escalate to concurrency-specialist review if necessary.

# Research integrity notes

- Full-source completion is not claimed yet.
- Current findings come only from the fully reviewed opening material and the source's explicit chapter structure.
- Existing `languages/rust.md` remains provisional.
- No claim should be attributed to Gjengset unless the completed chapter supports it.
- The final Rust lens must be cross-checked against the complete source, not only familiar Rust conventions.
- The source's guidance should be allowed to contradict current EngSense assumptions.

---

# Next research pass

Chapters 1–10 are complete.

Continue in source order:

1. Chapter 11 — Foreign Function Interfaces
2. Chapter 12 — Rust Without the Standard Library
3. Chapter 13 — The Rust Ecosystem
4. Index/reference cross-check

After the full-source pass, revise `languages/rust.md` from the completed evidence base and add Rust-specific eval fixtures.

Do not mark the mandatory Rust source complete or finalize Rust-specific evals until all 13 chapters have been reviewed.
