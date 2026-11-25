"""Synthetic unit tests for the release evidence schema, not live model results."""
import unittest

from validate_release_review import ENV_KEYS, REQUIRED_RUNS, validate


class ReleaseReviewTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            "status": "PASS",
            "reviewed_sha": "a" * 40,
            "environment": {key: "synthetic test value" for key in ENV_KEYS},
            "runs": [
                {"id": name, "status": "PASS", "rationale": "synthetic",
                 "transcript_ref": "synthetic"}
                for name in sorted(REQUIRED_RUNS)
            ],
        }

    def test_complete_shape(self):
        self.assertEqual(validate(self.record, "Status: PASS."), [])

    def test_unrun(self):
        self.assertTrue(validate(
            {"status": "NOT_RUN", "reviewed_sha": None, "environment": {}, "runs": []},
            "Status: NOT RUN.",
        ))

    def test_missing_case(self):
        self.record["runs"].pop()
        self.assertTrue(any("missing runs" in e for e in validate(self.record, "Status: PASS.")))

    def test_fail_or_inconclusive(self):
        for status in ("FAIL", "INCONCLUSIVE"):
            with self.subTest(status=status):
                self.record["runs"][0]["status"] = status
                self.assertTrue(validate(self.record, "Status: PASS."))

    def test_missing_evidence(self):
        self.record["runs"][0]["transcript_ref"] = ""
        self.assertTrue(validate(self.record, "Status: PASS."))

    def test_invalid_commit_or_environment(self):
        self.record["reviewed_sha"] = "main"
        self.record["environment"] = {}
        self.assertTrue(validate(self.record, "Status: PASS."))

    def test_duplicate_run(self):
        self.record["runs"].append(self.record["runs"][0].copy())
        self.assertTrue(any("duplicate run" in e for e in validate(self.record, "Status: PASS.")))

    def test_unknown_run(self):
        self.record["runs"].append({**self.record["runs"][0], "id": "unknown"})
        self.assertTrue(any("unknown" in e for e in validate(self.record, "Status: PASS.")))

    def test_missing_markdown_approval(self):
        self.assertTrue(validate(self.record, "Status: NOT RUN."))


if __name__ == "__main__":
    unittest.main()
