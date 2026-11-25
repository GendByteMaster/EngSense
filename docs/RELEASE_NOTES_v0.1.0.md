# EngSense v0.1.0 — Context-Aware Engineering Judgment

**Understand the context. Evaluate trade-offs. Preserve invariants.**

EngSense is a portable, static Agent Skill for software-engineering judgment. It helps coding agents evaluate code structure, refactoring, architecture, abstraction, compatibility, maintainability and testability without treating any single engineering school as universal doctrine.

This first public development release provides a reusable Skill and a GitHub-first installer for Codex, Claude Code and Cursor. It is not v1.0.0; the mandatory research corpus remains incomplete.

## What's included

- **Context-first decision framework:** inspect relevant repository evidence, identify constraints and invariants, compare viable alternatives, and choose the best engineering trade-off.
- **Progressive disclosure:** load only the language, domain and principle modules that materially affect a decision.
- **Ten engineering lenses:** Clean Code 2e, sustainable engineering, empirical architecture, complexity placement, evolution and compatibility, evidence-driven abstraction, performance engineering, change strategy, representation design, and reliability/operability.
- **Language-aware guidance:** Rust, TypeScript, Python and general engineering guidance.
- **Six domain modules:** API design, domain modeling, testing, concurrency, persistence and distributed systems.
- **Conflict matrix:** evaluate competing principles such as DRY vs local clarity, abstraction vs simplicity, and compatibility vs architectural freedom.
- **Evidence-based review:** actionable findings, appropriate authority, specialist deferral, and verification matched to risk.
- **Portable installer:** `install`, `status`, and `uninstall`, with user/project scopes and managed AGENTS integration.
- **Development validation:** 51 deterministic scenario specifications, static integrity checks, and installer lifecycle checks.

### How EngSense works

```text
Task
  |
  v
Context, repository evidence and invariants
  |
  v
Relevant language/domain/principle guidance
  |
  v
Trade-off analysis and engineering decision
  |
  v
Implementation or review — verification
```

EngSense does not execute a separate runtime, replace repository authorization rules, or substitute for specialist correctness reviews. Actual execution and verification belong to the host coding agent.

## Requirements

- Node.js 18 or later with npm/npx and Git for GitHub installation.
- Codex, Claude Code or Cursor with Agent Skills support.
- No npm-registry publication, model-provider API key, MCP server, or EngSense backend is required.

## Install or refresh directly from GitHub

To install the current default branch for Codex (or replace an existing EngSense installation):

~~~powershell
npx --yes github:GendByteMaster/EngSense install --client codex --global --force
~~~

For Claude Code, Cursor or all supported clients, replace `codex` with `claude`, `cursor` or `all`. Omit `--global` for the current project. Use the same source with `status` or `uninstall` (without `--force`). Restart the agent after installation.

This command follows `main`, not the immutable v0.1.0 release asset. A normal first installation does not need `--force`; it replaces the entire EngSense target directory, so back up any local additions first. If npm reports a GitFetcher error, use the versioned release tarball documented below.

## Install

The published npm tarball is the tested distribution path. It requires no npm registry publication and avoids a GitFetcher error observed in npm 10.8.2 when fetching a GitHub commit directly. Use the release asset in the commands below. GitHub source shorthand (`github:GendByteMaster/EngSense#v0.1.0`) may work with other npm versions but has not been verified for this release.


### Codex — user scope (recommended)

```powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense install --client codex --global
```

User-level Skill location: `~/.agents/skills/engsense/`.

### Codex — current repository

Run from the project root:

```powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense install --client codex
```

Project-level location: `.agents/skills/engsense/`.

EngSense also reconciles its marked block in the active Codex AGENTS instructions. Use `--no-agents` to skip AGENTS management. Restart Codex after installing to reload the Skill and instructions.

### Claude Code

~~~powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense install --client claude --global
~~~

User location: `~/.claude/skills/engsense/`. Without `--global`: `.claude/skills/engsense/`.

### Cursor

~~~powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense install --client cursor --global
~~~

User location: `~/.cursor/skills/engsense/`. Without `--global`: `.agents/skills/engsense/`.

### All three clients

~~~powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense install --client all --global
~~~

Codex remains the default. Codex and Cursor share a project-level payload; uninstalling either removes the shared copy and EngSense's Codex registration unless `--no-agents` is set. Claude Code and Cursor use native discovery without CLAUDE.md or Cursor rules modifications. Replace `--client codex` in status, refresh and uninstall examples with the desired client. Native activation and live model behavior for Claude Code and Cursor are not yet verified.

### Verify installation

```powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense status --client codex --global
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense --version
```

The status command reports installation presence and AGENTS linkage; `--version` reports the invoked CLI package version, not an independent installed-file version check.

## Refresh an existing installation

To reapply this exact release:

```powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense install --client codex --global --force
```

To refresh from the current default branch:

```powershell
npx --yes github:GendByteMaster/EngSense install --client codex --global --force
```

Preview a refresh:

```powershell
npx --yes github:GendByteMaster/EngSense install --client codex --global --force --dry-run
```

**Important:** `--force` replaces the EngSense target directory, including custom files stored inside it. Back up any local additions first. Keep personal instructions outside the Skill directory. The pinned command does not advance beyond its tag. EngSense has no background updater or separate `update` command.

## Uninstall

```powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense uninstall --client codex --global
```

Omit `--global` for project scope. Uninstall removes the target Skill directory and its managed AGENTS blocks. It preserves unrelated instruction content, but does not preserve custom files within the target Skill directory. Use `--dry-run` to preview.

## Example usage

After installation, start a new Codex session in a repository:

> Use $engsense to review the proposed refactor. Identify the actual problem, inspect relevant evidence, preserve compatibility and specialist invariants, compare viable alternatives, and recommend the smallest justified change. Do not expand the scope into unrelated cleanup.

## CLI reference

```text
engsense install    [--client all|codex|claude|cursor] [--global] [--force] [--no-agents] [--dry-run]
engsense status     [--client all|codex|claude|cursor] [--global] [--no-agents]
engsense uninstall  [--client all|codex|claude|cursor] [--global] [--no-agents] [--dry-run]
engsense --version
engsense --help
```

## Validation and known limitations

- The release workflow validates fixtures, static Skill integrity, Node installer tests and installation from the npm tarball built from the exact release commit before publication. The tarball is attached to the GitHub release.
- The 51 fixtures specify expected decisions; a structural pass is not 51 live model passes. Live Codex behavior review has not been run. This public development pre-release is not a behavior-verified release.
- Three of fourteen mandatory books are completed, alongside four supplemental full-text sources. Remaining book-specific lenses are research-gated.
- The portable installer targets Codex, Claude Code and Cursor. Live native activation and model behavior in Claude Code and Cursor are not yet verified.
- ChatGPT Skills smoke testing remains a v1.0 gate; this release does not claim that verification.
- EngSense is not a security auditor, profiler, distributed-systems verifier, or standalone agent service.

**Repository:** https://github.com/GendByteMaster/EngSense

**License:** MIT.
