#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
EVAL_ROOT = REPO_ROOT / "evals"
CASES_DIR = EVAL_ROOT / "cases"

CORE_CONTEXT_FILES = (
    "SKILL.md",
    "decision-framework.md",
    "review-workflow.md",
    "references/conflicts.md",
)

AUTO_ROUTE_RULES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("rust",), "languages/rust.md"),
    (("typescript", " ts ", ".ts", ".tsx"), "languages/typescript.md"),
    (("python", ".py", "asyncio"), "languages/python.md"),
    (("retry", "idempot", "rpc", "distributed", "replica", "network", "node failure"), "domains/distributed-systems.md"),
    (("persist", "schema", "database", "transaction", "durable", "storage"), "domains/persistence.md"),
    (("thread", "lock", "queue", "concurr", "async", "atomic", "backpressure"), "domains/concurrency.md"),
    (("test", "mock", "fake", "fixture", "coverage"), "domains/testing.md"),
    (("api", "protocol", "public", "cli", "provider"), "domains/api-design.md"),
    (("performance", "latency", "throughput", "benchmark", "profile", "zero-copy", "rtt", "memory"), "principles/performance-engineering.md"),
    (("rewrite", "refactor", "migration", "cutover", "rollback", "coexist"), "principles/change-strategy.md"),
    (("representation", "serialize", "serialization", "graph", "normalize", "provenance", "intermediate representation"), "principles/representation-design.md"),
    (("interface", "trait", "abstraction", "provider", "factory"), "principles/evidence-driven-abstraction.md"),
    (("compatib", "deprecat", "version", "public api", "persisted format"), "principles/evolution-and-compatibility.md"),
    (("complexity", "indirection", "caller", "centraliz", "locality"), "principles/complexity-placement.md"),
)


class EvalError(RuntimeError):
    pass


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def load_cases(selected: set[str] | None = None, limit: int | None = None) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in sorted(CASES_DIR.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        if selected and case["id"] not in selected:
            continue
        case["_path"] = str(path.relative_to(REPO_ROOT))
        cases.append(case)

    if selected:
        found = {case["id"] for case in cases}
        missing = selected - found
        if missing:
            raise EvalError(f"unknown case id(s): {', '.join(sorted(missing))}")

    return cases[:limit] if limit is not None else cases


def case_search_text(case: dict[str, Any]) -> str:
    values = [case["title"], case["task"], *case.get("context", []), *case.get("evidence", [])]
    if case.get("snippet"):
        values.append(case["snippet"])
    return "\n".join(values).lower()


def routed_context_files(case: dict[str, Any], mode: str) -> list[str]:
    if mode == "none":
        return []

    files = list(CORE_CONTEXT_FILES)
    if mode == "core":
        return files

    if mode == "all":
        for directory in ("languages", "domains", "principles"):
            for path in sorted((REPO_ROOT / directory).glob("*.md")):
                if path.name != "README.md":
                    files.append(str(path.relative_to(REPO_ROOT)))
        return dedupe(files)

    if mode != "auto":
        raise EvalError(f"unsupported context mode: {mode}")

    text = case_search_text(case)
    files.append("languages/general.md")
    for needles, path in AUTO_ROUTE_RULES:
        if any(needle in text for needle in needles):
            files.append(path)
    return dedupe(files)


def read_context_bundle(files: list[str]) -> str:
    sections: list[str] = []
    for rel in files:
        path = REPO_ROOT / rel
        if not path.exists():
            raise EvalError(f"context file does not exist: {rel}")
        sections.append(f"### {rel}\n\n{path.read_text(encoding='utf-8').strip()}")
    return "\n\n".join(sections)


def target_prompt(case: dict[str, Any], context_mode: str) -> tuple[str, list[str]]:
    files = routed_context_files(case, context_mode)
    scenario: dict[str, Any] = {
        "mode": case["mode"],
        "task": case["task"],
        "context": case["context"],
        "evidence": case["evidence"],
    }
    if case.get("snippet"):
        scenario["snippet"] = case["snippet"]

    parts = [
        "Apply EngSense to the engineering scenario below.",
        "Use only the scenario evidence and supplied EngSense context. Do not invent repository facts.",
        "Give a concrete decision or recommendation, material trade-offs, assumptions or uncertainty, and an appropriate verification path.",
        "If specialist semantics are required, state the boundary rather than guessing.",
        "Do not mention that this is an eval and do not discuss the hidden rubric.",
    ]
    if files:
        parts.extend(["## EngSense skill context", read_context_bundle(files)])
    parts.extend(["## Scenario", json.dumps(scenario, ensure_ascii=False, indent=2)])
    return "\n\n".join(parts), files


def criterion_array(count: int, bool_name: str) -> dict[str, Any]:
    return {
        "type": "array",
        "minItems": count,
        "maxItems": count,
        "items": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "criterion": {"type": "string"},
                bool_name: {"type": "boolean"},
                "evidence": {"type": "string"},
            },
            "required": ["criterion", bool_name, "evidence"],
        },
    }


