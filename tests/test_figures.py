"""Tests for AGEINT figure generation and registry integrity."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from PIL import Image

from figures import _02_part as figure_rendering
from figures import _02b_mermaid as mermaid_rendering
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
from figures.mermaid_contracts import mermaid_type_contracts
from manuscript_manifest import build_manuscript_manifest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"
MIN_READER_CAPTION_WORDS = 40
MIN_ALT_TEXT_WORDS = 24
MIN_LONG_DESCRIPTION_WORDS = 70


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


def _word_count(text: str) -> int:
    return len([word for word in text.replace("/", " ").split() if word.strip()])


def _assert_informative_reader_text(spec: FigureSpec | dict[str, object]) -> None:
    caption = str(spec["caption"] if isinstance(spec, dict) else spec.caption)
    alt_text = str(spec["alt_text"] if isinstance(spec, dict) else spec.alt_text)
    long_description = str(spec["long_description"] if isinstance(spec, dict) else spec.long_description)
    label = str(spec["label"] if isinstance(spec, dict) else spec.label)

    _assert_instructional_caption_and_alt_text(caption, alt_text)
    assert long_description.strip()
    assert _word_count(caption) >= MIN_READER_CAPTION_WORDS, f"{label}: {caption}"
    assert _word_count(alt_text) >= MIN_ALT_TEXT_WORDS, f"{label}: {alt_text}"
    assert _word_count(long_description) >= MIN_LONG_DESCRIPTION_WORDS, f"{label}: {long_description}"
    for phrase, text in (
        ("caption forthcoming", caption),
        ("alt text forthcoming", alt_text),
        ("description forthcoming", long_description),
    ):
        assert phrase not in text.lower()
    assert ".md" not in long_description.lower()
    assert ".markdown" not in long_description.lower()


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
    assert len(specs) == 173
    assert sum(spec.kind == FigureKind.MERMAID for spec in specs) == 115
    assert sum(spec.kind == FigureKind.PYTHON for spec in specs) == 48
    assert sum(spec.kind == FigureKind.HISTORICAL for spec in specs) == 4
    assert sum(spec.kind == FigureKind.AI_GENERATED for spec in specs) == 6
    assert sum(spec.kind == FigureKind.MERMAID for spec in specs) == curriculum.stats["parts"] + 1 + len(mermaid_rendering.SYNTHESIS_MERMAID)

    labels = [spec.label for spec in specs]
    paths = [spec.output_path for spec in specs]
    section_paths = {section.relative_path for section in manifest.sections}
    assert len(labels) == len(set(labels))
    required_labels = """
    fig:ageint-source-verification-flow fig:ageint-claim-ledger-flow fig:ageint-ai-compliance-map
    fig:ageint-agent-evaluation-loop fig:ageint-cross-border-data-flow fig:ageint-capstone-workflow
    fig:ageint-safe-substitution-matrix fig:ageint-instructor-assessment-lifecycle fig:ageint-accessibility-workflow
    fig:ageint-visual-accessibility-contract fig:ageint-visual-quality-audit-dashboard fig:ageint-artifact-evidence-control-loop
    fig:ageint-scholarship-triangulation-map fig:ageint-graphical-abstract fig:ageint-synthetic-tradecraft-method-contract
    fig:ageint-analysis-validation-matrix fig:ageint-analysis-validation-family-coverage fig:ageint-source-metadata-integrity
    fig:ageint-source-refresh-due-dashboard fig:ageint-agency-source-coverage
    fig:ageint-claim-calibration-and-visual-semantics
    fig:ageint-hria-dpia-map fig:ageint-procurement-oversight-loop fig:ageint-agent-incident-lifecycle
    fig:ageint-bounded-autonomy-recoverability fig:ageint-public-ai-register-lifecycle fig:ageint-ai-incident-reporting-loop
    fig:ageint-ot-definitive-architecture-record fig:ageint-data-lineage-registry fig:ageint-assessment-integrity-matrix
    fig:ageint-adversarial-assurance-cycle fig:ageint-model-dataset-card fig:ageint-agentic-intelligence-boundary
    fig:ageint-transparency-notice-flow fig:ageint-records-retention-audit fig:ageint-release-change-control
    fig:ageint-risk-exception-memo fig:ageint-learner-support-plan fig:ageint-instructor-question-bank
    fig:ageint-remediation-backlog fig:ageint-cdr-degradation-cascade fig:ageint-maestro-seven-layer
    fig:ageint-sre-circuit-breaker fig:ageint-cognitive-decoherence-cdr-isomorphism fig:ageint-unified-epistemic-stack
    fig:ageint-cognitive-attack-layers fig:ageint-hro-governance-crosswalk fig:ageint-claim-evidence-fit-map
    fig:ageint-mcp-version-boundary fig:ageint-active-inference-boundary-stack fig:ageint-prebunking-evidence-boundary
    fig:ageint-agentic-standards-landscape fig:ageint-agent-evaluation-evidence-ladder
    fig:ageint-synthetic-content-provenance-boundary fig:ageint-analytic-tradecraft-evidence-ladder
    fig:ageint-analytic-source-quality-boundary fig:ageint-first-principles-tradecraft-decomposition
    fig:ageint-redteam-tradecraft-negative-control-loop fig:ageint-icd203-probability-confidence-boundary
    fig:ageint-sat-evidence-boundary fig:ageint-warning-failure-feedback-loop fig:ageint-source-freshness-coverage
    fig:ageint-source-refresh-due-dashboard
    fig:ageint-memory-governance-plate fig:ageint-visual-provenance-plate
    fig:ageint-ai-data-security-lifecycle-plate fig:ageint-web-source-refresh-plate
    """.split()
    assert set(required_labels) <= set(labels)
    assert len(paths) == len(set(paths))
    for spec in specs:
        assert spec.label.startswith("fig:")
        assert spec.output_path.startswith("output/figures/")
        _assert_informative_reader_text(spec)
        assert spec.source_section in section_paths
        assert spec.section_label.startswith("sec:")
        assert spec.provenance
    model_card = next(spec for spec in specs if spec.label == "fig:ageint-model-dataset-card")
    assert model_card.kind == FigureKind.PYTHON
    assert "provenance" in model_card.caption
    assert "evaluation caveats" in model_card.caption
    boundary = next(spec for spec in specs if spec.label == "fig:ageint-agentic-intelligence-boundary")
    assert boundary.kind == FigureKind.PYTHON
    assert boundary.output_path == "output/figures/python/ageint-agentic-intelligence-boundary.png"
    assert "tool permissions" in boundary.caption
    assert "external action" in boundary.caption
    accessibility = next(spec for spec in specs if spec.label == "fig:ageint-visual-accessibility-contract")
    assert accessibility.kind == FigureKind.PYTHON
    assert accessibility.provenance["renderer_id"] == "visual_accessibility_contract"
    assert "long description" in accessibility.caption
    assert "rendered-artifact validation" in accessibility.caption
    quality = next(spec for spec in specs if spec.label == "fig:ageint-visual-quality-audit-dashboard")
    assert quality.kind == FigureKind.PYTHON
    assert quality.provenance["renderer_id"] == "visual_quality_audit_dashboard"
    evidence = next(spec for spec in specs if spec.label == "fig:ageint-artifact-evidence-control-loop")
    assert evidence.kind == FigureKind.PYTHON
    assert evidence.provenance["renderer_id"] == "artifact_evidence_control_loop"
    assert "PDF annotation audits" in evidence.caption
    metadata = next(spec for spec in specs if spec.label == "fig:ageint-source-metadata-integrity")
    assert metadata.kind == FigureKind.PYTHON
    assert metadata.provenance["renderer_id"] == "source_metadata_integrity"
    assert "source rows cannot silently fall back" in metadata.caption
    assert "denominator context" in metadata.caption
    assert "not a quality score" in metadata.caption
    refresh_due = next(spec for spec in specs if spec.label == "fig:ageint-source-refresh-due-dashboard")
    assert refresh_due.kind == FigureKind.PYTHON
    assert refresh_due.provenance["renderer_id"] == "source_refresh_due_dashboard"
    assert "source refresh due-date dashboard" in refresh_due.caption
    assert "472-row local source denominator" in refresh_due.caption
    assert "not a score or empirical performance claim" in refresh_due.caption
    agency_coverage = next(spec for spec in specs if spec.label == "fig:ageint-agency-source-coverage")
    assert agency_coverage.kind == FigureKind.PYTHON
    assert agency_coverage.provenance["renderer_id"] == "agency_source_coverage_dashboard"
    assert "agency-source coverage" in agency_coverage.caption
    assert "56-anchor denominator" in agency_coverage.caption
    assert "artifact-evidence failure path" in agency_coverage.caption
    calibration = next(
        spec for spec in specs if spec.label == "fig:ageint-claim-calibration-and-visual-semantics"
    )
    assert calibration.kind == FigureKind.PYTHON
    assert calibration.provenance["renderer_id"] == "claim_calibration_and_visual_semantics"
    assert calibration.semantic_role == "verifier_control_map"
    assert "claim-calibration verifier" in calibration.caption
    assert "reviewer inputs" in calibration.caption
    assert "not read the visual as a score" in calibration.caption
    atlas = next(spec for spec in specs if spec.label == "fig:ageint-graphical-abstract")
    assert atlas.kind == FigureKind.PYTHON
    assert atlas.output_path == "output/figures/python/ageint-graphical-abstract.png"
    assert atlas.provenance["renderer_id"] == "graphical_abstract_atlas"
    assert atlas.provenance["canvas_size"] == "2400"
    assert "not a claim that AGEINT has measured operational performance" in atlas.caption


def test_maestro_mermaid_source_uses_top_to_bottom_layout() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    spec = next(
        figure
        for figure in build_figure_specs(curriculum, manifest)
        if figure.label == "fig:ageint-maestro-seven-layer"
    )
    source = mermaid_rendering.mermaid_source(curriculum, spec)

    assert "\nflowchart TB\n" in source
    assert "\nflowchart LR\n" not in source
    assert 'subgraph STACK["MAESTRO lifecycle stack"]' in source
    assert "direction TB" in source


def test_mermaid_sources_use_reader_task_specific_chart_types() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    specs = build_figure_specs(curriculum, manifest)
    mermaid_specs = [spec for spec in specs if spec.kind == FigureKind.MERMAID]
    types = {str(spec.provenance["diagram_type"]) for spec in mermaid_specs}
    converted = {
        "fig:ageint-sre-circuit-breaker": "stateDiagram-v2",
        "fig:ageint-agent-evaluation-evidence-ladder": "sequenceDiagram",
        "fig:osint-collection-to-verification-pipeline": "sequenceDiagram",
        "fig:osint-provenance-verification-workflow": "sequenceDiagram",
        "fig:appendix-capstone-redteam-review": "journey",
        "fig:ageint-cdr-degradation-cascade": "timeline",
        "fig:ageint-claim-evidence-fit-map": "quadrantChart",
    }

    assert {
        "flowchart",
        "stateDiagram-v2",
        "sequenceDiagram",
        "journey",
        "timeline",
        "quadrantChart",
    } <= types
    assert {contract.diagram_type for contract in mermaid_type_contracts()} <= types
    by_label = {spec.label: spec for spec in mermaid_specs}
    for label, diagram_type in converted.items():
        spec = by_label[label]
        source = mermaid_rendering.mermaid_source(curriculum, spec)
        assert spec.provenance["diagram_type"] == diagram_type
        assert spec.provenance["reader_detail"]
        assert f"\n{diagram_type}\n" in source
        assert _word_count(spec.long_description) >= MIN_LONG_DESCRIPTION_WORDS
        assert "The full visual conveys" in spec.long_description


def test_render_figures_writes_registry_assets_and_mermaid_sources() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(
        PROJECT_ROOT,
        curriculum,
        manifest,
        allow_placeholder_figures=True,
    )
    registry = load_figure_registry(registry_path)

    assert registry_path == PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    assert registry["project"] == "AGEINT"
    assert registry["schema_version"] == "1.5"
    assert registry["figure_count"] == len(registry["figures"])
    assert registry["figure_count"] == 173
    guidance_urls = {row["url"] for row in registry["accessibility_guidance"]}
    assert {
        "https://www.w3.org/WAI/tutorials/images/complex/",
        "https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html",
        "https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html",
        "https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html",
        "https://www.section508.gov/create/alternative-text/",
        "https://www.section508.gov/create/making-color-usage-accessible/",
        "https://designsystem.digital.gov/components/data-visualizations/",
        "https://www.section508.gov/training/pdfs/aed-cop-pdf02/",
    } <= guidance_urls

    for entry in registry["figures"]:
        asset = PROJECT_ROOT / entry["output_path"]
        assert asset.is_file(), entry
        assert asset.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), entry["output_path"]
        _assert_informative_reader_text(entry)
        assert len(entry["sha256"]) == 64
        with Image.open(asset) as image:
            info = image.info
            for png_key, registry_key in (
                ("AGEINT.Label", "label"),
                ("AGEINT.Title", "title"),
                ("AGEINT.Caption", "caption"),
                ("AGEINT.AltText", "alt_text"),
                ("AGEINT.LongDescription", "long_description"),
                ("AGEINT.SourceSection", "source_section"),
                ("AGEINT.SectionLabel", "section_label"),
                ("AGEINT.SemanticRole", "semantic_role"),
                ("AGEINT.EvidenceRole", "evidence_role"),
                ("AGEINT.Unit", "unit"),
                ("AGEINT.Denominator", "denominator"),
                ("AGEINT.CountingRule", "counting_rule"),
                ("AGEINT.InterpretationLimit", "interpretation_limit"),
            ):
                assert info[png_key] == entry[registry_key]
            assert info["AGEINT.Quantitative"] == str(entry["quantitative"]).lower()
        if entry["kind"] == FigureKind.MERMAID.value:
            assert entry["provenance"]["diagram_type"]
            mermaid_source = PROJECT_ROOT / entry["source_artifact_path"]
            assert mermaid_source.is_file()
            assert mermaid_source.suffix == ".mmd"
            assert mermaid_source.with_suffix(".png").is_file()
    atlas = next(entry for entry in registry["figures"] if entry["label"] == "fig:ageint-graphical-abstract")
    with Image.open(PROJECT_ROOT / atlas["output_path"]) as image:
        assert image.size == (2400, 2400)
    assert atlas["kind"] == FigureKind.PYTHON.value


def test_rendered_figure_assets_are_readable_and_square_normalized() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(
        PROJECT_ROOT,
        curriculum,
        manifest,
        allow_placeholder_figures=True,
    )
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
        render_figures(PROJECT_ROOT, curriculum, manifest, allow_placeholder_figures=True)
    registry = load_figure_registry(registry_path)

    historical = [entry for entry in registry["figures"] if entry["kind"] == FigureKind.HISTORICAL.value]
    ai_generated = [entry for entry in registry["figures"] if entry["kind"] == FigureKind.AI_GENERATED.value]
    assert len(historical) == 4
    assert len(ai_generated) == 6
    for entry in historical:
        assert entry["provenance"]["usage"] == "Public Domain"
        assert entry["provenance"]["source_url"].startswith("https://www.usgs.gov/")
        assert (PROJECT_ROOT / entry["output_path"]).is_file()
    for entry in ai_generated:
        assert entry["provenance"]["prompt"]
        assert "no real target" in entry["provenance"]["prompt"].lower()
        visual_text = entry["provenance"].get("visual_text", "")
        assert visual_text
        assert "create a" not in visual_text.lower()
        assert "no real" not in visual_text.lower()
        assert "official logos" not in visual_text.lower()
        assert entry["provenance"]["model"] == "local deterministic conceptual renderer"


def test_figures_for_section_filters_by_source_section() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(
        PROJECT_ROOT,
        curriculum,
        manifest,
        allow_placeholder_figures=True,
    )
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
    if mermaid_rendering._discover_chrome_executable() is None:
        pytest.skip("chrome-headless-shell not available for mmdc")

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
    assert len(mermaid_entries) == 115
    assert len(mermaid_entries) == curriculum.stats["parts"] + 1 + len(mermaid_rendering.SYNTHESIS_MERMAID)
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
    registry_path = render_figures(
        PROJECT_ROOT,
        curriculum,
        manifest,
        allow_placeholder_figures=True,
    )
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
