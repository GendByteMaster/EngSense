# EngSense Decision Examples

These examples demonstrate decision shape, not universal answers.

## 1. Keep concrete implementation

**Context:** One repository-local provider exists. No caller requires substitution.

**Evidence:** Factory returns one concrete type; interface mirrors concrete methods.

**Conflict:** Dependency inversion vs concrete simplicity.

**Decision:** Keep the concrete implementation.

**Why:** The abstraction adds concepts and runtime indirection without protecting a real variation boundary.

**Verification:** Run existing behavior tests and confirm no caller needs substitution.

**Revisit when:** A second real provider or external substitution boundary appears.

---

## 2. Introduce provider abstraction

**Context:** Two production providers exist with different SDKs and capabilities.

**Evidence:** Provider-specific branches leak into callers.

**Conflict:** Direct locality vs provider isolation.

**Decision:** Introduce a stable provider boundary, with explicit capability differences rather than a false lowest-common-denominator contract.

**Verification:** Contract tests across both providers and runtime selection tests.

**Revisit when:** Provider set or capability model changes materially.

---

## 3. Keep a long cohesive function

**Context:** Parser function is long but implements one grammar production and shares parser state.

**Evidence:** Proposed helpers are tiny wrappers and increase navigation.

**Conflict:** Small functions vs locality.

**Decision:** Keep the cohesive function; extract only genuine semantic sub-units.

**Verification:** Parser regression tests.

**Revisit when:** Independent responsibilities appear.

---

## 4. Tolerate duplication

**Context:** Two similar workflows have different trust/error semantics and are evolving independently.

**Evidence:** Shared helper requires mode flags.

**Conflict:** DRY vs unstable abstraction.

**Decision:** Keep temporary duplication.

**Verification:** Independent tests for both workflows.

**Revisit when:** A stable shared invariant emerges and changes repeatedly move together.

---

## 5. Preserve observable API ordering

**Context:** Public API has returned stable ordering for years, though undocumented.

**Evidence:** Client examples and integration tests rely on it.

**Conflict:** Implementation freedom vs compatibility.

**Decision:** Preserve ordering for the current version or make a deliberate versioned migration.

**Verification:** Downstream/compatibility tests.

**Revisit when:** Consumer evidence proves the behavior unused or a versioned contract changes.

---

## 6. Accept a bounded performance fast path

**Context:** Generic path is correct but profiling identifies one dominant hot path.

**Evidence:** Specialized path produces material measured improvement and can be selected by explicit capability check.

**Conflict:** Strict layering vs measured performance.

**Decision:** Keep generic path as default and add a contained fast path.

**Verification:** Benchmarks, semantic-equivalence tests, fallback tests.

**Revisit when:** Dual-path maintenance cost exceeds benefit or the specialized path becomes the dominant architecture.

---

## 7. Keep simple architecture with known scale ceiling

**Context:** Single coordinator has major headroom; distributed replacement adds substantial operational complexity.

**Evidence:** No forecast reaches the ceiling soon.

**Conflict:** Simplicity now vs future scalability.

**Decision:** Keep current architecture and document the ceiling plus migration trigger.

**Verification:** Capacity metrics/alerts.

**Revisit when:** Growth or availability requirements approach the trigger.

---

## 8. Reject unbounded queue

**Context:** Producer can outrun storage indefinitely.

**Evidence:** Queue depth and process memory rise continuously under storage slowdown.

**Conflict:** Throughput decoupling vs bounded resource use.

**Decision:** Require explicit bounded overload semantics.

**Verification:** Load test with degraded downstream storage.

**Revisit when:** Workload/loss/durability requirements change.

---

## 9. Stage persistence migration

**Context:** Old and new app versions coexist during deployment.

**Evidence:** Destructive rename breaks old binaries and rollback.

**Conflict:** Migration simplicity vs mixed-version compatibility.

**Decision:** Use additive/staged migration before destructive cleanup.

**Verification:** Mixed-version and rollback tests.

**Revisit when:** Old versions are fully removed and compatibility window closes.

---

## 10. Prefer real deterministic test dependency

**Context:** In-memory implementation is fast, deterministic, and behaviorally faithful.

**Evidence:** Mock-heavy tests break on harmless call-order refactors.

**Conflict:** Isolation vs fidelity/refactor resilience.

**Decision:** Use the real in-memory implementation for these tests.

**Verification:** Compare runtime, determinism, and failure detection.

**Revisit when:** The dependency becomes slow, nondeterministic, or requires difficult failure injection.
