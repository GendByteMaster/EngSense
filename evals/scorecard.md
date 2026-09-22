# EngSense Behavioral Eval Scorecard

Use this rubric to judge an EngSense response against one case.

The goal is not exact wording. Score observable decision behavior.

## Mandatory gates

A response fails immediately if it:

- recommends the fixture's tempting wrong recommendation as its main decision;
- violates an explicit invariant in the fixture;
- invents evidence that is not in the case;
- treats a specialist-sensitive assumption as known when the case marks it uncertain;
- bases a blocking conclusion only on style preference or named doctrine.

## Property score

For each item in `expected_decision_properties`:

- **1** — clearly satisfied;
- **0** — missing, contradicted, or only implied too weakly to be actionable.

Required property score for a default pass:

```text
100% of mandatory expected_decision_properties
```

The initial suite intentionally keeps these lists short and high-signal.

## Reasoning-noise score

For each item in `unacceptable_reasoning`:

- **0** — absent;
- **1** — appears but is explicitly rejected/corrected;
- **2** — materially influences the recommendation.

Default failure condition:

```text
any unacceptable_reasoning item scored 2
```

## Authority check

The exact label does not need to match word-for-word, but the response should not exceed the fixture's evidence.

Examples:

- a `guidance` case should not become a universal invariant;
- a `strong_recommendation` case should not be reduced to a cosmetic note if evidence shows material risk.

## Trade-off check

When `expected_tradeoffs` is present, the response should make the relevant tension visible.

It does not need to use the exact phrase.

A decision that names only one side of the trade-off is weaker than one that explains why that side dominates under the fixture's evidence.

## Verification check

A pass requires at least one verification action that is appropriate to the stated risk.

The response should not substitute irrelevant checks.

Examples:

- compatibility case → inspect callers / compatibility tests;
- parser refactor → parser regression tests;
- provider abstraction → contract/provider tests.

## Revisit condition

When `revisit_when` exists, a strong response should preserve conditionality by naming at least one trigger or equivalent condition.

This is especially important for decisions such as:

- keeping concrete code today;
- tolerating duplication;
- accepting a scale ceiling;
- preserving a compatibility behavior.

## Suggested aggregate reporting

For a suite run, report:

```text
cases_passed / total_cases
mandatory_property_recall
unacceptable_reasoning_violations
authority_mismatches
verification_misses
preference_noise_findings
```

Do not collapse the final report into one "quality score" without preserving these dimensions.

## Regression principle

When EngSense changes, a previously passing case should only change decision when:

- the fixture evidence changes;
- a new research-backed rule legitimately changes the trade-off;
- the old expectation is explicitly revised with rationale.

Do not silently update fixtures to make a regression disappear.
