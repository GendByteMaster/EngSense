# Clean Code, 2nd Edition — EngSense Research Notes

Source: *Clean Code: A Handbook of Agile Software Craftsmanship, Second Edition*  
Author: Robert C. Martin  
Research basis: user-provided full-text PDF available in the EngSense research session

Research status: **IN PROGRESS — full-text study started**

This note intentionally separates:

- what the source argues;
- EngSense interpretation;
- candidate EngSense rules;
- failure modes and limits;
- tensions to compare against other sources.

No source is treated as absolute authority.

The copyrighted source text is not copied into this repository. These notes are original summaries and short source references only.

---

## Progress

- [x] Foreword / Introduction / structure
- [x] Chapter 1 — Clean Code
- [x] Chapter 2 — Clean That Code!
- [x] Chapter 3 — First Principles
- [x] Chapter 4 — Meaningful Names
- [x] Chapter 5 — Comments
- [x] Chapter 6 — Formatting
- [x] Chapter 7 — Clean Functions
- [x] Chapter 8 — Function Heuristics
- [x] Chapter 9 — The Clean Method
- [x] Chapter 10 — One Thing
- [x] Chapter 11 — Be Polite
- [x] Chapter 12 — Objects and Data Structures
- [x] Chapter 13 — Clean Classes
- [x] Chapter 14 — Testing Disciplines
- [x] Chapter 15 — Clean Tests
- [x] Chapter 16 — Acceptance Testing
- [x] Chapter 17 — AIs, LLMs, and God Knows What
- [ ] Chapter 18 — Simple Design
- [ ] Chapter 19 — The SOLID Principles
- [ ] Chapter 20 — Component Principles
- [ ] Chapter 21 — Continuous Design
- [ ] Chapter 22 — Concurrency
- [ ] Chapter 23 — The Two Values of Software
- [ ] Chapter 24 — Independence
- [ ] Chapter 25 — Architectural Boundaries
- [ ] Chapter 26 — Clean Boundaries
- [ ] Chapter 27 — The Clean Architecture
- [ ] Chapter 28 — Harm
- [ ] Chapter 29 — No Defect in Behavior or Structure
- [ ] Chapter 30 — Repeatable Proof
- [ ] Chapter 31 — Small Cycles
- [ ] Chapter 32 — Relentless Improvement
- [ ] Chapter 33 — Maintain High Productivity
- [ ] Chapter 34 — Work as a Team
- [ ] Chapter 35 — Estimate Honestly and Fairly
- [ ] Chapter 36 — Respect for Fellow Programmers
- [ ] Chapter 37 — Never Stop Learning
- [ ] Afterword
- [ ] Appendix — The Clean Code Debate

---

# Source scope

The second edition is much broader than the original code-style reputation of *Clean Code* suggests.

The book is explicitly organized into four layers:

1. **Code**
2. **Design**
3. **Architecture**
4. **Craftsmanship**

The source therefore mixes several different kinds of advice:

- local readability and naming;
- function and class design;
- testing discipline;
- design principles such as SOLID;
- component and architecture boundaries;
- concurrency;
- continuous design and small-cycle development;
- professional/craftsmanship norms.

This matters for EngSense because these recommendations should not all be routed with the same weight. A naming review should not automatically activate architectural doctrine, and an architectural decision should not be reduced to code-level cleanliness.

## EngSense routing implication

Treat Martin as a **family of related lenses**, not one monolithic rule set.

Candidate routing categories:

```text
clean-code.readability
clean-code.function-design
clean-code.testing-discipline
clean-code.simple-design
clean-code.solid
clean-code.component-boundaries
clean-code.architecture
clean-code.craftsmanship
```

The final implementation may expose fewer files, but the decision engine should preserve the distinction.

---

# Introduction

## Source thesis

The second edition explicitly revisits the 2008 material after major changes in languages, platforms, architectures, and AI-assisted programming.

The author does not present the new edition as a simple reprint. It adds and revises material on design, architecture, concurrency, ethics/craftsmanship, newer languages, and AI/LLMs.

The book also acknowledges that experienced programmers disagree about what clean code means and includes contrary viewpoints in the appendix rather than pretending the debate is settled.

## EngSense interpretation

This is important evidence against using "Clean Code" as a static checklist.

The source itself gives EngSense permission to model:

- historical context;
- evolving language ecosystems;
- competing expert views;
- rules as heuristics rather than timeless syntax;
- self-critique and revision.

## Candidate rule

When a Clean Code heuristic conflicts with language idioms, stronger domain invariants, or another well-supported engineering lens, do not resolve the conflict merely by author authority.

Prefer:

```text
source recommendation
+ actual context
+ competing lens
+ observable trade-off
→ contextual decision
```

---

# Chapter 1 — Clean Code

## Core source arguments

### 1. Code remains necessary even as abstraction levels rise

The chapter rejects the idea that AI, specifications, or higher-level languages remove the need for code-level precision.

The underlying argument is broader than syntax: executable systems still require sufficiently precise, formal details.

### EngSense interpretation

Do not treat prompts, generated code, DSLs, configuration, or specifications as exempt from engineering quality merely because a human did not write the final implementation manually.

Quality review should follow the artifact that carries executable intent.

Possible context signal:

```text
executable_intent:
  source-code | generated-code | prompt-spec | dsl | config | schema
```

---

### 2. Readability is an engineering throughput concern

A central argument is that developers spend much more time reading existing code than typing new code.

The important EngSense extraction is not a literal ratio. It is the directional principle:

> code optimized only for fast initial writing can create larger future reading and change costs.

### Candidate rule

When comparing a terse implementation with a clearer one, include future comprehension and modification cost.

Do not optimize merely for:

- shortest code;
- fewest files;
- fastest initial implementation.

But also do not equate readability with maximum decomposition. Readability can come from locality as well as naming and structure. This conflict must remain open for comparison with Ousterhout and other sources.

---

### 3. Cleanliness is continuous maintenance, not perfection

The chapter describes clean code as cared-for rather than immaculate.

The useful principle is continuous improvement: prevent small design debris from accumulating until normal changes become difficult.

### Candidate rule

Prefer **bounded opportunistic cleanup** when:

- it is local to the requested change;
- behavior is preserved;
- verification exists;
- the cleanup reduces real friction;
- scope does not expand into unrelated redesign.

### Anti-rule

Do not transform the Boy Scout Rule into:

```text
touch file
→ redesign everything nearby
```

That would conflict with EngSense's scope-control and change-risk principles.

---

### 4. "Make it easy to read" is not enough by itself

The chapter strongly prioritizes readability, but EngSense must make the quality dimension explicit.

Readable for whom?

Possible contexts differ:

- local application code;
- library API;
- concurrency primitive;
- parser;
- generated code;
- high-performance hot path;
- cryptographic implementation;
- data-oriented systems code.

