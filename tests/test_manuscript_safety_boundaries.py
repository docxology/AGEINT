"""Safety-boundary checks for generated AGEINT manuscript output."""

from __future__ import annotations

from pathlib import Path

from manuscript_quality.inventory_helpers import (
    BLOCKED_OPERATIONAL_PATTERN_PHRASES,
    PROJECT_ROOT,
    generated_output_files,
    manuscript_dir,
)


def test_safety_audit_blocks_operational_phrases_outside_source_audit_contexts(
    built_output: Path,
) -> None:
    output_manuscript = manuscript_dir(built_output)
    allowed_contexts = (
        "prohibit",
        "prohibits",
        "excluded",
        "blocked context",
        "unsafe source motif",
        "source motif retained for audit",
        "source_risk",
        "risk was avoided",
        "rather than",
        "does not",
        "do not",
        "no real",
        "no live",
        "tabletop",
        "synthetic",
        "fictional",
        "instructor-provided",
        "toy",
        "opt-in",
        "safe curriculum substitute",
        "safe curriculum treatment",
        "source title transformed",
    )
    for path in generated_output_files(output_manuscript):
        if "bibliography-atlas" in path.parts or path.name == "references.md":
            continue
        for line in path.read_text(encoding="utf-8").lower().splitlines():
            for phrase in BLOCKED_OPERATIONAL_PATTERN_PHRASES:
                if phrase not in line:
                    continue
                assert any(context in line for context in allowed_contexts), (
                    f"{path}: {phrase}: {line}"
                )


def test_safety_boundary_is_documented() -> None:
    safety = (PROJECT_ROOT / "docs" / "safety.md").read_text(encoding="utf-8").lower()
    assert "evidence-bounded" in safety
    assert "accountable" in safety
    assert "synthetic" in safety
    assert "unauthorized" in safety
    assert "non-operational" not in safety
