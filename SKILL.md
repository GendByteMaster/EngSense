---
name: engsense
description: Context-aware software engineering judgment for code review, refactoring, architecture, API design, maintainability, testability, and engineering trade-offs. Use when a task requires deciding between competing software-design principles or evaluating whether a structural change is justified. Do not use for purely mechanical formatting, trivial renames, or as a replacement for specialized security, performance, database, distributed-systems, or UI review.
---

# EngSense

EngSense is an engineering-judgment skill, not a style checklist.

Its job is to choose context-appropriate engineering trade-offs while preserving behavior and specialized invariants.

## Core rule

Do not ask:

> Which software-engineering rule should I apply?

Ask:

> Given this language, architecture, invariants, evidence, risks, lifecycle, and change scope, which option gives the best total engineering trade-off?

Do not optimize for one scalar "quality score."

## Activate EngSense when

Use this skill for tasks involving one or more of:

- code-structure or maintainability review;
- refactoring decisions;
- abstraction boundaries;
- API shape or compatibility;
- modularity, coupling, cohesion, locality, or discoverability;
- duplication versus abstraction;
- interface/trait extraction;
- testability and test-strategy trade-offs;
- migration/deprecation/change-cost decisions;
- architecture-quality review;
- over-engineering or under-engineering concerns;
- a conflict between two reasonable engineering principles.

Do not escalate a trivial task into an architecture review.

For mechanical formatting, syntax, simple renames, obvious lint fixes, or deterministic checks, use the appropriate tool directly instead of EngSense reasoning.

## Non-goals and deferral

EngSense does not replace specialist review.

If a decision materially depends on any of the following, preserve the relevant invariants and load the matching EngSense domain module where available, then request deeper specialized guidance when correctness depends on specialist semantics:

- cryptography, authentication, authorization, or security boundaries;
- performance claims that require profiling/benchmarking;
- database transactions, durability, or migration correctness → `domains/persistence.md`;
- distributed-system semantics such as retries, idempotency, consistency, ordering, deduplication, or quorum behavior → `domains/distributed-systems.md`;
- concurrency memory ordering, synchronization, atomicity, or happens-before → `domains/concurrency.md`;
- API/protocol compatibility → `domains/api-design.md`;
- test strategy/fidelity → `domains/testing.md`;
- UI/UX-specific design;
- legal/compliance requirements.

EngSense may still review structure around those concerns, but must not simplify away specialist semantics.

## Progressive disclosure

Start with:

1. this file;
2. `decision-framework.md`;
3. `review-workflow.md` when reviewing code or a change;
4. `languages/general.md` when language idioms materially affect the choice;
5. the matching language module for Rust, TypeScript, or Python when relevant;
6. only the references relevant to the decision.

Load `references/conflicts.md` whenever valid principles pull in different directions.

Do not load every reference for every task.

Current language modules:

- `languages/general.md`
- `languages/rust.md`
- `languages/typescript.md`
- `languages/python.md`

Current domain modules:

- `domains/api-design.md`
- `domains/testing.md`
- `domains/concurrency.md`
- `domains/persistence.md`
- `domains/distributed-systems.md`

Load them only when the task crosses the corresponding boundary.

Current research-grounded principle lenses:

- `principles/sustainable-engineering.md`
- `principles/empirical-architecture.md`
- `principles/complexity-placement.md`
- `principles/evolution-and-compatibility.md`
- `principles/evidence-driven-abstraction.md`

Load only the lenses whose questions materially affect the decision.

Source-specific Clean Code, Ousterhout, Fowler, DDD, DDIA, Release It!, Code Complete, Legacy Code, and related lenses remain blocked until their mandatory full-book research is complete.

## Context first

For non-trivial decisions, identify the relevant subset of:

- task goal;
- language/runtime;
- code role: application, library, service, CLI, desktop, framework, protocol, persisted format, tooling, etc.;
- current architecture and repository conventions;
- behavioral invariants;
- public/observable compatibility surface;
- expected lifetime;
- current and expected scale;
- real variation axes;
- consumer/provider count;
- performance constraints and measured bottlenecks;
- failure consequences;
- trust/security boundaries;
- concurrency/persistence/distribution boundaries;
- test/CI capabilities;
- migration, deprecation, and removal cost;
- contributor/organization scale when relevant.

Do not invent missing constraints.

If an unknown materially changes the decision, lower confidence, inspect repository evidence, or state the assumption.

## Evidence hierarchy

Prefer concrete evidence over doctrine.

Relevant evidence can include:

- tests and executable behavior;
- repository history and existing callers;
- measured runtime/benchmark data;
- production/operational observations;
- documented product or API requirements;
- current architecture and dependency graph;
- migration history;
- user/contributor evidence;
- qualitative evidence;
- estimates and assumptions.

Label assumptions as assumptions.

Do not justify a non-trivial recommendation solely with:

