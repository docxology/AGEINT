#!/usr/bin/env python3
"""Populate content_profile and practice_lens on chapter.json shards."""

from __future__ import annotations

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from curriculum import load_curriculum  # noqa: E402
from intelligence_content._06_part import (  # noqa: E402
    practice_lens_for_titles,
    profile_for_titles,
)


def main() -> None:
    curriculum = load_curriculum(PROJECT_ROOT / "data" / "curriculum")
    updated = 0
    for part in curriculum.parts:
        part_title = str(part["title"])
        for chapter in part["chapters"]:
            title = str(chapter["title"])
            profile = profile_for_titles(part_title, title)
            lens = practice_lens_for_titles(part_title, title)
            chapter_path = None
            for path in (PROJECT_ROOT / "data" / "curriculum" / "parts").rglob("chapter.json"):
                payload = json.loads(path.read_text(encoding="utf-8"))
                if payload.get("number") == chapter.get("number") and payload.get("title") == title:
                    chapter_path = path
                    break
            if chapter_path is None:
                continue
            payload = json.loads(chapter_path.read_text(encoding="utf-8"))
            payload["content_profile"] = profile.identifier
            payload["practice_lens"] = lens.identifier
            chapter_path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            updated += 1
    print(f"Updated {updated} chapter.json files")


if __name__ == "__main__":
    main()
