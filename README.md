# EngSense

**Context-aware software engineering judgment for coding agents.**

EngSense is a reusable Skill for code review, refactoring, architecture, API design, maintainability, testability, and engineering trade-offs.

It does not enforce one doctrine. Instead, it asks which trade-off dominates **in the current repository, language, lifecycle, risk profile, and change scope**.

> The goal is not maximum DRY, maximum abstraction, the smallest functions, or the most patterns. The goal is the best total engineering trade-off that preserves the required invariants.

## What EngSense does

EngSense helps an agent decide questions such as:

- Is an interface justified, or is it premature abstraction?
- Should duplicated code stay duplicated until the pattern stabilizes?
- Is a long function cohesive, or does it contain independent reasons to change?
- Should a subsystem evolve incrementally, migrate in stages, or be replaced?
- Is a performance-oriented escape hatch justified by evidence?
- Is complexity being removed, or merely pushed into callers, operations, migration, or support?
- Does a representation make the important invariant explicit?
- Which specialist boundary must be preserved before changing security-, persistence-, concurrency-, or distributed-systems-sensitive code?

## What EngSense is not

EngSense is not:

- a formatter or linter replacement;
- a style-enforcement checklist;
- a security or cryptography auditor;
- a performance profiler;
- a database-engine expert;
- a distributed-systems correctness verifier;
- a justification for rewriting code because another architecture looks cleaner.

It can recognize when one of those specialist reviews is required and should defer instead of guessing.

## Core model

~~~text
Task
  ↓
Understand the real problem
  ↓
Inspect relevant repository evidence
  ↓
Identify invariants and constraints
  ↓
Load only the relevant EngSense modules
  ↓
Identify competing principles
  ↓
Compare viable alternatives
  ↓
Choose the dominant trade-off
  ↓
Select a safe change strategy
  ↓
Verify
  ↓
Re-evaluate where complexity moved
~~~

The complete decision process lives in [decision-framework.md](decision-framework.md).

## Progressive disclosure

EngSense intentionally keeps [SKILL.md](SKILL.md) compact.

The root Skill acts as a router. It loads more detailed guidance only when the task needs it:

~~~text
SKILL.md
├── decision-framework.md
├── review-workflow.md
├── principles/
├── languages/
├── domains/
└── references/
~~~

Current research-grounded principle lenses include:

- Clean Code 2e source-specific engineering lens;
- sustainable engineering;
- empirical architecture;
- complexity placement;
- evolution and compatibility;
- evidence-driven abstraction;
- performance engineering;
- change strategy;
- representation design;
- reliability and operability.

Language modules currently cover Rust, TypeScript, Python, and general language-neutral guidance.

Domain modules cover API design, testing, concurrency, persistence, and distributed-systems engineering-quality boundaries.

## Example

A request says:

> Split this 180-line parser function into small functions because long functions are bad.

EngSense does not accept the premise automatically.

It checks whether the function has independent reasons to change, whether extraction improves comprehension, how much shared parser state exists, whether helpers become shallow wrappers, and whether locality is more valuable than decomposition.

The result can legitimately be:

~~~text
Decision:
Keep the cohesive parsing flow together.

Reason:
The function implements one sequential grammar operation and the proposed helpers
would primarily add navigation without isolating an independent invariant.

Revisit when:
Parsing, persistence, retry policy, or another independently changing responsibility
appears in the same function.
~~~

See [docs/USAGE.md](docs/USAGE.md) and [docs/EXAMPLE_REVIEWS.md](docs/EXAMPLE_REVIEWS.md) for more examples.

## Repository layout

~~~text
EngSense/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── decision-framework.md
├── review-workflow.md
├── principles/
├── languages/
├── domains/
├── references/
├── research/
├── evals/
├── docs/
├── CONTRIBUTING.md
└── RELEASE_CHECKLIST.md
~~~

The optional `agents/openai.yaml` file provides OpenAI Skill UI metadata and explicitly allows implicit invocation. EngSense declares no tool dependencies because its core workflow is instruction/reference based.

The deterministic fixtures under `evals/cases/` are development evidence for the Skill. They are intentionally lightweight and are not a model-execution platform.

## Research integrity

EngSense is research-informed, but books and engineering schools are treated as **lenses, not authorities**.

A source-specific lens is not added merely from summaries, quotations, reputation, or general model knowledge. The repository tracks source status in [references/source-status.md](references/source-status.md).

Completed full-text research currently includes:

- *Software Engineering at Google*;
- *The Architecture of Open Source Applications, Volume 1*;
- *The Architecture of Open Source Applications, Volume 2*;
- *The Performance of Open Source Applications*;
- *Site Reliability Engineering: How Google Runs Production Systems*;
- *Clean Code: A Handbook of Agile Software Craftsmanship, Second Edition*;
- *Rust for Rustaceans*.

Several planned source-specific lenses remain blocked until their required full-book research is complete. See [references/source-status.md](references/source-status.md).

## Install

EngSense follows the Agent Skills shape: a skill directory with a required `SKILL.md` and optional supporting resources.

### Recommended: install directly from GitHub with npx

Project scope for Codex:

~~~bash
npx skills add https://github.com/GendByteMaster/EngSense -a codex
~~~

Global/user scope for Codex:

~~~bash
npx skills add https://github.com/GendByteMaster/EngSense -a codex -g
~~~

The EngSense Skill source is GitHub; there is no separate EngSense npm package required.

Manual installation is also supported at:

~~~text
.agents/skills/engsense/
~~~

or user scope:

~~~text
~/.codex/skills/engsense/
~~~

The full folder must be available because `SKILL.md` references the supporting files in this repository.

For current ChatGPT installation and sharing options, see [docs/INSTALLATION.md](docs/INSTALLATION.md).

Official references:

- OpenAI — Build skills: https://developers.openai.com/docs/build-skills
- OpenAI Help Center — Skills in ChatGPT: https://help.openai.com/en/articles/20001066

## Documentation

- [Philosophy and design principles](docs/PHILOSOPHY.md)
- [Usage examples](docs/USAGE.md)
- [Installation](docs/INSTALLATION.md)
- [Example reviews](docs/EXAMPLE_REVIEWS.md)
- [Contributing](CONTRIBUTING.md)
- [v1.0 release checklist](RELEASE_CHECKLIST.md)

## Project status

The reusable Skill foundation, language/domain routing, conflict matrix, research-grounded general/source-specific lenses, and 45 deterministic eval fixtures are implemented.

EngSense is still **pre-v1.0** while the mandatory source corpus and blocked source-specific lenses remain incomplete. The release checklist records the remaining gates explicitly rather than treating unfinished research as complete.

## License

EngSense is licensed under the [MIT License](LICENSE).
