#!/usr/bin/env python3
"""One-shot generator for data/coursebook_profiles.yaml from canonical tables."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from intelligence_content._06_part import COURSEBOOK_PROFILES  # noqa: E402


def _serialize_profile(profile) -> dict[str, object]:
    return {
        "identifier": profile.identifier,
        "disciplinary_frame": profile.disciplinary_frame,
        "key_distinction": profile.key_distinction,
        "vocabulary": [{"term": term, "definition": definition} for term, definition in profile.vocabulary],
        "worked_scenario": profile.worked_scenario,
        "worked_input": profile.worked_input,
        "worked_process": profile.worked_process,
        "worked_output": profile.worked_output,
        "practice_focus": profile.practice_focus,
        "review_question": profile.review_question,
    }


def main() -> None:
    payload = {
        "profiles": [_serialize_profile(profile) for profile in COURSEBOOK_PROFILES.values()],
    }
    out = PROJECT_ROOT / "data" / "coursebook_profiles.yaml"
    out.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {len(COURSEBOOK_PROFILES)} profiles to {out}")


if __name__ == "__main__":
    main()