### EngSense extraction

Readability is a major quality dimension, not a universal trump card.

Candidate model:

```text
readability_weight =
  f(change_frequency,
    reader_population,
    risk,
    locality,
    performance_constraints,
    language_idioms,
    invariants)
```

No numeric score is required in the Skill; the point is to force context-sensitive reasoning.

---

# Early conflict inventory

These conflicts are already visible from the source structure and Chapter 1 and must be tested as research continues.

## Readability vs locality

Martin strongly values code that can be read smoothly.

Potential conflict:

```text
more extracted functions
→ smaller units
→ names expose intent

but also

more extracted functions
→ more navigation
→ weaker locality
→ more working-memory load
```

Do not resolve until the function chapters and Ousterhout source are studied in full.

---

## Continuous cleanup vs scope control

Martin's continuous-cleaning stance is valuable against decay.

Potential failure mode:

- opportunistic refactoring expands the requested change;
- unrelated cleanup increases review surface;
- behavior risk increases without user value.

EngSense should require cleanup to remain proportional to the task.

---

## Language-independent principles vs language-specific mechanics

The source argues that core cleanliness principles can apply across languages, while many examples and design techniques are historically Java/OOP shaped.

EngSense must separate:

- broadly useful goals such as clear intent and controlled coupling;
- implementation mechanics that may be language-specific.

This will be especially important when comparing with *Rust for Rustaceans*.

---

# Source-specific assumptions to track

The following assumptions require explicit review while reading later chapters:

- strong object-oriented heritage;
- frequent Java examples;
- preference for decomposition into small named functions;
- preference for explicit abstraction boundaries;
- TDD and testability as major design forces;
- architecture framed around dependency direction and replaceable mechanisms;
- professional discipline/craftsmanship as part of technical quality.

These are not criticisms by themselves. They are context signals for where mechanical transfer into Rust, data-oriented code, performance-sensitive code, or very small systems may be inappropriate.

---

# Candidate evals from the initial pass

## Eval: generated code is still engineering code

Context:

An AI generated a working implementation. The user asks whether review can be skipped because the code is disposable output from a model.

Expected EngSense behavior:

- reject authorship as a quality criterion;
- review executable intent and risk;
- scale review depth to lifetime and consequences;
- do not demand production-level ceremony for genuinely disposable code.

---

## Eval: Boy Scout Rule scope trap

Context:

A bug fix touches a legacy module with many unrelated smells.

Tempting wrong answer:

> Refactor the whole module while we are here.

Expected EngSense behavior:

- allow small cleanup directly supporting the change;
- preserve behavior;
- keep unrelated redesign out of scope;
- record larger debt separately when material.

---

## Eval: readability vs locality

Context:

A cohesive 40-line parsing routine could be split into eight 3–7 line helpers.

Expected EngSense behavior:

- do not split by line count alone;
- ask whether names expose real abstraction;
- evaluate navigation and shared-state locality;
- compare both forms before deciding.

---

# Chapter 2 — Clean That Code!

## Source thesis

The chapter treats cleanliness as a **process**, not an initial writing property.

The practical sequence is:

~~~text
make it work
→ inspect it
→ clean it
→ keep behavior protected while structure changes
~~~

The Roman-numeral example is especially useful because the author later criticizes parts of his own cleaned version. The second edition therefore does not support a simplistic interpretation such as "more extracted methods is always cleaner."

The chapter explicitly recognizes several costs of decomposition:

- choppiness;
- scrolling;
- loss of locality;
- naming that made sense to the author but not to a future reader;
- extra allocation/call overhead in contexts where performance matters.

It also contains a key counterexample to mechanical "small functions" advice: the author leaves a longer conversion function intact because further decomposition would obscure rather than clarify it.

## EngSense extraction

### Separate correctness work from structural improvement

A useful default is:

~~~text
establish behavior
→ gain verification confidence
→ improve structure
~~~

This is not permission to write recklessly first. It is recognition that feature reasoning and structural reasoning compete for attention.

### Cleaning must be empirical

A refactor should be judged after the change, not merely by whether it applies a known technique.

Ask:

- Is intent easier to recover?
- Did navigation cost increase?
- Did state movement become less obvious?
- Did tests expose missing cases?
- Did the refactor create performance or allocation costs that matter here?
- Does the resulting structure match the expected growth direction?

### Performance is contextual

The chapter explicitly accepts a clarity-for-speed trade when speed is irrelevant and rejects pretending the same trade is valid for real-time or performance-sensitive systems.

Candidate rule:

> Never call an abstraction "cleaner" without considering whether its runtime cost is material in the target context.

### Self-review over time is evidence

"Future Bob" is an important methodological signal: an author can understand a design while creating it and still discover readability defects later.

EngSense should therefore value review by:

- a fresh reader;
- a later pass;
- a separate agent/reviewer;
- an eval fixture that removes author context.

---

# Chapter 3 — First Principles

## Source thesis

The chapter begins by explicitly calling its principles **guidelines, not strict laws**. That qualification is important for EngSense.

The core slogan is:

~~~text
small
well named
organized
ordered
~~~

From there the chapter connects code-level decomposition with SRP, OCP, DIP, component isolation, and eventually architectural boundaries.

## Small functions — source position and limit

The source generally prefers small functions that do one thing and have names that expose intent.

However, combined with Chapter 2, the actual source position is more nuanced than a line-count rule.

## SRP — change isolation

The chapter frames SRP around isolating different reasons/stakeholder concerns for change.

EngSense extraction:

A decomposition is justified when it reduces the probability that an unrelated change will disturb another policy.

This is stronger than:

> each function should be short.

Candidate diagnostic:

~~~text
If concern A changes,
how much code for concern B must be understood, edited, rebuilt, or retested?
~~~

## OCP — growth locality

The useful source idea is not "use inheritance." It is:

> predictable feature growth should have a clear extension location rather than requiring edits across many unrelated places.

EngSense should model **change dispersion**:

~~~text
new concept
→ edits in 1 coherent extension point
~~~

is generally safer than:

~~~text
new concept
→ synchronized edits across N independent branches
~~~

But creating extension machinery before there is credible growth pressure can itself increase complexity.

## DIP — dependency direction

The chapter strongly argues that high-level policy should not depend directly on low-level details.

It uses recompilation/redeployment and cognitive dependency as practical consequences, not merely class-diagram purity.

EngSense extraction:

Use dependency inversion when it creates a real isolation boundary for:

- volatile details;
- independently deployable pieces;
- providers/plugins;
- policy/mechanism separation;
- substantial change-frequency asymmetry.

Do **not** infer:

~~~text
every concrete dependency
→ must gain an interface
~~~

