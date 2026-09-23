#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent

CORE_FILES = {
    Path("SKILL.md"),
    Path("decision-framework.md"),
    Path("review-workflow.md"),
    Path("agents/openai.yaml"),
    Path("package.json"),
    Path("bin/engsense.js"),
}

CORE_DIRS = (
    Path("principles"),
    Path("languages"),
    Path("domains"),
    Path("references"),
)

REFERENCE_PATTERN = re.compile(
    r"`((?:principles|languages|domains|references)/[a-z0-9-]+\.md|"
    r"decision-framework\.md|review-workflow\.md)`"
)

FORBIDDEN_EXECUTABLE_PATTERNS = {
    "OPENAI_API_KEY": re.compile(r"OPENAI_API_KEY", re.IGNORECASE),
    "API key assignment": re.compile(r"\bapi_key\s*=", re.IGNORECASE),
    "OpenAI Python SDK import": re.compile(
        r"^\s*(?:from\s+openai\s+import|import\s+openai\b)", re.MULTILINE
    ),
    "OpenAI JavaScript SDK import": re.compile(
        r"(?:from\s+['\"]openai['\"]|require\(['\"]openai['\"]\))"
    ),
    "OpenAI client construction": re.compile(r"\bOpenAI\s*\("),
    "OpenAI responses call": re.compile(r"\bclient\.responses\."),
    "OpenAI chat completions call": re.compile(r"\bclient\.chat\.completions\."),
}

EXECUTABLE_SUFFIXES = {
    ".py",
    ".js",
    ".mjs",
    ".cjs",
    ".sh",
    ".bash",
    ".yml",
    ".yaml",
}

EVAL_NAME_PATTERN = re.compile(r"^(\d{3})-[a-z0-9][a-z0-9-]*\.json$")
README_CASE_PATTERN = re.compile(r"^(\d+)\.\s+.+$", re.MULTILINE)
README_FIXTURE_COUNT_PATTERN = re.compile(r"\b(\d+) deterministic eval fixtures\b")
CHECKLIST_FIXTURE_COUNT_PATTERN = re.compile(r"Current fixture set contains (\d+) scenarios\.")


