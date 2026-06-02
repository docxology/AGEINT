#!/usr/bin/env python3
"""Validate authoritative declarative YAML tables via loader functions."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _data_loaders import SAFETY_ARTIFACT_TABLE_NAMES, validate_declarative_tables  # noqa: E402


def main() -> None:
    counts = validate_declarative_tables()
    print(f"coursebook_profiles: {counts['coursebook_profiles']} profiles")
    for name in SAFETY_ARTIFACT_TABLE_NAMES:
        print(f"{name}: {counts[name]} rows")
    print(f"topic_risk_rules: {counts['topic_risk_rules']} rules")
    print(f"topic_risk_chapter_rules: {counts['topic_risk_chapter_rules']} chapter rules")
    print("Declarative YAML validation passed.")


if __name__ == "__main__":
    main()
