from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from curriculum import Curriculum, load_curriculum
from citation_workflow import (
    render_citation_workflow_markdown,
    render_source_section_citation_rows,
    source_citation_coverage_summary,
)
from intelligence_content import (
    INTELLIGENCE_RESEARCH_ANCHORS,
    PRACTICE_LENSES,
    accessibility_review_rows,
    adversarial_assurance_rows,
    agent_incident_response_rows,
    assessment_integrity_rows,
    capstone_scaffold_rows,
    current_source_update_rows,
    data_lineage_registry_rows,
    hria_dpia_worksheet_rows,
    learner_support_rows,
    model_dataset_card_rows,
    practice_lens_rows,
    procurement_oversight_rows,
    profile_inventory_rows,
    question_bank_rows,
    release_change_control_rows,
    remediation_backlog_rows,
    research_anchor_rows,
    research_spine_summary,
    retention_audit_rows,
    risk_exception_rows,
    role_competency_rows,
    safe_substitution_rows,
    source_lane_rows,
    source_refresh_rows,
    transparency_notice_rows,
)

try:
    from intelligence_content.source_grounding import (
        clean_source_title as _sg_clean_title,
        safe_source_note as _sg_safe_note,
    )
except ImportError:  # pragma: no cover
    def _sg_clean_title(t: str) -> str: return t  # type: ignore[misc]
    def _sg_safe_note(n: str) -> str: return n   # type: ignore[misc]

from ._01_part import (
    SOURCE_QUALITY_ANCHORS,
    _clean_bibtex_text,
    _clean_bibtex_value,
    _join_note_parts,
    _reference_author,
    _source_quality_references,
    bibliography_rows,
    part_rows,
    pattern_rows,
)


def _render_bibtex_entries(references: list[dict[str, Any]]) -> str:
    entries: list[str] = []
    for ref in references:
        # Clean title: strip site-suffix noise and truncation markers
        raw_title = ref.get("title") or ""
        cleaned_title = _sg_clean_title(raw_title) if raw_title else raw_title
        title = _clean_bibtex_text(cleaned_title)
        author = _reference_author(ref)
        year = _clean_bibtex_value(ref.get("year") or "2026")
        url = _clean_bibtex_value(ref.get("url") or "")
        # Use safe_source_note to get the best available cleaned description
        raw_note = str(ref.get("note") or "")
        cleaned_note = _sg_safe_note(raw_note) if raw_note else ""
        note_parts = [cleaned_note or "SIST guide bibliography entry"]
        if ref.get("checked_as_of"):
            note_parts.append(f"Checked as of {ref['checked_as_of']}")
        if ref.get("citation_role"):
            note_parts.append(f"Citation role: {ref['citation_role']}")
        if ref.get("source_lane"):
            note_parts.append(f"Source lane: {ref['source_lane']}")
        if ref.get("source_tier"):
            note_parts.append(f"Source tier: {ref['source_tier']}")
        if ref.get("refresh_cadence"):
            note_parts.append(f"Refresh cadence: {ref['refresh_cadence']}")
        if ref.get("refresh_trigger"):
            note_parts.append(f"Refresh trigger: {ref['refresh_trigger']}")
        if ref.get("verification_method"):
            note_parts.append(f"Verification method: {ref['verification_method']}")
        if ref.get("claim_scope"):
            note_parts.append(f"Claim scope: {ref['claim_scope']}")
        if ref.get("stakeholder_role"):
            note_parts.append(f"Stakeholder role: {ref['stakeholder_role']}")
        if ref.get("assurance_use"):
            note_parts.append(f"Assurance use: {ref['assurance_use']}")
        if ref.get("rights_dimension"):
            note_parts.append(f"Rights dimension: {ref['rights_dimension']}")
        if ref.get("verification_note"):
            note_parts.append(str(ref["verification_note"]))
        note = _clean_bibtex_text(_join_note_parts(note_parts))
        entries.append(
            "\n".join(
                [
                    f"@misc{{{ref['key']},",
                    f"  title = {{{title}}},",
                    f"  author = {{{author}}},",
                    f"  year = {{{year}}},",
                    f"  url = {{{url}}},",
                    f"  note = {{{note}}},",
                    "}",
                ]
            )
        )
    return "\n\n".join(entries) + "\n"


