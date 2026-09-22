# Installing EngSense

EngSense is a standalone Agent Skill: the directory contains a required `SKILL.md` plus supporting Markdown resources.

The Skill depends on its supporting files, so install the **whole EngSense directory**, not only `SKILL.md`.

EngSense also includes optional OpenAI metadata at `agents/openai.yaml`. It provides user-facing metadata and keeps implicit invocation enabled. No MCP/tool dependencies are declared.

Official OpenAI references:

- Build skills: https://developers.openai.com/docs/build-skills
- Skills in ChatGPT: https://help.openai.com/en/articles/20001066

Product availability and installation UI can change. The instructions below follow the current OpenAI documentation as of September 2026.

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
            └── references/
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
└── references/
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

Current ChatGPT documentation exposes Skills through the Skills experience for eligible products/workspaces.

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

For Codex, restart after removal if the Skill remains visible in the current session.

## Security note

EngSense currently contains instructions, references, and deterministic eval fixtures. It does not require credentials, network access, or an MCP server to perform its core workflow.

As with any downloaded Skill, review the source before installing or sharing it.
