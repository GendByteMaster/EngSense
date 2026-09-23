# Rust Guidance

Status: **research-grounded**

Primary mandatory source: Jon Gjengset, *Rust for Rustaceans* — full user-provided edition reviewed end to end in `research/rust-for-rustaceans.md`.

This module translates that research into EngSense decision guidance. It is not a replacement for the source and does not make Gjengset an absolute authority. General EngSense rules, repository evidence, specialist invariants, and other completed sources may override or qualify a recommendation.

## Core orientation

Prefer designs that express the real invariant while keeping the costs of ownership, lifetimes, representation, dispatch, allocation, concurrency, and compatibility visible.

Do not start from a pattern such as:

```text
"clean architecture"
"everything behind a trait"
"zero-copy"
"async everywhere"
"lock-free"
"unsafe for speed"
```

Start from:

```text
behavior / invariant
        ↓
ownership + lifetime model
        ↓
type / representation / API contract
        ↓
dispatch + allocation + compatibility cost
        ↓
async / concurrency only when relevant
        ↓
unsafe / FFI only when justified
        ↓
target / toolchain / ecosystem constraints
        ↓
verification matched to the failure class
```

Do not transplant class-heavy or interface-per-type architecture into Rust automatically.

---

## Ownership and borrowing

Treat ownership as architecture, not syntax.

When reviewing a design or refactor, ask:

- who owns each long-lived value;
- which operations need shared access;
- which operations need exclusive access;
- whether a borrow is local or leaks into a public API;
- whether lifetime coupling is expressing a real relationship or merely implementation convenience;
- whether cloning/reference counting would simplify the design at acceptable cost;
- whether the representation itself is causing borrow-checker friction.

### Prefer borrowing when

- the relationship is naturally temporary;
- the owner clearly outlives the borrower;
- avoiding a copy/allocation is materially useful;
- the lifetime does not infect unrelated public surfaces.

### Prefer ownership when

- the value needs an independent lifecycle;
- borrowed lifetime coupling would spread through the API;
- a small copy/clone removes disproportionate complexity;
- delayed/asynchronous work must outlive the caller.

Do not clone reflexively to silence a borrow-checker problem when ownership is genuinely wrong.

Do not force zero-copy when retaining a large backing buffer, complicated lifetimes, or reference-counting costs more than the copy it avoids.

### Representation escape hatch

If internal references become difficult enough to require self-referential lifetimes, pervasive `Rc`/`Arc`, raw pointers, or `Pin`, reconsider the representation first.

Index/arena-style references can be a better trade-off when:

- data has one clear owner;
- stable indexes/handles are sufficient;
- cycles or multiple derived indexes are needed;
- deletion/update bookkeeping is cheaper than lifetime/unsafe complexity.

---

## Types, enums, and state

Prefer enums and exhaustive matching for closed state spaces such as:

- protocol variants;
- lifecycle states;
- result categories;
- mutually exclusive modes;
- small state machines.

Do not replace a closed enum with a trait-object hierarchy solely for hypothetical extensibility.

Use typestate/marker types when the compile-time state distinction has enough value to justify the type complexity, especially when:

- invalid transitions are dangerous;
- runtime recovery is weak;
- the state machine is small and stable;
- invalid states can be made unrepresentable;
- the representation is erased at runtime.

Do not add typestate ceremony to ordinary CRUD or low-consequence state merely because Rust can encode it.

---

## Traits

Traits have several valid roles. Runtime substitution is only one.

A trait can represent:

- a real capability;
- generic compile-time behavior;
- runtime polymorphism;
- marker semantics;
- an extension-method surface;
- a sealed/open implementation boundary;
- a stable contract shared by multiple implementations.

### Challenge a trait when

- one implementation exists and no stable capability boundary is gained;
- it mirrors a concrete type one-for-one;
- it exists only to satisfy a mocking framework;
- it forces `Box<dyn Trait>` without runtime heterogeneity;
- consumers still need implementation-specific details;
- the trait exposes unstable implementation choices as public promises.

### Static vs dynamic dispatch

Prefer generics/static dispatch when:

- polymorphism is known at compile time;
- monomorphization cost is acceptable;
- callers benefit from optimization/specialization;
- object safety would distort the API.

Prefer trait objects/dynamic dispatch when:

