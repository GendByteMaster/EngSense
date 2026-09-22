# EngSense Philosophy

EngSense exists because software-engineering guidance is usually useful **conditionally**, not universally.

Rules such as "keep functions small", "remove duplication", "depend on abstractions", "hide implementation details", or "prefer microservices" can improve a system under the right conditions and make it worse under the wrong ones.

EngSense therefore treats engineering schools as **lenses**, not authorities.

## 1. Context before doctrine

The same design can be appropriate in one system and harmful in another.

Before recommending a structural change, EngSense should understand the relevant context:

- language and runtime;
- architecture and repository conventions;
- current and expected scale;
- lifetime and rate of change;
- compatibility surface;
- variation points;
- test/verification strength;
- concurrency and persistence model;
- distribution/network boundaries;
- failure consequences;
- migration and rollback constraints.

If a missing fact materially changes the decision, it should be treated as uncertainty rather than silently invented.

## 2. Solve the real problem

"Make it cleaner" is not a sufficient engineering problem.

A useful review starts from something concrete:

- duplicated changes repeatedly drift;
- callers reconstruct an invariant incorrectly;
- a public API leaks unstable representation;
- retries amplify load;
- a queue grows without bound;
- a migration cannot preserve rollback;
- an abstraction adds concepts but protects no real boundary.

If the only problem is aesthetic discomfort, EngSense should say so.

## 3. Minimize total engineering complexity

Local simplicity can create global complexity.

Removing ten lines from a central component is not a win if the responsibility moves into one hundred callers.

Adding an abstraction is not a win if it creates:

- factories;
- adapters;
- mode flags;
- new lifecycle states;
- migration burden;
- debugging indirection

without protecting a real invariant or variation axis.

EngSense asks both:

- How much complexity exists?
- Where is it paid, and how many times?

Relevant locations include:

~~~text
core
callers
providers
public API
build/deploy
operations
migration
compatibility/support
contributors
users
~~~

## 4. Evidence beats pattern names

Pattern names can help communication. They are weak evidence by themselves.

Stronger evidence includes:

- executable tests;
- actual callers and implementations;
- measured profiles/benchmarks;
- production traces and incidents;
- public contracts;
- persisted data;
- dependency graphs;
- migration history;
- observed recurring changes.

Weaker evidence includes:

- hypothetical future requirements;
- style preference;
- "best practice";
- analogy without repository evidence.

Recommendation strength should track evidence strength.

## 5. Conflict is normal

Many engineering principles are in legitimate tension:

- decomposition vs locality;
- DRY vs unstable abstraction;
- compatibility vs architectural correction;
- standardization vs workload-specific specialization;
- encapsulation vs transparent data;
- throughput vs latency;
- strict layering vs bounded escape hatch;
- incremental migration vs coordinated cutover.

EngSense does not assign a permanent winner.

The central question is:

> Which trade-off dominates in this context, and what evidence supports that conclusion?

## 6. Abstractions need pressure

An abstraction is more credible when it protects something real:

- multiple implementations;
- stable repeated variation;
- provider/platform boundary;
- repeated invariant;
- independently changing lifecycle;
- volatile dependency;
- meaningful combinatorial duplication;
- stable semantic representation.

An abstraction is less credible when:

- one implementation exists;
- substitution is hypothetical;
- an interface mirrors one concrete type;
- callers still need implementation details;
- flags are required to hide fundamentally different concepts;
- it exists mainly to make mocking convenient.

"Maybe someday" is not enough by itself.

## 7. Locality is a quality property

Small functions and modules are not automatically easier to understand.

Splitting cohesive behavior can increase:

- navigation;
- hidden state transfer;
- shallow wrappers;
- call-chain depth;
- cognitive context switching.

EngSense preserves locality when the code represents one cohesive algorithm or lifecycle.

It recommends decomposition when there are genuinely independent reasons to change.

## 8. Duplication is not one thing

Two similar code blocks may represent:

- the same stable invariant;
- coincidental similarity;
- requirements that are still diverging;
- an abstraction that has not yet earned its shape.

Temporary duplication can be safer than an unstable abstraction.

Stable duplicated invariants that repeatedly change together are stronger candidates for centralization.

## 9. Representation is architecture

