"""Canonical AGEINT build pipeline."""

from __future__ import annotations

import os
from pathlib import Path
from typing import NamedTuple

from curriculum import Curriculum, build_curriculum, write_compact_curriculum_payload, write_curriculum_shards
from figures import load_figure_registry, render_figures
from manuscript_manifest import render_manuscript
from manuscript_templates import write_template_library
from manuscript_variables import generate_variables, reference_bibtex_files, save_variables, write_bibtex_files
from output_docs import write_output_directory_docs

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class BuildResult(NamedTuple):
    """Result paths and counts from an AGEINT build."""

    curriculum: Curriculum
    written_source_templates: int
    variables_path: Path
    figure_registry_path: Path
    output_manuscript: Path


def _mirror_curriculum_data(curriculum: Curriculum, destination: Path) -> None:
    write_curriculum_shards(curriculum.payload, destination / "curriculum")
    write_compact_curriculum_payload(curriculum.payload, destination / "curriculum_outline.json")


def run_build(
    project_root: Path = PROJECT_ROOT,
    *,
    regenerate_source_template_library: bool = False,
    allow_placeholder_figures: bool | None = None,
) -> BuildResult:
    """Load curriculum data, refresh generated outputs, and render the manuscript."""
    root = Path(project_root)
    if allow_placeholder_figures is None:
        allow_placeholder_figures = os.environ.get("AGEINT_REQUIRE_RENDERED_FIGURES", "") != "1"
    write_output_directory_docs(root)
    source = root / "SIST-Guide-TOC-and-Bibliography-v2.md"
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
    variables_path = save_variables(
        variables,
        root / "output" / "data" / "manuscript_variables.json",
    )
    figure_registry_path = render_figures(
        root,
        curriculum,
        allow_placeholder_figures=allow_placeholder_figures,
    )
    figure_registry = load_figure_registry(figure_registry_path)["figures"]
    output_manuscript = render_manuscript(root, curriculum, variables, figure_registry)
    write_bibtex_files(output_manuscript, bibtex_files)
    return BuildResult(
        curriculum,
        written_templates,
        variables_path,
        figure_registry_path,
        output_manuscript,
    )
