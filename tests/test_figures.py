"""Tests for AGEINT figure generation and registry integrity."""

from __future__ import annotations

from datetime import date
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
from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
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
    assert len(specs) == 161
    assert sum(spec.kind == FigureKind.MERMAID for spec in specs) == 115
    assert sum(spec.kind == FigureKind.PYTHON for spec in specs) == 36
    assert sum(spec.kind == FigureKind.HISTORICAL for spec in specs) == 4
    assert sum(spec.kind == FigureKind.AI_GENERATED for spec in specs) == 6
    assert sum(spec.kind == FigureKind.MERMAID for spec in specs) == curriculum.stats["parts"] + 1 + len(mermaid_rendering.SYNTHESIS_MERMAID)

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
        "fig:ageint-agentic-intelligence-boundary",
        "fig:ageint-transparency-notice-flow",
        "fig:ageint-records-retention-audit",
        "fig:ageint-release-change-control",
        "fig:ageint-risk-exception-memo",
        "fig:ageint-learner-support-plan",
        "fig:ageint-instructor-question-bank",
        "fig:ageint-remediation-backlog",
        "fig:ageint-cdr-degradation-cascade",
        "fig:ageint-maestro-seven-layer",
        "fig:ageint-sre-circuit-breaker",
        "fig:ageint-cognitive-decoherence-cdr-isomorphism",
        "fig:ageint-unified-epistemic-stack",
        "fig:ageint-cognitive-attack-layers",
        "fig:ageint-hro-governance-crosswalk",
        "fig:ageint-claim-evidence-fit-map",
        "fig:ageint-mcp-version-boundary",
        "fig:ageint-active-inference-boundary-stack",
        "fig:ageint-prebunking-evidence-boundary",
        "fig:ageint-agentic-standards-landscape",
        "fig:ageint-agent-evaluation-evidence-ladder",
        "fig:ageint-synthetic-content-provenance-boundary",
        "fig:ageint-analytic-tradecraft-evidence-ladder",
        "fig:ageint-analytic-source-quality-boundary",
        "fig:ageint-first-principles-tradecraft-decomposition",
        "fig:ageint-redteam-tradecraft-negative-control-loop",
        "fig:ageint-icd203-probability-confidence-boundary",
        "fig:ageint-sat-evidence-boundary",
        "fig:ageint-warning-failure-feedback-loop",
        "fig:ageint-source-freshness-coverage",
        "fig:ageint-memory-governance-plate",
        "fig:ageint-visual-provenance-plate",
        "fig:ageint-ai-data-security-lifecycle-plate",
        "fig:ageint-web-source-refresh-plate",
    } <= set(labels)
    assert len(paths) == len(set(paths))
    for spec in specs:
        assert spec.label.startswith("fig:")
        assert spec.output_path.startswith("output/figures/")
        _assert_instructional_caption_and_alt_text(spec.caption, spec.alt_text)
        assert spec.source_section in section_paths
        assert spec.section_label.startswith("sec:")
        assert spec.provenance
    model_card = next(spec for spec in specs if spec.label == "fig:ageint-model-dataset-card")
    assert model_card.kind == FigureKind.PYTHON
    assert "provenance" in model_card.caption
    assert "evaluation caveats" in model_card.caption
    boundary = next(
        spec for spec in specs if spec.label == "fig:ageint-agentic-intelligence-boundary"
    )
    assert boundary.kind == FigureKind.PYTHON
    assert boundary.output_path == "output/figures/python/ageint-agentic-intelligence-boundary.png"
    assert "tool permissions" in boundary.caption
    assert "external action" in boundary.caption


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
    assert registry["figure_count"] == len(registry["figures"])
    assert registry["figure_count"] == 161

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