def error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def load(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def validate_required_structure(errors: list[str]) -> None:
    for path in sorted(CORE_FILES):
        if not (ROOT / path).is_file():
            errors.append(f"missing required Skill/installer file: {path}")

    for directory in CORE_DIRS:
        full = ROOT / directory
        if not full.is_dir():
            errors.append(f"missing Skill support directory: {directory}")
            continue
        if not any(full.glob("*.md")):
            errors.append(f"Skill support directory has no Markdown modules: {directory}")


def validate_skill_references(errors: list[str]) -> None:
    skill = load(Path("SKILL.md"))
    referenced = sorted(set(REFERENCE_PATTERN.findall(skill)))
    for item in referenced:
        if not (ROOT / item).is_file():
            errors.append(f"SKILL.md references missing module: {item}")

    if "domains/domain-modeling.md" not in referenced:
        errors.append("SKILL.md must expose domains/domain-modeling.md in its routing surface")


def validate_installer_contract(errors: list[str]) -> None:
    try:
        package = json.loads(load(Path("package.json")))
    except json.JSONDecodeError as exc:
        errors.append(f"package.json is invalid JSON: {exc}")
        return

    if package.get("bin", {}).get("engsense") != "bin/engsense.js":
        errors.append("package.json must expose the engsense CLI at bin/engsense.js")

    cli = load(Path("bin/engsense.js"))
    required_tokens = (
        "install",
        "status",
        "uninstall",
        "--no-agents",
        "--global",
        "<!-- engsense:managed-start -->",
        "<!-- engsense:managed-end -->",
        "AGENTS.override.md",
        "AGENTS.md",
    )
    for token in required_tokens:
        if token not in cli:
            errors.append(f"bin/engsense.js is missing installer contract token: {token}")

    if "scripts/sync_agents.py" in load(Path("SKILL.md")):
        errors.append(
            "SKILL.md must not perform activation-time AGENTS self-registration; "
            "AGENTS integration belongs to the installer CLI"
        )


def validate_no_api_runtime_dependency(errors: list[str]) -> None:
    # EngSense may have installer/development executables, but not a model-provider runtime.
    candidates: list[Path] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts:
            continue
        if rel.parts and rel.parts[0] == "research":
            continue

        # The validator contains forbidden tokens as detection patterns.
        if rel == Path("evals/validate_skill.py"):
            continue

        if path.suffix.lower() in EXECUTABLE_SUFFIXES:
            candidates.append(path)

    for path in sorted(candidates):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        for label, pattern in FORBIDDEN_EXECUTABLE_PATTERNS.items():
            if pattern.search(text):
                errors.append(
                    f"{rel}: forbidden runtime/provider integration detected ({label}); "
                    "EngSense must remain a static Skill with installer-only local file management"
                )

    metadata = load(Path("agents/openai.yaml"))
    metadata_lower = metadata.lower()
    for forbidden in ("tool_dependencies:", "mcp_servers:", "mcp:", "api_key:", "api-key:"):
        if forbidden in metadata_lower:
            errors.append(
                f"agents/openai.yaml declares {forbidden.rstrip(':')}; "
                "metadata must remain invocation/UI metadata only"
            )


def validate_eval_catalog(errors: list[str]) -> int:
    cases_dir = ROOT / "evals" / "cases"
    paths = sorted(cases_dir.glob("*.json"))
    if not paths:
        errors.append("no eval fixtures found")
        return 0

    numbers: list[int] = []
    for path in paths:
        match = EVAL_NAME_PATTERN.fullmatch(path.name)
        if not match:
            errors.append(f"invalid eval filename: {path.relative_to(ROOT)}")
            continue

        numbers.append(int(match.group(1)))
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")

    expected = list(range(1, len(paths) + 1))
    if numbers != expected:
        errors.append(
            f"eval numbering must be contiguous 001..{len(paths):03d}; got "
            f"{', '.join(f'{n:03d}' for n in numbers)}"
        )

    eval_readme = load(Path("evals/README.md"))
    current_cases = eval_readme.split("## Current cases", 1)
    if len(current_cases) != 2:
        errors.append("evals/README.md is missing the Current cases section")
    else:
        section = current_cases[1].split("\n## ", 1)[0]
        listed = [int(n) for n in README_CASE_PATTERN.findall(section)]
        if listed != expected:
            errors.append(
                f"evals/README.md case catalog must list 1..{len(paths)} exactly once"
            )

    readme = load(Path("README.md"))
    readme_match = README_FIXTURE_COUNT_PATTERN.search(readme)
    if not readme_match or int(readme_match.group(1)) != len(paths):
        errors.append(f"README.md must report {len(paths)} deterministic eval fixtures")

    checklist = load(Path("RELEASE_CHECKLIST.md"))
    checklist_match = CHECKLIST_FIXTURE_COUNT_PATTERN.search(checklist)
    if not checklist_match or int(checklist_match.group(1)) != len(paths):
        errors.append(
            f"RELEASE_CHECKLIST.md must report {len(paths)} current scenarios"
        )

    return len(paths)


def main() -> int:
    errors: list[str] = []

    validate_required_structure(errors)
    validate_skill_references(errors)
    validate_installer_contract(errors)
    validate_no_api_runtime_dependency(errors)
    eval_count = validate_eval_catalog(errors)

    if errors:
        for message in errors:
            error(message)
        print(f"FAILED: {len(errors)} static Skill integrity error(s)", file=sys.stderr)
        return 1

    print(
        "OK: EngSense static Skill integrity validated "
        f"({eval_count} eval fixtures, ForgeGuard-style local installer, "
        "no API-key/model-provider runtime)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
