# Empirical Architecture Lens

Source basis: completed *The Architecture of Open Source Applications, Volume 1* research.

## Question this lens answers

> Does this architecture fit the actual workload, product goal, ecosystem, and constraints, or only an abstract ideal?

Use this lens when a design is being judged mainly by:

- architectural purity;
- named patterns;
- layer count;
- abstraction count;
- stylistic consistency.

## Architecture drivers first

Identify the real drivers:

- workload;
- platform;
- protocol;
- user/contributor model;
- performance constraints;
- deployment environment;
- extension needs;
- compatibility surface;
- failure model;
- ecosystem dependencies.

Do not judge structure before understanding those constraints.

## Successful systems can contain deliberate impurity

Real systems may legitimately contain:

- native escape hatches;
- controlled layering violations;
- centralized components;
- specialized fast paths;
- custom DSLs;
- compatibility shims;
- mixed implementation techniques.

An exception is not automatically a defect.

Evaluate whether it is:

- explicit;
- bounded;
- justified;
- observable;
- maintainable;
- reversible/containable.

## Product goals can dominate elegance

Examples of legitimate dominating goals include:

- contributor accessibility;
- low-latency interaction;
- scientific throughput;
- protocol compatibility;
- platform-native UX;
- operational recoverability.

A more elegant design is not better unless it improves the actual goal profile.

## Historical context

Before removing an awkward design, ask:

- What constraint originally caused it?
- Does that constraint still exist?
- Has the threat model changed?
- Has the scale changed?
- Has the ecosystem changed?
- Is this intentional residue or accidental residue?

Do not preserve obsolete rationale automatically.

Do not rewrite historical code merely because today's environment differs.

## Simple now can be correct now

A design can be intentionally simple while carrying a known future ceiling.

Capture:

```text
current scale
known ceiling
probability of reaching it
cost to cross it
migration trigger
```

Do not demand infinite scalability.

## Real use should update architecture

Observed use can reveal:

- new variation axes;
- incorrect abstractions;
- missing capabilities;
- unnecessary generality;
- unanticipated workflows.

Use production/user evidence to revise architecture.

## Anti-rules

Do not:

- equate architecture quality with visual symmetry;
- reject all escape hatches;
- assume standards are always better than workload-specific design;
- assume a future limit means the current design is wrong;
- protect an original architecture after evidence invalidates its assumptions.
