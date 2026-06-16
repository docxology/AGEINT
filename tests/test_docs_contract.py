"""Repository documentation contract checks."""

from __future__ import annotations

import json
import re
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
            PROJECT_ROOT / "docs" / "orchestration_contract.md",
            PROJECT_ROOT / "docs" / "troubleshooting.md",
        ]
    )

    assert "projects/working/AGEINT/output/manuscript" in docs
    assert "projects/AGEINT/output/manuscript" not in docs
    assert "infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript" in docs


def test_docs_describe_registry_backed_contract_map() -> None:
    docs = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            PROJECT_ROOT / "docs" / "README.md",
            PROJECT_ROOT / "docs" / "architecture.md",
            PROJECT_ROOT / "docs" / "orchestration_contract.md",
            PROJECT_ROOT / "docs" / "quickstart.md",
        ]
    )

    assert "audit_orchestration_contract.py --format json" in docs
    assert "PipelineStageContract" in docs
    assert "AuditContract" in docs
    assert "SourcePackRegistry" in docs
    assert "Mermaid chart types" in docs


def test_docs_figure_counts_match_rendered_registry() -> None:
    registry = json.loads((PROJECT_ROOT / "output" / "figures" / "figure_registry.json").read_text(encoding="utf-8"))
    mermaid_count = sum(1 for figure in registry["figures"] if figure["kind"] == "mermaid")
    jsonl_declared_count = mermaid_count - 17
    docs = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            PROJECT_ROOT / "docs" / "output_inventory.md",
            PROJECT_ROOT / "docs" / "rendering_pipeline.md",
        ]
    )

    assert registry["figure_count"] == 173
    assert mermaid_count == 115
    assert f"{mermaid_count} Mermaid" in docs
    assert f"{jsonl_declared_count} JSONL-declared" in docs
    assert "114 Mermaid" not in docs
    assert "97 JSONL-declared" not in docs


def test_docs_headings_are_informative_outside_code_fences() -> None:
    banned = {
        "see also",
        "source rules",
        "required evidence",
        "build command",
        "workflow",
        "gates",
        "contract",
        "verification",
        "layout",
        "resolution",
        "tokens",
        "figures",
        "citations",
        "cross-references",
        "safety boundary",
        "support rows",
        "registry objects",
        "retained records",
        "allowed contexts",
        "safe substitutes",
        "executive verdict",
    }
    failures: list[str] = []
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    for path in sorted((PROJECT_ROOT / "docs").glob("*.md")):
        in_fence = False
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = heading_re.match(line)
            if match and match.group(2).strip().lower() in banned:
                failures.append(f"{path.relative_to(PROJECT_ROOT)}:{line_number}: {line}")

    assert failures == []
