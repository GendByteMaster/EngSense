# EngSense Principles

The principle modules in this directory are **research-grounded lenses**, not universal rules.

## Implemented from completed full-text sources

The following modules are based only on sources that have been read in full:

- `sustainable-engineering.md`
- `empirical-architecture.md`
- `complexity-placement.md`
- `evolution-and-compatibility.md`
- `evidence-driven-abstraction.md`
- `performance-engineering.md`
- `change-strategy.md`

Primary completed sources:

- *Software Engineering at Google*
- *The Architecture of Open Source Applications, Volume 1*
- *The Architecture of Open Source Applications, Volume 2*
- *The Performance of Open Source Applications*

## Planned source-specific lenses still blocked

Do **not** claim the following source-specific lenses are complete until their mandatory full-book research is finished:

- Clean Code / Robert C. Martin
- Complexity / John Ousterhout
- Refactoring / Martin Fowler
- Pragmatic engineering / Thomas & Hunt
- Domain-driven design / Eric Evans
- Data-intensive systems / Kleppmann & Riccomini
- Production resilience / Michael Nygard
- Construction quality / Steve McConnell
- Legacy-code strategy / Michael Feathers
- Modern software engineering / David Farley
- Architecture trade-offs / Ford, Richards, Sadalage & Dehghani

These may exist later as separate modules, but the current implementation must not backfill them from summaries or generic knowledge.

## Loading rule

Load a principle module only when its question is relevant.

Do not load every lens for every task.

A useful sequence is:

```text
task/context
→ decision-framework
→ relevant language/domain modules
→ one or more principle lenses
→ conflict matrix if lenses pull in different directions
```
