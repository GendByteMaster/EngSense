#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

BEGIN = "<!-- engsense:begin -->"
END = "<!-- engsense:end -->"
BLOCK_RE = re.compile(
    rf"{re.escape(BEGIN)}.*?{re.escape(END)}",
    re.DOTALL,
)


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_block() -> str:
    path = skill_root() / "assets" / "agents-snippet.md"
    return path.read_text(encoding="utf-8").strip()


def detect_repo_root(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()

    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return Path.cwd().resolve()

    root = completed.stdout.strip()
    return Path(root).resolve() if root else Path.cwd().resolve()


def find_agents_file(root: Path) -> Path:
    canonical = root / "AGENTS.md"
    if canonical.exists():
        return canonical

    matches = sorted(
        (
            path
            for path in root.iterdir()
            if path.is_file() and path.name.casefold() == "agents.md"
        ),
        key=lambda path: path.name,
    )
    return matches[0] if matches else canonical


def render_updated(existing: str, block: str) -> tuple[str, bool]:
    has_begin = BEGIN in existing
    has_end = END in existing

    if has_begin != has_end:
        raise ValueError(
            "AGENTS.md contains only one EngSense managed marker; "
            "repair the malformed block before syncing"
        )

    if has_begin:
        matches = list(BLOCK_RE.finditer(existing))
        if len(matches) != 1:
            raise ValueError(
                "AGENTS.md must contain exactly one EngSense managed block"
            )
        updated = BLOCK_RE.sub(block, existing, count=1)
        return updated, updated != existing

    if not existing.strip():
        return block + "\n", True

    separator = "\n\n" if existing.endswith("\n") else "\n\n"
    return existing.rstrip() + separator + block + "\n", True


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)

    try:
        os.replace(temp_path, path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def render_removed(existing: str) -> tuple[str, bool]:
    has_begin = BEGIN in existing
    has_end = END in existing

    if has_begin != has_end:
        raise ValueError(
            "AGENTS.md contains only one EngSense managed marker; "
            "repair the malformed block before removing it"
        )

    if not has_begin:
        return existing, False

    matches = list(BLOCK_RE.finditer(existing))
    if len(matches) != 1:
        raise ValueError(
            "AGENTS.md must contain exactly one EngSense managed block"
        )

    match = matches[0]
    before = existing[: match.start()].rstrip()
    after = existing[match.end() :].lstrip("\n")

    if before and after:
        return before + "\n\n" + after, True
    if before:
        return before + "\n", True
    if after:
        return after, True
    return "", True


def sync(root: Path, *, check: bool, remove: bool) -> int:
    path = find_agents_file(root)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    try:
        if remove:
            updated, changed = render_removed(existing)
        else:
            updated, changed = render_updated(existing, load_block())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if check:
        if changed:
            print(
                f"OUTDATED: {path} does not contain the current EngSense managed block",
                file=sys.stderr,
            )
            return 1
        print(f"OK: EngSense block is current in {path}")
        return 0

    if not changed:
        action = "not present" if remove else "already current"
        print(f"OK: EngSense block {action} in {path}")
        return 0

    if remove and not updated:
        if path.exists():
            path.unlink()
        print(f"Removed EngSense-only AGENTS.md: {path}")
        return 0

    atomic_write(path, updated)
    action = "Removed EngSense block from" if remove else ("Created" if not existing else "Updated")
    print(f"{action}: {path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Idempotently register the EngSense Skill in the repository-root "
            "AGENTS.md while preserving all user-authored content."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Repository root. Defaults to git rev-parse --show-toplevel, then cwd.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Check whether AGENTS.md already contains the current managed block.",
    )
    mode.add_argument(
        "--remove",
        action="store_true",
        help="Remove only the EngSense managed block, preserving other AGENTS.md content.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = detect_repo_root(args.root)

    if not root.exists() or not root.is_dir():
        print(f"ERROR: repository root is not a directory: {root}", file=sys.stderr)
        return 2

    return sync(root, check=args.check, remove=args.remove)


if __name__ == "__main__":
    raise SystemExit(main())
