"""Regression checks for the pasted literature-review integration pass."""

from __future__ import annotations

from pathlib import Path

from manuscript_quality.inventory_helpers import generated_output_files, manuscript_dir


def test_literature_review_inputs_remain_discovery_only_in_generated_manuscript(
    built_output: Path,
) -> None:
    output_manuscript = manuscript_dir(built_output)
    orientation_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((output_manuscript / "orientation").glob("*.md"))
    )
    forbidden = (
        "pasted-text.txt",
        "Deep Literature Review: Synthetic Intelligence",
        "Synthetic Intelligence, Analytic Tradecraft, Operational Security, and Cognitive Security: A Deep Literature Review",
        "Structured Analytic Techniques: A Deep Literature Review",
    )

    assert "[@fig:ageint-si-tradecraft-opsec-cogsec-convergence]" in orientation_text
    assert "[@scholarly_caballero_jenkins_2024_llm_national_security]" in orientation_text
    assert "[@official_belfer_mcmahon_2024_ai_tradecraft_standards]" in orientation_text
    for path in generated_output_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            assert phrase not in text, path


def test_sat_literature_report_remains_discovery_only_and_sat_chapter_uses_verified_sources(
    built_output: Path,
) -> None:
    output_manuscript = manuscript_dir(built_output)
    sat_chapter = output_manuscript / "parts" / "epistemic-rigor-and-analytic-tradecraft" / "structured-analytic-techniques-sats"
    sat_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(sat_chapter.glob("*.md"))
    )
    required_citations = {
        "[@official_cia_cooper_2005_analytic_pathologies]",
        "[@official_cia_analytic_culture_us_ic]",
        "[@scholarly_coulthart_2017_core_sat_evaluation]",
        "[@scholarly_chang_2018_restructuring_sats]",
        "[@scholarly_whitesmith_2019_ach_bias]",
        "[@scholarly_karvetski_mandel_2020_ach_coherence]",
        "[@scholarly_wilcox_mandel_2024_ach_critical_review]",
        "[@scholarly_dhami_mandel_mellers_tetlock_2015_decision_science]",
        "[@official_iarpa_reason_program]",
    }
    forbidden = (
        "Structured Analytic Techniques: A Deep Literature Review",
        "18965849-a755-4bf3-aecb-9b1ee3ea4e02",
        "pasted-text.txt",
    )

    for citation in required_citations:
        assert citation in sat_text
    assert "universal debiasing" in sat_text
    assert "autonomous judgment replacements" in sat_text
    for path in generated_output_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            assert phrase not in text, path