def reference_bibtex_files(references: list[dict[str, Any]]) -> dict[str, str]:
    """Render split BibTeX files for source guide and verified anchor groups."""
    rendered: dict[str, str] = {}
    source_refs = sorted(
        (ref for ref in references if isinstance(ref.get("number"), int)),
        key=lambda ref: int(ref["number"]),
    )
    for index in range(0, len(source_refs), 50):
        chunk = source_refs[index : index + 50]
        first = int(chunk[0]["number"])
        last = int(chunk[-1]["number"])
        rendered[f"references-source-guide-{first:03d}-{last:03d}.bib"] = _render_bibtex_entries(chunk)
    extra_source_refs = [ref for ref in references if not isinstance(ref.get("number"), int)]
    if extra_source_refs:
        rendered["references-source-guide-custom.bib"] = _render_bibtex_entries(extra_source_refs)

    quality_refs = _source_quality_references()
    rendered["references-source-quality.bib"] = _render_bibtex_entries(quality_refs)

    research_refs = [anchor.as_reference() for anchor in INTELLIGENCE_RESEARCH_ANCHORS]
    for start in range(0, len(research_refs), 50):
        chunk = research_refs[start : start + 50]
        rendered[
            f"references-research-anchors-{start + 1:03d}-{start + len(chunk):03d}.bib"
        ] = _render_bibtex_entries(chunk)
    return rendered


def reference_bibtex(references: list[dict[str, Any]]) -> str:
    """Render BibTeX for parsed references plus official source anchors."""
    return "\n".join(reference_bibtex_files(references).values())


def _source_citation_coverage_summary_text(curriculum: Curriculum) -> str:
    """Return a compact prose summary for generated citation variables."""

    summary = source_citation_coverage_summary(curriculum)
    distribution = ", ".join(
        f"{count} citation(s): {sections} section(s)"
        for count, sections in summary.citation_count_distribution
    )
    return (
        f"{summary.section_count} source sections; "
        f"{summary.citation_occurrences} citation occurrences; "
        f"{summary.unique_citation_keys} unique source-guide keys; "
        f"{summary.zero_citation_sections} zero-citation source sections. "
        f"Distribution: {distribution}."
    )


