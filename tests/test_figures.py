"""Tests for AGEINT figure generation and registry integrity."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from PIL import Image

from figures import _02_part as figure_rendering
from curriculum import load_curriculum
from figures import (
    FigureKind,
    FigureSpec,
    build_figure_specs,
    figure_markdown,
    figures_for_section,
    load_figure_registry,
    render_figures,
)
from manuscript_manifest import build_manuscript_manifest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def _assert_mermaid_png_is_diagram(path: Path) -> None:
    """Text-plate fallbacks are smaller than rendered Mermaid diagrams."""
    assert path.stat().st_size >= 30_000, path
    with Image.open(path) as image:
        width, height = image.size
        image.verify()
    assert width > 0 and height > 0
    assert max(width / height, height / width) <= 1.1


def _assert_instructional_caption_and_alt_text(caption: str, alt_text: str) -> None:
    assert caption.strip()
    assert alt_text.strip()
    assert not caption.startswith("Generated "), caption
    assert not alt_text.startswith("Generated "), alt_text


def test_figure_specs_cover_all_asset_classes_with_unique_registry_fields() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    specs = build_figure_specs(curriculum, manifest)

    kinds = {spec.kind for spec in specs}
    assert kinds == {
        FigureKind.MERMAID,
        FigureKind.PYTHON,
        FigureKind.HISTORICAL,
        FigureKind.AI_GENERATED,
    }
    assert sum(spec.kind == FigureKind.MERMAID for spec in specs) == curriculum.stats["parts"] + 1
    assert sum(spec.kind == FigureKind.PYTHON for spec in specs) == 33
    assert sum(spec.kind == FigureKind.HISTORICAL for spec in specs) >= 4
    assert sum(spec.kind == FigureKind.AI_GENERATED for spec in specs) >= 3

    labels = [spec.label for spec in specs]
    paths = [spec.output_path for spec in specs]
    section_paths = {section.relative_path for section in manifest.sections}
    assert len(labels) == len(set(labels))
    assert {
        "fig:ageint-source-verification-flow",
        "fig:ageint-claim-ledger-flow",
        "fig:ageint-ai-compliance-map",
        "fig:ageint-agent-evaluation-loop",
        "fig:ageint-cross-border-data-flow",
        "fig:ageint-capstone-workflow",
        "fig:ageint-safe-substitution-matrix",
        "fig:ageint-instructor-assessment-lifecycle",
        "fig:ageint-accessibility-workflow",
        "fig:ageint-hria-dpia-map",
        "fig:ageint-procurement-oversight-loop",
        "fig:ageint-agent-incident-lifecycle",
        "fig:ageint-bounded-autonomy-recoverability",
        "fig:ageint-public-ai-register-lifecycle",
        "fig:ageint-ai-incident-reporting-loop",
        "fig:ageint-ot-definitive-architecture-record",
        "fig:ageint-data-lineage-registry",
        "fig:ageint-assessment-integrity-matrix",
        "fig:ageint-adversarial-assurance-cycle",
        "fig:ageint-model-dataset-card",
        "fig:ageint-transparency-notice-flow",
        "fig:ageint-records-retention-audit",
        "fig:ageint-release-change-control",
        "fig:ageint-risk-exception-memo",
        "fig:ageint-learner-support-plan",
        "fig:ageint-instructor-question-bank",
        "fig:ageint-remediation-backlog",
    } <= set(labels)
    assert len(paths) == len(set(paths))
    for spec in specs:
        assert spec.label.startswith("fig:")
        assert spec.output_path.startswith("output/figures/")
        _assert_instructional_caption_and_alt_text(spec.caption, spec.alt_text)
        assert spec.source_section in section_paths
        assert spec.section_label.startswith("sec:")
        assert spec.provenance


def test_render_figures_writes_registry_assets_and_mermaid_sources() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(PROJECT_ROOT, curriculum, manifest)
    registry = load_figure_registry(registry_path)

    assert registry_path == PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    assert registry["project"] == "AGEINT"
    assert registry["figure_count"] == len(registry["figures"])
    assert registry["figure_count"] >= curriculum.stats["parts"] + 41

    for entry in registry["figures"]:
        asset = PROJECT_ROOT / entry["output_path"]
        assert asset.is_file(), entry
        assert asset.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), entry["output_path"]
        _assert_instructional_caption_and_alt_text(entry["caption"], entry["alt_text"])
        assert len(entry["sha256"]) == 64
        if entry["kind"] == FigureKind.MERMAID.value:
            mermaid_source = PROJECT_ROOT / entry["source_artifact_path"]
            assert mermaid_source.is_file()
            assert mermaid_source.suffix == ".mmd"
            assert mermaid_source.with_suffix(".png").is_file()


def test_rendered_figure_assets_are_readable_and_square_normalized() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(PROJECT_ROOT, curriculum, manifest)
    registry = load_figure_registry(registry_path)

    for entry in registry["figures"]:
        asset = PROJECT_ROOT / entry["output_path"]
        with Image.open(asset) as image:
            width, height = image.size
            image.verify()
        assert width > 0 and height > 0, entry["output_path"]
        assert max(width / height, height / width) <= 1.1, entry["output_path"]


def test_corrupt_renderer_output_falls_back_to_valid_placeholder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def write_corrupt_png(root: Path, spec: FigureSpec, output: Path) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"\x89PNG\r\n\x1a\n\0\0\0\0")

    monkeypatch.setattr(figure_rendering, "_render_ai_concept_figure", write_corrupt_png)
    spec = FigureSpec(
        label="fig:test-corrupt-output",
        title="Corrupt renderer output",
        caption="A corrupt renderer output is replaced with a readable placeholder.",
        alt_text="Fallback plate for a corrupt renderer output.",
        kind=FigureKind.AI_GENERATED,
        output_path="output/figures/ai/corrupt-output.png",
        source_section="orientation.md",
        section_label="sec:curriculum_orientation",
        provenance={"prompt": "synthetic test fixture"},
    )

    figure_rendering._render_figure_asset(tmp_path, load_curriculum(DATA), spec, allow_placeholder_figures=True)
    asset = tmp_path / spec.output_path

    with Image.open(asset) as image:
        assert image.size == (1400, 1400)
        image.verify()


def test_historical_and_ai_figures_carry_local_provenance() -> None:
    registry_path = PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    if not registry_path.is_file():
        curriculum = load_curriculum(DATA)
        manifest = build_manuscript_manifest(curriculum)
        render_figures(PROJECT_ROOT, curriculum, manifest)
    registry = load_figure_registry(registry_path)

    historical = [entry for entry in registry["figures"] if entry["kind"] == FigureKind.HISTORICAL.value]
    ai_generated = [entry for entry in registry["figures"] if entry["kind"] == FigureKind.AI_GENERATED.value]
    assert historical
    assert ai_generated
    for entry in historical:
        assert entry["provenance"]["usage"] == "Public Domain"
        assert entry["provenance"]["source_url"].startswith("https://www.usgs.gov/")
        assert (PROJECT_ROOT / entry["output_path"]).is_file()
    for entry in ai_generated:
        assert entry["provenance"]["prompt"]
        assert "no real target" in entry["provenance"]["prompt"].lower()
        assert entry["provenance"]["model"] == "local deterministic conceptual renderer"


def test_figures_for_section_filters_by_source_section() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(PROJECT_ROOT, curriculum, manifest)
    registry = load_figure_registry(registry_path)
    figures = registry["figures"]
    orientation = figures_for_section(figures, "orientation.md")
    assert orientation
    assert all(entry["source_section"] == "orientation.md" for entry in orientation)
    assert figures_for_section(figures, "nonexistent/section.md") == []


@pytest.mark.requires_mermaid
def test_render_figures_strict_mode_produces_real_mermaid_diagrams() -> None:
    if shutil.which("mmdc") is None:
        pytest.skip("mmdc not on PATH")

    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(
        PROJECT_ROOT,
        curriculum,
        manifest,
        allow_placeholder_figures=False,
    )
    registry = load_figure_registry(registry_path)
    mermaid_entries = [entry for entry in registry["figures"] if entry["kind"] == FigureKind.MERMAID.value]
    assert len(mermaid_entries) == curriculum.stats["parts"] + 1
    for entry in mermaid_entries:
        asset = PROJECT_ROOT / entry["output_path"]
        assert asset.is_file(), entry["label"]
        assert entry["provenance"].get("renderer") == "mmdc", entry["label"]
        _assert_mermaid_png_is_diagram(asset)


def test_built_mermaid_figures_are_not_placeholder_plates(built_output: Path) -> None:
    registry_path = built_output / "figures" / "figure_registry.json"
    registry = load_figure_registry(registry_path)
    for entry in registry["figures"]:
        if entry["kind"] != FigureKind.MERMAID.value:
            continue
        asset = PROJECT_ROOT / entry["output_path"]
        assert asset.is_file(), entry["label"]
        _assert_mermaid_png_is_diagram(asset)


def test_figure_markdown_renders_label_path_and_escaped_caption() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(PROJECT_ROOT, curriculum, manifest)
    registry = load_figure_registry(registry_path)
    entry = next(item for item in registry["figures"] if item["label"] == "fig:ageint-curriculum-map")
    output_manuscript = PROJECT_ROOT / "output" / "manuscript"
    markdown = figure_markdown(
        entry,
        project_root=PROJECT_ROOT,
        manuscript_output_dir=output_manuscript,
        section_relative_path="orientation.md",
    )
    assert "{#fig:ageint-curriculum-map}" in markdown
    assert "output/figures/" in markdown or "../figures/" in markdown
    assert "[" in markdown and "](" in markdown
    assert "Generated " not in markdown
