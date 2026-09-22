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
```

The validator checks:

- valid JSON;
- unique IDs;
- required fields;
- supported modes;
- supported authority levels;
- non-empty expected/unacceptable property lists.

It does not judge model quality. Behavioral scoring will be added separately.

## Current cases

1. Premature interface
2. Real provider boundary
3. Large cohesive function
4. Unstable duplication
5. Public API observable compatibility

These cases intentionally include both over-engineering and under-engineering traps.