- runtime heterogeneity/substitution is part of the requirement;
- code-size/compile-time trade-offs favor one implementation body;
- plugin/provider selection happens at runtime;
- a stable erased capability boundary is valuable.

Treat dispatch choice as a trade-off involving:

- API flexibility;
- code size;
- compile time;
- allocation/indirection;
- object safety;
- compatibility.

### Extension traits

Extension traits are justified when adding ergonomic behavior to a type or base trait you do not control, or when a small stable base contract should evolve separately from convenience methods.

This means EngSense must not use the simplistic rule:

```text
trait only when multiple runtime implementations exist
```

---

## Public API contracts and hidden promises

Rust public APIs can create compatibility promises beyond function signatures.

Review changes to:

- trait implementations;
- auto-traits such as `Send` and `Sync`;
- re-exported dependency types;
- generic bounds;
- associated types;
- lifetime relationships;
- feature combinations;
- layout/representation guarantees when documented or externally observed;
- panic/error behavior;
- MSRV/toolchain promises.

A private field change can still be externally breaking if it changes an auto-trait or another observable contract.

Use compile-time assertions/tests when a trait/layout property is an intentional contract.

---

## API design

Prefer APIs that are:

- unsurprising;
- appropriately flexible;
- obvious to use correctly;
- constrained against invalid use.

Do not maximize all four blindly; they can conflict.

### Make costs visible

Be cautious with APIs that hide:

- cloning;
- allocation;
- blocking;
- runtime dispatch;
- synchronization;
- thread affinity;
- expensive conversion;
- background task lifetime.

### Borrowed vs owned inputs

Generic/borrowed inputs can improve ergonomics but may also:

- complicate inference;
- increase compile time;
- broaden the promise surface.

Choose the narrowest API that satisfies real callers.

### Destructors

Do not make critical failure or long blocking work depend invisibly on `Drop`.

If cleanup can fail materially, expose an explicit close/finish/commit operation and let `Drop` serve as fallback cleanup where appropriate.

---

## Error modeling

Use enumerated/typed errors when callers need to branch on meaningful failure categories.

Use opaque errors when callers primarily:

- log;
- attach context;
- propagate;
- surface the failure without recovery-specific branching.

Do not expose every internal error variant merely because Rust makes enums convenient.

At public boundaries, every exposed error variant becomes compatibility surface.

Preserve the semantic difference between:

```text
absence
!=
failure
```

Do not replace `Result<T, E>` with `Option<T>` unless the domain truly says the failure reason is irrelevant and non-exceptional.

Use `?` with awareness that early return still relies on correct RAII/cleanup behavior.

---

## Project structure, Cargo features, and MSRV

Create crate/workspace boundaries for real reasons:

- independently reusable/published components;
- dependency isolation;
- compile-time parallelism;
- proc-macro/build constraints;
- separate compatibility/release cadence;
- raw FFI bindings versus safe wrapper.

Do not split crates merely to imitate service/layer diagrams.

### Features

Cargo features should normally be additive and composable.

Test meaningful feature combinations because dependency feature unification can expose combinations the author did not run locally.

Avoid mutually exclusive feature designs unless the incompatibility is deliberate, documented, and enforced.

### MSRV

Treat minimum supported Rust version as a compatibility policy.

A convenience API requiring a newer compiler is not automatically worth downstream breakage.

Verify intentional MSRV claims in CI/toolchain checks.

---

## Testing and evidence

Match verification technique to the failure class.

### Unit tests

Use for local implementation invariants and private behavior.

### Integration tests

Use for public crate behavior because they compile as external consumers.

### Doctests

Use as executable documentation/API examples. Hidden setup must not make the visible example misleading.

### Compile-time tests/assertions

Use when the contract is itself type-level, such as:

- trait implementation;
- `Send`/`Sync`;
- expected compilation failure;
- size/layout when intentionally promised.

### Fuzzing / property tests

Use for large input spaces, parsers, serializers, and invariant-heavy transformations.

### Miri / sanitizers

Use to augment unsafe/memory-sensitive testing; they cover executed paths, not all possible paths.

### Loom / concurrency tools

Use for schedule/interleaving-sensitive code where ordinary tests cannot credibly explore the state space.

### Benchmarks

Treat benchmark design as part of the evidence.

Check:

- whether the workload matches the actual question;
- setup/I/O contamination;
- compiler elimination/constant folding;
- variance and distribution;
- warmup/repetition;
- before/after behavior under the target workload.

