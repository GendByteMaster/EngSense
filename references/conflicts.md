# EngSense Conflict Matrix

Status: **Provisional — based on currently completed sources and roadmap hypotheses**

A conflict is not a rule ordering.

For each pair, ask which side dominates under the current context.

| Principle A | Principle B | Signals favoring A | Signals favoring B |
|---|---|---|---|
| Small decomposition | Locality/deep cohesive behavior | independent reasons to change; isolated invariants; focused tests | shared state; sequential algorithm; shallow wrappers would add navigation |
| DRY | Duplication until stable | same invariant; synchronized changes; stable concept | unstable requirements; superficially similar concepts; abstraction needs flags |
| Dependency inversion | Concrete simplicity | real provider/platform boundary; multiple implementations; volatility isolation | one implementation; no substitution; added factory/adapter layers add no capability |
| Standardization | Local specialization | large org/repo; shared tooling; migration automation; cross-team mobility | distinct workload; measurable local need; standard solution imposes material cost |
| Strict layering | Bounded escape hatch | clear ownership; long-lived boundaries; widespread consumers | measured performance/native/protocol need; exception can be contained |
| Encapsulation | Transparent representation | invariant protection; changeable internals; external surface | simple stable data; transformation overhead/indirection dominates |
| General-purpose API | Narrow task-specific API | multiple real clients with stable common variation | one/few focused clients; generality creates unsupported features or weak semantics |
| Compatibility | Architectural correction | large external/persisted surface; expensive migration | early immature surface; broken semantics; migration is cheap/valuable |
| Centralization | Distribution | coordination, single source of truth, simpler invariants | scale/availability/failure isolation require decentralization |
| Uniform interface | Optional capabilities | implementations genuinely share semantics | providers differ materially; unsupported-operation API would lie |
| Portability | Native capability | broad platform support dominates | required OS/device/performance capability is unavailable portably |
| Extensibility | Surface simplicity | real third-party variation; ecosystem value | hypothetical plugins; compatibility/security burden exceeds value |
| Rich framework | Lightweight mechanism | lifecycle, discovery, isolation, complex plugins required | narrow extension need; platform mechanism already sufficient |
| Eager work/state | Lazy materialization | predictable need; simplicity; latency sensitivity | large state; low use fraction; expensive transfer/computation |
| Caching | Recompute/freshness | expensive deterministic work; repeated reads | memory pressure; side effects; freshness/invalidation complexity |
| Buffering/batching | Freshness/latency | throughput and amortization dominate | immediate visibility/latency dominates; queue pressure risk |
| Isolation/hermeticity | Production fidelity | determinism/diagnosis dominates | real contracts/emergent behavior cannot be simulated adequately |
| Unit tests | Larger/integration tests | local deterministic behavior | cross-component, deployment, protocol, performance, emergent risk |
| Real dependency | Fake/stub | cheap, deterministic, reliable dependency | dependency is slow/non-hermetic or error path is hard to trigger |
| State testing | Interaction testing | observable outcomes exist | interaction itself is the contract and state is not economically observable |
| Immutable input/state | In-place mutation | shared consumers; concurrency/invariant clarity | allocation/performance/editing semantics require mutation |
| Full snapshot | Change/event log | simple reconstruction, bounded state | provenance, replay, compact evolution, collaboration |
| Implicit coordination | Explicit orchestrator | policy is simple/local | execution/order policy is complex, distributed, or hard to reason about |
| Async semantics exposed | Sync convenience | ordering/concurrency affects correctness | truly local/atomic operation where async detail is irrelevant |
| Monolith/shared system | Service/process boundary | low operational cost; tight transactions/locality | isolation, independent scaling, language/privilege/restart boundary |
| Broad public API | Small surface | ecosystem requires capability | future change freedom and compatibility burden dominate |
| Reuse external dependency | Build locally | mature ecosystem; strong fit; reduced maintenance | poor fit; unstable provider; dependency/fork lifecycle cost dominates |
| Historical consistency | Modern/local improvement | uniformity/tooling benefit; migration expensive | old rationale obsolete; improvement material; mixed state safe |
| Immediate optimization | Measure first | only when a known invariant requires it | normal case: bottleneck uncertain, optimization adds complexity |
| Simplicity now | Future scalability | expected growth near ceiling; migration expensive/slow | current scale far below ceiling; simpler design is cheap to replace |
| Security/control | Product/incentive redesign | adversarial incentives unavoidable; harm high | product design can credibly eliminate/reduce incentive/attack surface |

---

## Rules for using this matrix

1. Do not choose a side because it appears in the left or right column.
2. Identify repository/product evidence.
3. State the dominant trade-off.
4. Prefer the smallest change that satisfies it.
5. Record a revisit trigger when the other side may become dominant.
6. If specialist semantics decide the outcome, defer to the specialist domain.

---

## Example

### Conflict

`Dependency inversion vs Concrete simplicity`

### Current evidence

- one provider;
- no public substitution contract;
- tests can use the concrete implementation;
- no volatile external boundary;
- proposed trait requires factory + adapter + dynamic dispatch.

### Decision

Keep the concrete implementation.

### Revisit when

A second real provider, external provider boundary, or independent substitution requirement appears.
