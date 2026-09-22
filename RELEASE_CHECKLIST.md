# EngSense v1.0 Release Checklist

This checklist separates **release packaging/documentation readiness** from **research completeness**.

A checked documentation item means the artifact exists and is internally consistent. It does not mean the mandatory research gate is complete.

## Current status

**Status: NOT READY FOR v1.0**

The Skill foundation is usable, but the mandatory source corpus and blocked source-specific lenses tracked in Issue #2 are not complete.

A pre-v1 development release may be reasonable once the repository is packaged and reviewed, but it must not claim the blocked source-specific coverage.

## 1. Skill structure

- [x] Root `SKILL.md` exists.
- [x] `SKILL.md` has `name` and `description` metadata.
- [x] Root Skill is a concise router rather than a giant checklist.
- [x] Decision framework exists.
- [x] Review workflow exists.
- [x] Principle modules are separated from language/domain modules.
- [x] References and research status are separated from runtime guidance.
- [x] Skill core does not depend on credentials, MCP servers, or model-provider SDKs.

## 2. Progressive disclosure

- [x] Language modules load only when language context matters.
- [x] Domain modules load only when the task crosses those boundaries.
- [x] Principle lenses have distinct questions/ownership.
- [x] Conflict matrix exists.
- [x] Specialist deferral is explicit.
- [x] Mechanical/trivial changes do not require full architecture analysis.

## 3. Current implemented guidance

- [x] General language-neutral guidance.
- [x] Rust guidance.
- [x] TypeScript guidance.
- [x] Python guidance.
- [x] API design domain guidance.
- [x] Testing domain guidance.
- [x] Concurrency domain guidance.
- [x] Persistence domain guidance.
- [x] Distributed-systems domain guidance.
- [x] Sustainable engineering lens.
- [x] Empirical architecture lens.
- [x] Complexity placement lens.
- [x] Evolution/compatibility lens.
- [x] Evidence-driven abstraction lens.
- [x] Performance engineering lens.
- [x] Change strategy lens.
- [x] Representation design lens.

## 4. Mandatory source-specific research gate

The following source-specific lenses must remain blocked until their repository research requirements are completed.

- [ ] Clean Code source-specific lens.
- [ ] Ousterhout / complexity source-specific lens.
- [ ] Fowler / refactoring source-specific lens.
- [ ] Pragmatic Programmer source-specific lens.
- [ ] Domain-Driven Design source-specific lens.
- [ ] Data-intensive systems source-specific lens.
- [ ] Production resilience / Release It! source-specific lens.
- [ ] Code Complete / construction-quality source-specific lens.
- [ ] Working Effectively with Legacy Code source-specific coverage.
- [ ] Architecture trade-off source-specific coverage required by Issue #2.
- [ ] Rust for Rustaceans source-specific coverage.
- [ ] Other mandatory sources tracked in Issue #2.

Do not mark these complete from summaries, excerpts, general knowledge, or unrelated sources.

## 5. Research integrity

- [x] Completed sources are tracked.
- [x] Blocked sources are tracked.
- [x] Completed research is separated from provisional guidance.
- [x] No book/author is treated as an absolute authority.
- [x] Cross-source synthesis is labeled as synthesis.
- [x] Long copyrighted passages are not copied into runtime guidance.
- [ ] Mandatory corpus gate from Issue #2 is complete.

## 6. Evals

- [x] Deterministic eval schema exists.
- [x] Structural validator exists.
- [x] CI validates fixtures.
- [x] Over-engineering traps exist.
- [x] Under-engineering traps exist.
- [x] Language-pattern transfer scenarios exist.
- [x] Specialist-boundary scenarios exist.
- [x] Performance/change-strategy/representation scenarios exist.
- [x] Current fixture set contains 32 scenarios.
- [ ] Final v1.0 fixture review after all mandatory source-specific lenses are added.

The eval folder remains lightweight development evidence. A model-execution platform is not part of the EngSense Skill.

## 7. Documentation

- [x] README.
- [x] Philosophy/design principles.
- [x] Usage guide.
- [x] Installation guide.
- [x] Example reviews.
- [x] Contribution guide.
- [x] v1.0 release checklist.
- [x] Source/research status reference.

## 8. Installation and packaging

- [x] Repository contains a valid `SKILL.md`-based Skill layout.
- [x] Codex repository-scope installation is documented.
- [x] Codex user-scope installation is documented.
- [x] ChatGPT installation flow is documented with current official references.
- [x] Supporting files are documented as required parts of the Skill.
- [x] Optional `agents/openai.yaml` metadata added; implicit invocation enabled; no tool dependencies declared.
- [ ] Final install smoke test in a clean Codex repository.
- [ ] Final install smoke test in a supported ChatGPT Skills surface, when available to the release tester.

## 9. Public repository readiness

- [x] Project purpose and non-goals are documented.
- [x] Contribution boundaries are documented.
- [x] Research status is visible.
- [ ] License selected and added if public redistribution is intended.
- [ ] Repository topics/description reviewed.
- [ ] Broken internal documentation links checked.
- [ ] Stale roadmap claims removed.
- [ ] Final spelling/terminology pass completed.

## 10. Final Skill behavior review

Before v1.0, manually verify representative scenarios:

- [ ] one implementation → avoids premature interface;
- [ ] multiple real providers → recognizes justified abstraction;
- [ ] cohesive long function → avoids line-count decomposition;
- [ ] multi-responsibility function → recommends meaningful decomposition;
- [ ] unstable duplication → tolerates duplication;
- [ ] stable duplicated invariant → recognizes centralization opportunity;
- [ ] simple CRUD → does not force rich domain architecture;
- [ ] complex domain → routes to relevant domain modeling lens once unblocked;
- [ ] distributed retry → preserves timeout/idempotency/failure semantics;
- [ ] security-sensitive refactor → defers specialist security semantics;
- [ ] measured performance escape hatch → allows bounded specialization;
- [ ] rewrite decision → evaluates behavioral oracle/migration/rollback;
- [ ] representation decision → preserves semantic capability differences.

These checks can be performed manually or with external test tooling. The tooling itself does not belong in the Skill.

## 11. Release decision

A v1.0 release requires all of the following:

- [ ] mandatory research gate complete;
- [ ] intended source-specific core lenses implemented;
- [ ] acceptance criteria in Issue #1 satisfied;
- [ ] final representative behavior review complete;
- [ ] installation smoke tests complete;
- [ ] documentation/repository audit complete;
- [ ] redistribution/license decision complete;
- [ ] release notes prepared;
- [ ] version/tag created only after the above gates pass.

## Pre-v1 development release

A pre-v1 tag/release may be created before the mandatory research corpus is complete if it clearly states:

- research is incomplete;
- source-specific blocked lenses are not implemented;
- current general lenses are based only on completed sources/synthesis;
- interfaces and guidance may still change before v1.0.

Do not label such a release `v1.0.0`.
