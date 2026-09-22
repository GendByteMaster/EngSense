# Complexity Placement Lens

Source basis: cross-source synthesis of completed Google SWE and AOSA Volume 1 research.

## Question this lens answers

> Did this design remove complexity, or merely move it—and who now pays for it?

"Reduce complexity" is too vague for many decisions.

A design can look locally simpler while distributing complexity across every caller, deployment, migration, or operator.

## Complexity locations

Track where complexity lives:

```text
core implementation
callers
providers/adapters
public API/protocol
build/deploy
operations
migration
compatibility/support
contributors
users
```

## Multiplicity matters

Ten lines of complexity in one well-owned module may be cheaper than two lines repeated in 100 consumers.

The opposite can also be true if the centralized module becomes:

- a bottleneck;
- a high-risk dependency;
- an overly generic framework.

Ask both:

- How much complexity?
- How many times is it paid?

## Typical displacement patterns

### Infrastructure → callers

Removing:

- transactions;
- joins;
- consistency guarantees;
- capability negotiation

can push responsibility into every application.

### Callers → central abstraction

A driver/provider layer can centralize repeated:

- platform logic;
- protocol normalization;
- compatibility behavior.

### Runtime → migration

A simpler new architecture may create an expensive transition period.

### Core → operations

A lean implementation can depend on manual deployment/recovery procedures.

### Product → security controls

Sometimes product/incentive design can reduce the need for complex technical enforcement.

## Evaluation template

For each alternative:

```text
Local complexity:
Repeated complexity:
Operational complexity:
Migration complexity:
Compatibility complexity:
Who owns it:
How often it changes:
Failure blast radius:
```

## Anti-rules

Do not say:

- "this removes complexity" without identifying what disappears;
- "fewer layers is simpler" if callers now duplicate invariants;
- "more abstraction is simpler" if the abstraction only hides flags and indirection;
- "NoSQL is simpler" without accounting for application-side semantics;
- "microservice extraction simplifies the module" without accounting for network/operations/migration.
