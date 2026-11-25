# Real Codex behavior review — v0.1.0 candidate

Status: NOT RUN. Static fixture validation is not a model behavior result.

Use an authenticated local Codex session in a disposable repository. Install EngSense at the candidate commit, record its SHA, the Codex version, model, effort, date, and instruction environment. Do not add a provider SDK or API runtime to EngSense.

Run structural checks first. Then start a fresh session per case, explicitly invoke EngSense, and provide only task, context, evidence and snippet (when present) from the fixture. Keep expected properties and wrong recommendations out of the prompt. Record which modules were actually consulted where observable; otherwise mark routing evidence unknown. Save the transcript and score against the fixture separately. Do not treat the agent's self-reported pass as evidence.

Representative cases: 001, 002, 003, 004, 009, 010, 017, 019, 020, 025, 032, 046, 047, 048, 049, 050, 051. Repeat critical specialist cases 009, 010, 051 in fresh sessions. Check a mechanical rename separately: EngSense must not force architecture analysis. For each run record PASS/FAIL/INCONCLUSIVE, rationale, observed modules, missing expected properties, prohibited reasoning, and transcript reference. PASS requires every mandatory property and no prohibited reasoning. Any critical failure or inconclusive required case blocks candidate approval until retested. This protocol is an external manual review, not a new runtime.

Do not claim effectiveness across all models or comparative improvement without a separate baseline experiment.

When all required cases and repeats are independently scored PASS, append the evidence record (candidate SHA, environment, case results and transcript references) and replace the current status line with `Status: PASS.` on its own line. Do not use that marker for a static-only review or an incomplete run.
