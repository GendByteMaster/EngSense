# Representation Design Lens

Source basis: completed Software Engineering at Google, AOSA Volume 1, AOSA Volume 2, and POSA research.

Status: **research-grounded representation/design lens — not a substitute for database, protocol, compiler, or serialization specialists**

## Question this lens answers

> Does the chosen representation make the system's important relationships, invariants, and operations explicit—or does it force callers to reconstruct them through conventions, duplicated state, or repeated translation?

Use this lens when the engineering decision is dominated by how information is represented rather than by class/module shape alone.

Typical examples:

- dependency graphs;
- immutable history and mutable references;
- intermediate representations;
- persisted schemas;
- message/envelope formats;
- build metadata;
- resource catalogs;
- event/change logs;
- state machines;
- cache keys/entries;
- typed IDs and domain values.

## Representation is architecture

A representation can determine:

- which invariants are expressible;
- which operations are cheap or expensive;
- whether work can be replayed;
- whether state can be migrated;
- whether dependencies can be scheduled;
- whether provenance survives transformations;
- whether consumers can evolve independently;
- whether testing/verification can operate without hidden context.

Do not reduce architecture review to folders, classes, services, or function size when the data model is doing the real architectural work.

## Model real relationships directly

Prefer a representation that encodes the relationship the system must reason about.

Examples:

- dependency graph instead of trial-and-error execution order;
- DAG ancestry instead of naming conventions for history;
- explicit state machine instead of scattered boolean combinations;
- typed capability/variant instead of unsupported-operation placeholders;
- explicit provenance instead of inferred origin.

A representation is stronger when illegal or ambiguous states become harder to express.

## Avoid duplicated state

Duplicated state is risky when two fields/structures can disagree.

Ask:

- Is this fact already derivable from another authoritative structure?
- Can membership/relationship encode the state directly?
- Who updates both copies?
- What happens after partial failure?

Prefer one authoritative representation when derivation is cheap and reliable.

Do not eliminate deliberate redundancy used for performance/reliability without understanding synchronization and failure semantics.

## Stable semantic core

A small stable intermediate representation can create leverage when many front ends, transformations, or backends vary around it.

Benefits can include:

- simpler transformations;
- focused invariant checking;
- easier extension;
- independent producer/consumer evolution;
- optimization below/above the boundary.

But do not invent an IR merely because compilers use them.

A useful IR needs real semantic stability and multiple operations/consumers that benefit from it.

## Normalize at boundaries

Boundary normalization is useful when it removes incidental variance early.

Examples:

- bytes to text at ingress;
- device-specific protocol to normalized observations;
- file-format details to a stable domain object;
- external provider payload to a typed internal contract.

Normalize only incidental differences.

Do not erase domain information that downstream code needs for correctness.

## Human vs machine representations

Human-readable presentation and machine contracts often need different guarantees.

Human output may rely on:

- visual grouping;
- context;
- omitted repeated fields;
- prose-oriented formatting.

Machine interfaces need:

- explicit fields;
- stable boundaries;
- versionable semantics;
- unambiguous ordering/identity.

Do not make automation scrape presentation output when a machine contract is warranted.

## Persisted representation has high inertia

Persisted schemas, file formats, event logs, and user-created content can outlive the code that created them.

Before making an internal runtime object the durable format, ask:

- Is its schema explicit?
- Can it be versioned?
- Can older/newer readers coexist?
- Can it be migrated?
- Is language/runtime identity leaking into storage?
- Can consumers reconstruct meaning without loading implementation classes?

Avoid serializing opaque internal object graphs as long-lived public/persisted contracts merely because serialization is easy.

## Logical model vs physical optimization

Keep the logical representation understandable while allowing lower-level physical optimization when possible.

Examples:

- logical immutable objects with packed/delta storage underneath;
- expression trees compiled differently per backend;
- normalized domain data with optimized cache/index structures;
- dependency graph with optimized runqueue scheduling.

Do not force physical storage/performance detail into every consumer when it can remain behind a stable semantic boundary.

## Representation and performance

Representation may dominate performance through:

- copies;
- serialization;
- index shape;
- cache locality;
- allocation count;
- data movement;
- query scope;
- dependency scheduling.

Use the performance lens before changing representation purely for speed.

A faster representation may introduce:

- migration cost;
- more complex ownership;
- worse debuggability;
- compatibility inertia.

## Representation and migration

When a representation changes, review:

- old/new coexistence;
- conversion ownership;
- backfill;
- mixed-version semantics;
- rollback;
- version markers;
- corrupted/partial states;
- removal of compatibility shims.

Use the change-strategy lens when the transition itself is material.

## Provenance

Preserve origin and decision history when later users/operators need to answer:

- where did this value come from?
- which rule produced this outcome?
- which remote/source system owned it?
- which transformation changed it?
- which version produced it?

Provenance is especially valuable in:

- automated policy systems;
- migrations;
- infrastructure changes;
- remote/local data merging;
- event processing;
- debugging complex transformations.

## Representation-specific finding gate

Before recommending a new representation, identify:

- what relationship/invariant it makes explicit;
- what current ambiguity/duplication it removes;
- who produces and consumes it;
- lifetime and compatibility surface;
- migration cost;
- performance implications;
- validation/invariant checks;
- failure/corruption behavior.

If the representation only renames the same structure with more types/layers, the recommendation is weak.

## Specialist boundary

Escalate when correctness depends on:

- database-engine storage/index/transaction semantics;
- protocol wire compatibility;
- compiler/verifier correctness;
- cryptographic canonicalization/signing formats;
- lock-free/shared-memory layout;
- schema evolution with external independently deployed consumers.

EngSense should reason about representation trade-offs without pretending to verify those specialist semantics.

## Anti-rules

Do not say:

- "use a graph" because graphs are elegant;
- "serialize the object" because the language supports it;
- "normalize everything" if callers need the original distinctions;
- "one canonical model" when providers genuinely expose incompatible capabilities;
- "human-readable output is good enough for automation";
- "the storage representation should match the API object exactly";
- "duplicate state is always wrong" without checking performance/reliability synchronization needs;
- "make the format generic for future use" without real consumers or stable variation.
