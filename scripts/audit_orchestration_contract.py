#!/usr/bin/env python3
"""Audit AGEINT orchestration, audit, source-pack, and Mermaid contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from orchestration_audit import (  # noqa: E402
    collect_orchestration_contract,
    render_orchestration_contract_markdown,
    write_orchestration_contract,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--write", action="store_true", help="Write reports under output/reports.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.write:
        _json_path, _md_path, payload = write_orchestration_contract(PROJECT_ROOT)
    else:
        payload = collect_orchestration_contract(PROJECT_ROOT)
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_orchestration_contract_markdown(payload), end="")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
