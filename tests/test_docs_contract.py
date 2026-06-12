"""Repository documentation contract checks."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_docs_use_working_checkout_template_validation_path() -> None:
    docs = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            PROJECT_ROOT / "AGENTS.md",
            PROJECT_ROOT / "docs" / "agent_instructions.md",
            PROJECT_ROOT / "docs" / "faq.md",
            PROJECT_ROOT / "docs" / "quickstart.md",
            PROJECT_ROOT / "docs" / "rendering_pipeline.md",
            PROJECT_ROOT / "docs" / "troubleshooting.md",
        ]
    )

    assert "projects/working/AGEINT/output/manuscript" in docs
    assert "projects/AGEINT/output/manuscript" not in docs
    assert "infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript" in docs
