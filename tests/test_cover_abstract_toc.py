"""Reader-facing cover, abstract, and TOC contracts."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image
import yaml

from manuscript_quality.inventory_helpers import manuscript_dir
from manuscript_manifest._heading_titles import chapter_landmark_titles

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text))


def test_cover_art_is_generated_non_numbered_and_configured(built_output: Path) -> None:
    cover = built_output / "figures" / "cover" / "ageint-cover-synthesis.png"
    metadata_path = cover.with_suffix(".json")
    config_path = manuscript_dir(built_output) / "config.yaml"
    registry_path = built_output / "figures" / "figure_registry.json"

    assert cover.is_file()
    assert metadata_path.is_file()
    with Image.open(cover) as image:
        width, height = image.size
        image.verify()
    assert width >= 1800
    assert height >= 1800
    assert max(width / height, height / width) <= 1.15

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["kind"] == "cover_art"
    assert metadata["non_numbered"] is True
    assert "placeholder" not in json.dumps(metadata).lower()
    assert metadata["output_path"] == "output/figures/cover/ageint-cover-synthesis.png"

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    assert config["book"]["cover"]["image"] == "../figures/cover/ageint-cover-synthesis.png"
    assert config["book"]["title"] == config["paper"]["title"]
    assert config["book"]["subtitle"] == config["paper"]["subtitle"]

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry_payload = json.dumps(registry)
    assert "output/figures/cover/ageint-cover-synthesis.png" not in registry_payload
    assert "fig:ageint-cover-synthesis" not in registry_payload


def test_abstract_is_single_substantial_plaintext_section(built_output: Path) -> None:
    abstract = (manuscript_dir(built_output) / "abstract.md").read_text(encoding="utf-8")

    assert "\n## Graphical Abstract" not in abstract
    assert "graphical abstract" not in abstract.lower()
    assert "{{VISUAL_SYNTHESIS}}" not in abstract
    assert "This front-matter section" not in abstract
    assert "Artifact path: `abstract.md`" not in abstract
    assert "Course path:" not in abstract
    assert "![" not in abstract
    assert not re.search(r"^##\s+", abstract, flags=re.MULTILINE)

    body = abstract.split("# Abstract {#sec:abstract}", 1)[1]
    assert 1_000 <= _word_count(body) <= 1_800
    for phrase in (
        "Synthetic Analytic Tradecraft",
        "source keys",
        "negative controls",
        "refresh triggers",
        "human review",
        "rollback",
        "evidence packet",
    ):
        assert phrase in body


def test_orientation_order_prioritizes_reader_navigation(built_output: Path) -> None:
    orientation_files = [
        path.name
        for path in sorted((manuscript_dir(built_output) / "orientation").glob("*.md"))
    ]

    assert orientation_files[:5] == [
        "00-how-to-use-this-atlas-sec-how-to-use-this-atlas.md",
        "01-synthetic-analytic-tradecraft-thesis-sec-synthetic-analytic-tradecraft-thesis.md",
        "02-reader-paths-sec-reader-paths.md",
        "03-curriculum-map-sec-curriculum-map.md",
        "04-runtime-inventory-sec-runtime-inventory.md",
    ]


def test_repeated_generated_heading_names_are_reader_specific(built_output: Path) -> None:
    text = "\n\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(manuscript_dir(built_output).rglob("*.md"))
        if path.name not in {"README.md", "AGENTS.md", "preamble.md"}
    )
    retired_headings = (
        "## Module architecture",
        "## Evidence and source canon",
        "## Research-backed synthesis",
        "## Agentic translation boundary",
        "## Review checklist",
        "## Cross-links",
    )
    for heading in retired_headings:
        assert not re.search(rf"^{re.escape(heading)}$", text, flags=re.MULTILINE)

    for heading in (
        "Module architecture and transfer contract",
        "Evidence canon and source spine",
        "Source-backed analytic synthesis",
        "Agentic translation: assist, approve, block",
        "Reviewer challenge checklist",
        "Learning-path cross-links",
    ):
        assert not re.search(rf"^## {re.escape(heading)}$", text, flags=re.MULTILINE)
        assert re.search(rf"^### {re.escape(heading)}$", text, flags=re.MULTILINE)

    chapter = (
        manuscript_dir(built_output)
        / "parts"
        / "ageint-agentic-intelligence"
        / "foundations-of-ageint"
        / "00-overview.md"
    ).read_text(encoding="utf-8")
    title = "Foundations of AGEINT"
    for landmark in chapter_landmark_titles(title).values():
        assert f"## {landmark}" in text
    assert "## Foundations of AGEINT orientation: reader task, learning outcomes, and core vocabulary" in chapter


def test_appendix_toc_headings_are_appendix_specific(built_output: Path) -> None:
    text = "\n\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((manuscript_dir(built_output) / "appendices").rglob("*.md"))
    )
    for bare_heading in (
        "Purpose",
        "Allowed inputs",
        "Excluded actions",
        "Expected artifacts",
        "Safe artifact schema",
        "Input/output contract",
        "Failure cases",
        "Rubric scoring bands",
        "Validation rubric",
    ):
        assert not re.search(rf"^## {re.escape(bare_heading)}$", text, flags=re.MULTILINE)

    assert re.search(
        r"^## .+ operating purpose$",
        text,
        flags=re.MULTILINE,
    )
    assert re.search(
        r"^## .+ failure cases and required responses$",
        text,
        flags=re.MULTILINE,
    )
