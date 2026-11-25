# EngSense Research Status

This file prevents the implemented EngSense core from being mistaken for a completed source-specific evidence base.

## Completed full-text sources (7 total; 3 mandatory, 4 supplemental)

- *The Architecture of Open Source Applications, Volume 1* — official AOSA edition.
- *The Architecture of Open Source Applications, Volume 2* — official AOSA edition.
- *The Performance of Open Source Applications* — official AOSA edition.

Completed research notes are tracked in the repository. The completed AOSA Volume 1, AOSA Volume 2, POSA, and Software Engineering at Google notes are integrated into `main`.

## Completed supplemental full-text sources

- *Site Reliability Engineering: How Google Runs Production Systems* — official complete online edition at `sre.google`; Foreword, Preface, Parts I–V, Chapters 1–34, Appendices A–F, and Bibliography studied in full. This source strengthens reliability/operability synthesis but does **not** replace any mandatory commercial source.

## Completed mandatory full-text sources (3 of 14)

- *Software Engineering at Google* — official Abseil digital edition; research integrated into `main`.

- *Clean Code: A Handbook of Agile Software Craftsmanship, 2nd Edition* — user-provided full-text edition reviewed end to end on `research/clean-code-2e`; structured research note, conflicts, qualifications, and eval candidates recorded.

- *Rust for Rustaceans* — user-provided full-text edition reviewed end to end on `research/rust-for-rustaceans`; structured research note, research-grounded Rust guidance, conflicts, and Rust-specific evals recorded.

## Mandatory corpus still open

Eleven of the fourteen mandatory sources remain open. The four supplemental completed sources do not substitute for them. Issue #2 is authoritative for the mandatory corpus; Issue #1 and `RELEASE_CHECKLIST.md` track implementation and release readiness.

Next priority: John Ousterhout, *A Philosophy of Software Design*, 2nd Edition. The author provides an [official edition page](https://web.stanford.edu/~ouster/cgi-bin/aposd.php) and a partial extract, not a complete lawful full-text edition. Access verification is partial progress only; source-specific guidance stays blocked until the entire edition is studied.

Therefore:

- General cross-source guidance may still be revised as the mandatory source-specific corpus is completed.
- Source-specific lens modules for unread or partially read books must not claim that those books were fully studied.
- Unresolved code-level conflicts remain unresolved.
- Future corpus research may revise the framework.
- Do not close the research gate until its original definition of done is actually satisfied.

## Implementation exception

The user explicitly authorized beginning implementation before the mandatory corpus was complete.

That authorization permits:

- Skill scaffolding;
- context/decision framework;
- review workflow;
- provisional language/domain guidance;
- principle lenses derived only from completed full-text sources;
- provisional conflict modeling;
- deterministic evaluation fixtures and structural validation.

It does **not** permit pretending the unread mandatory sources were completed or attributing rules to them.
