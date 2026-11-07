"""Build and render the AGEINT semantic manuscript manifest."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from citation_workflow import source_citation_spine, source_citation_spine_inline
    from intelligence_content import capstone_scaffold_rows, part_research_brief, profile_triangulation_anchors, safe_topic_entries
    from manuscript_manifest.types import section_label as _label
    from unit_education import render_unit_profile_markdown
except ImportError:  # pragma: no cover - exercised by thin CLI wrappers
    from ..citation_workflow import (  # type: ignore[no-redef]
        source_citation_spine,
        source_citation_spine_inline,
    )
    from ..intelligence_content import (  # type: ignore[no-redef]
        capstone_scaffold_rows,
        part_research_brief,
        profile_triangulation_anchors,
        safe_topic_entries,
    )
    from ..unit_education import render_unit_profile_markdown  # type: ignore[no-redef]
    from .types import section_label as _label  # type: ignore[no-redef]


def _citation_context(citation_numbers: list[int], *, limit: int = 2) -> str:
    """Return a compact, body-safe source-spine phrase."""

    selected = list(citation_numbers[:limit])
    if not selected:
        return "the surrounding verified source spine"
    return source_citation_spine(selected)


def _citation_context_inline(citation_numbers: list[int], *, limit: int = 2) -> str:
    """Return a compact source-spine phrase for mid-sentence joins."""

    selected = list(citation_numbers[:limit])
    if not selected:
        return "the surrounding verified source spine"
    return source_citation_spine_inline(selected)


def _part_source_context(part: dict[str, Any]) -> str:
    """Return a part-specific context phrase without repeating the part title."""

    citations: list[int] = []
    for chapter in part.get("chapters", []):
        for number in chapter.get("citations", []):
            if number not in citations:
                citations.append(number)
            if len(citations) >= 2:
                break
        if len(citations) >= 2:
            break
    return _citation_context(citations)


def _chapter_source_context(chapter: dict[str, Any]) -> str:
    """Return a chapter-specific source context without using its generated title."""

    return _citation_context(list(chapter.get("citations", [])))


def _chapter_source_context_inline(chapter: dict[str, Any]) -> str:
    """Return chapter source context without terminal punctuation."""

    return _citation_context_inline(list(chapter.get("citations", [])))


def _chapter_topic_context(chapter: dict[str, Any], part: dict[str, Any], *, limit: int = 2) -> str:
    """Return a compact topic cluster for body prose.

    Routes raw display titles through ``compact_topic`` so the registry
    parenthetical and trailing-qualifier boilerplate that pads design-pattern
    titles is dropped before the cluster is interpolated across ~13 body sites.
    """

    from intelligence_content.topic_lesson_voice import compact_topic_cluster

    topics = [entry.display_title for entry in safe_topic_entries(chapter, part)[:limit]]
    if not topics:
        return "the local source-topic cluster"
    # Bold the cluster so the rendered-reference sanitiser treats it as an
    # authored subject phrase: a lesson title like "History of Social
    # Engineering" must not have its embedded chapter-title substring
    # ("Social Engineering") neutralised into "History of the module".
    return f"**{compact_topic_cluster(topics)}**"


def _cognitive_attack_framework() -> str:
    return (
        "## Cognitive-security models: source scope before defensive use\n\n"
        "The CCDCOE research summary frames cognitive warfare as pressure on the structures through "
        "which a social system interprets evidence, establishes trust, and coordinates decisions. "
        "Its systemic invariants include epistemic frameworks, values, collective identity, trust "
        "architectures, and expectations about the future. This is a conceptual account, not evidence "
        "that disagreement, distress, or institutional failure was caused by a cognitive attack. "
        "The unit map [@fig:ageint-cognitive-attack-layers] separates those source concepts from "
        "AGEINT's proposed defensive checks; it does not attribute a biological/psychological/social "
        "attack taxonomy to that source [@scholarly_ccdcoe_cognitive_warfare_reconception].\n\n"
        "For a classroom case, first record the observable artifact and its origin, then compare "
        "ordinary error, ambiguity, missing context, and deliberate interference as live alternatives. "
        "A defender may check provenance, preserve dissent, and clarify decision ownership without "
        "profiling an audience or inferring an adversary. Assign the next check to the alternative "
        "it would discriminate; if the evidence cannot distinguish them, retain an unresolved judgment. "
        "These are instructional safeguards, not a claim of demonstrated protection.\n\n"
        "DARPA's Intrinsic Cognitive Security program is a separate, mixed-reality research effort "
        "aiming to develop and validate formal, model-scoped mitigation guarantees. A program goal "
        "does not establish a guarantee for an LLM, a human population, or this curriculum. "
        "Keep mixed-reality cognition, social-system theory, and agent-software security distinct "
        "when borrowing an analogy [@official_darpa_intrinsic_cognitive_security]."
    )


def _epistemic_stack_framework() -> str:
    return (
        "## An instructional epistemic coherence stack\n\n"
        "AGEINT groups its defensive checks into a proposed five-layer teaching architecture, shown "
        "in [@fig:ageint-unified-epistemic-stack]: technical integrity, operational controls, "
        "structured reasoning, epistemic review, and institutional governance. The grouping is "
        "author-defined; neither the ordering nor the necessity or sufficiency of its layers has "
        "been empirically established here. Sandboxing limits permissions, provenance records "
        "describe origins, and human review challenges conclusions; none alone establishes truth. "
        "A provenance signature is not a factuality certificate, and a verifier agent may share "
        "the generating agent's sources and failure modes.\n\n"
        "The cited epistemic-agent paper proposes a normative roadmap centered on competence, "
        "falsifiability, and epistemically virtuous behavior. Use it to formulate review questions, "
        "not as an evaluation showing that this stack protects a system's beliefs. DARPA's "
        "mixed-reality program likewise does not validate general agent assurance "
        "[@scholarly_deepmind_epistemic_agent_trust]; [@official_darpa_intrinsic_cognitive_security].\n\n"
        "## Reliability-inspired governance: analogy and test obligation\n\n"
        "The crosswalk [@fig:ageint-hro-governance-crosswalk] is an instructional analogy between "
        "high-reliability organizational principles and candidate agent controls. For each proposed "
        "mapping, name the failure it addresses, the observable signal, the person empowered to stop "
        "the exercise, and the synthetic negative control that would reveal a missed failure. "
        "For example, a review queue may miss a contradicted claim even when every tool call is logged; "
        "test the claim-review handoff rather than treating the presence of logs as assurance. "
        "Do not infer analytic accuracy from a reliability metaphor or a completed checklist. "
        "The judgment-correctives literature specifically challenges untested claims for analytic "
        "methods; agent red-team guidance supplies a review discipline rather than validation of "
        "this crosswalk [@scholarly_mandel_tetlock_judgment_correctives]; "
        "[@official_csa_nist_ai_agent_red_teaming_standards]."
    )


def _part_summary(part: dict[str, Any]) -> str:
    source_context = _part_source_context(part)
    title = str(part["title"])
    framework = ""
    if title == "COGNITIVE SECURITY":
        framework = _cognitive_attack_framework()
    elif title == "EPISTEMIC RIGOR AND ANALYTIC TRADECRAFT":
        framework = _epistemic_stack_framework()
    framework_suffix = f"\n\n{framework}" if framework else ""
    return (
        f"{render_unit_profile_markdown(part)}\n\n"
        "This unit introduces the part's governing question, evidence artifacts, "
        "source-support spine, and capstone thread before the individual modules "
        f"begin. {source_context}\n\n"
        "Learners carry one unit capstone thread through the part: define an "
        "accountable intelligence question, bind it to source-quality constraints, "
        "produce a reviewable artifact, test the artifact against failure modes, "
        "and hand it off with enough context for another analyst or instructor "
        "to audit. The capstone remains public, synthetic, or owned-lab "
        f"throughout; its first source anchors are {source_context}\n\n"
        "This unit's deliverables are a source-canon card, claim/evidence ledger, "
        "safe-practice lab packet, failure-mode note, instructor rubric, and "
        "debrief memo. The full source-lane and evidence-package ledgers appear "
        "in the orientation and appendices; this unit introduction keeps only "
        f"the learner-facing spine for {source_context}\n\n"
        "This unit's safety gates are documented authority for the exact activity, "
        "rights review, permitted data provenance, tool allowlisting, human oversight, "
        "and evidence-bounded output. A missing or unknown gate pauses the affected "
        "activity, including processing or sharing already supplied data. A written "
        "risk exception cannot waive authority or rights. A replacement tabletop "
        "may begin only after independently permitted synthetic inputs, tools and "
        "review responsibilities are established; it does not inherit permission "
        f"from the stopped activity. Inspect the applicable source context: {source_context}\n\n"
        "Capstone thread:\n\n"
        f"{capstone_scaffold_rows()}\n\n"
        f"{part_research_brief(part)}"
        f"{framework_suffix}"
    )


def _part_chapter_rows(part: dict[str, Any], chapter_files: dict[int, str]) -> str:
    rows = ["| Module | Section reference | Source spine |", "|---|---|---|"]
    for chapter in part["chapters"]:
        chapter_slug = Path(chapter_files[chapter["number"]]).stem
        section_ref = f"[@{_label('chapter', chapter_slug)}]"
        rows.append(f"| {chapter['title']} | {section_ref} | {source_citation_spine(chapter['citations'])} |")
    return "\n".join(rows)


def _source_canon(chapter: dict[str, Any], part: dict[str, Any], source_spine: str) -> str:
    source_context = _chapter_source_context(chapter)
    source_context_inline = _chapter_source_context_inline(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    triangulation = profile_triangulation_anchors(str(part["title"]), str(chapter["title"]), chapter=chapter, surface="source-canon section")
    return "\n".join(
        [
            f"The source canon has three tiers; the local spine begins with {source_context}",
            "",
            "| Tier | What counts | How it is used |",
            "|---|---|---|",
            f"| Source guide | {source_spine} | Preserves the inherited AGEINT outline and `ageintNNN` keys. |",
            ("| Verified anchors | Official, standards, public-domain, or scholarly sources in `references-*.bib` | Supplies governance, quality, legal, safety, and technical constraints. |"),
            ("| Runtime profile | The profile matched to the current unit and current module | Selects the practice lens, method stack, failure modes, and defensive boundary for generated prose. |"),
            "",
            triangulation,
            "",
            f"Maintenance rule: Perplexity may suggest candidates for {topic_context} and {source_context_inline}, but only directly verified source URLs are encoded as citations.",
        ]
    )


def _claim_evidence_ledger(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return (
        "The claim and evidence ledger follows the canonical "
        "claim-class ladder in the shared method-and-assurance reference "
        "([@sec:method-assurance-reference]). Apply the source-spine, "
        "research-backed governance, agentic-workflow, empirical or evaluated "
        "capability, safety, and cross-module "
        "claim classes to every assertion, attaching the required "
        "evidence and clearing the matching review gate before reuse. The local "
        f"topic cluster is {topic_context}, and the source spine for these checks "
        f"begins with {source_context}"
    )


def _review_checklist(chapter: dict[str, Any], part: dict[str, Any] | None = None) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part) if part is not None else "the local topic cluster"
    triangulation = ""
    if part is not None:
        triangulation = profile_triangulation_anchors(str(part["title"]), str(chapter["title"]), chapter=chapter, surface="review-checklist section")
    return "\n".join(
        [
            f"Before marking the work complete, verify the local source spine beginning with {source_context}",
            "",
            triangulation,
            "",
            f"- The module source spine resolves to Pandoc citation keys and no raw source URLs are pasted into prose, here covering {topic_context}. {source_context}",
            "- Every research-backed claim has a directly verified source anchor or is clearly marked as source-guide context.",
            "- Agentic affordances are limited to retrieval, comparison, drafting, simulation, critique, and audit support.",
            "- The lab packet uses public, benign, owned-lab, or synthetic material only.",
            "- The artifact names assumptions, caveats, uncertainty, excluded actions, and human review points.",
            "- No Figure, Section, Equation, chapter, or appendix numbers are hard-coded outside generated labels.",
        ]
    )
