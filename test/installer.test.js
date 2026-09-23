import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const CLI = resolve('bin/engsense.js');
const START = '<!-- engsense:managed-start -->';
const END = '<!-- engsense:managed-end -->';

function tempProject() {
  return mkdtempSync(join(tmpdir(), 'engsense-installer-'));
}

function run(cwd, args = [], env = {}) {
  return spawnSync(process.execPath, [CLI, ...args], {
    cwd,
    env: { ...process.env, ...env },
    encoding: 'utf8'
  });
}

test('install copies Skill and creates managed AGENTS block', () => {
  const cwd = tempProject();
  const result = run(cwd, ['install']);

  assert.equal(result.status, 0, result.stderr);
  assert.equal(existsSync(join(cwd, '.agents', 'skills', 'engsense', 'SKILL.md')), true);

  const agents = readFileSync(join(cwd, 'AGENTS.md'), 'utf8');
  assert.match(agents, /## EngSense/);
  assert.equal(agents.split(START).length - 1, 1);
  assert.equal(agents.split(END).length - 1, 1);
});

test('reinstall is idempotent and preserves user AGENTS content', () => {
  const cwd = tempProject();
  writeFileSync(join(cwd, 'AGENTS.md'), '# Project\n\nKeep this rule.\n', 'utf8');

  assert.equal(run(cwd, ['install']).status, 0);
  const once = readFileSync(join(cwd, 'AGENTS.md'), 'utf8');

  assert.equal(run(cwd, ['install']).status, 0);
  const twice = readFileSync(join(cwd, 'AGENTS.md'), 'utf8');

  assert.equal(once, twice);
  assert.match(twice, /Keep this rule\./);
  assert.equal(twice.split(START).length - 1, 1);
});

test('non-empty AGENTS.override.md has priority and regular managed block is removed', () => {
  const cwd = tempProject();
  writeFileSync(
    join(cwd, 'AGENTS.md'),
    `# Regular\n\n${START}\nold\n${END}\n`,
    'utf8'
  );
  writeFileSync(join(cwd, 'AGENTS.override.md'), '# Override\n', 'utf8');

  const result = run(cwd, ['install']);
  assert.equal(result.status, 0, result.stderr);

  const regular = readFileSync(join(cwd, 'AGENTS.md'), 'utf8');
  const override = readFileSync(join(cwd, 'AGENTS.override.md'), 'utf8');

  assert.doesNotMatch(regular, /engsense:managed-start/);
  assert.match(regular, /# Regular/);
  assert.match(override, /# Override/);
  assert.match(override, /engsense:managed-start/);
});

test('uninstall removes only EngSense managed content', () => {
  const cwd = tempProject();
  writeFileSync(join(cwd, 'AGENTS.md'), '# Project\n\nKeep me.\n', 'utf8');

  assert.equal(run(cwd, ['install']).status, 0);
  const result = run(cwd, ['uninstall']);

  assert.equal(result.status, 0, result.stderr);
  assert.equal(existsSync(join(cwd, '.agents', 'skills', 'engsense')), false);

  const agents = readFileSync(join(cwd, 'AGENTS.md'), 'utf8');
  assert.equal(agents, '# Project\n\nKeep me.\n');
});

test('uninstall deletes AGENTS file when it contained only EngSense content', () => {
  const cwd = tempProject();
  assert.equal(run(cwd, ['install']).status, 0);
  assert.equal(existsSync(join(cwd, 'AGENTS.md')), true);

  assert.equal(run(cwd, ['uninstall']).status, 0);
  assert.equal(existsSync(join(cwd, 'AGENTS.md')), false);
});

test('install migrates legacy self-registration markers', () => {
  const cwd = tempProject();
  writeFileSync(
    join(cwd, 'AGENTS.md'),
    '# Project\n\n<!-- engsense:begin -->\nold legacy block\n<!-- engsense:end -->\n',
    'utf8'
  );

  const result = run(cwd, ['install']);
  assert.equal(result.status, 0, result.stderr);

  const agents = readFileSync(join(cwd, 'AGENTS.md'), 'utf8');
  assert.doesNotMatch(agents, /engsense:begin/);
  assert.match(agents, /engsense:managed-start/);
  assert.match(agents, /# Project/);
});

test('malformed managed markers fail without overwriting AGENTS', () => {
  const cwd = tempProject();
  const original = `# Project\n\n${START}\nbroken\n`;
  writeFileSync(join(cwd, 'AGENTS.md'), original, 'utf8');

  const result = run(cwd, ['install']);
  assert.equal(result.status, 1);
  assert.equal(readFileSync(join(cwd, 'AGENTS.md'), 'utf8'), original);
});

test('--no-agents installs Skill without touching AGENTS', () => {
  const cwd = tempProject();
  const result = run(cwd, ['install', '--no-agents']);

  assert.equal(result.status, 0, result.stderr);
  assert.equal(existsSync(join(cwd, '.agents', 'skills', 'engsense', 'SKILL.md')), true);
  assert.equal(existsSync(join(cwd, 'AGENTS.md')), false);
});

test('status reports Skill and AGENTS integration', () => {
  const cwd = tempProject();
  assert.equal(run(cwd, ['install']).status, 0);

  const result = run(cwd, ['status']);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /installed codex:/);
  assert.match(result.stdout, /linked\s+agents:/);
});
