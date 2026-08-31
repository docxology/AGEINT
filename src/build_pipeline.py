"""Canonical AGEINT build pipeline."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from curriculum import Curriculum, build_curriculum, write_compact_curriculum_payload, write_curriculum_shards
from figures import load_figure_registry, render_evidence_transit_map, render_figures
from manuscript_manifest import render_manuscript
from manuscript_templates import write_template_library
from manuscript_variables import generate_variables, reference_bibtex_files, save_variables, write_bibtex_files
from orchestration_contracts import output_build_sentinels, source_freshness_roots, validate_pipeline_stage_contracts
from output_docs import write_output_directory_docs
from published_counts_gate import verify_published_counts

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_SUPPORT_MARKDOWN = {"AGENTS.md", "README.md", "preamble.md"}

# See the matching constant/comment in src/pdf_quality.py: a fresh git
# checkout writes every tracked file at roughly the same instant in
# tree-walk order, not logical source-before-output order, so a strict `>`
# mtime comparison can spuriously read as "stale" from checkout-ordering
# noise alone. Confirmed live via a real `git clone` of this repo. A
# genuine edit-then-rebuild gap is seconds to minutes; this tolerance only
# absorbs checkout noise.
STALE_OUTPUT_TOLERANCE_SECONDS = 30.0

# Output-relative path of the build stamp: the source digest a build was produced
# from. Committing it lets a fresh clone decide freshness by content instead of
# by mtimes, which git does not preserve.
BUILD_STAMP_PATH = Path("data/build_stamp.json")


@dataclass(frozen=True)
class BuildConfig:
    """Runtime build flags for AGEINT pipeline entrypoints."""

    require_rendered_figures: bool = False
    source_path: Path | None = None

    @classmethod
    def from_env(cls) -> BuildConfig:
        import os

        return cls(require_rendered_figures=os.environ.get("AGEINT_REQUIRE_RENDERED_FIGURES", "") == "1")

    @property
    def allow_placeholder_figures(self) -> bool:
        return not self.require_rendered_figures

    def resolve_source_path(self, project_root: Path) -> Path:
        if self.source_path is not None:
            return self.source_path
        return project_root / "SIST-Guide-TOC-and-Bibliography-v2.md"


class BuildResult(NamedTuple):
    """Result paths and counts from an AGEINT build."""

    curriculum: Curriculum
    written_source_templates: int
    variables_path: Path
    figure_registry_path: Path
    output_manuscript: Path


def _iter_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.is_dir():
        return []
    return [candidate for candidate in path.rglob("*") if candidate.is_file() and "__pycache__" not in candidate.parts and ".pytest_cache" not in candidate.parts]


def _latest_mtime(paths: list[Path]) -> float:
    latest = 0.0
    for path in paths:
        for candidate in _iter_files(path):
            latest = max(latest, candidate.stat().st_mtime)
    return latest


def source_content_digest(project_root: Path) -> str:
    """Return a stable digest of every source input the build reads.

    Hashes each file's repo-relative path and bytes in sorted order, so the
    result depends only on content — not on mtimes, checkout order, or where the
    checkout lives.
    """
    digest = hashlib.sha256()
    for root_relative in sorted(source_freshness_roots()):
        for candidate in sorted(_iter_files(project_root / root_relative)):
            relative = candidate.relative_to(project_root).as_posix()
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(hashlib.sha256(candidate.read_bytes()).digest())
    return digest.hexdigest()


def write_build_stamp(project_root: Path, output: Path) -> Path:
    """Record the source digest this build was produced from."""
    stamp_path = output / BUILD_STAMP_PATH
    stamp_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": 1, "source_digest": source_content_digest(project_root)}
    stamp_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return stamp_path


def read_build_stamp(output: Path) -> dict[str, object] | None:
    """Return the recorded build stamp, or None when absent or unreadable."""
    stamp_path = output / BUILD_STAMP_PATH
    if not stamp_path.is_file():
        return None
    try:
        loaded = json.loads(stamp_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return loaded if isinstance(loaded, dict) else None


def generated_output_is_stale(project_root: Path, output: Path) -> bool:
    """Return true when generated output no longer matches its source inputs.

    Prefers a content comparison against the build stamp. Git does not preserve
    mtimes, so after any clone or checkout every file carries roughly the
    checkout time in arbitrary order, and an mtime comparison stops meaning
    "source changed after the build" — which is why freshness could report drift
    on a tree that was in fact coherent.

    The mtime heuristic remains as a fallback for trees built before stamps
    existed, so an un-stamped checkout behaves exactly as it did before.
    """

    validate_pipeline_stage_contracts()
    sentinels = [output / path for path in output_build_sentinels()]
    if any(not path.is_file() for path in sentinels):
        return True

    stamp = read_build_stamp(output)
    if stamp is not None:
        recorded = stamp.get("source_digest")
        if isinstance(recorded, str) and recorded:
            return recorded != source_content_digest(project_root)

    source_paths = [project_root / path for path in source_freshness_roots()]
    latest_source = _latest_mtime(source_paths)
    if latest_source == 0.0:
        return True
    oldest_sentinel = min(path.stat().st_mtime for path in sentinels)
    return latest_source > oldest_sentinel + STALE_OUTPUT_TOLERANCE_SECONDS


def _mirror_curriculum_data(curriculum: Curriculum, destination: Path) -> None:
    write_curriculum_shards(curriculum.payload, destination / "curriculum")
    write_compact_curriculum_payload(curriculum.payload, destination / "curriculum_outline.json")


def _generated_markdown_file_count(output_manuscript: Path) -> int:
    return sum(1 for path in output_manuscript.rglob("*.md") if path.name not in MANUSCRIPT_SUPPORT_MARKDOWN)


def run_build(project_root: Path = PROJECT_ROOT, *, regenerate_source_template_library: bool = False, allow_placeholder_figures: bool | None = None, config: BuildConfig | None = None) -> BuildResult:
    """Load curriculum data, refresh generated outputs, and render the manuscript."""
    root = Path(project_root)
    from template_resolver import ensure_template_repo_on_path

    build_config = config or BuildConfig.from_env()
    validate_pipeline_stage_contracts()
    ensure_template_repo_on_path(root)
    from _data_loaders import validate_declarative_tables

    validate_declarative_tables()
    if allow_placeholder_figures is None:
        allow_placeholder_figures = build_config.allow_placeholder_figures
    write_output_directory_docs(root)
    source = build_config.resolve_source_path(root)
    data_path = root / "data" / "curriculum"
    curriculum = build_curriculum(source, data_path)
    _mirror_curriculum_data(curriculum, root / "output" / "data")

    written_templates = 0
    if regenerate_source_template_library:
        written = write_template_library(root / "manuscript" / "templates")
        written_templates = len(written)

    variables = generate_variables(root)
    bibtex_files = reference_bibtex_files(curriculum.references)
    write_bibtex_files(root / "manuscript", bibtex_files)
    variables_path = save_variables(variables, root / "output" / "data" / "manuscript_variables.json")
    figure_registry_path = render_figures(root, curriculum, allow_placeholder_figures=allow_placeholder_figures)
    figure_registry = load_figure_registry(figure_registry_path)["figures"]
    output_manuscript = render_manuscript(root, curriculum, variables, figure_registry)
    render_evidence_transit_map(root, curriculum, figure_count=len(figure_registry), generated_markdown_files=_generated_markdown_file_count(output_manuscript))
    write_bibtex_files(output_manuscript, bibtex_files)
    # Gate: published counts must match a fresh re-count of the source data
    # and the figure registry, or the build fails on drift.
    verify_published_counts(root, curriculum_stats=curriculum.stats, figure_count=len(figure_registry))
    # Written last: the stamp asserts "this output was produced from that source",
    # so it must only exist once every artifact above has been written.
    write_build_stamp(root, root / "output")
    return BuildResult(curriculum, written_templates, variables_path, figure_registry_path, output_manuscript)


def run_build_figures(project_root: Path = PROJECT_ROOT, curriculum: Curriculum | None = None, *, allow_placeholder_figures: bool | None = None, config: BuildConfig | None = None) -> Path:
    """Refresh only AGEINT figure assets and the registry."""
    root = Path(project_root)
    from template_resolver import ensure_template_repo_on_path

    build_config = config or BuildConfig.from_env()
    ensure_template_repo_on_path(root)
    if allow_placeholder_figures is None:
        allow_placeholder_figures = build_config.allow_placeholder_figures
    if curriculum is None:
        source = build_config.resolve_source_path(root)
        data_path = root / "data" / "curriculum"
        curriculum = build_curriculum(source, data_path)
    return render_figures(root, curriculum, allow_placeholder_figures=allow_placeholder_figures)
