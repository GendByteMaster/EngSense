#!/usr/bin/env node

import {
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  rmSync,
  unlinkSync,
  writeFileSync
} from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SKILL_NAME = 'engsense';
const VERSION = '0.1.0';
const PACKAGE_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

const SKILL_ENTRIES = [
  'SKILL.md',
  'agents',
  'decision-framework.md',
  'review-workflow.md',
  'principles',
  'languages',
  'domains',
  'references'
];

const AGENTS_START = '<!-- engsense:managed-start -->';
const AGENTS_END = '<!-- engsense:managed-end -->';
const LEGACY_AGENTS_START = '<!-- engsense:begin -->';
const LEGACY_AGENTS_END = '<!-- engsense:end -->';

const AGENTS_BLOCK = `${AGENTS_START}
## EngSense

- For non-trivial software-engineering judgment—code review, refactoring, architecture, API design, abstraction, maintainability, testability, or engineering trade-offs—load and apply the \`${SKILL_NAME}\` Skill.
- Prefer repository evidence over doctrine, preserve behavior/compatibility/specialist invariants, and load only the EngSense modules relevant to the current decision.
- Do not invoke EngSense for mechanical formatting, trivial renames, deterministic lint fixes, or as a replacement for specialist security, database, distributed-systems, concurrency, performance, or UI review.
- If the Skill cannot be loaded, report that explicitly and continue with the repository's existing instructions; do not invent missing EngSense policy.
${AGENTS_END}`;

function usage() {
  console.log(`EngSense v${VERSION}

Usage:
  engsense install [options]
  engsense status [options]
  engsense uninstall [options]

Options:
  --client <codex>   Target client (default: codex)
  --global           Install in the user-level Skill directory
  --force            Replace an existing EngSense installation
  --no-agents        Do not manage Codex AGENTS.md integration
  --dry-run          Print actions without changing files
  -h, --help         Show help
  -v, --version      Show version

Examples:
  engsense install
  engsense install --client codex
  engsense install --client codex --global
  engsense install --force
  engsense status
  engsense uninstall
`);
}

function fail(message) {
  console.error(`EngSense: ${message}`);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const out = {
    command: 'install',
    client: 'codex',
    global: false,
    force: false,
    noAgents: false,
    dryRun: false
  };

  const args = [...argv];
  if (args[0] && !args[0].startsWith('-')) out.command = args.shift();

  while (args.length) {
    const arg = args.shift();
    if (arg === '--client') out.client = args.shift();
    else if (arg?.startsWith('--client=')) out.client = arg.slice('--client='.length);
    else if (arg === '--global') out.global = true;
    else if (arg === '--force') out.force = true;
    else if (arg === '--no-agents') out.noAgents = true;
    else if (arg === '--dry-run') out.dryRun = true;
    else if (arg === '-h' || arg === '--help') out.help = true;
    else if (arg === '-v' || arg === '--version') out.version = true;
    else throw new Error(`unknown option: ${arg}`);
  }

  if (out.client !== 'codex') {
    throw new Error(`unsupported client: ${out.client}`);
  }

  if (!['install', 'status', 'uninstall', 'help'].includes(out.command)) {
    throw new Error(`unknown command: ${out.command}`);
  }

  return out;
}

function codexHome() {
  return process.env.CODEX_HOME ? resolve(process.env.CODEX_HOME) : join(homedir(), '.codex');
}

function targetPath(globalScope) {
  return globalScope
    ? join(homedir(), '.agents', 'skills', SKILL_NAME)
    : join(process.cwd(), '.agents', 'skills', SKILL_NAME);
}

function agentsPaths(globalScope) {
  const base = globalScope ? codexHome() : process.cwd();
  return {
    override: join(base, 'AGENTS.override.md'),
    regular: join(base, 'AGENTS.md')
  };
}

function isNonEmptyFile(path) {
  return existsSync(path) && readFileSync(path, 'utf8').trim().length > 0;
}

function findBlock(text, startMarker, endMarker, label) {
  const start = text.indexOf(startMarker);
  const endStart = text.indexOf(endMarker);

  if (start === -1 && endStart === -1) return null;
  if (start === -1 || endStart === -1 || endStart < start) {
    throw new Error(`found a malformed ${label} managed block in AGENTS instructions`);
  }

  const secondStart = text.indexOf(startMarker, start + startMarker.length);
  const secondEnd = text.indexOf(endMarker, endStart + endMarker.length);
  if (secondStart !== -1 || secondEnd !== -1) {
    throw new Error(`found multiple ${label} managed blocks in AGENTS instructions`);
  }

  return { start, end: endStart + endMarker.length };
}

function removeBlock(text, startMarker, endMarker, label) {
  const block = findBlock(text, startMarker, endMarker, label);
  if (!block) return text;

  const before = text.slice(0, block.start).trimEnd();
  const after = text.slice(block.end).trimStart();
  return [before, after].filter(Boolean).join('\n\n');
}

