# Change Strategy Lens

Source basis: completed Software Engineering at Google, AOSA Volume 1, AOSA Volume 2, and POSA research.

Status: **research-grounded change-strategy lens — not a substitute for source-specific Fowler/Feathers guidance**

## Question this lens answers

> Should this system be left alone, refactored incrementally, migrated in stages, changed in one coordinated transition, or replaced by a new implementation?

Use this lens when the main engineering risk is not the target design alone, but **how to move from the current state to the target state safely**.

Do not attribute this module to Martin Fowler or Michael Feathers; their mandatory full-book research is still open.

## Start from the current cost

Do not recommend restructuring only because the target architecture looks cleaner.

Identify the current material cost:

- repeated defects;
- high change cost;
- impossible extension;
- unsafe compatibility behavior;
- operational failure;
- performance bottleneck;
- blocked migration;
- security debt;
- untestable critical behavior;
- contributor/onboarding cost.

If the current structure is merely inelegant and stable, the best decision may be to leave it alone.

## Change-strategy options

Consider at least the strategies that are actually viable.

### Leave in place

Appropriate when:

- current cost is low;
- replacement benefit is speculative;
- migration risk is high;
- the structure is ugly but stable and well understood;
- a better alternative has not been demonstrated.

### Incremental refactor

Appropriate when:

- behavior can be preserved in small steps;
- verification exists at each step;
- old/new structure can coexist cheaply;
- boundaries can be improved without long-lived semantic duplication.

### Staged migration

Appropriate when:

- consumers/versions cannot move atomically;
- persisted/public/protocol surfaces have inertia;
- rollout/rollback matters;
- adapters, dual-read/write, backfill, or compatibility bridges are practical.

### Coordinated cross-cutting change

Appropriate when:

- the invariant/representation spans many tightly coupled components;
- mixed old/new states are more complex or dangerous than one coordinated transition;
- strong verification and rollback exist;
- the blast radius is understood.

Do not require every change to be decomposed into tiny steps when the transition state itself is the larger risk.

### Replacement / rewrite

Consider only when the evidence supports a new implementation more strongly than continued evolution.

A rewrite is not justified by code age, aesthetics, or framework preference alone.

## Rewrite-readiness model

A replacement becomes more credible as the following strengthen:

    behavioral_understanding
    verification_strength
    old_system_as_oracle
    replacement_advantage
    migration_and_cutover_plan
    rollback_or_reversal_path
    coexistence_cost_is_bounded
    user/operator_choice_is_clear
    ownership_and_maintenance_capacity

Weakness in several of these dimensions should lower confidence.

## Behavioral oracle

A mature old implementation can be valuable evidence during replacement.

Useful oracles include:

- regression tests;
- recorded/replayable production inputs;
- contract tests;
- old/new side-by-side outputs;
- stable externally observable behavior;
- migration fixtures;
- historical incidents.

Do not confuse "the old implementation exists" with "its behavior is correct." Known defects and accidental behavior should be classified explicitly.

## High-consequence threshold

Raise the evidence and verification threshold when failure can cause severe:

- data loss/corruption;
- patient/safety impact;
- security compromise;
- financial loss;
- irreversible compatibility break;
- widespread service outage.

In high-consequence code, structural cleanliness is weak evidence for a rewrite.

Prefer stronger:

- characterization/contract tests;
- staged rollout;
- explicit rollback;
- independent verification;
- migration rehearsal.

## Mixed-version and coexistence cost

Old/new coexistence is not free.

Track:

- duplicate implementations;
- compatibility bridges;
- dual-read/dual-write logic;
- operational branching;
- test matrix expansion;
- support burden;
- user confusion;
- duplicated bug fixes;
- removal conditions.

A rewrite that never completes can be worse than a less elegant incremental evolution.

## Staged migration design

A staged migration should define:

    discover consumers/state
    add compatible target capability
    support transition safely
    migrate/backfill
    prevent backsliding
    verify mixed-mode behavior
    move traffic/consumers
    remove old dependency
    delete bridge/compatibility code

Not every migration needs every step.

The important property is that the transition itself is designed.

## Compatibility inertia

Raise migration scrutiny for:

- public APIs;
- protocols;
- persisted schemas;
- plugin contracts;
- user-created content/languages;
- file formats;
- external automation.

User-created content can have stronger inertia than a documented API because the historical corpus may embody parser/behavior semantics.

## Temporary architecture is allowed

A stepping-stone architecture can be correct when it:

- reduces migration risk;
- makes progress independently verifiable;
- has a defined removal condition;
- does not become an unowned permanent layer.

Do not reject temporary adapters merely because they are not the final architecture.

## Rewrite communication is part of the design

When users or contributors can choose between old and new systems, define:

- supported choice;
- migration direction;
- deprecation state;
- cutover plan;
- long-term owner.

Technical coexistence without clear product guidance creates ecosystem debt.

## Refactoring and performance

Performance can justify structural change when the bottleneck is architectural, but use the performance lens first.

Examples:

- serialized ownership blocks parallelism;
- data representation forces repeated copying;
- process topology creates dominant round trips.

Do not use performance as a generic excuse to rewrite.

## Refactoring and security debt

"Do not add more" is insufficient when existing severe security debt remains reachable.

If a legacy mechanism violates a hard safety boundary, active removal may be required even when migration is expensive.

Route security semantics to specialist review.

## Reversibility

Classify actual reversal support:

    theoretical
    manual
    tested
    automated
    staged

"We can restore from Git" is not enough when:

- data has migrated;
- clients have upgraded;
- protocols changed;
- user content transformed;
- external systems depend on the new behavior.

## Finding gate

Before recommending a material rewrite or migration, identify:

- current cost;
- target benefit;
- affected invariants;
- behavioral evidence/oracle;
- compatibility surface;
- coexistence cost;
- migration/cutover path;
- verification;
- rollback/reversal;
- removal condition.

If these are absent, downgrade the recommendation.

## Revisit triggers

Reconsider a current strategy when:

- defects/change cost continue rising;
- a stable behavioral oracle becomes available;
- migration tooling improves;
- a public surface can be versioned;
- old/new coexistence cost exceeds benefit;
- a legacy security/correctness issue becomes material;
- a coordinated maintenance window becomes available;
- a replacement proves itself under representative traffic.

## Anti-rules

Do not say:

- "never rewrite";
- "rewrite because the code is old";
- "refactor only in tiny steps" when mixed-mode transition is the real risk;
- "keep backward compatibility forever";
- "ship old and new indefinitely and let users choose";
- "the new architecture is cleaner, therefore migration is worth it";
- "the old system can be deleted after the new code compiles";
- "rollback is easy because version control exists."
