#!/usr/bin/env python3
"""Generate tests/fixtures/topic_rotation_parity.json from the live curriculum."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from curriculum import load_curriculum  # noqa: E402
from intelligence_content._11_part import _coursebook_profile_for_titles  # noqa: E402
from intelligence_content._12_topic_frames import (  # noqa: E402
    misconception_for_entry,
    why_it_matters_for_entry,
)
from intelligence_content import profile_for_titles  # noqa: E402
from intelligence_content.topic_entries import safe_topic_entries  # noqa: E402

DATA = PROJECT_ROOT / "data" / "curriculum"
OUT = PROJECT_ROOT / "tests" / "fixtures" / "topic_rotation_parity.json"


def main() -> None:
    curriculum = load_curriculum(DATA)
    rows: list[dict[str, str]] = []
    for part in curriculum.parts:
        part_title = str(part["title"])
        for chapter in part["chapters"]:
            chapter_title = str(chapter["title"])
            profile = profile_for_titles(part_title, chapter_title, chapter=chapter)
            coursebook = _coursebook_profile_for_titles(part_title, chapter_title)
            for entry in safe_topic_entries(chapter, part):
                rows.append(
                    {
                        "display_title": entry.display_title,
                        "raw_title": entry.raw_title,
                        "risk_category": entry.risk_category,
                        "part_title": part_title,
                        "chapter_title": chapter_title,
                        "why_it_matters": why_it_matters_for_entry(
                            entry,
                            profile,
                            coursebook,
                            lesson_index=1,
                            chapter_title=chapter_title,
                        ),
                        "misconception": misconception_for_entry(
                            entry,
                            coursebook,
                            lesson_index=1,
                            chapter_title=chapter_title,
                        ),
                    }
                )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
