# Installing EngSense

EngSense is a standalone Agent Skill plus a small GitHub-first installer CLI.

The Skill itself remains static: Markdown guidance and metadata. The CLI only installs/removes local Skill files and manages EngSense's bounded Codex `AGENTS.md` block.

No OpenAI API key, model-provider SDK, MCP server, or EngSense backend is required.

## Other coding agents

EngSense uses one portable Skill payload. The installer supports Codex, Claude Code and Cursor.

| Client | Project | User |
|---|---|---|
| Codex | `.agents/skills/engsense/` | `~/.agents/skills/engsense/` |
| Claude Code | `.claude/skills/engsense/` | `~/.claude/skills/engsense/` |
| Cursor | `.agents/skills/engsense/` | `~/.cursor/skills/engsense/` |

~~~bash
npx --yes github:GendByteMaster/EngSense install --client claude --global
npx --yes github:GendByteMaster/EngSense install --client cursor --global
npx --yes github:GendByteMaster/EngSense install --client all --global
~~~

Use the same client for status, refresh with `install --force`, and uninstall. Omit `--global` for project scope. Default remains Codex for compatibility. Claude Code and Cursor rely on native Skill discovery; the CLI does not create or modify CLAUDE.md or Cursor rules. Codex and Cursor share one project payload; `all` deduplicates it, and removing it for either client removes it for both and unlinks EngSense's Codex block (unless `--no-agents`). Cursor may discover additional compatible paths; avoid duplicate global copies if the host reports ambiguity. Global installs are separate directories. Native host behavior must be verified separately; installer tests alone do not establish model behavior.

## Install or refresh directly from GitHub

To install the current default branch for Codex (or replace an existing EngSense installation):

~~~powershell
npx --yes github:GendByteMaster/EngSense install --client codex --global --force
~~~

For Claude Code, Cursor or all supported clients, replace `codex` with `claude`, `cursor` or `all`. Omit `--global` for the current project. Use the same source with `status` or `uninstall` (without `--force`). Restart the agent after installation.

This command follows `main`, not the immutable v0.1.0 release asset. A normal first installation does not need `--force`; it replaces the entire EngSense target directory, so back up any local additions first. If npm reports a GitFetcher error, use the versioned release tarball documented below.

## Recommended — ForgeGuard-style GitHub install

Install EngSense into the current repository for Codex:

~~~bash
npx --yes github:GendByteMaster/EngSense install --client codex
~~~

This performs both actions in one command:

1. installs the Skill at `.agents/skills/engsense/`;
2. adds/updates the EngSense managed block in the active root Codex instructions.

Check status:

~~~bash
npx --yes github:GendByteMaster/EngSense status --client codex
~~~

Remove EngSense:

~~~bash
npx --yes github:GendByteMaster/EngSense uninstall --client codex
~~~

Uninstall removes the installed Skill and only the EngSense-managed AGENTS block. Unrelated repository instructions are preserved.

## AGENTS.md integration

The installer uses the same ownership model as ForgeGuard.

Managed markers:

~~~text
<!-- engsense:managed-start -->
...
<!-- engsense:managed-end -->
~~~

For project scope, the installer looks at the current repository/work directory:

~~~text
AGENTS.override.md
AGENTS.md
~~~

If a non-empty `AGENTS.override.md` exists, EngSense links its block there. Otherwise it uses `AGENTS.md`.

If the managed block exists in the non-active file, the installer removes that EngSense block so only one active EngSense instruction remains.

Reinstall is idempotent: the block is updated, not duplicated.

The installer also migrates the earlier experimental markers:

~~~text
<!-- engsense:begin -->
<!-- engsense:end -->
~~~

to the current managed format.

Malformed or duplicate managed blocks cause the installer to fail instead of guessing.

After installing/updating AGENTS instructions, start a new Codex session so the changed instructions are reloaded.

## Options

~~~text
engsense install [options]
engsense status [options]
engsense uninstall [options]

--client <all|codex|claude|cursor>
--global
--force
--no-agents
--dry-run
--help
--version
~~~

Examples:

~~~bash
npx --yes github:GendByteMaster/EngSense install --client codex --force
npx --yes github:GendByteMaster/EngSense install --client codex --dry-run
npx --yes github:GendByteMaster/EngSense install --client codex --no-agents
~~~

## User/global scope

Install the Skill at user scope:

