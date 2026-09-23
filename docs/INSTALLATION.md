# Installing EngSense

EngSense is a standalone Agent Skill: the directory contains a required `SKILL.md` plus supporting Markdown resources.

The Skill depends on its supporting files, so install the **whole EngSense directory**, not only `SKILL.md`.

EngSense also includes optional OpenAI metadata at `agents/openai.yaml`. It provides user-facing metadata and keeps implicit invocation enabled. This file does **not** create an OpenAI API integration. EngSense does not require `OPENAI_API_KEY`, an OpenAI SDK, direct model HTTP calls, an MCP server, or any other model-provider runtime.

Official OpenAI references:

- Build skills: https://developers.openai.com/docs/build-skills
- Skills in ChatGPT: https://help.openai.com/en/articles/20001066

Product availability and installation UI can change. The instructions below follow the current OpenAI documentation as of September 2026.

## Recommended — npx from GitHub

The recommended one-command install uses the open `skills` CLI with EngSense sourced directly from GitHub.

Project scope for Codex with immediate `AGENTS.md` registration:

~~~bash
npx skills add https://github.com/GendByteMaster/EngSense -a codex -y && python .agents/skills/engsense/scripts/sync_agents.py
~~~

Plain Skill install is still supported:

~~~bash
npx skills add https://github.com/GendByteMaster/EngSense -a codex
~~~

When EngSense is later activated in a writable repository, its Skill instructions tell the agent to run the same idempotent registration helper automatically.

Global/user scope:

~~~bash
npx skills add https://github.com/GendByteMaster/EngSense -a codex -g
~~~

Non-interactive global install:

~~~bash
npx skills add https://github.com/GendByteMaster/EngSense -a codex -g -y
~~~

The EngSense source is the GitHub repository URL above. EngSense does not need its own npm package.

The `skills` CLI is a third-party open Agent Skills installer rather than an OpenAI product. Its upstream repository is `vercel-labs/skills`: https://github.com/vercel-labs/skills. Review its current repository/package documentation before using it in locked-down or security-sensitive environments.

## Automatic `AGENTS.md` registration

Codex automatically reads repository `AGENTS.md` instructions, so EngSense can keep a compact persistent activation rule there.

EngSense ships:

~~~text
assets/agents-snippet.md
scripts/sync_agents.py
~~~

The helper:

- discovers the Git repository root (or accepts `--root`);
- creates root `AGENTS.md` when no case-variant exists;
- reuses an existing `AGENTS.md` / `agents.md` case variant;
- preserves all existing user-authored instructions;
- manages only the block between `<!-- engsense:begin -->` and `<!-- engsense:end -->`;
- is idempotent, so repeated activation does not duplicate the block;
- refuses to guess if the managed markers are malformed.

Manual sync:

~~~bash
python .agents/skills/engsense/scripts/sync_agents.py
~~~

Check without modifying:

~~~bash
python .agents/skills/engsense/scripts/sync_agents.py --check
~~~

Remove only the EngSense managed block:

~~~bash
python .agents/skills/engsense/scripts/sync_agents.py --remove
~~~

For a globally installed Skill, run the bundled helper from the global EngSense directory while your shell is inside the target repository, or pass `--root <repo>`.

The current open `skills` CLI does not provide Codex install hooks, so a plain `npx skills add ...` cannot safely mutate repository `AGENTS.md` as an installer side effect. EngSense therefore uses two supported paths:

1. the one-line project install above, which immediately runs the deterministic helper;
2. Skill self-registration on first/subsequent activation in a writable repository.

This keeps EngSense a Skill rather than introducing a separate installer service or runtime.

## Codex — repository scope

Use repository scope when EngSense should apply only to one codebase.

From the target repository, place the Skill at:

~~~text
.agents/skills/engsense/
~~~

The resulting layout should contain:

~~~text
<your-repository>/
└── .agents/
    └── skills/
        └── engsense/
            ├── SKILL.md
            ├── agents/
            │   └── openai.yaml
            ├── decision-framework.md
            ├── review-workflow.md
            ├── principles/
            ├── languages/
            ├── domains/
            ├── references/
            ├── assets/
            │   └── agents-snippet.md
            └── scripts/
                └── sync_agents.py