The source itself notes that the stronger decomposition becomes worthwhile as the project/growth context becomes large enough for those burdens to matter.

## Architectural boundaries have a cost

The chapter explicitly acknowledges:

- more modules;
- more indirection;
- cognitive overhead;
- potential runtime overhead.

This is crucial evidence for EngSense.

Candidate decision rule:

~~~text
boundary_value
=
change isolation
+ deployment isolation
+ policy protection
- navigation cost
- abstraction cost
- runtime cost
- migration cost
~~~

Do not add a boundary unless the positive terms are material.

## Tests as refactoring infrastructure

The chapter relies on pre-existing tests during structural changes and intentionally tries to keep tests decoupled enough that production refactoring does not force constant test rewrites.

Candidate rule:

Before deep structural refactoring, establish behavior evidence sufficient to distinguish intended design changes from accidental regressions.

---

# Chapter 4 — Meaningful Names

## Source scope

This chapter treats naming as an audience/communication problem.

The key framing is:

> code is written once but read by a community.

That supports EngSense's repository-aware approach: a name should be evaluated against the codebase vocabulary and its readers, not the author's private mental model.

## Intention-revealing names

Names should expose:

- why something exists;
- what role it plays;
- how it is used.

A comment that merely compensates for a misleading local name is a design signal.

## Build a system of names

The source goes beyond individual naming and argues for a coherent vocabulary across the application.

EngSense extraction:

Review names at two levels:

1. **local precision** — does this identifier communicate intent?
2. **system consistency** — does it use the same concept vocabulary as nearby and domain code?

This intersects directly with DDD/ubiquitous-language research later, but it should not be conflated with DDD yet.

## Avoid disinformation and fake distinctions

Strong reusable heuristics include:

- do not encode a collection/container type inaccurately;
- avoid nearly identical names for different concepts;
- avoid meaningless numeric suffixes;
- avoid noise suffixes such as Info, Data, Object when they do not represent a real distinction;
- similar concepts should be named similarly; different concepts should be meaningfully distinguishable.

## Searchability and scope

The chapter gives a contextual rather than absolute rule for name length.

Useful extraction:

- tiny scope can justify a tiny conventional name;
- larger scope increases the value of descriptive/searchable names;
- globally visible concepts should be especially easy to search and distinguish.

This prevents an EngSense anti-pattern where every variable is forced into a long sentence.

## Naming as design feedback

A recurring implication is that inability to name something clearly may indicate that the abstraction itself is confused.

Candidate rule:

> When naming remains difficult after understanding the context, inspect the underlying responsibility/data structure before inventing a clever label.

---

# Chapter 5 — Comments

## Source position

The chapter is intentionally skeptical of comments, but its conclusion is not "never comment."

The source distinguishes comments that compensate for poor expression from comments that preserve information code cannot express clearly enough.

## Useful comment categories

The chapter accepts comments that explain things such as:

- legal/licensing requirements;
- intent;
- rationale;
- warnings about consequences;
- public API documentation where it adds real contract value;
- genuinely non-obvious algorithmic reasoning.

A particularly strong example is explaining **why** a square-root limit is correct in a prime-number algorithm: a name or structural rewrite does not communicate the mathematical rationale as well.

## Harmful comment categories

Reusable failure modes include:

- redundant comments;
- misleading/stale comments;
- mandated comments with no information value;
- history/journal comments better handled by version control;
- commented-out code;
- local comments containing nonlocal system facts they cannot keep authoritative;
- attribution/byline clutter;
- excessive historical exposition next to unrelated implementation;
- comments whose relationship to the code is unclear.

## EngSense extraction: comments are consistency liabilities

A comment creates another representation of intent that can drift away from executable behavior.

So the decision is not:

~~~text
comment = bad
~~~

It is:

~~~text
information value
vs
drift/maintenance risk
~~~

Prefer code for **what** when code can communicate it directly.

Prefer comments/documentation for **why**, constraints, provenance, mathematical reasoning, external contracts, or non-obvious invariants when the information cannot be encoded more reliably elsewhere.

## TODO nuance

The author now prefers not to commit TODO comments, instead moving work to a backlog or resolving it.

EngSense should not universalize that repository-management preference.

A better contextual rule:

- TODOs without ownership/context can become permanent noise;
- structured repositories may intentionally allow TODO/FIXME markers if policy, tooling, and ownership make them actionable;
- issue trackers/backlogs are preferable for durable project work.

## Explicit conflict to preserve

The appendix contains a direct Martin/Ousterhout disagreement about comments.

Therefore EngSense must not finalize the comment heuristic until the appendix and *A Philosophy of Software Design* are both fully studied.

---

# Chapter 6 — Formatting

## Source thesis

Formatting is treated primarily as **communication**, not aesthetics.

The strongest modern extraction is consistency and perceptual grouping, not exact historical line/file limits.

## Vertical structure

The chapter argues for:

- blank lines between distinct concepts;
- density among closely related lines;
- declarations near use;
- callers and callees positioned to support top-to-bottom reading;
- conceptually related functions kept near each other.

This aligns with an important EngSense dimension:

~~~text
navigation cost
~~~

## Locality signal

Chapter 6 is an interesting counterweight to an over-simplified "split everything" reading of earlier chapters.

It explicitly says closely related concepts should remain vertically close and should not be placed in separate files without good reason.

EngSense extraction:

> Decomposition that destroys useful locality is not automatically an improvement.

This should become an explicit conflict fixture.

## File size guidance

The source uses empirical examples to show that significant systems can be built from relatively small files, but explicitly says the observed sizes are not hard rules.

EngSense should therefore never produce:

~~~text
file > N lines
→ finding
~~~

without additional evidence of mixed responsibilities, navigation cost, or change coupling.

## Horizontal formatting

The chapter prefers short lines and strongly dislikes forcing readers to scroll horizontally, while acknowledging that exact width limits are conventions.

Modern EngSense rule:

Defer exact line length and whitespace details to repository formatter/linter policy unless formatting materially harms comprehension.

## Team rules over personal preference

This is one of the strongest transferable principles in the chapter.

When a repository has an established formatter/style:

~~~text
repository/team convention
> reviewer personal preference
~~~

unless the convention itself creates a material engineering problem.

## Automation

Formatting rules are good automation targets because machines can enforce them consistently and cheaply.

EngSense should avoid spending review budget on style disputes already handled by formatters.

---

# New cross-chapter synthesis from Chapters 2–6

## 1. Smallness is instrumental, not the objective

The source often favors small functions/files, but also explicitly acknowledges cases where more decomposition obscures intent.

EngSense should encode:

~~~text
smallness
→ useful when it improves naming, isolation, ordering, or change locality
→ harmful when it adds navigation, state scattering, or artificial boundaries
~~~

## 2. Structure should follow expected change