Important architecture often lives in the representation of information, not only in folders, classes, or services.

Examples include:

- dependency graphs;
- state machines;
- persisted schemas;
- event/change logs;
- intermediate representations;
- provenance records;
- capability models.

A good representation can make invariants explicit and remove repeated reconstruction from callers.

A bad representation can hide required semantics or create long-lived compatibility debt.

## 10. Compatibility has inertia

A private helper and a public protocol should not receive the same compatibility policy.

Surface inertia rises with:

- external consumers;
- persisted data;
- protocols;
- plugin contracts;
- public ecosystems;
- user-created content.

Undocumented behavior may still be relied upon.

At the same time, compatibility is not automatically sacred. Broken or immature behavior can sometimes be corrected cheaply, especially before a surface becomes widely depended on.

## 11. Migration is part of design

A target architecture is incomplete if the path to it is ignored.

Material changes should consider:

- consumer discovery;
- old/new coexistence;
- conversion/backfill;
- version skew;
- rollback;
- cutover;
- backsliding prevention;
- deprecation;
- final removal.

Sometimes incremental change is safer.

Sometimes the mixed state created by an incremental migration is the larger risk, and a coordinated transition is better.

EngSense decides from the actual transition constraints.

## 12. Performance claims require scoped evidence

Performance is not one number.

Relevant dimensions may include:

- latency;
- throughput;
- memory;
- CPU;
- I/O;
- network round trips;
- energy;
- fairness;
- overload behavior.

EngSense distinguishes evidence scope:

~~~text
production/user observation
representative end-to-end benchmark
component/distributed benchmark
profile/trace under representative load
microbenchmark of a proven hot operation
static cost hypothesis
unsupported intuition
~~~

A microbenchmark can be valid for a narrow hot primitive, but it does not automatically prove end-to-end improvement.

Correctness, safety, durability, and security invariants outrank speed.

## 13. Reversibility must be real

"We can change it later" is not a rollback strategy.

Reversibility can be:

~~~text
theoretical
manual
tested
automated
staged
~~~

Real reversibility depends on things such as:

- tests;
- adapters;
- schema/version support;
- rollback tooling;
- feature flags;
- data backfill;
- deployment mechanics.

Version control alone cannot undo a migrated database or an external protocol adoption.

## 14. Human scalability matters

Architecture is used by people as well as machines.

EngSense considers:

- discoverability;
- contributor skill distribution;
- onboarding cost;
- knowledge concentration;
- review burden;
- repeated manual work;
- operational ownership.

A technically elegant design can be poor if it depends on one expert understanding hidden constraints forever.

## 15. Specialist boundaries are explicit

EngSense is an engineering-judgment layer, not a universal expert.

It should defer when correctness depends on specialist semantics such as:

- cryptography;
- authentication/authorization;
- lock-free memory ordering;
- database-engine isolation/durability;
- consensus/quorum guarantees;
- transport internals;
- legal/compliance requirements;
- specialized UI/UX constraints.

The Skill may identify the engineering trade-off around those concerns, but it should not invent specialist facts.

## 16. Use the weakest justified authority

Not every recommendation is a rule.

EngSense distinguishes:

- **Invariant / hard gate**
- **Rule**
- **Strong recommendation**
- **Guidance**
- **Heuristic**
- **Note**

Style preferences are normally suppressed.

This reduces false certainty and low-value review noise.

## 17. Progressive disclosure over giant prompts

The root `SKILL.md` should remain a router.

Only the relevant language, domain, principle, and reference modules should be loaded for a task.

This keeps the Skill:

- focused;
- composable;
- easier to update;
- less likely to drown important evidence in unrelated guidance.

## 18. Research integrity

EngSense separates:

- completed source-derived guidance;
- cross-source synthesis;
- provisional guidance;
- blocked source-specific lenses.

No source is treated as infallible.

No unread book is used as authority merely because its ideas are well known.

Disagreement between engineering schools should be preserved when the disagreement is materially useful.

## Definition of success

EngSense succeeds when the agent stops asking:

> Which engineering rule should I apply?

and instead asks:

> Given this language, architecture, invariants, evidence, risks, lifecycle, and change scope, which option gives the best total engineering trade-off?
