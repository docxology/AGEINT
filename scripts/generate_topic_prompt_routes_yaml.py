#!/usr/bin/env python3
"""Regenerate data/topic_prompt_routes.yaml from canonical tables in src/topic_route_tables.py."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from topic_route_tables import write_topic_prompt_routes_yaml  # noqa: E402


def main() -> None:
    out = write_topic_prompt_routes_yaml(PROJECT_ROOT)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
