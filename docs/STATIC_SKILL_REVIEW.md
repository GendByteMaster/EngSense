# Static Skill Behavior Review

Date: 2026-09-23

Scope: EngSense as a **static Agent Skill**.

This review does **not** call the OpenAI API, does not use `OPENAI_API_KEY`, does not invoke a model-provider SDK, and does not run a separate EngSense service.

The purpose is to review the Skill's instruction/routing contract, deterministic fixtures, and installation shape without turning EngSense into a model-execution system.

## Review boundary

Reviewed:

- `SKILL.md`;
- `decision-framework.md`;
- `review-workflow.md`;
- language modules;
- domain modules;
- principle lenses;
- routing/conflict references;
- deterministic eval fixtures;
- Skill metadata;
- install/static validation workflows.

Not claimed by this review:

- that a particular model will always follow the Skill perfectly;
- behavioral pass/fail from external API model execution;
- completion of source-specific lenses whose research gates remain open;
- specialist correctness for security, database engines, consensus, cryptography, or lock-free memory ordering.

---

## 1. Skill/runtime boundary

Result: **PASS**

EngSense remains instruction/reference based.

Core behavior requires:

```text
SKILL.md
+ static Markdown guidance
+ repository/task evidence supplied to the active coding agent
```

It does not require:

- OpenAI API credentials;
- OpenAI SDK;
- direct model HTTP calls;
- a dedicated EngSense backend/service;
- MCP;
- a database;
- a vector store;
- a separate agent runtime.

`agents/openai.yaml` is optional Skill metadata for interface/invocation behavior. It is not an API client configuration.

A deterministic static validator now guards against accidental model-provider runtime integration in executable project files.

---

## 2. Progressive disclosure

Result: **PASS after routing hardening**

The root Skill stays a router rather than absorbing all engineering doctrine.

Current load shape:

```text
SKILL.md
→ decision framework
→ review workflow when reviewing changes
→ language module when mechanism depends on language
→ domain module when specialist semantics matter
→ one primary principle lens
→ supporting lens only for a real second trade-off
→ routing map when ownership is ambiguous
→ conflict matrix when valid principles disagree
```

The new `references/routing-map.md` makes lens ownership explicit and reduces the risk of loading every lens for every task.

---

## 2a. Repository instruction registration

Result: **PASS with installer-owned integration**

EngSense now follows the ForgeGuard model.

Persistent Codex repository instructions are managed by the GitHub-first installer CLI, not by `SKILL.md` activation.

The installer:

- installs/removes the Skill in project or user scope;
- prefers a non-empty `AGENTS.override.md` over `AGENTS.md`;
- preserves all unrelated instructions;
- owns only `<!-- engsense:managed-start --> ... <!-- engsense:managed-end -->`;
- updates rather than duplicates the block on reinstall;
- removes only EngSense-owned content on uninstall;
- supports `--no-agents`, `--force`, and `--dry-run`;
- migrates the earlier experimental `engsense:begin/end` block;
- fails closed on malformed/duplicate managed markers.

The CLI performs local file management only. It does not add a model-provider runtime to EngSense.

---

## 3. Principle overlap

Result: **PASS with explicit resolution rules**

The audit identified expected overlap pairs:

- Clean Code vs Complexity Placement;
- Sustainable Engineering vs Evolution/Compatibility;
- Evidence-Driven Abstraction vs Representation Design;
- Change Strategy vs Evolution/Compatibility;
- Performance vs Reliability/Operability;
- Domain Modeling vs Representation Design;
- Concurrency vs Distributed Systems.

These overlaps are not treated as duplicate modules.

The routing map now chooses the primary lens from the dominant question and explains when a second lens materially changes the decision.

---

## 4. Language precedence

Result: **PASS**

The Skill preserves engineering goals while allowing language-specific mechanisms to override source-specific mechanics.

Important case:

```text
Clean Code / OO-shaped mechanism
+
Rust task
→ preserve boundary/invariant goal
→ choose Rust-native mechanism
```

The research-grounded Rust module explicitly covers:

- ownership/lifetimes;
- traits and dispatch;
- enums/state modeling;
- async/concurrency;
- unsafe;
- FFI;
- Cargo/features/MSRV;
- no_std constraints.

This prevents a source-specific OO lens from becoming a Java-pattern transplant.

---

## 5. Domain vs distributed routing

Result: **PASS**

The Skill now treats domain complexity and distributed complexity as independent axes.

Examples:

