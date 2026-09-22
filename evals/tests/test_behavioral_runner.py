from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "evals" / "run_behavioral.py"

spec = importlib.util.spec_from_file_location("run_behavioral", MODULE_PATH)
assert spec and spec.loader
run_behavioral = importlib.util.module_from_spec(spec)
sys.modules["run_behavioral"] = run_behavioral
spec.loader.exec_module(run_behavioral)


class BehavioralRunnerTests(unittest.TestCase):
    def sample_case(self) -> dict:
        return {
            "id": "sample-case",
            "title": "Sample performance migration",
            "mode": "architecture",
            "task": "Review a Python service rewrite for latency.",
            "context": ["The service uses asyncio and a public API."],
            "evidence": ["A benchmark shows network RTT dominates local CPU."],
            "expected_decision_properties": ["Use the measured bottleneck."],
            "unacceptable_reasoning": ["Rewrite because Python is slow."],
            "expected_quality_dimensions": ["end_to_end_latency"],
            "expected_authority": "guidance",
            "verification_expectations": ["Rerun the end-to-end benchmark."],
            "specialist_boundary": ["Transport tuning needs networking expertise."],
        }

    def test_auto_routing_loads_relevant_modules(self) -> None:
        files = run_behavioral.routed_context_files(self.sample_case(), "auto")
        self.assertIn("SKILL.md", files)
        self.assertIn("languages/python.md", files)
        self.assertIn("principles/performance-engineering.md", files)
        self.assertIn("principles/change-strategy.md", files)
        self.assertIn("domains/api-design.md", files)

    def test_target_prompt_does_not_leak_hidden_rubric(self) -> None:
        prompt, _ = run_behavioral.target_prompt(self.sample_case(), "none")
        self.assertIn("Review a Python service rewrite for latency.", prompt)
        self.assertNotIn("Use the measured bottleneck.", prompt)
        self.assertNotIn("Rewrite because Python is slow.", prompt)

    def test_judge_schema_has_strict_top_level_object(self) -> None:
        schema = run_behavioral.judge_schema(self.sample_case())
        self.assertEqual(schema["type"], "object")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            schema["properties"]["decision_properties"]["minItems"],
            1,
        )

    def test_aggregate_passes_when_all_required_components_pass(self) -> None:
        case = self.sample_case()
        judgment = {
            "case_id": case["id"],
            "decision_properties": [
                {
                    "criterion": case["expected_decision_properties"][0],
                    "met": True,
                    "evidence": "Uses RTT evidence.",
                }
            ],
            "unacceptable_reasoning": [
                {
                    "criterion": case["unacceptable_reasoning"][0],
                    "present": False,
                    "evidence": "",
                }
            ],
            "verification": [
                {
                    "criterion": case["verification_expectations"][0],
                    "met": True,
                    "evidence": "Requests an end-to-end rerun.",
                }
            ],
            "quality_dimensions": [
                {
                    "criterion": case["expected_quality_dimensions"][0],
                    "addressed": True,
                    "evidence": "Discusses end-to-end latency.",
                }
            ],
            "authority": {
                "expected": "guidance",
                "observed": "guidance",
                "acceptable": True,
                "reason": "Scoped recommendation.",
            },
            "specialist_boundary_ok": True,
            "summary": "Pass",
        }
        passed, components = run_behavioral.aggregate_judgment(case, judgment)
        self.assertTrue(passed)
        self.assertTrue(all(components.values()))

    def test_unacceptable_reasoning_fails_case(self) -> None:
        case = self.sample_case()
        judgment = {
            "case_id": case["id"],
            "decision_properties": [
                {
                    "criterion": case["expected_decision_properties"][0],
                    "met": True,
                    "evidence": "Uses RTT evidence.",
                }
            ],
            "unacceptable_reasoning": [
                {
                    "criterion": case["unacceptable_reasoning"][0],
                    "present": True,
                    "evidence": "Recommends rewrite because Python is slow.",
                }
            ],
            "verification": [
                {
                    "criterion": case["verification_expectations"][0],
                    "met": True,
                    "evidence": "Rerun benchmark.",
                }
            ],
            "quality_dimensions": [
                {
                    "criterion": case["expected_quality_dimensions"][0],
                    "addressed": True,
                    "evidence": "Latency discussed.",
                }
            ],
            "authority": {
                "expected": "guidance",
                "observed": "guidance",
                "acceptable": True,
                "reason": "Scoped.",
            },
            "specialist_boundary_ok": True,
            "summary": "Fail",
        }
        passed, components = run_behavioral.aggregate_judgment(case, judgment)
        self.assertFalse(passed)
        self.assertFalse(components["unacceptable_reasoning_absent"])

    def test_parse_json_text_requires_object(self) -> None:
        with self.assertRaises(run_behavioral.EvalError):
            run_behavioral.parse_json_text(json.dumps(["not", "an", "object"]))


if __name__ == "__main__":
    unittest.main()
