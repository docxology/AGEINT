from __future__ import annotations

from typing import Protocol, Sequence, TypeVar

from .source_tiers import source_is_primary_support


class _TopicSource(Protocol):
    url: str
    verified: bool


_SourceT = TypeVar("_SourceT", bound=_TopicSource)

ANALYTIC_ANCHORS = (
    "[@official_odni_icd_203]; [@official_cia_tradecraft_primer]; "
    "[@official_cia_sherman_kent_profession]; [@official_911_commission_report]; "
    "[@official_robb_silberman_wmd_report]; [@scholarly_rand_2016_sat_evaluation]; "
    "[@scholarly_marcoci_2019_tradecraft_reliability]; "
    "[@scholarly_barnes_mandel_2014_forecast_accuracy]"
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
        "the empirical limit that would force a weaker claim."
    )


def tradecraft_context_support(display_title: str, citation_spine: str) -> str:
    """Source-support line for analytic rows backed only by context sources."""
    inherited = citation_spine.strip().rstrip(".")
    return (
        f"**{display_title}** uses curated analytic-tradecraft anchors "
        f"{ANALYTIC_ANCHORS}. The inherited guide citation(s) {inherited} "
        "remain context only; primary support must keep likelihood, confidence, "
        "assumptions, alternatives, dissent, source quality, and refresh duty separate."
    )
