"""Regression tests for manuscript-review recommendation fixes."""

from __future__ import annotations

from pathlib import Path
import re

from manuscript_quality.inventory_helpers import manuscript_dir


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def test_related_work_protocol_and_memory_boundaries_render(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    orientation = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((output_manuscript / "orientation").glob("*.md"))
    )
    method_ref = (
        output_manuscript / "method-assurance-reference.md"
    ).read_text(encoding="utf-8")

    assert "Related work and contribution boundary" in orientation
    assert (
        "not a new agent architecture, cognitive theory, attack benchmark"
        in _normalized(orientation)
    )
    assert "MCP references use the 2025-06-18 specification" in _normalized(method_ref)
    assert (
        "external-memory governance, tool boundaries, logging, and retention"
        in _normalized(method_ref)
    )
    assert "not cognitive-taxonomy claims" in _normalized(method_ref)


def test_sre_circuit_breaker_is_author_defined_not_vendor_attributed(
    built_output: Path,
) -> None:
    output_manuscript = manuscript_dir(built_output)
    security_overview = (
        output_manuscript
        / "parts"
        / "ageint-agentic-intelligence"
        / "ageint-security-and-adversarial-considerations"
        / "00-overview.md"
    ).read_text(encoding="utf-8")
    assert "Microsoft's SRE-for-agents" not in security_overview
    assert "author-defined SRE circuit-breaker teaching pattern" in security_overview
