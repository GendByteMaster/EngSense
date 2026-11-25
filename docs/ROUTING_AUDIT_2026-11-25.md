# Routing audit — 2026-11-25

Static review of main at a570f630d90e028cbe60c6f39056861ee217366b. This follow-up does not claim live model verification or exhaustive installer/security audit.

| Finding | Risk | Correction |
|---|---|---|
| Decision framework unconditionally loaded conflicts.md while root/router required a material conflict | Medium | Conditional loading |
| Router listed one primary lens even when domain/language guidance suffices | Medium | Explicit zero-lens route and early ambiguity resolution |
| Review workflow accepted most finding criteria, while SKILL.md required all | Medium | Require all; qualify uncertain verification gaps |
| No explicit precedence for specialist invariants over idiomatic suggestions | High potential impact | Preserve verified invariants, stop at unresolved specialist gate |
| Research status grouped mandatory Google source with supplemental AOSA and lacked count | Low | Explicit 3/14 mandatory, 4 supplemental |

New structural scenarios 049–051 exercise these risks. Actual Codex behavior remains NOT RUN. CI must validate the exact candidate revision before release. No research gate is closed by this audit.
