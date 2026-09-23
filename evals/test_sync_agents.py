#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "sync_agents.py"
BEGIN = "<!-- engsense:begin -->"
END = "<!-- engsense:end -->"


class SyncAgentsTests(unittest.TestCase):
    def run_sync(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def test_creates_canonical_agents_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_sync(root)
            self.assertEqual(result.returncode, 0, result.stderr)

            path = root / "AGENTS.md"
            self.assertTrue(path.is_file())
            content = path.read_text(encoding="utf-8")
            self.assertIn(BEGIN, content)
            self.assertIn(END, content)

    def test_preserves_existing_content_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "AGENTS.md"
            path.write_text("# Project\n\nKeep this rule.\n", encoding="utf-8")

            first = self.run_sync(root)
            self.assertEqual(first.returncode, 0, first.stderr)
            once = path.read_text(encoding="utf-8")

            second = self.run_sync(root)
            self.assertEqual(second.returncode, 0, second.stderr)
            twice = path.read_text(encoding="utf-8")

            self.assertIn("Keep this rule.", twice)
            self.assertEqual(once, twice)
            self.assertEqual(twice.count(BEGIN), 1)
            self.assertEqual(twice.count(END), 1)

    def test_updates_stale_managed_block_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "AGENTS.md"
            path.write_text(
                "# Project\n\n"
                f"{BEGIN}\nold EngSense text\n{END}\n\n"
                "## User rule\nPreserve me.\n",
                encoding="utf-8",
            )

            result = self.run_sync(root)
            self.assertEqual(result.returncode, 0, result.stderr)

            content = path.read_text(encoding="utf-8")
            self.assertNotIn("old EngSense text", content)
            self.assertIn("## User rule\nPreserve me.", content)
            self.assertEqual(content.count(BEGIN), 1)

    def test_reuses_existing_case_variant(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lower = root / "agents.md"
            lower.write_text("# Existing\n", encoding="utf-8")

            result = self.run_sync(root)
            self.assertEqual(result.returncode, 0, result.stderr)

            self.assertTrue(lower.exists())
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertIn(BEGIN, lower.read_text(encoding="utf-8"))

    def test_check_reports_outdated_then_current(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            before = self.run_sync(root, "--check")
            self.assertEqual(before.returncode, 1)

            synced = self.run_sync(root)
            self.assertEqual(synced.returncode, 0, synced.stderr)

            after = self.run_sync(root, "--check")
            self.assertEqual(after.returncode, 0, after.stderr)

    def test_remove_preserves_user_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "AGENTS.md"
            path.write_text("# Project\n\nKeep me.\n", encoding="utf-8")

            synced = self.run_sync(root)
            self.assertEqual(synced.returncode, 0, synced.stderr)

            removed = self.run_sync(root, "--remove")
            self.assertEqual(removed.returncode, 0, removed.stderr)

            content = path.read_text(encoding="utf-8")
            self.assertEqual(content, "# Project\n\nKeep me.\n")
            self.assertNotIn(BEGIN, content)

    def test_remove_deletes_engsense_only_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "AGENTS.md"

            synced = self.run_sync(root)
            self.assertEqual(synced.returncode, 0, synced.stderr)
            self.assertTrue(path.exists())

            removed = self.run_sync(root, "--remove")
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertFalse(path.exists())

    def test_malformed_markers_fail_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "AGENTS.md"
            original = f"# Project\n\n{BEGIN}\nbroken\n"
            path.write_text(original, encoding="utf-8")

            result = self.run_sync(root)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
