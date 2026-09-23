# Clean Code Lens — Robert C. Martin, Second Edition

Status: **research-grounded source-specific lens**

Primary source:

- Robert C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship, Second Edition*
- Full user-provided edition reviewed end to end in `research/clean-code-2e.md`.

This lens represents what is useful from this source for EngSense. It does **not** make Martin an authority, and it does not flatten the explicit Martin/Ousterhout disagreements preserved in the book's appendix.

Use this lens when the task materially concerns:

- readability and intent;
- naming and vocabulary;
- function or class decomposition;
- comments/documentation trade-offs;
- duplication and abstraction;
- SOLID-style change boundaries;
- component/package cohesion and coupling;
- policy/detail boundaries;
- testing as refactoring infrastructure;
- architecture that protects policy from volatile mechanisms;
- small feedback cycles and change safety.

Do not load it for trivial formatting or naming work that deterministic repository tooling already decides.

---

## Core orientation

Optimize for code that another developer can understand and safely change.

Do not optimize for a superficial Clean Code score such as:

- shortest function;
- most extracted helpers;
- fewest comments;
- most interfaces;
- maximum DRY;
- maximum test coverage percentage;
- most architectural layers.

The second edition itself contains explicit counterweights to those interpretations.

A useful summary is:

```text
clarity
+ meaningful decomposition
+ controlled dependencies
+ trustworthy verification
+ changeability
-
unnecessary indirection
- entanglement
- speculative abstraction
- representation leakage
- verification theater
```

---

## 1. Reader-first design

Treat readability as an engineering throughput concern because code is repeatedly read, reviewed, modified, debugged, and integrated.

Ask:

- Is intent visible without reconstructing irrelevant implementation detail?
- Can a reader discover the relevant behavior quickly?
- Does the structure preserve locality where locality matters?
- Are abstraction levels mixed in a way that forces repeated context switching?
- Does the code require knowledge from distant modules that is not obvious?

Do not assume readability means maximum decomposition. The source explicitly accepts that over-decomposition can make code harder to understand.

---

## 2. Naming is part of modeling

Prefer names that reveal:

- why a thing exists;
- what role it plays;
- how it participates in the system.

Evaluate naming at two levels:

### Local precision

Does the identifier communicate the local intent?

### System vocabulary

Does the code use consistent terms for the same concepts across the repository?

Challenge:

- misleading collection/type names;
- meaningless numeric suffixes;
- fake distinctions such as multiple `*Info` / `*Data` / `*Object` names with no semantic difference;
- names that require private author knowledge to interpret.

If something remains difficult to name after the behavior is understood, inspect whether the abstraction itself is confused.

Do not require long names merely to avoid comments. The appendix explicitly leaves that trade-off unresolved.

---

## 3. Function decomposition is conditional

Small functions are a source preference, not a line-count rule.

Prefer extraction when it:

- exposes a meaningful lower-level abstraction;
- separates independent reasons to change;
- keeps one abstraction level visible;
- makes high-level policy easier to scan;
- gives a useful name to implementation detail.

Prefer locality or re-inline when extraction:

- creates shallow wrappers;
- merely gives a name to one obvious statement;
- requires the reader to carry substantial caller context;
- scatters tightly related state transitions;
- increases navigation more than it reduces cognitive load;
- complicates ownership/lifetimes in the target language;
- creates material performance cost.

### Required check

For any non-trivial extraction, compare:

```text
abstraction gain
+ change isolation
+ naming value
vs
entanglement
+ navigation cost
+ locality loss
+ runtime/language cost
```

Never report a function as defective solely because it has more than N lines.

---

## 4. Comments are an information-channel decision

Do not use the shorthand "comments are failures" as an EngSense rule.

Prefer code, types, and names for facts that can be expressed and mechanically kept consistent there.

Use comments/documentation for information such as:

- rationale and why;
- public or cross-team contracts;
- surprising side effects;
- mathematical reasoning;
- external constraints;
- historical constraints that still govern behavior;
- non-obvious invariants;
- warnings whose consequence is not visible from code.

Challenge comments that are:

- redundant;
- stale or misleading;
- mandated noise;
- source-control history in source files;
- commented-out code;
- nonlocal facts that the local code cannot keep authoritative.

### Decision model

```text
information value
vs
drift / maintenance risk
```

