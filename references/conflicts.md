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
| Maximum parallelism | Bounded concurrency/overload control | independent work; spare resource headroom; low coordination cost | scarce shared resource; queue growth; fairness or collapse risk |
| Zero-copy/in-place | Copy/lifetime simplicity | copy cost is measured and ownership/lifetime is controlled | retained backing storage; simpler ownership; locality or release of large allocations dominates |
| Throughput/batching | Latency/freshness | amortization and sustained throughput dominate | tail latency, immediate visibility, or queue pressure dominates |
| Generic path | Bounded specialization | common semantics and maintenance simplicity dominate | measured stable hotspot; explicit eligibility; fallback remains correct |
| Aggressive cache reuse | Freshness/failover | repeated expensive work; stable validity; bounded resource use | invalidation, stale routing/data, memory pressure, or availability semantics dominate |
| Simplicity now | Future scalability | expected growth near ceiling; migration expensive/slow | current scale far below ceiling; simpler design is cheap to replace |
| Security/control | Product/incentive redesign | adversarial incentives unavoidable; harm high | product design can credibly eliminate/reduce incentive/attack surface |
| Incremental refactor | Coordinated change | independently verifiable steps; cheap coexistence; rollback per step | mixed-mode state is more dangerous/expensive; invariant spans coupled components; strong coordinated verification exists |
| Evolve in place | Rewrite/replace | behavior poorly specified; migration risk high; current architecture still adaptable | old behavior is understood/tested; replacement advantage material; cutover/coexistence plan credible |
| Compatibility bridge | Clean cutover | consumers cannot move atomically; rollback/version skew matters | consumer set controlled; transition state costly; coordinated cutover is safer |
| Stable ugly mechanism | Architectural replacement | current mechanism reliable; replacement benefit speculative | recurring defects/cost; old variation model no longer fits; replacement has evidence and migration path |
| Normalized representation | Preserve source-specific detail | variance is incidental; consumers need one stable semantic model | source distinction affects correctness/capability/policy |
| Explicit dependency/state graph | Implicit convention/order | scheduling, validation, replay, or partial ordering is material | flow is tiny, local, and convention is cheaper than a graph model |
| Durable explicit schema | Serialize internal object graph | long-lived/versioned/interoperable persistence required | only short-lived/private cache state with controlled identical runtime version |
| Shared semantic core/IR | Direct per-consumer translation | many transformations/backends share stable semantics | one narrow path; IR adds translation concepts without leverage |
| Machine contract | Human-readable presentation | automation, versioning, unambiguous fields matter | only human consumption; machine contract adds unnecessary surface |
| Maximum reliability | Product/change velocity and cost | severe failure consequence; explicit user need; exhausted error budget; weak recovery | additional reliability is not user-visible; engineering cost dominates; strong recovery/reversibility |
| Manual judgment | Automation | ambiguous/high-context decision; automation blast radius is high; human verification is a required control | stable repeated procedure; human error/latency dominates; scope and rollback are bounded |
| Uniform service guarantees | Differentiated service classes | users require one semantic guarantee; differentiation would create confusing surface/operations | workload classes have materially different latency/throughput/criticality needs and can be expressed safely |
| Immediate root-cause investigation | Stabilize/mitigate first | impact is contained; evidence may disappear; mitigation itself risks corruption | active severe user/data impact; safe containment can reduce blast radius quickly |
| Small independent rollout | Coordinated transition | changes are reversible; old/new coexist safely; attribution matters | mixed-version state is more dangerous; invariant spans tightly coupled components |
| Replication | Independent backup/recovery | failure model is infrastructure/node loss and replicas are independent enough | destructive bug/operator/config error can propagate; historical restore is required |
| Broad alert coverage | Human attention/actionability | missed detection cost dominates and alerts are actionable | noisy/duplicate signals consume attention; service-level symptoms can aggregate lower-level causes |
| Local retry | Global overload safety | isolated/partial backend failure; retry budget is bounded; idempotency and deadlines are clear | service-wide saturation; layered retries amplify load; caller can no longer benefit |

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
