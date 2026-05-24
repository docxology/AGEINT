#!/usr/bin/env python3
"""Prepare AGEINT output scaffolding after the shared clean stage."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from output_docs import write_output_directory_docs  # noqa: E402


def main() -> int:
    written = write_output_directory_docs(PROJECT_ROOT)
    print(f"Wrote {len(written)} AGEINT output documentation files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