The Conference Room example is fundamentally about making foreseeable business growth land in stable, isolated places.

Candidate context signals:

- change frequency by concern;
- expected extension axes;
- deployment boundary;
- provider/plugin volatility;
- consumer count;
- runtime/performance sensitivity.

## 3. Naming and comments are different channels

Prefer names/code structure for information that belongs to executable concepts.

Use comments for information outside normal executable expression, especially rationale and constraints.

Do not force either channel to carry information it is bad at expressing.

## 4. Locality must become a first-class EngSense quality dimension

The chapters repeatedly show that readability depends on keeping related concepts near each other, even while also advocating decomposition.

Add/retain explicit quality dimensions:

~~~text
cohesion
coupling
locality
navigation cost
change isolation
discoverability
~~~

## 5. Team/repository conventions are evidence

Naming, formatting, ordering, and local structure should be reviewed against the repository's established vocabulary and automated rules.

Consistency is not proof that the architecture is good, but gratuitous deviation imposes cognitive cost.

---

# Additional eval candidates

## Eval: premature DIP

Context:

A small internal module has one stable concrete dependency and no separate deployment/provider boundary.

Tempting recommendation:

> Introduce interface + factory solely to satisfy DIP.

Expected EngSense behavior:

- ask what low-level volatility is being isolated;
- quantify the actual change/deployment/testing benefit;
- keep the concrete dependency if the inversion buys nothing material;
- define a revisit condition.

## Eval: real policy/detail boundary

Context:

Business policy depends directly on multiple external provider details that change independently and require separate deployment/testing.

Expected EngSense behavior:

- recognize a real inversion boundary;
- move volatile details outward;
- keep policy independent of provider mechanics;
- verify that new indirection has a measurable purpose.

## Eval: naming problem is a modeling problem

Context:

A codebase contains UserData, UserInfo, UserObject, and UserDetails with overlapping fields and responsibilities.

Expected EngSense behavior:

- do not merely rename identifiers;
- determine whether multiple concepts actually exist;
- consolidate or separate the model based on real semantic distinctions.

## Eval: comment preserves rationale

Context:

A numerical bound is derived from a non-obvious mathematical or protocol invariant.

Expected EngSense behavior:

- keep/document the rationale even if code is well named;
- avoid replacing the explanation with an opaque helper solely to remove a comment.

## Eval: formatter preference

Context:

A reviewer dislikes a project's automated formatting style.

Expected EngSense behavior:

- do not report a style-only finding;
- follow repository formatter policy unless readability is materially impaired.

# Chapter 7 — Clean Functions

## Source thesis

The chapter strongly prefers small functions, but it explicitly says this is not a hard rule and can be overdone. Some functions read better when they are not decomposed further.

The more durable idea is not a line-count target. It is **abstraction discipline**:

- one level of abstraction per function;
- top-down reading through the Stepdown Rule;
- names that describe intent rather than mechanics;
- lower-level details placed behind meaningful names.

## Entanglement is an acknowledged cost

The chapter directly engages John Ousterhout's objection that extracting functions can create entanglement: understanding the child may require remembering context established by the parent.

Martin accepts some entanglement when:

- the lower-level function is directly below its caller;
- it descends one abstraction level;
- the name carries useful intent.

But the source explicitly acknowledges that severe entanglement can make extraction a bad trade.

### EngSense extraction

Do not treat extraction as automatically good.

Evaluate:

~~~text
intent gained from naming
+ abstraction separation
+ change isolation
-
context carried from caller
- navigation cost
- state scattering
~~~

When the lower-level function cannot be understood without many facts from its caller, locality may dominate decomposition.

## Switch statements

Martin's preferred OO strategy is to isolate switching in a low-level/construction area and use polymorphism elsewhere.

This is a **source-specific OO heuristic**, not a universal EngSense rule.

EngSense must gate it by:

- language idioms;
- openness of the type set;
- volatility of types vs operations;
- runtime dispatch cost;
- plugin/provider requirements.

Chapter 12 later supplies the important counterbalance.

## PINCH model

The chapter describes clean functions through five attributes:

- contextual;
- nameable;
- insulated;
- homogenous;
- pure.

Useful EngSense translations:

### Contextual

A function belongs to a coherent context/module. Public behavior and private implementation should form a meaningful boundary.

### Nameable

Names should be slightly more abstract than their implementation.

### Insulated

Inputs/outputs and other couplings should be kept purposeful. Argument count is a signal, not a score.

### Homogenous

A function should avoid mixing high-level policy with low-level mechanics.

### Pure

Purity is framed observationally: internal mutation does not necessarily make a function externally impure if all externally visible state is preserved.

That is a useful distinction for EngSense because "contains assignment" is not a sufficient impurity finding.

## Performance qualification

The source explicitly allows lower-level optimization when measured runtime constraints justify it.

EngSense rule:

> Maintainability heuristics are defaults until evidence shows a materially different performance constraint.

---

# Chapter 8 — Function Heuristics

## Source status of the rules

The chapter explicitly calls these **heuristics and biases, not hard-and-fast rules**.

That wording should be preserved in EngSense.

## Arguments are coupling

The source prefers fewer declared arguments and uses three as a personal rough limit, while acknowledging that the number is arbitrary and language features such as named arguments affect the trade-off.

### EngSense extraction

Argument count should trigger a question, not an automatic finding.

Ask whether several arguments:

- form a real cohesive value;
- expose missing context;
- are easy to misorder;
- would be clearer as a typed structure;
- are naturally separate and should remain separate.

Do not create parameter objects merely to reduce a number.

## Flag arguments

Boolean flags often indicate multiple modes hidden behind one name and make call sites opaque.

But the source explicitly allows exceptions.

Candidate rule:

Challenge a flag when the call site cannot communicate what mode it selects or when the two branches represent meaningfully separate operations.

Do not ban booleans categorically.

## Output arguments

The source prefers return values or meaningful result structures because readers normally expect data to enter through parameters and leave through returns.

EngSense should translate this through language idioms:

- tuple/multiple returns may be natural;
- a result struct may be clearer;
- mutation through an output buffer may be justified by performance or FFI constraints.

## Command Query Separation

CQS is presented as useful where practical, not universal.

The source explicitly discusses `pop()` as a convenient command+query and notes concurrency/exception-safety implications.

EngSense extraction:

Use CQS as a clarity and concurrency lens, not a prohibition.

## Exceptions vs error codes

The source prefers exceptions in languages where they are reliable and idiomatic, but explicitly treats Go-style returned errors as reasonable because Go does not use exceptions.

This is critical for EngSense:

> Error-handling advice must be language/runtime specific.

Never export "prefer exceptions" into the Rust lens. Rust's `Result` model must be judged using Rust sources.

## Error handling as a separate concern