~~~bash
npx --yes github:GendByteMaster/EngSense install --client codex --global
~~~

The Skill target is:

~~~text
~/.agents/skills/engsense/
~~~

For global Codex instructions, EngSense targets:

~~~text
$CODEX_HOME/AGENTS.override.md
$CODEX_HOME/AGENTS.md
~~~

or `~/.codex/... ` when `CODEX_HOME` is not set.

Status:

~~~bash
npx --yes github:GendByteMaster/EngSense status --client codex --global
~~~

Uninstall:

~~~bash
npx --yes github:GendByteMaster/EngSense uninstall --client codex --global
~~~

## `npx` does not create a permanent command

~~~bash
npx --yes github:GendByteMaster/EngSense ...
~~~

downloads/runs the EngSense CLI for that invocation.

If you want a permanent `engsense` command, install the CLI globally from GitHub:

~~~bash
npm install --global github:GendByteMaster/EngSense
engsense --version
~~~

Then:

~~~bash
engsense install --client codex
engsense status --client codex
engsense uninstall --client codex
~~~

The EngSense `--global` flag controls the **target Skill scope**. It is separate from npm global CLI installation.

## Existing Skill installation

If `.agents/skills/engsense/` already exists, a normal install does not overwrite it.

Use:

~~~bash
npx --yes github:GendByteMaster/EngSense install --client codex --force
~~~

to refresh the Skill files.

AGENTS integration is still reconciled even when Skill copying is skipped.

## Install without AGENTS management

Use:

~~~bash
npx --yes github:GendByteMaster/EngSense install --client codex --no-agents
~~~

This installs only the Skill.

The same flag can be used with status/uninstall when AGENTS integration should intentionally be left untouched.

## Dry run

Preview changes without writing files:

~~~bash
npx --yes github:GendByteMaster/EngSense install --client codex --dry-run
~~~

## Alternative — generic Skills CLI

The generic `skills` CLI can still install the Skill:

~~~bash
npx skills add https://github.com/GendByteMaster/EngSense -a codex
~~~

However, this path does not run EngSense's own installer, so it does **not** automatically manage EngSense's AGENTS block.

Use the recommended GitHub-first EngSense command when ForgeGuard-style automatic AGENTS integration is wanted.

## Manual project installation

Copy the Skill payload to:

~~~text
.agents/skills/engsense/
~~~

The installed Skill needs:

~~~text
engsense/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── decision-framework.md
├── review-workflow.md
├── principles/
├── languages/
├── domains/
└── references/
~~~

Manual copying does not automatically modify `AGENTS.md`.

## ChatGPT

EngSense can still be used as a normal Skill in supported ChatGPT Skills surfaces.

The GitHub installer CLI supports local Codex, Claude Code and Cursor Skill installation, with AGENTS integration for Codex. It does not turn EngSense into an API-backed service.

## Development checkout

~~~bash
git clone https://github.com/GendByteMaster/EngSense.git
cd EngSense
npm test
python evals/validate.py
python evals/validate_skill.py
~~~

Test the installer locally in another repository with:

~~~bash
node /path/to/EngSense/bin/engsense.js install --client codex
~~~

## Updating

Project scope:

~~~bash
npx --yes github:GendByteMaster/EngSense install --client codex --force
~~~

Global scope:

~~~bash
npx --yes github:GendByteMaster/EngSense install --client codex --global --force
~~~

This refreshes the Skill and reconciles the managed AGENTS block.

## Security boundary

EngSense remains a static Skill.

The installer performs local file operations only:

- copy/remove EngSense Skill files;
- read/update/remove EngSense's marked AGENTS block.

It does not require:

- `OPENAI_API_KEY`;
- OpenAI/model-provider SDKs;
- direct model HTTP calls;
- MCP;
- a database;
- a vector store;
- an EngSense server.

## Released package (recommended for v0.1.0)

Once the GitHub release is published, install the tested npm tarball without an npm registry account:

~~~powershell
npm exec --yes --package="https://github.com/GendByteMaster/EngSense/releases/download/v0.1.0/gendbytemaster-engsense-0.1.0.tgz" -- engsense install --client all --global
~~~

Replace `all` with `codex`, `claude` or `cursor`; omit `--global` for project scope. Use the same package argument for status, refresh or uninstall. Direct GitHub source shorthand is an alternative, but npm 10.8.2 failed the pinned-commit smoke with a GitFetcher error; use the release package if affected.