The appendix documents a genuine Martin/Ousterhout disagreement over the relative costs of missing versus misleading comments. Preserve that disagreement.

---

## 5. DRY is semantic, not textual

Distinguish:

### Essential duplication

Two implementations represent the same concept and should evolve together.

### Accidental duplication

Two implementations happen to look similar but belong to different change responsibilities.

Deduplicate when shared behavior represents one stable concept or invariant.

Keep duplication when abstraction would couple independent policies or when the common concept is not yet stable.

Ask:

> Will these copies need to change together for the same reason?

Do not extract a helper solely because code looks similar.

---

## 6. SRP means change responsibility, not tiny modules

Use SRP to identify independently changing policies or stakeholder concerns.

Evidence for separation includes:

- different policy owners/actors;
- different release cadence;
- repeated independent change;
- unrelated failures caused by one shared implementation;
- a class/module name that can no longer summarize one coherent responsibility.

Do not split a cohesive module based on imagined future changes.

Observed change pressure is stronger evidence than hypothetical variation.

---

## 7. OCP is strategic closure

Do not attempt to make every dimension extensible.

Use OCP when there is credible evidence that a particular axis will vary and modifying existing policy repeatedly would create meaningful risk.

Good signals:

- repeated new provider/type variants;
- stable policy with volatile mechanisms;
- extension by independent teams/plugins;
- compatibility-sensitive stable core.

Bad signal:

- "we may need another implementation someday."

The cost of extension machinery is real and must be included.

---

## 8. LSP is behavioral substitutability

A shared interface is useful only if implementations are behaviorally substitutable for the caller's contract.

Check more than signatures:

- accepted inputs;
- output semantics;
- errors/failures;
- side effects;
- ordering;
- consistency;
- resource/lifecycle behavior when contractually relevant.

If callers require implementation-specific conditionals, question whether one abstraction is truthful.

This applies to classes, traits, structural interfaces, providers, services, and protocols.

---

## 9. ISP is dependency diet

The useful principle is:

> Do not depend on capabilities you do not need.

Review the dependency surface and transitive change burden rather than counting interface methods.

A cohesive larger interface may be correct when consumers genuinely need it.

Multiple microinterfaces can be worse if they fragment one concept without reducing coupling.

---

## 10. DIP targets volatile concrete details

Do not interpret DIP as "interface every concrete type."

The second edition explicitly acknowledges that stable concrete dependencies are often fine and that slavish DIP can create interface explosion.

Prefer inversion when:

- the dependency is volatile;
- the caller is high-value/stable policy;
- multiple real implementations exist;
- an external provider/platform boundary exists;
- independent substitution/testing has real value;
- representation translation protects the core.

Prefer concrete simplicity when those benefits are absent.

For Rust and other non-Java ecosystems, load the language lens before choosing the mechanism.

---

## 11. Objects vs data structures depends on variation axis

Do not force behavior-rich objects into every domain.

Use this source distinction:

### Objects

Useful when representation should be hidden and new data/type variants are a likely extension axis.

### Data structures / DTOs

Useful when transparent data is intentional and new operations over stable data are the likely extension axis.

Ask:

```text
variation_axis:
  types | operations | mixed | unknown
```

A transport/database/message DTO can legitimately be plain data.

Private fields plus trivial getters/setters do not automatically create encapsulation.

---

## 12. Component boundaries are contextual

Use REP/CCP/CRP as competing lenses:

- **REP** — reusable units should have coherent release/version meaning;
- **CCP** — things that change together should be packaged together;
- **CRP** — do not force consumers to depend on things they do not use.

These principles conflict.

Project maturity changes their relative importance.

Early product code may optimize developability/closure.

Mature reusable libraries may optimize release/reuse and consumer dependency surface.

Do not treat the current package graph as timeless.

---

## 13. Dependency cycles are a change-risk signal

A component-level cycle matters when it creates:

- coupled release/build order;
- forced simultaneous change;
- inability to test/deploy independently;
- team coordination cost.

Possible remedies include:

- dependency inversion;
- extraction of a real shared concept;
- boundary redesign.

Do not create a meaningless `common` package merely to hide the cycle.

Do not assign the same severity to every low-level import cycle without evidence of material consequences.

---

## 14. Architecture protects policy from volatile details

The source's architecture chapters are best read as dependency and representation rules, not a template.

