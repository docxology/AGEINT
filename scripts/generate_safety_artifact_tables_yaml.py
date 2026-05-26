#!/usr/bin/env python3
"""One-shot generator for data/safety_artifact_tables.yaml from canonical tables."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from intelligence_content import _08_part as tables  # noqa: E402

TABLE_NAMES: tuple[str, ...] = (
    "SAFE_SUBSTITUTION_PATTERNS",
    "CAPSTONE_SCAFFOLDS",
    "ACCESSIBILITY_REVIEW_STEPS",
    "PROCUREMENT_OVERSIGHT_STEPS",
    "HRIA_DPIA_WORKSHEET",
    "DATA_LINEAGE_REGISTRY",
    "ASSESSMENT_INTEGRITY_PROTOCOL",
    "AGENT_INCIDENT_RESPONSE_DRILL",
    "ROLE_BASED_COMPETENCY_MAP",
    "ADVERSARIAL_ASSURANCE_CYCLE",
    "MODEL_DATASET_CARD",
    "TRANSPARENCY_NOTICE_WORKFLOW",
    "RETENTION_AUDIT_TRAIL",
    "RELEASE_CHANGE_CONTROL_GATE",
    "RISK_EXCEPTION_MEMO",
    "LEARNER_SUPPORT_PLAN",
    "INSTRUCTOR_QUESTION_BANK",
)


def main() -> None:
    payload: dict[str, list[dict[str, str]]] = {}
    for name in TABLE_NAMES:
        rows = getattr(tables, name)
        payload[name] = [dict(row) for row in rows]
    out = PROJECT_ROOT / "data" / "safety_artifact_tables.yaml"
    out.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {len(TABLE_NAMES)} tables to {out}")


if __name__ == "__main__":
    main()
