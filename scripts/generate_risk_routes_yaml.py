#!/usr/bin/env python3
"""Validate data/topic_risk_routes.yaml (authoritative SSOT for risk routing)."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _data_loaders import topic_risk_routes_payload  # noqa: E402


def main() -> None:
    payload = topic_risk_routes_payload()
    topic_count = len(payload["topic_rules"])
    chapter_count = len(payload["chapter_context_rules"])
    print(f"topic_risk_routes.yaml: {topic_count} topic rules, {chapter_count} chapter rules")
    print("Validation passed.")


if __name__ == "__main__":
    main()