def judge_schema(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "case_id": {"type": "string"},
            "decision_properties": criterion_array(len(case["expected_decision_properties"]), "met"),
            "unacceptable_reasoning": criterion_array(len(case["unacceptable_reasoning"]), "present"),
            "verification": criterion_array(len(case["verification_expectations"]), "met"),
            "quality_dimensions": criterion_array(len(case["expected_quality_dimensions"]), "addressed"),
            "authority": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "expected": {"type": "string"},
                    "observed": {"type": "string"},
                    "acceptable": {"type": "boolean"},
                    "reason": {"type": "string"},
                },
                "required": ["expected", "observed", "acceptable", "reason"],
            },
            "specialist_boundary_ok": {"type": "boolean"},
            "summary": {"type": "string"},
        },
        "required": [
            "case_id",
            "decision_properties",
            "unacceptable_reasoning",
            "verification",
            "quality_dimensions",
            "authority",
            "specialist_boundary_ok",
            "summary",
        ],
    }


def judge_prompt(case: dict[str, Any], response: str) -> str:
    rubric = {
        "case_id": case["id"],
        "task": case["task"],
        "context": case["context"],
        "evidence": case["evidence"],
        "expected_decision_properties": case["expected_decision_properties"],
        "unacceptable_reasoning": case["unacceptable_reasoning"],
        "expected_quality_dimensions": case["expected_quality_dimensions"],
        "expected_authority": case["expected_authority"],
        "verification_expectations": case["verification_expectations"],
        "expected_tradeoffs": case.get("expected_tradeoffs", []),
        "specialist_boundary": case.get("specialist_boundary", []),
    }
    return "\n\n".join(
        [
            "You are judging an EngSense behavioral evaluation.",
            "Judge only the assistant response against the supplied rubric and scenario evidence.",
            "Do not reward matching wording; judge whether the engineering behavior is materially present.",
            "Copy every rubric criterion exactly into the corresponding criterion field and preserve rubric order.",
            "Unacceptable reasoning is present only when it drives the answer, not when it is mentioned to reject it.",
            "Authority is acceptable when certainty and severity fit the evidence; exact vocabulary is not required.",
            "Verification is met only when the answer gives a materially equivalent check.",
            "specialist_boundary_ok is true when no boundary is required or when required boundaries are respected.",
            "Do not reveal chain-of-thought. Return only the requested JSON object.",
            "## Rubric",
            json.dumps(rubric, ensure_ascii=False, indent=2),
            "## Assistant response",
            response,
        ]
    )