The chapter favors keeping happy-path logic readable and isolating error-processing structure when that reduces mixing of concerns.

The exact try/catch extraction style is language-specific; the general principle is not.

## Essential vs accidental duplication

This is one of the most valuable EngSense contributions in the chapter.

The source distinguishes:

- **essential duplication** — code that represents the same concept and should evolve together;
- **accidental duplication** — code that merely looks similar but belongs to different change responsibilities and may evolve apart.

Candidate rule:

> Deduplicate by shared reason to change, not by textual similarity.

This supports EngSense's existing conflict:

~~~text
DRY
vs
duplication until the concept is stable
~~~

## Side effects and temporal coupling

The chapter connects side effects to ordering constraints and temporal coupling.

EngSense should treat a side effect as important when it creates hidden requirements such as:

~~~text
A must happen before B
resource must be acquired before use
state must be initialized before read
operation must be undone after use
~~~

Functional style can reduce such coupling but does not eliminate all side effects.

The source also argues OO encapsulation can hide side effects behind a boundary, with concurrency caveats.

---

# Chapter 9 — The Clean Method

## Source thesis

The chapter describes development as nested short feedback loops rather than a single write-then-clean event.

Core process:

~~~text
make a small behavior work
→ verify
→ clean one small thing
→ verify
→ revert on failure
→ repeat
~~~

## Tests are required infrastructure for cleaning

The source states that serious cleanup depends on tests that are:

- fast;
- convenient;
- trusted;
- sufficiently comprehensive.

EngSense extraction:

The safe refactoring budget depends on verification quality.

When tests are weak, the appropriate response may be:

- add characterization/behavior tests first;
- reduce refactoring scope;
- avoid speculative cleanup.

## Tests should tolerate implementation evolution

The Bobolia example shows a second important principle: test code can itself be overcoupled to production representation.

When adding a field forces broad unrelated test edits, that is evidence that tests know too much incidental structure.

Candidate rule:

Tests should preserve behavioral intent while minimizing coupling to irrelevant production details.

## Tests as an independent statement of intent

The source avoids reusing the production tax table in tests because the test is intended to provide an independent statement of expected behavior.

EngSense extraction:

Avoid tests whose expected result is computed by the same logic or data source they are supposed to verify.

This does not mean "duplicate every algorithm manually." It means preserve independent evidence at the boundary where correctness matters.

## Architecture can emerge from observed axes of change

The worked example repeatedly steps back from local cleanup and notices emerging change axes.

This is important because it weakens a caricature of Clean Code as purely upfront OOP design.

Candidate rule:

> Introduce stronger architectural boundaries when repeated change reveals stable axes worth isolating.

This aligns with evidence-driven abstraction.

## Language idioms matter

The Python example uses duck typing rather than creating explicit interface declarations.

EngSense should preserve the architectural purpose while adapting the mechanism to the language.

---

# Chapter 10 — One Thing

## Defining "one thing"

The chapter proposes a practical test:

> a function does one thing when no additional **meaningful** extraction remains.

The qualifier "meaningful" is the important part.

The source explicitly demonstrates that extraction can go too far when:

- the extracted name merely repeats the implementation;
- a pure delegator adds no useful boundary;
- the parts are naturally one cohesive operation.

## "Extract till you drop" is not literal

The author calls the phrase cheeky and says to **consider** many extractions, not necessarily perform all of them.

This is essential for EngSense. A simplistic agent that maximizes function count would misread the source.

## The strongest counterargument: entanglement

The chapter lists multiple objections to tiny functions and identifies entanglement as the strongest.

If extraction requires the reader to remember several facts from the parent context, the source explicitly says the extraction may not be worth doing.

It ends the discussion as a judgment call.

### EngSense rule

A candidate extraction should pass both tests:

1. **abstraction gain** — the new name hides a meaningful lower-level concept;
2. **context independence** — the extracted body does not require excessive hidden caller state to understand.

If either fails, keep or re-inline the code.

## Extraction as a diagnostic technique

The Video Store example uses extraction not only as a final design but as a way to discover misplaced behavior, responsibilities, and class boundaries.

This suggests a useful EngSense technique:

~~~text
temporary extraction
→ inspect cohesion/change ownership
→ move behavior if a real boundary appears
→ strategically inline again when extraction adds no lasting value
~~~

The source explicitly suggests "extract first, then strategically inline" as one possible discovery strategy.

## Language-specific warning

The chapter's major worked example is object-oriented and introduces polymorphic types.

The source itself includes a later note acknowledging more idiomatic Go alternatives.

EngSense must not copy this class/type-hierarchy result into Rust, Go, TypeScript, or functional code without checking their idioms and actual variation axis.

---

# Chapter 11 — Be Polite

## Source thesis

A polite module lets a reader obtain the level of detail they need and stop.

The source borrows Ousterhout's idea of a narrow interface/deep implementation and combines it with Martin's Stepdown Rule.

The goal is to reduce **interruption cost** while reading.

## Newspaper metaphor

High-level intent appears first; details become progressively deeper.

The source does not define a module by "one file" or "one class." It explicitly describes a module as a cohesive bounded set of functions and variables that may span multiple files/classes.

### EngSense extraction

Do not equate module boundaries with filesystem boundaries.

Review modules by:

- cohesion;
- public interface;
- hidden implementation;
- conceptual responsibility;
- reader navigation.

## Abstraction roller coaster

Mixing policy and low-level detail forces the reader to repeatedly abandon and reconstruct a mental model.

This gives EngSense a concrete readability failure mode:

~~~text
high-level policy
→ low-level detail
→ high-level policy
→ unrelated mechanism
→ policy again
~~~

Report this when it materially increases reasoning cost, not merely because different abstraction levels are technically present.

## Reader-oriented completion criterion

The chapter says working code is not the end; code should also be organized for the reader.

EngSense should temper this with scope/risk constraints:

- improve readability when it reduces future change cost;
- do not turn every feature into an open-ended cleanup;
- preserve performance/security/domain invariants.

## Explicit non-dogmatism

The chapter again says these are defaults, not religious rules.

That should be preserved in the final lens.

---

# Chapter 12 — Objects and Data Structures

## Source thesis

This chapter is particularly important for EngSense because it rejects a universal "objects everywhere" position.

It contrasts:

- **objects** — expose behavior, hide representation;
- **data structures** — expose representation, carry little or no meaningful behavior.

Neither is universally superior.

## Getters/setters are not automatic abstraction

The source explicitly rejects the idea that private fields plus trivial getters/setters automatically create good encapsulation.

EngSense extraction:

> Encapsulation is about protecting a representation/decision, not accessor syntax.

A transparent DTO may be more honest than a pseudo-object whose accessors merely expose every field.

## Data/Object Antisymmetry

The central trade-off is change direction.

