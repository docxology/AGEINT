"""AGEINT curriculum parser, template writer, and runtime injection helpers."""

from .build_pipeline import BuildResult, run_build, run_build_figures
from .citation_workflow import (
    CitationCountRow,
    CitationCoverageSummary,
    generated_markdown_citation_inventory,
    render_citation_workflow_markdown,
    render_source_section_citation_rows,
    source_citation_cell,
    source_citation_coverage_summary,
    source_citation_spine,
    source_key,
    source_section_citation_inventory,
)
from .curriculum import (
    Curriculum,
    build_curriculum,
    load_curriculum,
    parse_curriculum_guide,
)
from .figures import (
    load_figure_registry,
    render_figures,
)
from .manuscript_manifest import (
    ManuscriptManifest,
    ManuscriptSection,
    build_manuscript_manifest,
    render_manuscript,
)
from .manuscript_variables import (
    generate_variables,
    reference_bibtex_files,
    save_variables,
    write_bibtex_files,
)
from .output_docs import write_output_directory_docs
from .pdf_quality import (
    PdfPhraseHit,
    PdfQualityReport,
    audit_pdf_quality,
    extract_pdf_text,
    pdf_metadata,
    render_pdf_quality_markdown,
    report_json,
)
from .rendered_heading_support import (
    HeadingSupportRow,
    HeadingSupportSummary,
    heading_support_inventory,
    heading_support_summary,
    render_heading_support_markdown,
)
from .source_identity import (
    build_source_identity_lock,
    load_source_identity_lock,
    source_identity_mismatches,
)
from .template_resolver import ensure_template_repo_on_path, resolve_template_repo
from .unit_education import (
    UnitEducationProfile,
    render_unit_profile_markdown,
    unit_profile_for_number,
    unit_profile_for_part,
)

__all__ = [
    "BuildResult",
    "CitationCountRow",
    "CitationCoverageSummary",
    "Curriculum",
    "HeadingSupportRow",
    "HeadingSupportSummary",
    "ManuscriptManifest",
    "ManuscriptSection",
    "PdfPhraseHit",
    "PdfQualityReport",
    "UnitEducationProfile",
    "audit_pdf_quality",
    "build_curriculum",
    "build_manuscript_manifest",
    "build_source_identity_lock",
    "ensure_template_repo_on_path",
    "extract_pdf_text",
    "generated_markdown_citation_inventory",
    "generate_variables",
    "heading_support_inventory",
    "heading_support_summary",
    "load_curriculum",
    "load_figure_registry",
    "load_source_identity_lock",
    "parse_curriculum_guide",
    "pdf_metadata",
    "reference_bibtex_files",
    "render_citation_workflow_markdown",
    "render_figures",
    "render_heading_support_markdown",
    "render_manuscript",
    "render_pdf_quality_markdown",
    "render_source_section_citation_rows",
    "render_unit_profile_markdown",
    "report_json",
    "resolve_template_repo",
    "run_build",
    "run_build_figures",
    "save_variables",
    "source_citation_cell",
    "source_citation_coverage_summary",
    "source_citation_spine",
    "source_identity_mismatches",
    "source_key",
    "source_section_citation_inventory",
    "unit_profile_for_number",
    "unit_profile_for_part",
    "write_bibtex_files",
    "write_output_directory_docs",
]
