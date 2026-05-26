#!/usr/bin/env python3
"""Validate authoritative declarative YAML tables via loader functions."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _data_loaders import (  # noqa: E402
    SAFETY_ARTIFACT_TABLE_NAMES,
    coursebook_profiles,
    safety_artifact_tables_payload,
)


def main() -> None:
    profiles = coursebook_profiles()
    payload = safety_artifact_tables_payload()
    yaml_keys = set(payload)
    expected_keys = set(SAFETY_ARTIFACT_TABLE_NAMES)
    missing = expected_keys - yaml_keys
    extra = yaml_keys - expected_keys
    if missing or extra:
        missing_text = ", ".join(sorted(missing)) or "-"
        extra_text = ", ".join(sorted(extra)) or "-"
        raise SystemExit(
            f"safety_artifact_tables.yaml key drift: missing={missing_text}; extra={extra_text}"
        )
    row_counts = {name: len(payload[name]) for name in SAFETY_ARTIFACT_TABLE_NAMES}
    print(f"coursebook_profiles: {len(profiles)} profiles")
    for name, count in row_counts.items():
        print(f"{name}: {count} rows")
    print("Declarative YAML validation passed.")


if __name__ == "__main__":
    main()
