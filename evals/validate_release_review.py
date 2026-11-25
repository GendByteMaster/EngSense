#!/usr/bin/env python3
"""Validate the manual evidence manifest; never invoke or score a model."""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_RUNS = {
    "001", "002", "003", "004", "009", "010", "017", "019", "020",
    "025", "032", "046", "047", "048", "049", "050", "051",
    "009-repeat", "010-repeat", "051-repeat", "mechanical-rename",
}
ENV_KEYS = {
    "codex_version", "model", "effort", "date", "instruction_environment",
}
REVIEWED_PATHS = [
    "SKILL.md", "agents", "bin", "package.json", "decision-framework.md",
    "review-workflow.md", "principles", "languages", "domains", "references",
    "evals/cases", "test",
]


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: object, review: str) -> list[str]:
    if not isinstance(data, dict):
        return ["evidence manifest must be a JSON object"]
    errors = []
    if data.get("status") != "PASS" or review.splitlines().count("Status: PASS.") != 1:
        errors.append("manual Codex review is not recorded as PASS")
    sha = data.get("reviewed_sha")
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
        errors.append("reviewed_sha must be an exact 40-character commit SHA")
    env = data.get("environment")
    if not isinstance(env, dict) or any(not nonempty(env.get(k)) for k in ENV_KEYS):
        errors.append("review environment is incomplete")
    runs = data.get("runs")
    if not isinstance(runs, list):
        return errors + ["runs must be a list"]
    seen = set()
    for run in runs:
        if not isinstance(run, dict) or not isinstance(run.get("id"), str):
            errors.append("each run needs a string id")
            continue
        name = run["id"]
        if name in seen:
            errors.append(f"duplicate run: {name}")
        seen.add(name)
        if run.get("status") != "PASS":
            errors.append(f"run {name} did not pass")
        if not nonempty(run.get("rationale")) or not nonempty(run.get("transcript_ref")):
            errors.append(f"run {name} lacks rationale or transcript reference")
    missing = REQUIRED_RUNS - seen
    if missing:
        errors.append("missing runs: " + ", ".join(sorted(missing)))
    return errors


def main() -> int:
    try:
        data = json.loads((ROOT / "docs/CODEX_BEHAVIOR_RESULTS.json").read_text(encoding="utf-8"))
        review = (ROOT / "docs/CODEX_BEHAVIOR_REVIEW.md").read_text(encoding="utf-8")
        errors = validate(data, review)
        if not errors:
            sha = data["reviewed_sha"]
            result = subprocess.run(
                ["git", "diff", "--quiet", sha, "HEAD", "--", *REVIEWED_PATHS],
                cwd=ROOT, check=False,
            )
            if result.returncode != 0:
                errors.append("reviewed payload differs from HEAD or reviewed commit is unavailable")
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print("OK: manual evidence manifest complete and reviewed payload unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
