"""Reader-facing cover, abstract, and TOC contracts."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image
import yaml

from figures._03l_cover_art import (
    COVER_DOMAIN_LABELS,
    COVER_FOREGROUND_REGIONS,
    COVER_MIN_FONT_SIZE,
)
from manuscript_quality.inventory_helpers import manuscript_dir
from manuscript_manifest._heading_titles import chapter_detail_titles, chapter_scaffold_titles

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text))


def _boxes_overlap(
    first: tuple[int, int, int, int],
    second: tuple[int, int, int, int],
) -> bool:
    return not (
        first[2] <= second[0]
        or second[2] <= first[0]
        or first[3] <= second[1]
        or second[3] <= first[1]
    )


def test_cover_layout_contract_expands_int_domains_without_foreground_overlap() -> None:
    assert COVER_MIN_FONT_SIZE >= 24
    assert COVER_DOMAIN_LABELS == (
        "HUMINT",
        "SIGINT",
        "OSINT",
        "GEOINT/IMINT",
        "FININT",
        "CYBINT/CTI",
        "TECHINT/MASINT",
        "CI",
        "COGSEC",
        "ALL-SOURCE FUSION",
    )

    region_names = [name for name, _ in COVER_FOREGROUND_REGIONS]
    assert len(region_names) == len(set(region_names))
    for name, box in COVER_FOREGROUND_REGIONS:
        x0, y0, x1, y1 = box
        assert 80 <= x0 < x1 <= 2320, name
        assert 80 <= y0 < y1 <= 2320, name

    overlaps: list[str] = []
    for index, (first_name, first_box) in enumerate(COVER_FOREGROUND_REGIONS):
        for second_name, second_box in COVER_FOREGROUND_REGIONS[index + 1 :]:
            if _boxes_overlap(first_box, second_box):
                overlaps.append(f"{first_name} overlaps {second_name}")
    assert overlaps == []


def test_cover_art_is_generated_non_numbered_and_configured(built_output: Path) -> None:
    cover = built_output / "figures" / "cover" / "ageint-cover-synthesis.png"
    metadata_path = cover.with_suffix(".json")
    config_path = manuscript_dir(built_output) / "config.yaml"
    registry_path = built_output / "figures" / "figure_registry.json"

    assert cover.is_file()
    assert metadata_path.is_file()
    with Image.open(cover) as image:
        width, height = image.size
        png_text = dict(image.text)
    with Image.open(cover) as image:
        image.verify()
    assert width >= 1800
    assert height >= 1800
    assert max(width / height, height / width) <= 1.15

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["kind"] == "cover_art"
    assert metadata["non_numbered"] is True
    assert "placeholder" not in json.dumps(metadata).lower()
    assert metadata["output_path"] == "output/figures/cover/ageint-cover-synthesis.png"
    assert metadata["domain_labels"] == list(COVER_DOMAIN_LABELS)
    assert metadata["minimum_font_size"] == COVER_MIN_FONT_SIZE
    assert png_text["AGEINT.DomainLabels"] == "|".join(COVER_DOMAIN_LABELS)
    assert "conceptual domain map" in metadata["description"]
    assert "performance or completeness claim" in metadata["description"]

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    assert config["book"]["cover"]["image"] == "../figures/cover/ageint-cover-synthesis.png"
    assert config["book"]["title"] == config["paper"]["title"]
    assert config["book"]["subtitle"] == config["paper"]["subtitle"]

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry_payload = json.dumps(registry)
    assert "output/figures/cover/ageint-cover-synthesis.png" not in registry_payload
    assert "fig:ageint-cover-synthesis" not in registry_payload


def test_page_two_visual_is_generated_non_numbered_and_configured(built_output: Path) -> None:
    visual = built_output / "figures" / "frontmatter" / "ageint-evidence-transit-map.png"
    metadata_path = visual.with_suffix(".json")
    config_path = manuscript_dir(built_output) / "config.yaml"
    registry_path = built_output / "figures" / "figure_registry.json"

    assert visual.is_file()
    assert metadata_path.is_file()
    with Image.open(visual) as image:
        width, height = image.size
        png_text = dict(image.text)
    with Image.open(visual) as image:
        image.verify()
    assert width >= 1800
    assert height >= 1800
    assert max(width / height, height / width) <= 1.15
    assert png_text["AGEINT.Kind"] == "front_matter_visual"
    assert png_text["AGEINT.NonNumbered"] == "true"

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["kind"] == "front_matter_visual"
    assert metadata["non_numbered"] is True
    assert metadata["output_path"] == "output/figures/frontmatter/ageint-evidence-transit-map.png"
    assert metadata["provenance"]["telemetry"]["outputs"]["generated_markdown_files"] > 0
    assert metadata["provenance"]["telemetry"]["outputs"]["registered_figures"] > 0
    assert "page_count" not in json.dumps(metadata)
    assert "link_count" not in json.dumps(metadata)

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    visual_config = config["front_matter"]["page_two_visual"]
    assert visual_config["image"] == "../figures/frontmatter/ageint-evidence-transit-map.png"
    assert "artifact telemetry only" in visual_config["caption"]

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry_payload = json.dumps(registry)
    assert "output/figures/frontmatter/ageint-evidence-transit-map.png" not in registry_payload
    assert "fig:ageint-evidence-transit-map" not in registry_payload


def test_abstract_is_single_substantial_plaintext_section(built_output: Path) -> None:
    abstract = (manuscript_dir(built_output) / "abstract.md").read_text(encoding="utf-8")
    abstract_template = (PROJECT_ROOT / "manuscript" / "templates" / "abstract.md").read_text(
        encoding="utf-8"
    )

    assert "\n## Graphical Abstract" not in abstract
    assert "graphical abstract" not in abstract.lower()
    assert "{{VISUAL_SYNTHESIS}}" not in abstract
    assert "{{SOURCE_QUALITY_SPINE}}" not in abstract_template
    assert "{{INTELLIGENCE_RESEARCH_SPINE}}" not in abstract_template
    assert "This front-matter section" not in abstract
    assert "Artifact path: `abstract.md`" not in abstract
    assert "Course path:" not in abstract
    assert "![" not in abstract
    assert not re.search(r"^##\s+", abstract, flags=re.MULTILINE)

    body = abstract.split("{#sec:abstract}", 1)[1]
    paragraphs = [block for block in re.split(r"\n\s*\n", body.strip()) if block.strip()]
    assert len(paragraphs) == 1
    assert 1_200 <= _word_count(body) <= 1_600
    for phrase in (
        "Synthetic Analytic Tradecraft",
        "source keys",
        "claim calibration",
        "negative controls",
        "refresh triggers",
        "human review",
        "rollback",
        "evidence packet",
        "not a benchmark",
    ):
        assert phrase in body


def test_orientation_order_prioritizes_reader_navigation(built_output: Path) -> None:
    orientation_files = [
        path.name
        for path in sorted((manuscript_dir(built_output) / "orientation").glob("*.md"))
    ]

    assert orientation_files[:5] == [
        "00-how-to-use-this-atlas-navigation-path-evidence-checks-and-verifier-handoff-sec-how-to-use-this-atlas.md",
        "01-synthetic-analytic-tradecraft-thesis-synthetic-fixtures-source-discipline-and-reviewable-claims-sec-synthetic-analytic-tradecraft-thesis.md",
        "02-reader-paths-instructor-learner-reviewer-and-maintainer-handoffs-sec-reader-paths.md",
        "03-curriculum-map-parts-modules-and-source-backed-route-choices-sec-curriculum-map.md",
        "04-runtime-inventory-generated-counts-anchors-and-method-appendices-sec-runtime-inventory.md",
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
        "Governance, rights, and assurance",
        "Assessment artifacts and capstone pathway",
        "Refresh, safety, and source maps",
        "Reviewer challenge checklist",
        "Learning-path cross-links",
    ):
        assert not re.search(rf"^## {re.escape(heading)}$", text, flags=re.MULTILINE)
        assert not re.search(rf"^### {re.escape(heading)}$", text, flags=re.MULTILINE)

    chapter_path = (
        manuscript_dir(built_output)
        / "parts"
        / "ageint-agentic-intelligence"
        / "foundations-of-ageint"
        / "00-overview.md"
    )
    chapter = "\n\n".join(
        fragment.read_text(encoding="utf-8")
        for fragment in sorted(chapter_path.parent.glob("*.md"))
    )
    title = "Foundations of AGEINT"
    chapter_h2 = [
        line.removeprefix("## ").strip()
        for line in chapter.splitlines()
        if line.startswith("## ") and not line.startswith("### ")
    ]
    assert len(chapter_h2) == 3
    assert any(
        heading.endswith(f" frame for {title}: source context, topic focus, and reader task")
        for heading in chapter_h2
    )
    assert any(
        heading.endswith(f" path for {title}: lesson cluster, safe artifact, and review")
        for heading in chapter_h2
    )
    assert f"{title} assurance handoff: evidence, governance, refresh, and capstone" in chapter_h2
    for scaffold in chapter_scaffold_titles(title).values():
        assert f"### {scaffold}" in chapter
    for detail in chapter_detail_titles(title).values():
        assert f"### {detail}" in chapter


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
        r"^### .+ operating purpose$",
        text,
        flags=re.MULTILINE,
    )
    assert re.search(
        r"^### .+ failure cases and required responses$",
        text,
        flags=re.MULTILINE,
    )
    assert re.search(
        r"^## .+ workbook scope: purpose, safety envelope, and reuse decision$",
        text,
        flags=re.MULTILINE,
    )