If the system is more likely to gain **new types/data representations**, object-oriented polymorphism can localize that change.

If the system is more likely to gain **new operations over stable data**, exposed data structures plus procedures/switching can localize that change better.

This is a major EngSense decision axis:

~~~text
variation_axis:
  types | operations | mixed | unknown
~~~

Do not choose OO/procedural/data-oriented structure without asking what is expected to vary.

## Law of Demeter / Tell the Other Guy

The useful generalization is not "never use dots."

It is:

- avoid navigating through object internals merely to assemble the resources needed for an operation;
- when an object owns the capability/invariant, prefer asking it to perform the operation.

This must not be applied mechanically to DTOs/data structures, where traversal is the intended model.

## DTOs are legitimate

The source explicitly recognizes DTOs as useful at database, message, socket, and translation boundaries.

This directly supports EngSense's rule against wrapping plain data in pointless getter/setter layers.

## ORM limitation framing

The source treats object behavior and relational data structure as fundamentally different representations. An ORM can translate/load data, but should not be mistaken for eliminating the conceptual boundary.

EngSense extraction:

Keep persistence representation and domain behavior conceptually distinct when their change forces differ.

## Switch statements revisited: major correction to earlier chapters

Earlier chapters strongly favor polymorphism for repeated switches. Chapter 12 adds the crucial trade-off.

Polymorphism is beneficial when new **types** are the likely change.

Procedural switching is beneficial when new **operations** over existing types are the likely change.

The source explicitly says not to force OO into areas where behavior is more volatile than data.

This means EngSense's Clean Code lens must **not** contain:

~~~text
switch/if chain
→ replace with polymorphism
~~~

Instead:

~~~text
identify dominant variation axis
→ choose representation that localizes that change
~~~

## Performance qualification

The source acknowledges that switch-based dispatch can be faster than polymorphic dispatch and permits local departures from OCP/DIP when nanoseconds materially matter.

Candidate rule:

Prefer architecture for changeability by default, but allow measured hot paths to use a more direct representation without forcing the whole system into the same style.

---

# Cross-chapter synthesis from Chapters 7–12

## 1. "Small functions" must become a conditional heuristic

A faithful EngSense interpretation is:

~~~text
Prefer extraction when:
- it reveals a meaningful abstraction;
- lowers mixed-abstraction reasoning;
- isolates a real change responsibility;
- improves navigation through naming.

Prefer locality/inlining when:
- extraction repeats implementation in the name;
- caller context must be carried mentally;
- ownership/state becomes scattered;
- hot-path cost is material;
- language idioms favor a direct form.
~~~

## 2. Variation axis is more important than pattern preference

Chapter 12 provides one of the strongest anti-dogma principles in the book:

~~~text
new types expected
→ behavioral polymorphism may localize change

new operations expected
→ transparent data + procedures may localize change
~~~

This should become a first-class EngSense context signal.

## 3. Error handling is language-sensitive

The book itself distinguishes Java/Python exception environments from Go's explicit returned-error model.

Therefore any EngSense source lens that emits language-independent "prefer exceptions" guidance would misrepresent the source.

## 4. DRY must be semantic

Textual similarity is not sufficient evidence for abstraction.

Use co-evolution/change responsibility to distinguish essential from accidental duplication.

## 5. Side effects should be reviewed as temporal coupling

The important question is not whether mutation exists but whether external observers must know hidden ordering/state requirements.

This will interact strongly with the Rust ownership/concurrency lens later.

## 6. Tests are architecture for change

Across the chapters, tests are not merely verification artifacts. Their design determines how safely production structure can evolve.

Useful quality dimensions:

- independent statement of behavior;
- change resilience;
- feedback latency;
- representation coupling.

---

# Additional eval candidates from Chapters 7–12

## Eval: "more than three args" false positive

Context:

A low-level numeric function naturally accepts four coordinates and the language/call site makes ordering clear.

Expected EngSense behavior:

- treat argument count as a signal only;
- do not invent an object with no semantic identity merely to satisfy a threshold.

## Eval: boolean flag with two real operations

Context:

`render(document, compact: true)` selects two independently meaningful public behaviors and callers frequently misread the call.

Expected:

- consider named variants/options or separate functions;
- judge language support for named arguments/options;
- do not ban boolean fields used as actual state.

## Eval: Rust Result vs Clean Code exception preference

Context:

Idiomatic Rust API returns `Result<T, E>`.

Expected:

- Rust language lens overrides the Java-centric exception preference;
- preserve typed error semantics;
- do not recommend exceptions/panics merely because Clean Code prefers exceptions to error codes in other languages.

## Eval: accidental duplication

Context:

Two similar validation blocks belong to unrelated domain actors and are already diverging.

Expected:

- preserve duplication;
- reject common helper extraction based solely on textual similarity.

## Eval: essential duplication

Context:

The same protocol framing logic appears in several places and must change together on every version update.

Expected:

- recognize a shared concept;
- centralize the invariant where doing so reduces synchronized-edit risk.

## Eval: externally pure mutable helper

Context:

A function uses local mutation internally but exposes deterministic output and no observable side effect.

Expected:

- do not flag it as impure merely because assignments exist;
- evaluate purity at the observable boundary relevant to callers/concurrency.

## Eval: OO vs procedural variation

Context A:
Many new variants are expected; operation set is stable.

Expected:
- favor a representation that localizes type extension.

Context B:
Data variants are stable; analysts continuously add new operations.

Expected:
- consider transparent data/procedural/data-oriented processing;
- do not force a method onto every type for each new operation.

## Eval: DTO pseudo-encapsulation

Context:

A transport model has private fields and one-to-one getters/setters with no invariants.

Expected:

- recognize it as data;
- do not add ceremony solely to appear object-oriented;
- preserve validation at the actual boundary where it belongs.

# Chapter 13 — Clean Classes

## Source scope

This chapter, by Jeff Langr, carries the earlier function-level ideas upward to classes/modules.

It explicitly separates **class/module design** from file layout. Files are packaging units; the engineering concern is how related concepts are grouped and how they change.

## Quality is assessed under change

One of the strongest claims in the chapter is that class quality becomes visible when requirements change.

Useful EngSense signals include:

- how many existing modules must be opened for a feature;
- whether unrelated policies change together;
- whether defects rise as the system grows;
- whether the class name still summarizes its responsibilities;
- whether isolated behavior is independently testable.

This aligns with EngSense's existing focus on change cost rather than static pattern compliance.

## SRP without speculative decomposition

The chapter favors small, cohesive, single-responsibility classes, but explicitly says SRP does **not** require guessing every future reason to change.

A particularly useful source rule is:

> do not roam the codebase creating speculative classes; use real change requests as evidence and reshape the design when an independent axis of change appears.

