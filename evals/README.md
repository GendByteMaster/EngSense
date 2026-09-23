# EngSense Evals

EngSense evals are deterministic scenario specifications for testing engineering judgment.

They do **not** require an answer to match one exact paragraph. They evaluate whether the answer preserves the expected decision properties and avoids known failure modes.

## Goals

The eval suite should detect whether EngSense:

- identifies the actual engineering problem rather than applying a slogan;
- uses repository/task context;
- distinguishes evidence from assumptions;
- names the relevant trade-off;
- avoids premature abstraction and premature simplification;
- respects public compatibility and specialist invariants;
- suppresses preference-only review noise;
- chooses an appropriate authority level;
- provides a verification path;
- records a concrete revisit trigger when useful.

## Case format

Each case is a JSON document under `evals/cases/`.

Required fields:

- `id`
- `title`
- `mode`
- `task`
- `context`
- `evidence`
- `tempting_wrong_recommendation`
- `expected_decision_properties`
- `unacceptable_reasoning`
- `expected_quality_dimensions`
- `expected_authority`
- `verification_expectations`

Optional fields:

- `snippet`
- `expected_tradeoffs`
- `revisit_when`
- `specialist_boundary`
- `notes`

## Evaluation model

An evaluator should score properties, not wording.

A response passes a case when:

1. all mandatory expected decision properties are present;
2. none of the unacceptable reasoning patterns drive the decision;
3. the recommendation is compatible with the evidence in the fixture;
4. authority/severity is not inflated beyond the evidence;
5. verification is appropriate to the risk.

Do not require the model to use the exact vocabulary in the fixture.

## Running structural validation

Run:

```bash
python evals/validate.py
python evals/validate_skill.py
```

`validate.py` validates fixture structure.

`validate_skill.py` validates the static Skill package itself: module references, required files, contiguous eval numbering/counts, and the invariant that EngSense does not acquire an API-key/model-provider runtime.

The validator checks:

- valid JSON;
- unique, well-formed IDs;
- required fields;
- unknown fields;
- supported modes;
- supported authority levels;
- required non-empty string lists;
- optional list/string field shapes.

It does not judge model quality. Behavioral scoring can be performed externally when needed.

## Current cases

1. Premature interface
2. Real provider boundary
3. Large cohesive function
4. Unstable duplication
5. Public API observable compatibility
6. Rust Java-style trait/factory layering
7. TypeScript discriminated union vs class hierarchy
8. Python enterprise-style CRUD layering
9. Distributed retry/idempotency specialist boundary
10. Security-sensitive authentication refactor
11. Vertical-slice locality vs strict horizontal layering
12. Unbounded queue and missing backpressure
13. Rolling persistence migration compatibility
14. Chatty remote API / RPC granularity
15. Test-double overuse against a cheap deterministic dependency
16. Known future scale ceiling without current pressure
17. Bounded measured performance escape hatch
18. Complexity displacement from a shared invariant into callers
19. Large multi-responsibility function
20. Stable duplicated invariant abstraction opportunity
21. Benchmark driver saturation / measurement validity
22. Aggregate performance score hides a critical workload regression
23. Network round-trip dominated latency vs local CPU rewrite
24. Zero-copy backing-buffer retention
25. High-consequence rewrite proposed for structural cleanliness
26. Indefinite old/new implementation coexistence
27. Mature tested subsystem with a credible rewrite path
28. Coordinated cross-cutting representation migration
29. Internal runtime object graph used as durable storage
30. Dependency order discovered through retry instead of an explicit graph
31. Human CLI presentation scraped as a machine protocol
32. Normalization layer erases a provider capability required for correctness
33. Cohesive function should not be split by line count
34. Preserve non-obvious rationale in the right information channel
35. TDD vs disciplined small bundles
36. High coverage without semantic confidence
37. Data/operations vs polymorphism from the dominant variation axis
38. Unsafe Rust without an explicit safety proof
39. Relaxed atomic ordering used for security-sensitive publication state
40. Detached async task lifecycle / durability mismatch
41. FFI handle marked `Send` without a foreign thread-safety contract
42. False `no_std` compatibility inferred from the crate attribute alone
43. Macro used where type-level variation belongs in generics
44. Self-referential/raw-pointer design versus index/arena representation
45. Cargo feature-composition failure under feature unification
46. Repeated business invariant needs an authoritative domain home
47. Straightforward CRUD should not be escalated into rich domain architecture
48. In-process concurrency should not be treated as a distributed system without a remote failure boundary

The suite intentionally includes:

- over-engineering traps;
- under-engineering traps;
- language-pattern transfer traps;
- specialist-boundary cases;
- compatibility risks;
- conflicting-principle scenarios.