- "best practice";
- a design-pattern name;
- an author's authority;
- style preference;
- hypothetical reuse.

## Guidance authority

Classify guidance before emitting it:

- **Invariant / hard gate** — correctness, safety, compatibility, or explicit project constraint with very high confidence.
- **Rule** — strongly scoped repository/platform requirement.
- **Strong recommendation** — high-confidence quality issue with material impact.
- **Guidance** — contextual improvement with real trade-offs.
- **Heuristic** — useful but defeasible.
- **Note** — informational/non-blocking.
- **Preference** — normally suppress.

The stronger the authority, the higher the evidence threshold.

## Finding acceptance gate

Before reporting a finding, ask:

1. Is it relevant to the requested scope?
2. Is it understandable?
3. Is it actionable?
4. Is it supported by evidence?
5. Does it improve a named quality dimension or preserve an invariant?
6. Is confidence appropriate to severity?
7. Is a deterministic tool better suited to detect or fix it?
8. Is it merely a personal/style preference?

Suppress low-value preference noise.

Do not maximize finding count.

## Quality dimensions

Select only dimensions affected by the decision.

Possible dimensions include:

- correctness;
- comprehension;
- cognitive complexity;
- cohesion;
- coupling;
- locality;
- discoverability;
- maintainability;
- evolvability;
- compatibility;
- testability;
- reliability;
- operability;
- reproducibility;
- deployability;
- human scalability;
- knowledge resilience;
- provenance;
- contributor accessibility;
- migration cost;
- removal cost;
- reversibility;
- extension safety;
- coordination cost;
- user impact.

Do not collapse them into one numeric score.

## Complexity placement

When claiming that a design is simpler, identify where complexity goes.

Ask:

- Who pays for the complexity?
- How many times is it repeated?
- Who must understand it?
- How often does it change?
- At what lifecycle stage is it paid?
- Did the change remove complexity or merely move it?

Common locations include:

- core implementation;
- each caller;
- each provider/adapter;
- build/deploy tooling;
- runtime operations;
- migration;
- contributors;
- users.

## Abstraction rule

Prefer evidence-driven abstractions.

A new abstraction is more justified when it protects at least one real property such as:

- multiple real implementations;
- an independently varying concern;
- a meaningful policy/provider/platform boundary;
- a stable domain concept;
- an external contract;
- a repeated invariant;
- a volatile dependency;
- a real substitution need;
- a repeated stable process;
- focused testability.

Do not add an interface, factory, adapter, strategy, framework, or plugin mechanism merely because another implementation might exist someday.

A boundary is not real if consumers still reach through it for hidden implementation context.

## Public surface rule

Raise the design threshold as surface inertia increases.

Think in levels such as:

`private → module → repository → organization → external API → protocol/persisted format → public ecosystem standard`

For high-inertia surfaces, explicitly evaluate:

- observable behavior;
- compatibility;
- versioning;
- migration;
- deprecation;
- rollback;
- consumer count;
- hidden dependencies.

## Reversibility rule

Do not call a decision reversible merely because another implementation could theoretically be written later.

Identify the actual reversal capability:

- theoretical;
- manual;
- tested;
- automated;
- staged/rollback-capable.

Tests, migration tooling, compatibility layers, version control, feature flags, and rollout/rollback systems are what make decisions reversible.

## Escape hatches

Do not reject an abstraction escape hatch automatically.

A bounded exception can be valid for:

- measured performance;
- required platform/native capability;
- protocol semantics;
- migration compatibility;
- operational constraints.

Prefer escape hatches that are:

- explicit;
- bounded;
- observable;
- justified;
- owned;
- testable;
- containable.

Treat hidden or unbounded escape hatches as architectural risk.

## Scale rule

Distinguish:

- current scale;
- expected scale;
- known scale ceiling;
- cost to cross the ceiling;
- migration trigger.

A simple design with a known future ceiling can be correct now.

Do not require infinite scalability.

## Review behavior

When reviewing code:

- report correctness/invariant risks first;
- report meaningful structural risks second;
- suppress style-only preferences;
- do not say "I would write it differently" as a finding;
- do not recommend broad rewrites when a smaller safe change addresses the problem;
- distinguish repository convention from universal engineering truth;
- preserve rationale for non-obvious decisions.

Use `review-workflow.md`.

## Decision output

For a non-trivial decision, use a compact record when useful:

- Context
- Goal
- Invariants
- Evidence
- Alternatives
- Trade-offs
- Decision
- Assumptions
- Verification
- Revisit when

Do not create ceremony for trivial changes.

## Research integrity

EngSense is research-informed but no source is an authority.

Current foundation rules are provisional until the mandatory research corpus is complete.

Do not attribute an EngSense rule to a book or author unless the repository research note actually supports that attribution.

Preserve unresolved disagreements instead of inventing consensus.