function renderWithoutManagedBlocks(text) {
  let next = removeBlock(text, AGENTS_START, AGENTS_END, 'EngSense');
  next = removeBlock(next, LEGACY_AGENTS_START, LEGACY_AGENTS_END, 'legacy EngSense');
  return next;
}

function hasManagedBlock(text) {
  return (
    findBlock(text, AGENTS_START, AGENTS_END, 'EngSense') !== null ||
    findBlock(text, LEGACY_AGENTS_START, LEGACY_AGENTS_END, 'legacy EngSense') !== null
  );
}

function ensureManagedBlock(path, dryRun) {
  const original = existsSync(path) ? readFileSync(path, 'utf8') : '';
  const withoutBlock = renderWithoutManagedBlocks(original);
  const next = withoutBlock.trim()
    ? `${withoutBlock.trimEnd()}\n\n${AGENTS_BLOCK}\n`
    : `${AGENTS_BLOCK}\n`;

  if (original === next) {
    console.log(`linked   agents: ${path}`);
    return;
  }

  console.log(`${dryRun ? 'would link' : 'link    '} agents: ${path}`);
  if (dryRun) return;

  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, next, 'utf8');
}

function removeManagedBlocks(path, dryRun) {
  if (!existsSync(path)) return false;

  const original = readFileSync(path, 'utf8');
  if (!hasManagedBlock(original)) return false;

  const next = renderWithoutManagedBlocks(original);
  console.log(`${dryRun ? 'would unlink' : 'unlink  '} agents: ${path}`);
  if (dryRun) return true;

  if (!next.trim()) unlinkSync(path);
  else writeFileSync(path, `${next.trimEnd()}\n`, 'utf8');
  return true;
}

function installAgentsIntegration(options) {
  if (options.noAgents) return;

  const paths = agentsPaths(options.global);
  const target = isNonEmptyFile(paths.override) ? paths.override : paths.regular;
  const other = target === paths.override ? paths.regular : paths.override;

  removeManagedBlocks(other, options.dryRun);
  ensureManagedBlock(target, options.dryRun);
}

function statusAgentsIntegration(options) {
  if (options.noAgents) return;

  const paths = agentsPaths(options.global);
  const linked = [paths.override, paths.regular].filter((path) => {
    if (!existsSync(path)) return false;
    return hasManagedBlock(readFileSync(path, 'utf8'));
  });

  if (!linked.length) {
    console.log(`missing   agents: ${options.global ? codexHome() : process.cwd()}`);
    return;
  }

  for (const path of linked) console.log(`linked    agents: ${path}`);
}

function uninstallAgentsIntegration(options) {
  if (options.noAgents) return;

  const paths = agentsPaths(options.global);
  const removedOverride = removeManagedBlocks(paths.override, options.dryRun);
  const removedRegular = removeManagedBlocks(paths.regular, options.dryRun);

  if (!removedOverride && !removedRegular) {
    console.log('skip      agents: no EngSense managed block found');
  }
}

function copySkill(target, options) {
  if (existsSync(target) && !options.force) {
    console.log(`skip      codex: ${target} (already exists; use --force)`);
    return;
  }

  console.log(`${options.dryRun ? 'would install' : 'install   '} codex: ${target}`);
  if (options.dryRun) return;

  if (existsSync(target)) rmSync(target, { recursive: true, force: true });
  mkdirSync(target, { recursive: true });

  for (const entry of SKILL_ENTRIES) {
    const source = join(PACKAGE_ROOT, entry);
    if (!existsSync(source)) {
      throw new Error(`bundled Skill entry is missing: ${source}`);
    }
    cpSync(source, join(target, entry), { recursive: true });
  }
}

function install(options) {
  copySkill(targetPath(options.global), options);
  installAgentsIntegration(options);

  if (!options.noAgents && !options.dryRun) {
    console.log('note      codex: start a new session to reload AGENTS instructions');
  }
}

function status(options) {
  const target = targetPath(options.global);
  const installed = existsSync(join(target, 'SKILL.md'));
  console.log(`${installed ? 'installed' : 'missing  '} codex: ${target}`);
  statusAgentsIntegration(options);
}

function uninstall(options) {
  const target = targetPath(options.global);
  if (!existsSync(target)) {
    console.log(`skip      codex: ${target} (not installed)`);
  } else {
    console.log(`${options.dryRun ? 'would remove' : 'remove   '} codex: ${target}`);
    if (!options.dryRun) rmSync(target, { recursive: true, force: true });
  }

  uninstallAgentsIntegration(options);
}

try {
  const options = parseArgs(process.argv.slice(2));

  if (options.help || options.command === 'help') usage();
  else if (options.version) console.log(VERSION);
  else if (options.command === 'install') install(options);
  else if (options.command === 'status') status(options);
  else if (options.command === 'uninstall') uninstall(options);
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
  usage();
}