def generate_variables(project_root: Path) -> dict[str, str]:
    """Generate AGEINT manuscript variables from the parsed curriculum JSON."""
    curriculum_path = project_root / "data" / "curriculum"
    curriculum = load_curriculum(curriculum_path)
    stats = curriculum.stats
    return {
        "CURRICULUM_TITLE": curriculum.payload.get(
            "title",
            "Agentic Intelligence Modular Curriculum",
        ),
        "CURRICULUM_SOURCE_GUIDE": "SIST Guide TOC and Bibliography",
        "CURRICULUM_PART_COUNT": str(stats["parts"]),
        "CURRICULUM_CHAPTER_COUNT": str(stats["chapters"]),
        "CURRICULUM_APPENDIX_COUNT": str(stats["appendices"]),
        "CURRICULUM_PATTERN_COUNT": str(stats["patterns"]),
        "CURRICULUM_REFERENCE_COUNT": str(stats["references"]),
        "SOURCE_QUALITY_ANCHOR_COUNT": str(len(SOURCE_QUALITY_ANCHORS)),
        "INTELLIGENCE_RESEARCH_ANCHOR_COUNT": str(len(INTELLIGENCE_RESEARCH_ANCHORS)),
        "INTELLIGENCE_PRACTICE_LENS_COUNT": str(len(PRACTICE_LENSES)),
        "SOURCE_QUALITY_SPINE": (
            "Official source-quality anchors include OECD agentic AI, NIST AI RMF, "
            "NIST AI 600-1, NSA MCP security guidance, NIST SP 800-82 Rev. 3, "
            "ISA/IEC 62443, ODNI ICD 203, the EU AI Act, CISA foreign influence "
            "guidance, and NATO counter-information-threat guidance."
        ),
        "INTELLIGENCE_RESEARCH_SPINE": research_spine_summary(),
        "INTELLIGENCE_RESEARCH_ROWS": research_anchor_rows(),
        "INTELLIGENCE_SOURCE_LANE_ROWS": source_lane_rows(),
        "SOURCE_REFRESH_ROWS": source_refresh_rows(),
        "CURRENT_SOURCE_UPDATE_ROWS": current_source_update_rows(),
        "CITATION_WORKFLOW_GUIDE": render_citation_workflow_markdown(curriculum),
        "SOURCE_SECTION_CITATION_ROWS": render_source_section_citation_rows(curriculum),
        "SOURCE_CITATION_COVERAGE_SUMMARY": _source_citation_coverage_summary_text(curriculum),
        "SAFE_SUBSTITUTION_ROWS": safe_substitution_rows(),
        "CAPSTONE_SCAFFOLD_ROWS": capstone_scaffold_rows(),
        "ACCESSIBILITY_REVIEW_ROWS": accessibility_review_rows(),
        "PROCUREMENT_OVERSIGHT_ROWS": procurement_oversight_rows(),
        "HRIA_DPIA_WORKSHEET_ROWS": hria_dpia_worksheet_rows(),
        "DATA_LINEAGE_REGISTRY_ROWS": data_lineage_registry_rows(),
        "ASSESSMENT_INTEGRITY_ROWS": assessment_integrity_rows(),
        "AGENT_INCIDENT_RESPONSE_ROWS": agent_incident_response_rows(),
        "ROLE_COMPETENCY_ROWS": role_competency_rows(),
        "ADVERSARIAL_ASSURANCE_ROWS": adversarial_assurance_rows(),
        "MODEL_DATASET_CARD_ROWS": model_dataset_card_rows(),
        "TRANSPARENCY_NOTICE_ROWS": transparency_notice_rows(),
        "RETENTION_AUDIT_ROWS": retention_audit_rows(),
        "RELEASE_CHANGE_CONTROL_ROWS": release_change_control_rows(),
        "RISK_EXCEPTION_ROWS": risk_exception_rows(),
        "LEARNER_SUPPORT_ROWS": learner_support_rows(),
        "QUESTION_BANK_ROWS": question_bank_rows(),
        "REMEDIATION_BACKLOG_ROWS": remediation_backlog_rows(),
        "INTELLIGENCE_PROFILE_ROWS": profile_inventory_rows(),
        "INTELLIGENCE_PRACTICE_LENS_ROWS": practice_lens_rows(),
        "CURRICULUM_PART_ROWS": part_rows(curriculum),
        "AGEINT_PATTERN_ROWS": pattern_rows(curriculum.patterns),
        "BIBLIOGRAPHY_ATLAS_ROWS": bibliography_rows(curriculum.references),
        "BIBTEX_REFERENCES": reference_bibtex(curriculum.references),
        "BIBTEX_REFERENCE_FILES": json.dumps(
            reference_bibtex_files(curriculum.references),
            ensure_ascii=False,
            sort_keys=True,
        ),
    }


def save_variables(variables: dict[str, str], output_path: Path) -> Path:
    """Write generated variables to JSON for auditability."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(variables, indent=2, sort_keys=True, ensure_ascii=False)
    output_path.write_text(payload, encoding="utf-8")
    return output_path


def write_bibtex_files(target_dir: Path, files: dict[str, str]) -> None:
    """Write BibTeX shard files and remove legacy combined references."""
    target_dir.mkdir(parents=True, exist_ok=True)
    legacy = target_dir / "references.bib"
    if legacy.exists():
        legacy.unlink()
    for stale in target_dir.glob("references-*.bib"):
        stale.unlink()
    for name, text in files.items():
        (target_dir / name).write_text(text, encoding="utf-8")
