from __future__ import annotations

from typing import Protocol, Sequence, TypeVar

from .source_tiers import source_is_primary_support


class _TopicSource(Protocol):
    url: str
    verified: bool


_SourceT = TypeVar("_SourceT", bound=_TopicSource)

ANALYTIC_ANCHORS = (
    "[@official_odni_icd_203]; [@official_cia_tradecraft_primer]; "
    "[@official_cia_sherman_kent_profession]; "
    "[@official_cia_cooper_2005_analytic_pathologies]; "
    "[@official_cia_analytic_culture_us_ic]; [@official_911_commission_report]; "
    "[@official_robb_silberman_wmd_report]; "
    "[@official_senate_2004_prewar_iraq_assessment]; "
    "[@scholarly_rand_2016_sat_evaluation]; "
    "[@scholarly_coulthart_2017_core_sat_evaluation]; "
    "[@scholarly_chang_2018_restructuring_sats]; "
    "[@scholarly_dhami_2019_ach_intelligence_analysis]; "
    "[@scholarly_whitesmith_2019_ach_bias]; "
    "[@scholarly_karvetski_mandel_2020_ach_coherence]; "
    "[@scholarly_wilcox_mandel_2024_ach_critical_review]; "
    "[@scholarly_barnes_mandel_2014_forecast_accuracy]; "
    "[@scholarly_dhami_mandel_mellers_tetlock_2015_decision_science]; "
    "[@official_iarpa_ace_program]; [@official_iarpa_reason_program]; "
    "[@official_belfer_mcmahon_2024_ai_tradecraft_standards]"
)


def primary_topic_sources(risk_category: str, sources: Sequence[_SourceT]) -> tuple[_SourceT, ...]:
    """Return source-guide rows eligible for primary generated claim prose."""
    if risk_category != "analytic_tradecraft":
        return tuple(sources)
    return tuple(source for source in sources if source_is_primary_support(source))


def curated_tradecraft_evidence(display_title: str) -> str:
    """Evidence prompt used when analytic guide rows are context-only."""
    return (
        f"For **{display_title}**, use the curated analytic-tradecraft anchors "
        f"{ANALYTIC_ANCHORS}. Pull observation, inference, assumption, likelihood, "
        "confidence, dissent, decision-uptake boundary, postmortem learning, and "
        "the empirical limit that would force a weaker claim. Treat SATs as "
        "reviewable reasoning artifacts, not validated universal debiasing or "
        "autonomous judgment replacements."
    )


def tradecraft_context_support(display_title: str, citation_spine: str) -> str:
    """Source-support line for analytic rows backed only by context sources."""
    inherited = citation_spine.strip().rstrip(".")
    return (
        f"**{display_title}** uses curated analytic-tradecraft anchors "
        f"{ANALYTIC_ANCHORS}. The inherited guide citation(s) {inherited} "
        "remain context only; primary support must keep likelihood, confidence, "
        "assumptions, alternatives, dissent, source quality, ACH limits, and "
        "refresh duty separate."
    )