"Tests pass" is not evidence for every property.

---

## Macros

Use the simplest mechanism that expresses the abstraction.

A useful decision order:

```text
runtime behavior
→ function

type-dependent behavior
→ generics / traits

repetitive source shape
→ declarative macro

complex compile-time parsing/transformation
→ procedural macro
```

Do not introduce a macro solely to remove a few repeated lines.

For public macros, include:

- diagnostic quality;
- spans/error locality;
- compile-time cost;
- generated-code volume;
- discoverability;
- IDE/tooling behavior;
- public DSL compatibility.

Derive macros should normally produce behavior users can predict from the type/trait.

---

## Async

Async is a concurrency mechanism for waiting-heavy workloads, not a synonym for performance.

Before introducing async, ask:

- is the workload I/O/wait dominated;
- how many concurrent waits exist;
- is thread-per-operation cost material;
- is CPU parallelism actually required;
- which runtime/executor becomes part of the architecture;
- how cancellation, errors, and task lifetime are handled.

### Concurrency vs parallelism

A single executor thread can run many futures concurrently without parallel execution.

Parallel async work requires explicit task boundaries and the appropriate `Send` constraints.

### Blocking

Do not hide blocking or CPU-heavy work inside async code if it can stall the executor.

Move such work to an appropriate blocking/compute pool or otherwise structure it so scheduler progress remains possible.

### Spawning

`spawn` changes ownership/lifecycle/error semantics.

Do not detach important work simply to avoid awaiting it.

Review:

- task supervision;
- error observation;
- shutdown behavior;
- cancellation;
- whether the task may outlive caller state;
- whether completion is required for correctness/durability.

### Runtime coupling

An `async fn` signature alone does not guarantee runtime neutrality.

Inspect leaf resources, timers, I/O types, and executor-specific assumptions.

---

## Concurrency

Do not refactor synchronization based on readability alone.

Preserve and understand:

- ownership;
- `Send`/`Sync`;
- lock ordering;
- atomicity;
- memory ordering;
- channel/backpressure behavior;
- cancellation;
- shutdown;
- panic behavior.

### Choose a model from the workload

Shared memory fits coordinated updates to genuinely shared state.

Worker pools fit homogeneous operations over independent jobs/data.

Actors fit resources that can be exclusively owned behind message passing.

Do not choose actors, locks, or lock-free algorithms by fashion.

### Start simple

Prefer:

```text
channels / locks / simple ownership
→ benchmark
→ locate actual contention
→ local optimization
→ atomics / lock-free only if justified
```

More cores can reduce throughput when contention or shared resources dominate.

### Atomics

Nontrivial atomic orderings require an explicit execution/happens-before argument.

Do not weaken `SeqCst` to Acquire/Release/Relaxed from intuition alone.

Use specialist concurrency review when correctness depends on subtle memory ordering.

### Concurrency verification

For schedule-sensitive code, combine appropriate:

- stress tests;
- assertions;
- Loom/model checking;
- ThreadSanitizer or current equivalent;
- targeted benchmarks.

Be aware that debugging instrumentation such as synchronous printing can alter timing and hide races.

---

## Unsafe Rust

Treat every unsafe boundary as a proof obligation.

Distinguish:

- `unsafe fn` — caller must uphold documented preconditions;
- `unsafe {}` — implementation author asserts that the enclosed unsafe operations satisfy their contracts.

### Prefer a small unsafe core

Prefer:

```text
narrow unsafe internals
→ safe constrained interface
```

over distributing unsafe obligations through the codebase.

Audit the full **privacy boundary** capable of invalidating the safety proof, not just the lines inside `unsafe {}`.

### Safety invariants to review

Depending on the operation:

- pointer validity;
- alignment;
- initialization;
- valid bit patterns;
- aliasing;
- lifetime;
- ownership;
- layout;
- thread-safety;
- panic/early-exit behavior.

`repr(Rust)` is not a stable layout promise.

### Safety comments

Unsafe blocks/functions/impls should document the relevant safety invariants and why they hold.

This is not redundant commentary; it is part of the proof and maintenance contract.

### Performance

Do not introduce unchecked operations or unsafe layout tricks for hypothetical speed.

Measure first.

If unsafe is justified, add targeted regression evidence and automated tooling where appropriate.

---

## FFI

Treat FFI as an ABI + ownership + safety boundary.

Review:

