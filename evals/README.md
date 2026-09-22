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
- unique, well-formed IDs;
- required fields;
- unknown fields;
- supported modes;
- supported authority levels;
- required non-empty string lists;
- optional list/string field shapes.

Structural validation does not judge model quality. Behavioral scoring is handled separately by `evals/run_behavioral.py`.

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

The suite intentionally includes:

- over-engineering traps;
- under-engineering traps;
- language-pattern transfer traps;
- specialist-boundary cases;
- compatibility risks;
- conflicting-principle scenarios.


## Behavioral runner

The behavioral runner executes each selected fixture against:

1. a **target** model/agent that receives the EngSense context plus only the visible scenario fields; and
2. a separate **judge** that receives the hidden rubric and the target response.

The target never receives:

- `expected_decision_properties`;
- `unacceptable_reasoning`;
- `expected_authority`;
- `verification_expectations`.

The judge scores properties rather than wording. The runner computes the final pass/fail result from:

- all expected decision properties being met;
- no unacceptable reasoning materially driving the answer;
- all required verification expectations being present;
- authority/certainty matching the evidence;
- specialist boundaries being respected.

Expected quality dimensions are recorded for diagnostics but are not an independent hard pass gate.

### Context modes

`--context-mode auto` is the default.

It loads the EngSense core plus language/domain/principle modules selected from deterministic scenario signals.

Other modes:

- `core` — root Skill + decision framework + review workflow + conflict matrix;
- `all` — all implemented language/domain/principle modules;
- `none` — scenario only, useful as a no-skill baseline.

The report records the exact context files loaded for every case.

### Command providers

Both target and judge can be arbitrary commands that read the prompt from standard input and write their response to standard output.

Example environment:

```bash
export ENGSENSE_EVAL_TARGET_PROVIDER=command
export ENGSENSE_EVAL_TARGET_CMD='your-agent-command'
export ENGSENSE_EVAL_JUDGE_PROVIDER=command
export ENGSENSE_EVAL_JUDGE_CMD='your-judge-command'

python evals/run_behavioral.py --case premature-interface --fail-on-eval-failure
```

The judge command also receives the required JSON Schema through the `ENGSENSE_EVAL_JSON_SCHEMA` environment variable.

`{case_id}` inside a command argument is replaced with the current fixture id.

### OpenAI Responses API provider

The runner also has a dependency-free OpenAI Responses API adapter.

Set `OPENAI_API_KEY` and pass model ids explicitly:

```bash
python evals/run_behavioral.py \
  --target-provider openai \
  --target-model <target-model> \
  --judge-provider openai \
  --judge-model <judge-model> \
  --case premature-interface \
  --fail-on-eval-failure
```

The runner does not hardcode model ids.

For judge calls it requests structured JSON output using the per-case judgment schema.

Responses are sent with storage disabled.

### Reports

By default, results are written to:

```text
evals/out/behavioral-results.json
evals/out/behavioral-results.md
```

The output directory is ignored by Git.

The JSON report preserves:

- target response;
- judge result;
- component-level pass/fail;
- loaded context files;
- provider/model or command metadata;
- aggregate counts.

### CI policy

Normal pull-request CI runs:

```bash
python evals/validate.py
python -m unittest discover -s evals/tests -p 'test_*.py'
```

It deliberately does **not** call paid/external models.

Full behavioral runs are explicit/manual so that cost, model choice, secrets, and nondeterminism remain visible.
