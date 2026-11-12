"""Teaching-phase ordering invariants for generated AGEINT chapters."""

from __future__ import annotations

from pathlib import Path

from manuscript_quality.inventory_helpers import (
    chapter_title_from_text,
    chapter_text,
    generated_chapter_files,
    manuscript_dir,
)
from manuscript_manifest._heading_titles import chapter_detail_titles, chapter_teaching_titles


def test_coursebook_sections_precede_runtime_maps_in_fixed_order(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path)
        title = chapter_title_from_text(text)
        teaching = chapter_teaching_titles(title)
        details = chapter_detail_titles(title)
        resolved_order = [
            f"### {teaching['primer']}",
            f"### {teaching['outcomes']}",
            f"### {teaching['vocabulary']}",
            f"### {teaching['lessons']}",
            f"### {teaching['example']}",
            f"### {teaching['sequence']}",
            f"### {teaching['check']}",
            f"### {details['architecture']}",
            f"### {details['evidence']}",
            f"#### {details['runtime_map']}",
            f"#### {details['subsection_contract']}",
        ]
        positions = [text.index(heading) for heading in resolved_order]
        assert positions == sorted(positions), path

