# Contributing to EngSense

EngSense is a context-aware software engineering Skill. Contributions should improve engineering judgment without turning the project into a universal checklist, style guide, or specialist replacement.

## Contribution principles

A good contribution should preserve these properties:

- context before doctrine;
- evidence before pattern names;
- explicit trade-offs;
- language/ecosystem awareness;
- specialist boundaries;
- progressive disclosure;
- low preference noise;
- research integrity.

Before adding guidance, ask:

> What real decision does this help an agent make, and under which conditions can the opposite recommendation also be correct?

If the answer is "this rule is always better", the contribution probably needs more context.

## Repository areas

### `SKILL.md`

Keep the root Skill concise.

It should primarily define:

- activation;
- scope/non-scope;
- routing;
- invariant preservation;
- evidence expectations;
- authority levels;
- specialist deferral.

Do not move full principle/domain material into `SKILL.md`.

### `principles/`

Principle files are decision lenses.

A principle should normally include:

- the question it answers;
- signals supporting different options;
- conflicts/trade-offs;
- anti-rules;
- revisit triggers;
- specialist boundaries when relevant.

A principle should not be a list of slogans.

### `languages/`

Language modules should encode ecosystem-specific engineering judgment.

Examples:

- language-native representation choices;
- abstraction mechanisms;
- ownership/lifetime models;
- runtime behavior;
- idiomatic module/type boundaries.

Do not transplant architecture from another language merely because the pattern name is familiar.

### `domains/`

Domain modules should help EngSense recognize engineering-quality concerns in areas such as:

- API design;
- testing;
- concurrency;
- persistence;
- distributed systems.

They must remain routing/judgment guidance rather than pretending to replace deep specialist verification.

### `references/`

Reference files capture:

- conflicts;
- smells;
- examples;
- source/research status.

Keep reference material composable and avoid duplicating entire principle files.

### `research/`

Research notes contain original summaries and EngSense-oriented synthesis.

Do not copy long copyrighted passages.

Preserve source disagreements and assumptions.

### `evals/`

Evals are deterministic judgment scenarios.

They are development evidence for the Skill, not a runtime platform.

Each case should define:

- task/context;
- evidence;
- tempting wrong recommendation;
- expected decision properties;
- unacceptable reasoning;
- expected quality dimensions;
- authority;
- verification expectations.

Run structural validation before opening a PR:

~~~bash
python evals/validate.py
~~~

## Research integrity

### Source-specific lenses

Do not create a lens named after a book/author/school until the required research status supports it.

For example, do not create a `refactoring-fowler.md` lens from:

- general model knowledge;
- web summaries;
- quotations;
- reviews;
- memory of the book.

If the full source has not been studied under the repository research policy, keep the lens blocked.

### Cross-source synthesis

General lenses may be created from completed sources when the repository clearly marks them as synthesis rather than pretending they are direct teaching from one unread source.

Current examples include:

- complexity placement;
- evidence-driven abstraction;
- performance engineering;
- change strategy;
- representation design.

### Source status

Update `references/source-status.md` when:

- a source is started;
- a source is completed;
- a source becomes unavailable;
- a lens becomes unblocked.

Do not mark research complete unless the defined research gate was actually met.

## Adding a principle lens

Before adding a new principle file:

1. identify the decision/question it owns;
2. confirm existing lenses do not already own it;
3. identify the completed research basis;
4. document competing signals;
5. include anti-rules;
6. define when specialist review is required;
7. add/adjust conflict-matrix entries;
8. add at least one eval when the new behavior is materially testable;
9. update `principles/README.md`;
10. update `SKILL.md` routing only if the lens needs explicit routing.

Avoid "lens explosion". A new file should provide a genuinely distinct decision surface.

## Adding a language module

A language module should answer questions that change because of the language/runtime.

Useful content includes:

- native abstraction tools;
- state modeling;
- ownership/resource lifetime;
- error model;
- concurrency model;
- type-system capabilities;
- common cross-language pattern mistakes.

Add an eval when the module is intended to prevent a specific pattern transfer.

## Adding a domain module

A domain module should focus on engineering judgment and routing.

For example, a persistence module may help preserve:

- migration;
- replay;
- compatibility;
- atomicity/durability boundaries.

It should not claim to prove a particular database engine's isolation behavior without database-specific evidence.

## Adding an eval

A useful eval contains a real tension.

Good:

- one provider vs hypothetical interface;
- stable shared invariant vs accidental duplication;
- public compatibility vs local cleanup;
- measured hot path vs strict layering;
- coordinated migration vs long-lived mixed state.

Weak:

- "bad code should be improved";
- a case with only one obviously valid answer and no tempting engineering failure mode;
- a style-only preference.

### Eval quality checklist

An eval should:

- have enough context to make a decision;
- avoid hidden required facts;
- contain plausible wrong reasoning;
- test behavior rather than exact wording;
- use authority appropriate to the evidence;
- specify verification.

## Documentation changes

Documentation should describe current repository behavior, not planned functionality as though it already exists.

When documenting external product behavior (for example ChatGPT or Codex installation), verify current official documentation before changing instructions.

## Pull requests

Keep PRs scoped.

A PR should explain:

- what decision capability is being added/changed;
- why the current Skill is insufficient;
- research/source basis when relevant;
- files changed;
- eval impact;
- specialist-boundary impact;
- what remains intentionally out of scope.

Do not mix unrelated refactors into a lens/documentation change.

## Review standard

Review contributions in this order:

1. research/source integrity;
2. correctness and specialist-boundary safety;
3. scope ownership;
4. conflicting-principle handling;
5. evidence quality;
6. progressive disclosure/context size;
7. eval coverage;
8. documentation consistency;
9. style.

Do not reject a contribution because a reviewer simply prefers another coding style.

## Commit style

Use concise conventional-style messages where practical, for example:

~~~text
feat(skill): add representation design lens
docs: add installation guide
test(evals): add migration tradeoff case
fix(skill): preserve specialist boundary for retries
~~~

## Before requesting merge

At minimum:

~~~bash
python evals/validate.py
~~~

Also verify:

- referenced files exist;
- `SKILL.md` remains concise;
- new guidance has an owner/module;
- no source-specific claim exceeds research status;
- README/docs reflect the actual implementation;
- Issue #1 / research status are updated when applicable.

## Scope discipline

The project should remain a Skill.

Do not add model orchestration, provider SDKs, authentication flows, agent hosting, or general-purpose evaluation infrastructure to EngSense unless the project scope is explicitly changed first.

External tooling can test EngSense without becoming part of the Skill itself.