```text
simple CRUD
→ no rich domain model by default

repeated business transition invariant
→ domain-modeling router

in-process memory queue
→ concurrency/lifecycle
→ not distributed automatically

remote at-least-once worker
→ distributed + concurrency
→ domain-modeling only when business invariants also matter
```

This directly addresses the v1.0 acceptance criterion about recognizing when DDD/distributed guidance is relevant and when it is not without pretending the blocked Evans/DDIA source lenses are complete.

---

## 6. Source gating

Result: **PASS**

Completed source-specific/runtime guidance may be used only where repository research supports it.

Currently completed relevant source-specific coverage includes:

- Clean Code 2e lens;
- Rust for Rustaceans-derived Rust language guidance.

Blocked source-specific lenses remain blocked.

The neutral modules may still route decisions in those areas, but must not claim:

- Ousterhout-specific guidance;
- Fowler-specific guidance;
- Evans/DDD-specific guidance;
- DDIA-specific guidance;
- Nygard-specific guidance;
- McConnell-specific guidance;
- Feathers-specific guidance;

until their research gates are completed.

---

## 7. Evidence and review-noise gate

Result: **PASS**

The Skill consistently requires repository/task evidence before non-trivial recommendations.

A finding should be suppressed when it is only:

- style preference;
- named-pattern preference;
- hypothetical future reuse;
- deterministic lint/formatting work;
- an unsupported performance assumption.

This is consistent across `SKILL.md`, the decision framework, and review workflow.

---

## 8. Specialist boundaries

Result: **PASS**

The Skill does not claim to replace specialist review for:

- cryptography/authentication/authorization;
- database-engine isolation/durability;
- consensus/quorum/replication;
- subtle atomic/lock-free memory ordering;
- legal/compliance;
- specialized UI/UX;
- high-consequence hardware/FFI behavior where platform details dominate.

The domain/language modules provide routing context, not false specialist certainty.

---

## 9. Deterministic eval contract

Result: **PASS structurally**

The repository currently contains 48 deterministic fixtures.

The fixtures test decision properties rather than exact wording.

The static validation layer checks:

- fixture JSON/schema structure;
- contiguous fixture numbering;
- README/checklist fixture-count consistency;
- Skill module references;
- required Skill structure;
- absence of API-key/model-provider runtime integration.

This remains development evidence for the Skill, not a model-execution platform.

---

## 10. Representative static routing review

These scenarios were reviewed against the static routing contract.

| Scenario | Expected route |
|---|---|
| One concrete provider, no variation | evidence-driven abstraction + language module if needed |
| Multiple real providers | evidence-driven abstraction + API/language guidance |
| Cohesive long function | Clean Code + conflict/locality reasoning |
| Multi-responsibility function | Clean Code + relevant domain boundary |
| Unstable duplication | evidence-driven abstraction / Clean Code conflict |
| Stable repeated invariant | evidence-driven abstraction + owning domain |
| Simple CRUD | domain-modeling router should decline rich modeling |
| Complex business transition | domain-modeling router |
| Distributed retry | distributed-systems + concurrency/API as needed |
| Security-sensitive refactor | specialist deferral |
| Measured performance escape hatch | performance engineering + relevant language/domain |
| Rewrite/migration | change strategy + evolution/compatibility |
| Representation loses capability | representation design + API/domain as relevant |
| Rust unsafe change | Rust guidance + specialist boundary when soundness is subtle |

The static instructions contain a coherent route for each scenario.

This is **not** equivalent to a live model-behavior test.

---

## 11. Remaining behavior-review gap

The release checklist's final live behavior review remains intentionally open.

It can be tested by installing EngSense as a Skill in a supported coding-agent/ChatGPT surface and giving it the representative scenarios directly.

That test does not require EngSense itself to contain an API key or API client.

Do not add an OpenAI API eval harness solely to close this gate.

If automated model execution is ever desired as external project tooling, keep it outside the EngSense Skill core and do not make Skill operation depend on it.

---

## 12. Current conclusion

EngSense remains a **Skill**, not a standalone software system.

The current architecture is appropriately:

```text
static instructions
+ progressive-disclosure reference modules
+ small local installer CLI for Skill/AGENTS management
+ deterministic development fixtures
+ static integrity checks
```

The next major quality gains should come from:

1. completing additional research-gated source lenses;
2. live manual Skill invocation checks in a supported surface;
3. refining fixtures when real Skill usage exposes a routing regression.

Do not introduce a model-provider API runtime to solve a problem that the Skill format already solves.