~~~

Codex scans repository skill locations while walking from the current working directory toward the repository root.

After installation, start/restart Codex from the repository if the new Skill is not immediately visible.

## Codex — user scope

Use user scope when EngSense should be available across repositories.

Install the full EngSense directory at:

~~~text
~/.codex/skills/engsense/
~~~

Expected layout:

~~~text
~/.codex/skills/engsense/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── decision-framework.md
├── review-workflow.md
├── principles/
├── languages/
├── domains/
├── references/
├── assets/
│   └── agents-snippet.md
└── scripts/
    └── sync_agents.py
~~~

If Codex does not detect an updated Skill, restart Codex.

## Codex — skill installer

Current Codex documentation also supports the built-in Skill installer.

Invoke:

~~~text
$skill-installer
~~~

and ask it to install EngSense from:

~~~text
https://github.com/GendByteMaster/EngSense
~~~

Review the installed files and ensure the Skill root contains `SKILL.md` plus the supporting directories.

## ChatGPT

Current ChatGPT documentation exposes Skills to eligible Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability.

Typical flow:

1. Open **Plugins** from the ChatGPT sidebar.
2. Open the **Skills** tab.
3. Choose **Create**.
4. Choose **Upload from your computer**.
5. Upload/import the EngSense Skill directory/package using the format the current UI requests.
6. Review the Skill before installing it.

In supported ChatGPT experiences, an installed Skill can be selected explicitly and may also be invoked automatically when its name/description match the task.

Availability and sharing controls depend on the current product and workspace settings. Refer to the current Help Center page rather than assuming the same UI exists on every plan or surface.

OpenAI's current Skill format also supports optional `agents/openai.yaml` metadata for user-facing interface settings, invocation policy, and tool dependency declarations. EngSense uses only the interface/invocation metadata and intentionally declares no external tool dependency.

## Development checkout

For contributors, keep a normal clone:

~~~bash
git clone https://github.com/GendByteMaster/EngSense.git
cd EngSense
~~~

Then either:

- work directly in the repository;
- copy/symlink the repository into a local Skill location;
- use a repository-scoped install in a separate test project.

Do not edit an installed copy and a development clone independently unless you intentionally want them to diverge.

## Verify installation

A simple activation test is:

~~~text
Use EngSense to review whether this interface is justified. There is currently one
implementation and no external provider boundary.
~~~

Expected behavior:

- EngSense should inspect evidence rather than automatically defend the interface;
- it should recognize premature abstraction as possible;
- it should provide a revisit trigger rather than claiming interfaces are always bad.

A second test:

~~~text
Use EngSense to review a retry loop in a distributed backend. Preserve idempotency,
timeout, and failure semantics.
~~~

Expected behavior:

- EngSense should recognize the distributed-systems boundary;
- it should load relevant domain guidance;
- it should not treat retries as a cosmetic style issue.

## Updating

If installed from a local copy, replace/update the complete EngSense directory.

If installed through a product-managed Skill installer, use that product's current update/reinstall workflow.

Because supporting files are part of the Skill, avoid updating only `SKILL.md` while leaving old principle/domain files behind.

## Uninstalling

Remove the EngSense skill directory from the scope where it was installed, or use the current Skills UI/installer removal action for the relevant product.

For Codex, you can first remove the managed repository instruction with:

~~~bash
python <engsense-skill-path>/scripts/sync_agents.py --remove
~~~

Then remove the EngSense skill directory. Restart Codex if the Skill remains visible in the current session.

## Security note

EngSense currently contains instructions, references, and deterministic eval fixtures. Its core workflow is static and does not require credentials, `OPENAI_API_KEY`, an OpenAI/model-provider SDK, direct model API calls, network access, or an MCP server. Network access used by an installer or GitHub Actions smoke test is installation/development tooling, not EngSense runtime behavior.

As with any downloaded Skill, review the source before installing or sharing it.
