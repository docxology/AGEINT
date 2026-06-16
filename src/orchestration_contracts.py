"""Typed orchestration contracts for AGEINT build and reporting stages."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PipelineStageContract:
    """One source-owned AGEINT pipeline stage and its observable contract."""

    stage_id: str
    title: str
    purpose: str
    inputs: tuple[Path, ...]
    outputs: tuple[Path, ...]
    depends_on: tuple[str, ...] = ()
    strict_gate: str = ""
    failure_mode: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "title": self.title,
            "purpose": self.purpose,
            "inputs": [path.as_posix() for path in self.inputs],
            "outputs": [path.as_posix() for path in self.outputs],
            "depends_on": list(self.depends_on),
            "strict_gate": self.strict_gate,
            "failure_mode": self.failure_mode,
        }


PIPELINE_STAGE_CONTRACTS: tuple[PipelineStageContract, ...] = (
    PipelineStageContract(
        stage_id="source_validation",
        title="Source validation",
        purpose="Validate declarative curriculum, route, source, and template inputs before rendering.",
        inputs=(Path("data"), Path("manuscript/templates"), Path("src")),
        outputs=(Path("output/README.md"), Path("output/AGENTS.md")),
        strict_gate="validate_declarative_tables",
        failure_mode="A malformed route table or source surface reaches manuscript rendering.",
    ),
    PipelineStageContract(
        stage_id="curriculum_build",
        title="Curriculum build",
        purpose="Load the sharded curriculum spine and optional guide source into the runtime curriculum model.",
        inputs=(Path("data/curriculum"), Path("SIST-Guide-TOC-and-Bibliography-v2.md")),
        outputs=(Path("output/data/curriculum/metadata.json"), Path("output/data/curriculum_outline.json")),
        depends_on=("source_validation",),
        strict_gate="curriculum_stats_and_identity_tests",
        failure_mode="Generated paths, labels, or counts no longer match the source spine.",
    ),
    PipelineStageContract(
        stage_id="template_library",
        title="Neutral template library",
        purpose="Optionally regenerate neutral source templates without hard-coding generated chapter data.",
        inputs=(Path("src/manuscript_templates.py"),),
        outputs=(Path("manuscript/templates/chapter.md"),),
        depends_on=("source_validation",),
        strict_gate="explicit_regeneration_flag",
        failure_mode="Reusable templates drift into chapter-specific source text.",
    ),
    PipelineStageContract(
        stage_id="variables_and_bibliography",
        title="Variables and bibliography",
        purpose="Refresh manuscript variables plus source and output BibTeX files from current references.",
        inputs=(Path("data/research_anchors"), Path("data/curriculum/references"), Path("src/manuscript_variables")),
        outputs=(
            Path("output/data/manuscript_variables.json"),
            Path("manuscript/references-source-guide-001-050.bib"),
            Path("output/manuscript/references-source-guide-001-050.bib"),
        ),
        depends_on=("curriculum_build",),
        strict_gate="manuscript_variable_and_reference_tests",
        failure_mode="Counts, citation keys, or bibliography shards certify stale source metadata.",
    ),
    PipelineStageContract(
        stage_id="figures",
        title="Figure registry and assets",
        purpose="Render Mermaid, Python, historical, and synthetic figures with registry metadata.",
        inputs=(Path("data/figures"), Path("src/figures"), Path("data/curriculum")),
        outputs=(
            Path("output/figures/figure_registry.json"),
            Path("output/figures/visual_quality_audit.json"),
            Path("output/figures/cover/ageint-cover-synthesis.png"),
        ),
        depends_on=("curriculum_build",),
        strict_gate="figure_registry_and_quality_tests",
        failure_mode="A figure is decorative, inaccessible, stale, or rendered with unsupported chart semantics.",
    ),
    PipelineStageContract(
        stage_id="manuscript_render",
        title="Semantic manuscript render",
        purpose="Render source-owned manifest sections into generated Markdown under output/manuscript.",
        inputs=(Path("src/manuscript_manifest"), Path("manuscript/templates"), Path("output/figures/figure_registry.json")),
        outputs=(Path("output/manuscript/README.md"),),
        depends_on=("variables_and_bibliography", "figures"),
        strict_gate="manifest_inventory_reader_quality_tests",
        failure_mode="Generated prose, headings, citations, or cross-references drift from the manifest contract.",
    ),
    PipelineStageContract(
        stage_id="evidence_transit",
        title="Evidence transit map",
        purpose="Render the frontmatter evidence-transit figure from current curriculum and artifact counts.",
        inputs=(Path("output/figures/figure_registry.json"), Path("output/manuscript")),
        outputs=(Path("output/figures/frontmatter/ageint-evidence-transit-map.png"),),
        depends_on=("manuscript_render",),
        strict_gate="frontmatter_transit_figure_tests",
        failure_mode="Frontmatter evidence counts diverge from the generated manuscript and figure registry.",
    ),
    PipelineStageContract(
        stage_id="artifact_reports",
        title="Artifact and readiness reports",
        purpose="Bind current outputs to fail-closed audit, source, figure, PDF, and readiness evidence.",
        inputs=(Path("output/manuscript"), Path("output/figures"), Path("output/pdf"), Path("data/research_anchors")),
        outputs=(
            Path("output/reports/current_artifact_evidence.json"),
            Path("output/reports/source_metadata.json"),
            Path("output/reports/reference_quality.json"),
            Path("output/reports/claim_calibration.json"),
        ),
        depends_on=("manuscript_render", "evidence_transit"),
        strict_gate="artifact_evidence_and_publication_readiness_tests",
        failure_mode="A stale or partial artifact is certified as locally ready.",
    ),
)


def pipeline_stage_contracts() -> tuple[PipelineStageContract, ...]:
    """Return AGEINT pipeline stages in execution order."""
    return PIPELINE_STAGE_CONTRACTS


def pipeline_contract_by_id() -> dict[str, PipelineStageContract]:
    """Return pipeline stage contracts keyed by stage id."""
    return {stage.stage_id: stage for stage in PIPELINE_STAGE_CONTRACTS}


def source_freshness_roots() -> tuple[Path, ...]:
    """Return unique source paths that should make generated outputs stale."""
    paths: list[Path] = [
        Path("pyproject.toml"),
        Path("scripts/build_curriculum.py"),
        Path("scripts/generate_figures.py"),
        Path("scripts/z_generate_manuscript_variables.py"),
    ]
    for stage in PIPELINE_STAGE_CONTRACTS:
        for path in stage.inputs:
            if path.parts and path.parts[0] == "output":
                continue
            if path.name == "SIST-Guide-TOC-and-Bibliography-v2.md":
                continue
            paths.append(path)
    return tuple(_dedupe_paths(paths))


def output_build_sentinels() -> tuple[Path, ...]:
    """Return output-relative sentinels that prove the core build completed."""
    sentinels: list[Path] = []
    for stage in PIPELINE_STAGE_CONTRACTS:
        if stage.stage_id in {"source_validation", "artifact_reports"}:
            continue
        for path in stage.outputs:
            if path.parts and path.parts[0] == "output":
                sentinels.append(Path(*path.parts[1:]))
    required = [
        Path("data/curriculum_outline.json"),
        Path("data/manuscript_variables.json"),
        Path("figures/figure_registry.json"),
        Path("figures/frontmatter/ageint-evidence-transit-map.png"),
        Path("manuscript/README.md"),
    ]
    return tuple(_dedupe_paths([*sentinels, *required]))


def validate_pipeline_stage_contracts() -> None:
    """Fail if the registered stage graph is incomplete or cyclic."""
    by_id = pipeline_contract_by_id()
    if len(by_id) != len(PIPELINE_STAGE_CONTRACTS):
        raise ValueError("AGEINT pipeline stage ids must be unique")
    for stage in PIPELINE_STAGE_CONTRACTS:
        if not stage.inputs:
            raise ValueError(f"Pipeline stage {stage.stage_id} must declare inputs")
        if not stage.outputs:
            raise ValueError(f"Pipeline stage {stage.stage_id} must declare outputs")
        missing = [dependency for dependency in stage.depends_on if dependency not in by_id]
        if missing:
            raise ValueError(f"Pipeline stage {stage.stage_id} has unknown dependencies: {missing}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(stage_id: str) -> None:
        if stage_id in visited:
            return
        if stage_id in visiting:
            raise ValueError(f"Pipeline stage graph contains a cycle at {stage_id}")
        visiting.add(stage_id)
        for dependency in by_id[stage_id].depends_on:
            visit(dependency)
        visiting.remove(stage_id)
        visited.add(stage_id)

    for stage in PIPELINE_STAGE_CONTRACTS:
        visit(stage.stage_id)


def pipeline_contract_report(project_root: Path) -> dict[str, Any]:
    """Return a machine-readable AGEINT orchestration contract report."""
    validate_pipeline_stage_contracts()
    root = Path(project_root)
    output = root / "output"
    sentinels = output_build_sentinels()
    source_roots = source_freshness_roots()
    return {
        "project": "AGEINT",
        "schema_version": "1.0",
        "stage_count": len(PIPELINE_STAGE_CONTRACTS),
        "stages": [stage.as_dict() for stage in PIPELINE_STAGE_CONTRACTS],
        "source_freshness_roots": [path.as_posix() for path in source_roots],
        "output_build_sentinels": [path.as_posix() for path in sentinels],
        "missing_output_sentinels": [
            path.as_posix() for path in sentinels if not (output / path).exists()
        ],
    }


def render_pipeline_contract_markdown(payload: dict[str, Any]) -> str:
    """Render the orchestration contract report as reader-facing Markdown."""
    lines = [
        "# AGEINT Orchestration Contract",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| Registered stages | {payload['stage_count']} |",
        f"| Source freshness roots | {len(payload['source_freshness_roots'])} |",
        f"| Output sentinels | {len(payload['output_build_sentinels'])} |",
        f"| Missing output sentinels | {len(payload['missing_output_sentinels'])} |",
        "",
        "## Pipeline Stages",
        "",
        "| Stage | Purpose | Gate | Failure mode |",
        "|---|---|---|---|",
    ]
    for stage in payload["stages"]:
        lines.append(
            f"| `{stage['stage_id']}` | {stage['purpose']} | `{stage['strict_gate']}` | {stage['failure_mode']} |"
        )
    lines.extend(
        [
            "",
            "## Output Sentinels",
            "",
            "| Sentinel |",
            "|---|",
        ]
    )
    for path in payload["output_build_sentinels"]:
        lines.append(f"| `{path}` |")
    return "\n".join(lines) + "\n"


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        normalized = path.as_posix()
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(path)
    return result


__all__ = [
    "PIPELINE_STAGE_CONTRACTS",
    "PipelineStageContract",
    "output_build_sentinels",
    "pipeline_contract_by_id",
    "pipeline_contract_report",
    "pipeline_stage_contracts",
    "render_pipeline_contract_markdown",
    "source_freshness_roots",
    "validate_pipeline_stage_contracts",
]