Useful questions:

- Does core policy depend on framework/database/vendor representations?
- Are external details leaking through core APIs?
- Can the important behavior be tested without booting the whole external mechanism?
- Is the detail actually volatile enough to justify a boundary?
- Does the boundary preserve useful optionality at acceptable cost?

Strong boundary candidates:

- third-party/provider SDKs;
- hardware;
- unstable external services;
- persistence formats;
- framework-generated representations;
- separately owned subsystems.

Weak boundary candidate:

- a stable local helper wrapped one-to-one only to look "architectural."

### No mandatory layer count

The source explicitly says the Clean Architecture circles are schematic.

Do not require:

- Entities folder;
- UseCases folder;
- Ports folder;
- Adapters folder;
- exactly four layers.

Evaluate dependency direction and change isolation instead.

---

## 15. Keep vendor knowledge narrow

When an external dependency is material and volatile:

```text
application-owned semantics
→ adapter
→ vendor semantics
```

Prefer a narrow application-shaped contract over spreading the vendor's vocabulary and types through the core.

Use focused learning/contract tests to verify the subset of external behavior the application relies on.

Do not wrap stable trivial dependencies when the wrapper adds no semantic boundary.

---

## 16. YAGNI is a cost comparison

Do not reduce YAGNI to "never build for the future."

Compare:

- probability of future need;
- carrying cost now;
- migration/lock-in cost later;
- reversibility;
- evidence available now versus later.

Early flexibility can be justified when later change is destructive, externally constrained, or very expensive.

Speculative extensibility with cheap future migration is usually not justified.

---

## 17. Verification enables structural change

Tests are infrastructure for refactoring, but passing tests are not proof of architecture quality or formal correctness.

Useful properties:

- fast enough for the intended loop;
- trusted;
- repeatable;
- meaningful assertions;
- independent enough from implementation details;
- coverage of material risk.

Avoid tests that compute expected results using the same logic they are supposed to verify.

### Coverage

Use coverage as a developer feedback signal, not a management score or automatic quality grade.

High line coverage with weak assertions is weak evidence.

Mutation testing can reveal semantic gaps, but route it by risk and cost.

Prefer **semantic confidence** over a percentage.

---

## 18. TDD is not mandatory EngSense policy

The second edition explicitly presents TDD, TCR, and Small Bundles as legitimate disciplines.

The appendix preserves a real Martin/Ousterhout disagreement over TDD versus larger design-centered bundles.

The common engineering properties are more useful than the ceremony:

```text
bounded change
+ nearby verification
+ short rollback/debug distance
+ deliberate design review
+ continuous structural correction
```

Do not report test-after-code as defective when the team uses disciplined small bundles and retains strong verification.

Do not report TDD as defective merely because design also requires strategic thought.

Evaluate actual outcomes and feedback structure.

---

## 19. Acceptance evidence is durable regression evidence

When requirements can be meaningfully expressed as executable scenarios, keep them as regression evidence after implementation.

Possible mechanisms:

- acceptance tests;
- executable examples;
- conformance vectors;
- contract tests;
- scenario tests.

Do not pretend every requirement is reducible to one executable assertion.

Security, usability, accessibility, latency distributions, compliance, and operability may need additional specialist evidence.

---

## 20. Concurrency is a semantic decision

Do not recommend concurrency for "scalability" without a concrete need.

Require evidence such as:

- exploitable I/O wait;
- independent requests;
- parallelizable computation;
- measured throughput/latency need;
- scheduling requirement.

Review:

- shared mutable state;
- ordering;
- atomicity;
- visibility;
- contention;
- cancellation/shutdown;
- resource lifetime;
- failure/recovery behavior.

Possible solutions include:

- remove concurrency;
- partition state;
- serialize;
- lock/transaction;
- immutable/copy state;
- reorder lifecycle;
- accept and recover from a cheap conflict.

The most concurrent solution is not automatically best.

Use the specialized concurrency/language lens when correctness depends on runtime or memory-model details.

---

## 21. Small cycles reduce integration risk

Prefer feedback/integration cycles short enough that:

- failures are attributable;
- merges remain understandable;
- rollback distance is bounded;
- other work is not blocked unnecessarily.

Do not prescribe one Git strategy universally.

Longer branches can be reasonable when:

- the work is strongly isolated;
- overlap is low;
- integration contracts are stable;
- verification is strong.

