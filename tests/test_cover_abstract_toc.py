"""Reader-facing cover, abstract, and TOC contracts."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image
import yaml

from figures._03l_cover_art import COVER_BOUNDARY_TERMS, COVER_DOMAIN_LABELS, COVER_FOREGROUND_REGIONS
from manuscript_quality.inventory_helpers import manuscript_dir

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _boxes_overlap(first: tuple[int, int, int, int], second: tuple[int, int, int, int]) -> bool:
    return not (first[2] <= second[0] or second[2] <= first[0] or first[3] <= second[1] or second[3] <= first[1])


def test_cover_foreground_regions_stay_within_canvas_without_overlap() -> None:
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
    assert metadata["output_path"] == "output/figures/cover/ageint-cover-synthesis.png"
    assert metadata["domain_labels"] == list(COVER_DOMAIN_LABELS)
    assert metadata["boundary_terms"] == list(COVER_BOUNDARY_TERMS)
    assert png_text["AGEINT.DomainLabels"] == "|".join(COVER_DOMAIN_LABELS)
    assert png_text["AGEINT.BoundaryTerms"] == "|".join(COVER_BOUNDARY_TERMS)

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

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry_payload = json.dumps(registry)
    assert "output/figures/frontmatter/ageint-evidence-transit-map.png" not in registry_payload
    assert "fig:ageint-evidence-transit-map" not in registry_payload


def test_abstract_is_single_plaintext_section(built_output: Path) -> None:
    abstract = (manuscript_dir(built_output) / "abstract.md").read_text(encoding="utf-8")
    assert "![" not in abstract
    assert not re.search(r"^##\s+", abstract, flags=re.MULTILINE)

    body = abstract.split("{#sec:abstract}", 1)[1]
    paragraphs = [block for block in re.split(r"\n\s*\n", body.strip()) if block.strip()]
    assert len(paragraphs) == 1


def test_early_orientation_creative_visuals_are_slotted_before_late_inventory(built_output: Path) -> None:
    orientation_dir = manuscript_dir(built_output) / "orientation"
    placements = {
        "00-how-to-use-this-atlas": "fig:ageint-reader-route-compass",
        "01-synthetic-analytic-tradecraft-thesis": "fig:ageint-synthetic-tradecraft-workbench",
        "04-runtime-inventory": "fig:ageint-source-constellation-map",
        "06-analysis-validation-protocol": "fig:ageint-assurance-cockpit",
    }
    orientation_files = sorted(orientation_dir.glob("*.md"))
    joined = "\n\n".join(path.read_text(encoding="utf-8") for path in orientation_files)
    late_inventory = next(orientation_dir.glob("*orientation-figures-and-course-links*.md"))
    late_text = late_inventory.read_text(encoding="utf-8")

    for prefix, label in placements.items():
        fragment = next(path for path in orientation_files if path.name.startswith(prefix))
        text = fragment.read_text(encoding="utf-8")
        figure_definition = f"{{#{label}}}"
        assert figure_definition in text
        assert figure_definition not in late_text
        assert joined.count(figure_definition) == 1