### EngSense extraction

~~~text
observed independent change pressure
→ evidence for decomposition

imagined possible future change
→ not sufficient by itself
~~~

This is strong support for evidence-driven abstraction.

## Tiny classes and overengineering

The source defends small classes and argues that class creation is cheap, but also acknowledges the "ravioli" extreme and says design principles require balance.

The chapter's own Beck-rule discussion notes that minimizing the number of elements acts as a counterpressure against useless micro-abstractions.

EngSense must preserve both sides:

- large multipurpose modules hide reasons to change;
- tiny modules with no useful boundary create navigation and conceptual overhead.

## Policy vs implementation detail

The chapter distinguishes:

- orchestration/policy;
- implementation-specific domain/utility behavior.

It recommends avoiding classes that mix both when they change for independent reasons.

EngSense extraction:

Separate policy from detail when it creates a real stability/change boundary. Do not create delegation layers merely because "policy" and "implementation" can be named separately.

## OCP as observed change locality

The chapter strongly favors classes that can become closed to modification while new behavior is added through extension.

But the most useful operational question is simpler:

> How many existing classes did the last feature force us to edit?

This should be an EngSense diagnostic, not a requirement to make every class plugin-like.

## Testing public concepts, not implementation fragments

When a new extracted strategy becomes a meaningful reusable/public concept, focused tests can document it directly.

When an extracted class is only a private implementation detail, the source advises against exposing it merely for testing.

Candidate rule:

> Do not distort visibility boundaries just to unit-test internal mechanics. Test stable behavioral concepts at the narrowest meaningful public boundary.

## AI section — source position, not EngSense fact

The chapter argues that modular, small, testable units are advantageous for AI-generated code because failures are easier to localize and generated modules can be verified through tests.

The source also makes speculative claims about future AI capability and error rates. EngSense must treat those as author opinion, not validated engineering facts.

Useful extraction that does survive:

- AI-generated code still requires behavioral verification;
- examples/tests can constrain generation;
- modular boundaries can reduce verification scope;
- generated code does not remove the need for architecture.

---

# Chapter 14 — Testing Disciplines

## Source thesis

The chapter broadens the first edition's TDD-only position and presents **three acceptable testing disciplines**:

1. TDD;
2. Test && Commit || Revert (TCR);
3. Small Bundles.

Martin remains personally committed to TDD, but explicitly says other disciplines can be compatible with clean code and that there may be more.

That is important for EngSense: the source itself rejects a single mandatory ritual.

## TDD

The source describes the three laws as a seconds-scale feedback loop:

- no production code without a failing test;
- write only enough test to fail;
- write only enough production code to make the current failure pass.

EngSense should record this as the source's strongest testing discipline, not as a universal rule.

## TCR

TCR permits code/test ordering freedom but automatically commits passing states and reverts failing states.

The engineering property of interest is **very small recoverable steps**, not the specific tool ritual.

## Small Bundles

Ousterhout's Small Bundles approach uses a longer cycle—minutes rather than seconds—and allows code-first, test-first, or interleaved work, provided each small bundle ends with strong coverage and all tests passing.

This is a major cross-source bridge.

### EngSense extraction

The common invariant across the three approaches is:

~~~text
bounded change
+ nearby verification
+ frequent known-good state
+ low rollback/debug distance
~~~

EngSense should optimize for those properties rather than enforcing one ceremony.

## Strategic design vs tactical discipline

The chapter explicitly says testing disciplines do not replace strategic design.

Martin states:

- upfront thinking is important;
- months of design without code is harmful;
- code without strategic thinking is also harmful;
- TDD can help with low-level design but does not guarantee good architecture.

This directly prevents a common misuse:

~~~text
tests are green
→ design must be good
~~~

False.

## Disciplines are not universally applicable

The chapter says these disciplines should be taken seriously but not followed blindly.

EngSense candidate rule:

> Treat process disciplines as tools with intended safety properties. Preserve the safety property when context requires a different ritual.

## Untestable boundaries

The source identifies practical testing limits around:

- hardware/UI boundaries;
- external I/O;
- third-party frameworks;
- subjective outputs.

Its response is to keep hard-to-test boundary code thin and push testable intelligence inward (Humble Object style).

EngSense should preserve the architectural idea without pretending all external behavior is literally untestable; modern integration, browser, snapshot, hardware-in-loop, and contract tests may change what is practical in a given repository.

---

# Chapter 15 — Clean Tests

## Source thesis

The chapter summarizes good tests as:

- readable;
- fast;
- isolated;
- repeatable;
- self-verifying;
- timely;
- designed.

Test code is treated as production-critical engineering infrastructure, not disposable support code.

## Readability and test DSLs

The source encourages refactoring test setup/assertion noise into a domain-specific testing API.

Useful forms include:

- helpers that express domain setup;
- composed assertions;
- composed results;
- Arrange / Act / Assert.

The goal is not abstraction for its own sake; it is to let the test state its behavioral intent without drowning in irrelevant setup mechanics.

## Dual standard

The source permits test code to make different performance/resource trade-offs from production code.

That is not a license for dirty tests.

EngSense extraction:

~~~text
production constraints != test constraints
quality/readability requirements still matter
~~~

For example, a test may allocate freely when production cannot, if that makes intent clearer and test runtime remains acceptable.

## Single Assert → Single Act

The chapter corrects a common interpretation.

"One assert" does not mean one assertion statement. Multiple assertions may verify one logical outcome.

The stronger rule is **Single Act**:

- arrange;
- perform one action;
- verify its resulting behavior.

This reduces causal ambiguity and test dependence.

## FIRST

The source's memory aid:

- Fast;
- Isolated;
- Repeatable;
- Self-validating;
- Timely.

EngSense should use these as diagnostic dimensions, not checkbox dogma.

## Test-suite coupling

A test suite is poorly designed when one production change forces broad unrelated test rewrites.

This mirrors production change coupling.

Candidate metric/question:

~~~text
one behavior/API change
→ how many unrelated tests must be edited?
~~~

Broad blast radius may indicate tests are coupled to incidental implementation structure.

---

# Chapter 16 — Acceptance Testing

## Source thesis

The chapter treats executable acceptance tests as a formal representation of requirements and definition of done.

Its strict form involves business analysts and QA producing feature-level specifications/tests shortly before implementation, with developers automating them.

## EngSense extraction

The durable principle is not the exact BA/QA role assignment.

It is:

> important requirements should have executable, reviewable evidence that the implemented system satisfies them.

Useful forms can include:

- acceptance tests;
- executable examples;
- BDD/Given-When-Then;
- contract tests;
- conformance vectors;
- scenario tests.

## Requirements as tests — qualification

The source makes a strong claim that the acceptance tests are the "true requirements."

EngSense should not flatten all requirements into tests.