A persistently ignored broken CI signal is worse than either fixing the build or fixing/removing the bad check.

---

## 22. Continuous improvement must remain bounded

Small cleanups can expose change friction and prevent gradual structural decay.

But EngSense must preserve scope.

Perform opportunistic cleanup when it:

- directly supports the current change;
- preserves behavior;
- is easy to verify;
- reduces real friction.

Do not convert the Boy Scout Rule into repository-wide cleanup on every task.

Emergency compromises may be acceptable when consequence requires speed, but make the debt explicit and do not silently build more dependency on known-bad structure.

---

## 23. Risk scales verification

The craftsmanship section's strongest technical contribution is proportionality:

```text
greater failure consequence
→ stronger independent evidence
→ lower tolerance for unknown behavior
```

This does not make EngSense a security, safety, cryptography, legal, or compliance specialist.

When those invariants dominate, route to the specialist workflow.

---

## 24. Generated code is still engineering code

AI authorship does not reduce the need for:

- precise contracts;
- clear intent;
- architecture;
- verification;
- independent evidence.

Tests generated from the same ambiguous prompt as the implementation can share the same misunderstanding.

For material behavior, ask:

- What independent oracle exists?
- Which invariant would catch a shared misinterpretation?
- Which requirement is expressed in another form?

Useful redundancy can include:

```text
prose requirement
+ executable example
+ type/schema/contract
+ independent review/test oracle
```

Do not adopt the source's broader philosophical claims about whether LLMs "reason" as EngSense facts.

---

# Explicit anti-rules

Do **not** infer any of the following from this lens:

- function > N lines is a defect;
- every conditional body should be a function;
- every comment is a failure;
- long names should replace all documentation;
- every concrete dependency needs an interface;
- every switch should become polymorphism;
- every DTO should become a rich object;
- every database requires a repository abstraction;
- every system needs four Clean Architecture layers;
- every package cycle has the same severity;
- 100% line coverage proves quality;
- 100% coverage should be a management/build gate;
- TDD is the only professional testing discipline;
- feature branches are always wrong;
- microservices are cleaner than a monolith;
- more concurrency is more scalable;
- framework independence requires wrapping every stable library;
- source-specific OO mechanisms should override target-language idioms.

---

# Conflict routing

Load `references/conflicts.md` when this lens encounters:

- decomposition vs locality/deep behavior;
- code-expressed intent vs comments/documentation;
- DRY vs stable duplication;
- dependency inversion vs concrete simplicity;
- extensibility vs YAGNI/current surface simplicity;
- test isolation vs production fidelity;
- TDD short cycles vs larger design bundles;
- coverage quantity vs semantic confidence;
- options-open architecture vs abstraction carrying cost;
- polymorphism vs transparent data/procedural change;
- concurrency/parallelism vs simpler sequential semantics.

When the conflict is unresolved in the source, preserve it.

---

# Language precedence

This source contains substantial Java/OOP-oriented mechanisms.

Apply the **goal** before the mechanism.

Examples:

```text
goal: isolate volatile provider detail
Rust mechanism may be:
  trait
  generic parameter
  enum
  function/closure
  module boundary
  explicit adapter

not automatically:
  Java-style interface + factory + DI container
```

The target-language module has priority over source-specific mechanics when it preserves the same engineering intent more idiomatically.

---

# Authority model

Use this lens mostly as:

- **guidance** for contextual design choices;
- **heuristic** for naming, decomposition, comments, and local structure;
- **strong recommendation** only when repository evidence shows material change/coupling/verification risk;
- **hard gate** only when another explicit invariant or project requirement makes it one.

Do not cite "Clean Code says so" as sufficient evidence.

---

# Research traceability

Primary research note:

- `research/clean-code-2e.md`

Important unresolved/cross-source comparisons:

- Martin vs Ousterhout on method decomposition and entanglement;
- Martin vs Ousterhout on comments/documentation;
- Martin vs Ousterhout on TDD vs larger design bundles;
- Clean Architecture optionality vs premature abstraction;
- test isolation vs realistic integration evidence;
- OO polymorphism vs language/data-oriented alternatives.

The appendix supplies Ousterhout's side only for the topics debated there. Do **not** treat that as a substitute for the mandatory full read of *A Philosophy of Software Design, 2nd Edition*.
