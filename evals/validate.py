#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
CASES_DIR = ROOT / "cases"

REQUIRED = {
    "id",
    "title",
    "mode",
    "task",
    "context",
    "evidence",
    "tempting_wrong_recommendation",
    "expected_decision_properties",
    "unacceptable_reasoning",
    "expected_quality_dimensions",
    "expected_authority",
    "verification_expectations",
}

OPTIONAL = {
    "snippet",
    "expected_tradeoffs",
    "revisit_when",
    "specialist_boundary",
    "notes",
}

ALLOWED = REQUIRED | OPTIONAL

LIST_FIELDS = {
    "context",
    "evidence",
    "tempting_wrong_recommendation",
    "expected_decision_properties",
    "unacceptable_reasoning",
    "expected_quality_dimensions",
    "verification_expectations",
}

OPTIONAL_LIST_FIELDS = {
    "expected_tradeoffs",
    "revisit_when",
    "specialist_boundary",
}

MODES = {"focused", "refactoring", "architecture"}
AUTHORITIES = {
    "invariant",
    "rule",
    "strong_recommendation",
    "guidance",
    "heuristic",
    "note",
}

ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]+$")


def fail(path: Path, message: str) -> str:
    return f"{path.relative_to(ROOT.parent)}: {message}"


def validate_string_list(path: Path, case: dict, field: str, *, required: bool) -> list[str]:
    if field not in case:
        return [] if not required else [fail(path, f"{field} is required")]

    value = case[field]
    if not isinstance(value, list):
        return [fail(path, f"{field} must be a list")]

    if required and not value:
        return [fail(path, f"{field} must be a non-empty list")]

    if any(not isinstance(item, str) or not item.strip() for item in value):
        return [fail(path, f"{field} must contain only non-empty strings")]

    return []


def validate_case(path: Path) -> tuple[dict | None, list[str]]:
    errors: list[str] = []

    try:
        case = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [fail(path, f"invalid JSON: {exc}")]

    if not isinstance(case, dict):
        return None, [fail(path, "top-level value must be an object")]

    missing = sorted(REQUIRED - case.keys())
    if missing:
        errors.append(fail(path, f"missing required fields: {', '.join(missing)}"))

    unknown = sorted(case.keys() - ALLOWED)
    if unknown:
        errors.append(fail(path, f"unknown fields: {', '.join(unknown)}"))

    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id.strip():
        errors.append(fail(path, "id must be a non-empty string"))
    elif not ID_PATTERN.fullmatch(case_id):
        errors.append(
            fail(path, "id must match ^[a-z0-9][a-z0-9-]+$")
        )

    for field in ("title", "task"):
        value = case.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(fail(path, f"{field} must be a non-empty string"))

    if case.get("mode") not in MODES:
        errors.append(fail(path, f"unsupported mode: {case.get('mode')!r}"))

    if case.get("expected_authority") not in AUTHORITIES:
        errors.append(
            fail(path, f"unsupported expected_authority: {case.get('expected_authority')!r}")
        )

    for field in LIST_FIELDS:
        errors.extend(validate_string_list(path, case, field, required=True))

    for field in OPTIONAL_LIST_FIELDS:
        errors.extend(validate_string_list(path, case, field, required=False))

    if "snippet" in case and not isinstance(case["snippet"], str):
        errors.append(fail(path, "snippet must be a string when present"))

    if "notes" in case:
        notes = case["notes"]
        if not isinstance(notes, str) or not notes.strip():
            errors.append(fail(path, "notes must be a non-empty string when present"))

    return case, errors


def main() -> int:
    if not CASES_DIR.exists():
        print("evals/cases directory does not exist", file=sys.stderr)
        return 1

    paths = sorted(CASES_DIR.glob("*.json"))
    if not paths:
        print("no eval cases found", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_ids: dict[str, Path] = {}

    for path in paths:
        case, case_errors = validate_case(path)
        errors.extend(case_errors)
        if case is None:
            continue

        case_id = case.get("id")
        if isinstance(case_id, str) and case_id:
            if case_id in seen_ids:
                errors.append(
                    fail(
                        path,
                        f"duplicate id {case_id!r}; first seen in "
                        f"{seen_ids[case_id].relative_to(ROOT.parent)}",
                    )
                )
            else:
                seen_ids[case_id] = path

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
        return 1

    print(f"OK: {len(paths)} EngSense eval case(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