Some requirements are difficult to encode as simple pass/fail acceptance cases:

- usability;
- accessibility;
- security properties;
- latency distributions;
- organizational constraints;
- legal/compliance requirements;
- long-horizon operability.

Candidate EngSense rule:

> Use executable acceptance evidence wherever the requirement is meaningfully testable, but retain non-executable constraints explicitly rather than pretending they do not exist.

## Definition of done and continuous build

Once an acceptance test passes, the source expects it to join the continuously executed suite.

A previously green requirement becoming red is treated as an immediate regression signal.

EngSense extraction:

Acceptance evidence should become durable regression evidence, not a one-time signoff artifact.

---

# Chapter 17 — AIs, LLMs, and God Knows What

## Source framing

This chapter is the author's 2025-era view of programming with LLMs.

It mixes:

- historical analogy;
- observed prompt/generation examples;
- engineering recommendations;
- speculative claims about AI cognition and future labor.

EngSense must separate these categories carefully.

## Durable engineering observation: prompts are specifications with ambiguity

The example demonstrates that a natural-language prompt can leave core terms underspecified, such as definitions and behavioral edge cases.

A regenerated solution can also differ substantially from the previous solution while still appearing plausible.

EngSense extraction:

For non-trivial AI-generated software, do not rely on one prose instruction as the sole behavioral oracle.

Use redundant/independent evidence such as:

- explicit definitions;
- constraints;
- examples;
- executable scenarios;
- tests;
- schemas/contracts;
- invariants.

## "Overloading" intent

The source uses "overloading" to mean stating intent in more than one independent form so inconsistency can reveal errors.

This maps naturally to EngSense:

~~~text
prose requirement
+ executable example/test
+ type/schema/invariant where appropriate
→ stronger specification evidence
~~~

The important property is **independence**. Having an LLM generate both implementation and tests from the same ambiguous interpretation can reproduce the same misunderstanding.

## Generated tests are not automatically trustworthy

The chapter's example shows generated tests and generated implementation failing to agree with intended semantics.

Candidate EngSense rule:

> Tests generated by the same model from the same prompt are evidence, but not independent validation unless a human, separate specification, oracle, or other independent mechanism verifies them.

This is particularly relevant to coding-agent workflows.

## Source claims that EngSense must NOT adopt as established fact

The author argues that current LLMs are statistical rather than inferential and concludes they do not reason. That is an author's technical/philosophical claim, not something this source alone establishes for EngSense.

Likewise, predictions about programmer employment and future AI capability are outside EngSense's code-quality mandate.

EngSense should extract the engineering lesson—ambiguity and verification risk—without embedding the author's broader AI predictions as rules.

## AI does not remove engineering discipline

The source's most useful conclusion for EngSense is that increasing generation capability raises the importance of:

- precise constraints;
- formalizable contracts;
- independent verification;
- tests;
- architecture and modularity.

That aligns with EngSense's role as a judgment layer around generated as well as human-written code.

---

# Cross-chapter synthesis from Chapters 13–17

## 1. Change evidence should drive decomposition

Chapter 13 strengthens a recurring principle:

~~~text
speculative future variation
≠ sufficient abstraction evidence

observed independent change axes
= strong abstraction evidence
~~~

## 2. Testing discipline is about feedback distance

TDD, TCR, and Small Bundles differ in ritual but share a deeper property: the distance between a known-good state and a defect is kept small.

EngSense should reason about **feedback latency** and **rollback distance**, not prescribe TDD universally.

## 3. Test architecture is real architecture

Tests have:

- coupling;
- APIs;
- abstraction levels;
- change blast radius;
- performance constraints;
- maintenance costs.

A production architecture that can change safely while its tests shatter on every refactor is not actually easy to evolve.

## 4. Executable specifications are powerful but incomplete

Acceptance tests are strong evidence for testable behavior.

They do not eliminate the need to model non-functional and qualitative constraints separately.

## 5. AI-generated artifacts require independent evidence

Authorship is irrelevant to correctness.

For generated code, generated tests, prompts, and model-produced design, EngSense should ask:

~~~text
what is the independent oracle?
what invariant is checked?
what evidence would detect a shared misunderstanding?
~~~

This is stronger than merely asking whether "the AI wrote tests."

---

# Additional eval candidates from Chapters 13–17

## Eval: speculative SRP split

Context:

A cohesive class has one current change axis. A reviewer invents four hypothetical future policies and proposes four classes now.

Expected:

- reject speculative decomposition;
- preserve current cohesion;
- define observable change pressure that would justify extraction later.

## Eval: real SRP split discovered by change

Context:

Two policies in one service repeatedly change independently for different requirements.

Expected:

- identify independent reasons to change;
- separate them behind meaningful boundaries;
- avoid preserving the monolith only for file-count simplicity.

## Eval: green tests do not prove good design

Context:

A deeply coupled module has excellent coverage and all tests pass.

Expected:

- credit verification strength;
- still evaluate coupling/change cost separately;
- do not use test success as proof of architecture quality.

## Eval: test suite mirrors implementation

Context:

A small refactor preserving behavior breaks hundreds of unit tests because they directly assert private call sequences.

Expected:

- identify test-design coupling;
- move tests toward stable behavioral contracts where appropriate;
- preserve implementation-level tests only when those implementation details are themselves important contracts.

## Eval: generated code + generated tests share ambiguity

Context:

One coding agent generates implementation and tests from the same underspecified prompt; all tests pass.

Expected:

- do not treat green tests as independent proof;
- inspect the original requirement ambiguity;
- add an independent scenario/invariant/oracle before claiming correctness.

## Eval: acceptance test cannot represent full requirement

Context:

An accessibility requirement is reduced to one DOM assertion.

Expected:

- recognize that the executable assertion covers only part of the requirement;
- retain additional accessibility checks/review rather than declaring the requirement fully specified.

# Research integrity notes

- The source is being read from a user-provided full-text copy.
- Completion is not claimed until every listed chapter, afterword, and appendix has been reviewed.
- Later sections may revise the early interpretations above.
- The future source-specific lens must distinguish Martin's claims from EngSense synthesis.
- Conflicts with Ousterhout, Fowler, Gjengset, Feathers, and other mandatory sources must remain explicit until those sources are also complete.

---

# Next research pass

Part I (Code) is now complete.

Continue with Part II (Design):

1. Chapter 18 — Simple Design;
2. Chapter 19 — The SOLID Principles;
3. Chapter 20 — Component Principles;
4. Chapter 21 — Continuous Design;
5. Chapter 22 — Concurrency.

Then continue into Part III (Architecture). Source-specific conclusions still remain provisional until Parts II–IV and the appendix debate are complete.

Do not create the final Clean Code lens or mark Issue #2 complete until the full source has been studied.