- calling convention;
- symbol/link contract;
- type layout/alignment/endianness;
- ownership transfer;
- allocator/deallocator pairing;
- pointer/lifetime duration;
- mutability;
- thread-safety;
- panic/error translation;
- opaque handle typing;
- build/binding reproducibility.

Prefer:

```text
raw bindings (-sys style when useful)
→ narrow unsafe wrapper
→ safe Rust API
```

Do not expose raw foreign handles throughout application code when a typed wrapper can encode the contract.

Never add `Send`/`Sync` to a foreign handle merely because concurrent tests happened to pass. Require the foreign contract or enforce synchronization yourself.

Keep panics from accidentally unwinding across an ABI that does not support it.

Treat static versus dynamic linking as a deployment/security/distribution trade-off, not a style preference.

---

## `no_std`, allocation, and target constraints

Treat target capabilities as architecture.

The useful capability layers are:

```text
core
core + alloc
std
```

`#![no_std]` alone is not proof that a crate is truly usable on a no-std target.

Verify intended targets in CI, including transitive dependencies/features.

### Allocation

When heap availability/failure is constrained, consider:

- bounded/static storage;
- caller-provided buffers;
- fallible allocation;
- explicit capacity;
- heapless data structures.

Prefer safe representations until measured requirements justify unsafe optimization.

### Panic / OOM / startup

For embedded/kernel/constrained software, explicitly understand:

- panic handler;
- unwind vs abort/reset/loop;
- OOM behavior;
- startup/runtime initialization.

### Hardware access

Use volatile operations for side-effecting memory-mapped hardware where ordinary memory optimization rules do not apply.

Do not use volatile as a substitute for concurrency atomics.

Use typestate when it materially prevents dangerous illegal hardware transitions.

---

## Ecosystem and dependencies

Before writing custom machinery, inspect whether the standard library or a mature crate already provides the capability.

But adopting a dependency also has costs:

- supply-chain/security policy;
- licensing;
- MSRV;
- compile time;
- transitive dependency size;
- maintenance;
- public API coupling.

Evaluate both sides.

Use current tooling when relevant to inspect:

- dependency graph/policy;
- feature combinations;
- macro expansion;
- compile-time hot spots;
- stale/unused dependencies;
- benchmark distributions;
- type/layout contracts.

Tool names from historical research are examples, not permanent requirements. Verify the maintained tool at application time.

### Preludes

Treat a crate prelude as curated public API.

Do not dump every export into it; glob imports can grow compatibility/ambiguity risk.

---

## Anti-pattern transfer examples

Usually challenge:

- interface + implementation + factory for every type;
- runtime DI container for simple construction;
- trait objects where a closed enum is the real model;
- `Arc<Mutex<_>>` added merely to silence ownership questions;
- `clone()` everywhere to avoid designing ownership;
- async wrappers over synchronous CPU-bound work with no concurrency benefit;
- custom lock-free algorithms without measured contention;
- `unsafe` unchecked access without a proven hot path;
- raw FFI pointers leaking beyond the binding layer;
- `#![no_std]` claims not verified on a real no-std target;
- macros used where a function or generic is clearer.

These are review triggers, not automatic defects.

---

## Revisit triggers

Reconsider a concrete implementation as a trait boundary when:

- a second real implementation appears;
- plugins/providers must be selected at runtime;
- callers need a narrower stable capability;
- generic algorithms need a shared compile-time contract.

Reconsider safe/simple code for lower-level optimization when:

- profiling/benchmarks identify a concrete bottleneck;
- the requirement cannot be met by the safe design;
- the new invariant can be documented and verified.

Reconsider borrowed representation when:

- lifetimes become part of unrelated public APIs;
- async/background work needs independent ownership;
- retention cost exceeds copy cost.

Reconsider sync design for async when:

- concurrent waiting dominates;
- thread-per-operation costs become material;
- the target ecosystem/runtime already requires async integration.

---

## Specialist boundaries

EngSense can identify these risks but should not pretend to replace specialist review when:

- unsafe correctness depends on unsettled language-memory-model details;
- custom atomics/lock-free algorithms depend on subtle memory ordering;
- cryptographic constant-time/security properties are involved;
- FFI ABI details are platform-specific and high consequence;
- embedded/kernel hardware contracts are safety critical.

In those cases, preserve the Rust-specific context above and coordinate deeper specialist verification.