def test_internet_backed_visuals_have_current_source_anchor_contracts() -> None:
    anchors = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    required = {
        "official_nist_ai_800_2_automated_benchmark_evaluations",
        "official_oecd_agentic_ai_landscape",
        "official_nsa_mcp_security_design_considerations",
        "scholarly_roozenbeek_2022_psychological_inoculation",
    }
    assert required <= anchors.keys()
    for key in required:
        anchor = anchors[key]
        assert date.fromisoformat(anchor.checked_as_of) >= date(2026, 6, 11)
        assert anchor.source_lane
        assert anchor.source_tier
        assert anchor.assurance_use
        assert anchor.rights_dimension

    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    specs = build_figure_specs(curriculum, manifest)
    source_freshness = next(spec for spec in specs if spec.label == "fig:ageint-source-freshness-coverage")
    assert source_freshness.kind == FigureKind.PYTHON
    assert source_freshness.provenance["renderer_id"] == "source_freshness_coverage"
    analytic_boundary = next(
        spec for spec in specs if spec.label == "fig:ageint-analytic-source-quality-boundary"
    )
    assert analytic_boundary.kind == FigureKind.PYTHON
    assert analytic_boundary.provenance["renderer_id"] == "analytic_source_quality_boundary"


def test_analytic_tradecraft_source_refresh_has_boundary_contracts() -> None:
    anchors = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    required = {
        "official_cia_sherman_kent_profession",
        "official_cia_kent_analyst_policymaker_relations",
        "scholarly_wohlstetter_1962_pearl_harbor_warning_decision",
        "official_cia_grabo_warning_intelligence_handbook",
        "official_irtpa_2004_analytic_integrity",
        "official_911_commission_report",
        "official_robb_silberman_wmd_report",
        "official_nato_alternative_analysis_handbook",
        "scholarly_rand_2016_sat_evaluation",
        "scholarly_marcoci_2019_tradecraft_reliability",
        "scholarly_barnes_mandel_2014_forecast_accuracy",
        "scholarly_ard_2023_sat_pragmatic",
        "scholarly_stromer_galley_2020_flexible_sat",
        "scholarly_betts_1978_intelligence_failure",
        "scholarly_jervis_2022_postmortems_fail",
        "scholarly_wirtz_2023_intelligence_failures_inevitable",
    }
    assert len(INTELLIGENCE_RESEARCH_ANCHORS) == 248
    assert required <= anchors.keys()

    weak_hosts = ("wikipedia.org", "amazon.", "goodreads.", "scribd.", "blogspot.")
    for key in required:
        anchor = anchors[key]
        assert date.fromisoformat(anchor.checked_as_of) >= date(2026, 6, 11)
        assert anchor.url.startswith("https://")
        assert not any(host in anchor.url for host in weak_hosts), anchor.url
        assert anchor.source_lane in {
            "analytic_tradecraft_evidence",
            "warning_intelligence",
            "intelligence_failure_postmortem",
            "sat_evaluation_evidence",
            "forecasting_calibration_evidence",
        }
        assert anchor.source_tier
        assert anchor.verification_method
        assert anchor.claim_scope
        assert anchor.assurance_use
        assert anchor.rights_dimension

    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    specs = build_figure_specs(curriculum, manifest)
    tradecraft_labels = {
        "fig:ageint-analytic-tradecraft-evidence-ladder",
        "fig:ageint-analytic-source-quality-boundary",
        "fig:ageint-first-principles-tradecraft-decomposition",
        "fig:ageint-redteam-tradecraft-negative-control-loop",
        "fig:ageint-icd203-probability-confidence-boundary",
        "fig:ageint-sat-evidence-boundary",
        "fig:ageint-warning-failure-feedback-loop",
    }
    tradecraft_specs = {spec.label: spec for spec in specs if spec.label in tradecraft_labels}
    assert tradecraft_labels <= tradecraft_specs.keys()
    for spec in tradecraft_specs.values():
        assert spec.kind in {FigureKind.MERMAID, FigureKind.PYTHON}
        assert "Source-backed" in spec.caption
        caption = spec.caption.lower()
        assert any(
            token in caption
            for token in (
                "overclaim",
                "separat",
                "single technique",
                "universal debiasing",
                "evidence lane",
                "false-certification",
            )
        )


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


def test_pdf_preamble_uses_compact_pdf_typography() -> None:
    preamble = (PROJECT_ROOT / "manuscript" / "preamble.md").read_text(encoding="utf-8")
    assert r"\changefontsizes[9.2pt]{8pt}" in preamble
    assert r"\setlength{\parskip}{0.15em}" in preamble
    assert r"\renewcommand{\arraystretch}{0.88}" in preamble
    assert r"\setlength{\LTpre}{2pt}" in preamble
    assert r"\setlength{\LTpost}{2pt}" in preamble