def parse_json_text(text: str) -> dict[str, Any]:
    stripped = text.strip()
    fence = chr(96) * 3
    if stripped.startswith(fence):
        lines = stripped.splitlines()[1:]
        if lines and lines[-1].strip() == fence:
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()

    try:
        value = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise EvalError(f"judge did not return valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise EvalError("judge JSON must be an object")
    return value


def validate_judgment_shape(case: dict[str, Any], judgment: dict[str, Any]) -> None:
    if judgment.get("case_id") != case["id"]:
        raise EvalError(f"judge returned wrong case_id: {judgment.get('case_id')!r}")

    checks = (
        ("decision_properties", case["expected_decision_properties"], "met"),
        ("unacceptable_reasoning", case["unacceptable_reasoning"], "present"),
        ("verification", case["verification_expectations"], "met"),
        ("quality_dimensions", case["expected_quality_dimensions"], "addressed"),
    )
    for field, expected, bool_field in checks:
        items = judgment.get(field)
        if not isinstance(items, list) or len(items) != len(expected):
            raise EvalError(f"judge field {field!r} must contain {len(expected)} item(s)")
        for index, (item, criterion) in enumerate(zip(items, expected, strict=True)):
            if not isinstance(item, dict):
                raise EvalError(f"judge field {field}[{index}] must be an object")
            if item.get("criterion") != criterion:
                raise EvalError(f"judge field {field}[{index}].criterion must exactly match the rubric")
            if not isinstance(item.get(bool_field), bool):
                raise EvalError(f"judge field {field}[{index}].{bool_field} must be boolean")
            if not isinstance(item.get("evidence"), str):
                raise EvalError(f"judge field {field}[{index}].evidence must be a string")

    authority = judgment.get("authority")
    if not isinstance(authority, dict):
        raise EvalError("judge authority must be an object")
    if authority.get("expected") != case["expected_authority"]:
        raise EvalError("judge authority.expected must match the rubric")
    if not isinstance(authority.get("acceptable"), bool):
        raise EvalError("judge authority.acceptable must be boolean")
    if not isinstance(authority.get("observed"), str) or not isinstance(authority.get("reason"), str):
        raise EvalError("judge authority observed/reason must be strings")
    if not isinstance(judgment.get("specialist_boundary_ok"), bool):
        raise EvalError("judge specialist_boundary_ok must be boolean")
    if not isinstance(judgment.get("summary"), str):
        raise EvalError("judge summary must be a string")


def aggregate_judgment(case: dict[str, Any], judgment: dict[str, Any]) -> tuple[bool, dict[str, bool]]:
    validate_judgment_shape(case, judgment)
    components = {
        "decision_properties": all(item["met"] for item in judgment["decision_properties"]),
        "unacceptable_reasoning_absent": not any(item["present"] for item in judgment["unacceptable_reasoning"]),
        "verification": all(item["met"] for item in judgment["verification"]),
        "authority": bool(judgment["authority"]["acceptable"]),
        "specialist_boundary": bool(judgment["specialist_boundary_ok"]),
    }
    return all(components.values()), components


class CommandProvider:
    def __init__(self, command: str, timeout: int):
        if not command or not command.strip():
            raise EvalError("command provider requires a command")
        self.argv = shlex.split(command)
        self.timeout = timeout

    def generate(self, prompt: str, case_id: str, schema: dict[str, Any] | None = None) -> str:
        argv = [part.replace("{case_id}", case_id) for part in self.argv]
        env = os.environ.copy()
        if schema is not None:
            env["ENGSENSE_EVAL_JSON_SCHEMA"] = json.dumps(schema, ensure_ascii=False)
        proc = subprocess.run(
            argv,
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=REPO_ROOT,
            env=env,
            timeout=self.timeout,
            check=False,
        )
        if proc.returncode != 0:
            raise EvalError(f"command failed for {case_id} with exit {proc.returncode}: {proc.stderr.strip()[:1000]}")
        output = proc.stdout.strip()
        if not output:
            raise EvalError(f"command returned empty output for {case_id}")
        return output


class OpenAIProvider:
    def __init__(self, model: str, timeout: int, max_output_tokens: int):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EvalError("OPENAI_API_KEY is required for the OpenAI provider")
        if not model:
            raise EvalError("OpenAI provider requires a model")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.max_output_tokens = max_output_tokens
        self.base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

    def generate(self, prompt: str, case_id: str, schema: dict[str, Any] | None = None) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "input": prompt,
            "store": False,
            "max_output_tokens": self.max_output_tokens,
            "metadata": {"engsense_eval_case": case_id},
        }
        if schema is not None:
            payload["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": "engsense_eval_judgment",
                    "strict": True,
                    "schema": schema,
                }
            }

        request = urllib.request.Request(
            f"{self.base_url}/responses",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise EvalError(f"OpenAI API HTTP {exc.code}: {detail[:1200]}") from exc
        except urllib.error.URLError as exc:
            raise EvalError(f"OpenAI API request failed: {exc}") from exc

        if body.get("status") not in (None, "completed"):
            raise EvalError(f"OpenAI response status is {body.get('status')!r}")

        text_parts: list[str] = []
        refusals: list[str] = []
        for item in body.get("output", []):
            if not isinstance(item, dict):
                continue
            for part in item.get("content", []):
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                    text_parts.append(part["text"])
                elif part.get("type") == "refusal" and isinstance(part.get("refusal"), str):
                    refusals.append(part["refusal"])

        if refusals and not text_parts:
            raise EvalError(f"OpenAI provider refused case {case_id}: {' '.join(refusals)[:800]}")
        output = "\n".join(text_parts).strip()
        if not output:
            raise EvalError(f"OpenAI provider returned no output text for {case_id}")
        return output


def make_provider(kind: str, command: str | None, model: str | None, timeout: int, max_output_tokens: int):
    if kind == "command":
        return CommandProvider(command or "", timeout)
    if kind == "openai":
        return OpenAIProvider(model or "", timeout, max_output_tokens)
    raise EvalError(f"unsupported provider: {kind}")


def write_markdown_report(path: Path, report: dict[str, Any]) -> None:
    target_label = report["target"].get("model") or report["target"].get("command") or ""
    judge_label = report["judge"].get("model") or report["judge"].get("command") or ""
    lines = [
        "# EngSense Behavioral Eval Report",
        "",
        f"- Timestamp: {report['created_at']}",
        f"- Target: {report['target']['provider']} {target_label}".rstrip(),
        f"- Judge: {report['judge']['provider']} {judge_label}".rstrip(),
        f"- Context mode: {report['context_mode']}",
        f"- Cases: {report['summary']['total']}",
        f"- Passed: {report['summary']['passed']}",
        f"- Failed: {report['summary']['failed']}",
        f"- Errors: {report['summary']['errors']}",
        "",
        "## Results",
        "",
        "| Case | Result | Summary |",
        "|---|---|---|",
    ]
    for item in report["cases"]:
        status = "ERROR" if item.get("error") else ("PASS" if item.get("passed") else "FAIL")
        summary = item.get("judgment", {}).get("summary", item.get("error", ""))
        summary = str(summary).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {item['id']} | {status} | {summary} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run EngSense behavioral evaluation cases.")
    parser.add_argument("--case", action="append", dest="cases", help="Case id to run; repeatable.")
    parser.add_argument("--limit", type=int, help="Run only the first N selected cases.")
    parser.add_argument("--context-mode", choices=("auto", "core", "all", "none"), default="auto")
    parser.add_argument("--target-provider", choices=("command", "openai"), default=os.environ.get("ENGSENSE_EVAL_TARGET_PROVIDER", "command"))
    parser.add_argument("--target-command", default=os.environ.get("ENGSENSE_EVAL_TARGET_CMD"))
    parser.add_argument("--target-model", default=os.environ.get("ENGSENSE_EVAL_TARGET_MODEL"))
    parser.add_argument("--judge-provider", choices=("command", "openai"), default=os.environ.get("ENGSENSE_EVAL_JUDGE_PROVIDER", "command"))
    parser.add_argument("--judge-command", default=os.environ.get("ENGSENSE_EVAL_JUDGE_CMD"))
    parser.add_argument("--judge-model", default=os.environ.get("ENGSENSE_EVAL_JUDGE_MODEL"))
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--target-max-output-tokens", type=int, default=2500)
    parser.add_argument("--judge-max-output-tokens", type=int, default=3500)
    parser.add_argument("--output", type=Path, default=EVAL_ROOT / "out" / "behavioral-results.json")
    parser.add_argument("--fail-on-eval-failure", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        selected = set(args.cases) if args.cases else None
        cases = load_cases(selected, args.limit)
        if not cases:
            raise EvalError("no eval cases selected")

        target = make_provider(args.target_provider, args.target_command, args.target_model, args.timeout, args.target_max_output_tokens)
        judge = make_provider(args.judge_provider, args.judge_command, args.judge_model, args.timeout, args.judge_max_output_tokens)

        results: list[dict[str, Any]] = []
        for index, case in enumerate(cases, start=1):
            case_id = case["id"]
            print(f"[{index}/{len(cases)}] {case_id}", flush=True)
            result: dict[str, Any] = {"id": case_id, "title": case["title"], "fixture": case["_path"]}
            try:
                prompt, context_files = target_prompt(case, args.context_mode)
                response = target.generate(prompt, case_id)
                raw_judgment = judge.generate(judge_prompt(case, response), case_id, judge_schema(case))
                judgment = parse_json_text(raw_judgment)
                passed, components = aggregate_judgment(case, judgment)
                result.update(
                    {
                        "context_files": context_files,
                        "response": response,
                        "judgment": judgment,
                        "components": components,
                        "passed": passed,
                    }
                )
                print("  PASS" if passed else "  FAIL", flush=True)
            except Exception as exc:
                result.update({"passed": False, "error": f"{type(exc).__name__}: {exc}"})
                print(f"  ERROR: {exc}", file=sys.stderr, flush=True)
            results.append(result)

        passed_count = sum(1 for item in results if item.get("passed"))
        errors = sum(1 for item in results if item.get("error"))
        failed_count = len(results) - passed_count - errors

        report = {
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "context_mode": args.context_mode,
            "target": {
                "provider": args.target_provider,
                "model": args.target_model if args.target_provider == "openai" else None,
                "command": args.target_command if args.target_provider == "command" else None,
            },
            "judge": {
                "provider": args.judge_provider,
                "model": args.judge_model if args.judge_provider == "openai" else None,
                "command": args.judge_command if args.judge_provider == "command" else None,
            },
            "summary": {
                "total": len(results),
                "passed": passed_count,
                "failed": failed_count,
                "errors": errors,
            },
            "cases": results,
        }

        output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_markdown_report(output.with_suffix(".md"), report)

        print(f"Behavioral evals: {passed_count}/{len(results)} passed, {failed_count} failed, {errors} error(s)")
        try:
            print(f"Report: {output.relative_to(REPO_ROOT)}")
        except ValueError:
            print(f"Report: {output}")

        if args.fail_on_eval_failure and (failed_count or errors):
            return 1
        return 0
    except EvalError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
