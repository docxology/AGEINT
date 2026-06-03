from __future__ import annotations

"""Build and render the AGEINT semantic manuscript manifest."""

import json
from pathlib import Path
import re
import shutil
from typing import Any

try:
    from manuscript_injection import substitute_manuscript_text
except ImportError:  # pragma: no cover - package import
    from ..manuscript_injection import substitute_manuscript_text  # type: ignore[no-redef]

try:
    from .types import (
        ManuscriptManifest,
        ManuscriptSection,
        SlugRegistry as _SlugRegistry,
        ordering_config_yaml as _ordering_config_yaml,
        section_label as _label,
        slugify as _slug,
    )
except ImportError:  # pragma: no cover - merged part module
    from manuscript_manifest.types import (  # type: ignore[no-redef]
        ManuscriptManifest,
        ManuscriptSection,
        SlugRegistry as _SlugRegistry,
        ordering_config_yaml as _ordering_config_yaml,
        section_label as _label,
        slugify as _slug,
    )

try:  # Support package and script-level imports.
    from .curriculum import Curriculum
    from .citation_workflow import source_citation_spine
    from .figures import figure_markdown, figures_for_section
    from .markdown_refs import figure_ref_list, section_ref_list
    from .unit_education import render_unit_profile_markdown
    from .rendered_reference_audit import (
        sanitize_rendered_section_title_mentions,
        section_title_rules,
    )
    from .intelligence_content import (
        accessibility_review_rows,
        adversarial_assurance_rows,
        agent_incident_response_rows,
        assessment_integrity_rows,
        chapter_key_terms,
        chapter_knowledge_check,
        chapter_learning_outcomes,
        capstone_scaffold_rows,
        chapter_practice_lens,
        chapter_practice_sequence,
        chapter_research_brief,
        chapter_source_annotations,
        chapter_textbook_primer,
        chapter_topic_lessons,
        chapter_worked_example,
        safe_topic_entries,
        anchor_references,
        data_lineage_registry_rows,
        hria_dpia_worksheet_rows,
        learner_support_rows,
        model_dataset_card_rows,
        part_research_brief,
        practice_lens_for_titles,
        procurement_oversight_rows,
        profile_for_titles,
        question_bank_rows,
        release_change_control_rows,
        remediation_backlog_rows,
        retention_audit_rows,
        risk_exception_rows,
        role_competency_rows,
        safe_curriculum_treatment,
        safe_pattern_treatment,
        safe_substitution_rows,
        source_lane_rows,
        subsection_practice_rows,
        transparency_notice_rows,
    )
    from .manuscript_templates import DEFAULT_TEMPLATES
    from .manuscript_variables import appendix_rows
except ImportError:  # pragma: no cover - exercised by thin CLI wrappers
    from curriculum import Curriculum  # type: ignore[no-redef]
    from citation_workflow import source_citation_spine  # type: ignore[no-redef]
    from figures import figure_markdown, figures_for_section  # type: ignore[no-redef]
    from markdown_refs import figure_ref_list, section_ref_list  # type: ignore[no-redef]
    from unit_education import render_unit_profile_markdown  # type: ignore[no-redef]
    from rendered_reference_audit import (  # type: ignore[no-redef]
        sanitize_rendered_section_title_mentions,
        section_title_rules,
    )
    from intelligence_content import (  # type: ignore[no-redef]
        accessibility_review_rows,
        adversarial_assurance_rows,
        agent_incident_response_rows,
        assessment_integrity_rows,
        chapter_key_terms,
        chapter_knowledge_check,
        chapter_learning_outcomes,
        capstone_scaffold_rows,
        chapter_practice_lens,
        chapter_practice_sequence,
        chapter_research_brief,
        chapter_source_annotations,
        chapter_textbook_primer,
        chapter_topic_lessons,
        chapter_worked_example,
        safe_topic_entries,
        anchor_references,
        data_lineage_registry_rows,
        hria_dpia_worksheet_rows,
        learner_support_rows,
        model_dataset_card_rows,
        part_research_brief,
        practice_lens_for_titles,
        procurement_oversight_rows,
        profile_for_titles,
        question_bank_rows,
        release_change_control_rows,
        remediation_backlog_rows,
        retention_audit_rows,
        risk_exception_rows,
        role_competency_rows,
        safe_curriculum_treatment,
        safe_pattern_treatment,
        safe_substitution_rows,
        source_lane_rows,
        subsection_practice_rows,
        transparency_notice_rows,
    )
    from manuscript_templates import DEFAULT_TEMPLATES  # type: ignore[no-redef]
    from manuscript_variables import (  # type: ignore[no-redef]
        appendix_rows,
    )

def _citation_context(citation_numbers: list[int], *, limit: int = 2) -> str:
    """Return a compact, body-safe source-spine phrase."""

    selected = list(citation_numbers[:limit])
    if not selected:
        return "the surrounding verified source spine"
    return source_citation_spine(selected)

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

def _chapter_topic_context(chapter: dict[str, Any], part: dict[str, Any], *, limit: int = 2) -> str:
    """Return a compact topic cluster for body prose."""

    topics = [entry.display_title for entry in safe_topic_entries(chapter, part)[:limit]]
    if not topics:
        return "the local source-topic cluster"
    return "; ".join(topics)

def _cognitive_attack_framework() -> str:
    return (
        "## How adversaries target cognition\n\n"
        "This unit is organized around the NATO/INSS reconception of cognitive warfare, summarized for "
        "the unit in [@fig:ageint-cognitive-attack-layers], which distinguishes three layers of "
        "engagement by their target. The biological layer targets cognitive capacity itself through "
        "neuroscience-informed pressure on the nervous system, with AI optimizing delivery timing and "
        "channel selection. The psychological layer targets cognitive interpretation, manipulating "
        "individual cognition and exploiting biases at scale, with AI tailoring influence to "
        "vulnerability profiles. The social layer targets cognitive cohesion, fracturing shared "
        "narratives and weaponizing identity to manufacture epistemic chaos, with AI coordinating "
        "synthetic influence across platforms [@scholarly_ccdcoe_cognitive_warfare_reconception]. "
        "Holding the three layers apart matters because each demands a different defense -- resilience "
        "of attention, inoculation against manipulation, and protection of shared sense-making -- and a "
        "defender who conflates them will mismatch the countermeasure to the attack. Every exercise in "
        "this unit stays defensive, synthetic, and non-operational: the taxonomy is taught to build "
        "inoculation and detection, never to script influence "
        "[@official_darpa_intrinsic_cognitive_security]."
    )


def _epistemic_stack_framework() -> str:
    return (
        "## The unified epistemic coherence stack\n\n"
        "This unit synthesizes the book's defensive techniques into one five-layer architecture for "
        "maintaining epistemic coherence, shown for the unit in [@fig:ageint-unified-epistemic-stack]. "
        "The base is a technical substrate -- formal verification in the spirit of intrinsic cognitive "
        "security, prompt-infection defense, sandboxing and worktree isolation, and provenance signals "
        "such as SynthID and C2PA. Above it sits operational security -- MAESTRO threat modeling, CDR "
        "degradation monitoring, zero-trust identity, and circuit breakers. Above that is structured "
        "reasoning and tradecraft -- analysis of competing hypotheses, pre-mortem red teaming, and "
        "key-assumptions auditing, now executable as AI-augmented structured analytic techniques at "
        "scale. The fourth layer is epistemic integrity -- verifier agents and intent-alignment "
        "monitoring that protect the trustworthiness of what the system believes. The top layer is "
        "institutional governance -- analytic standards, red-team programs, and error-budget "
        "governance. The load-bearing claim is that each layer is necessary but insufficient alone, and "
        "the layers are mutually reinforcing: a technical fix without governance, or tradecraft without "
        "integrity checks, leaves an exploitable seam [@scholarly_deepmind_epistemic_agent_trust]; "
        "[@official_darpa_intrinsic_cognitive_security].\n\n"
        "## From reliability theory to AI governance\n\n"
        "The governance layer is not invented from scratch; it borrows from High-Reliability "
        "Organization theory. As the crosswalk in [@fig:ageint-hro-governance-crosswalk] shows, Weick "
        "and Sutcliffe's five HRO principles map directly onto observable AI-agent controls: "
        "preoccupation with failure becomes safety-SLI monitoring and drift detection; reluctance to "
        "simplify becomes multi-hypothesis behavioral analysis; sensitivity to operations becomes "
        "real-time tool-invocation auditing and context-window analysis; commitment to resilience "
        "becomes circuit breakers, chaos engineering, and progressive rollout behind "
        "service-level-objective gates; and deference to expertise becomes human-in-the-loop authority "
        "for high-stakes actions under least privilege. The crosswalk turns an organizational "
        "philosophy into a checklist of testable mechanisms, which is exactly how this unit asks "
        "learners to use it [@scholarly_mandel_tetlock_judgment_correctives]; "
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
        f"begin. The source path begins with {source_context}\n\n"
        "Learners carry one unit capstone thread through the part: define an "
        "authorized intelligence question, bind it to source-quality constraints, "
        "produce a reviewable artifact, test the artifact against failure modes, "
        "and hand it off with enough context for another analyst or instructor "
        "to audit. The capstone remains public, synthetic, or owned-lab "
        f"throughout; its first source anchors are {source_context}\n\n"
        "This unit's deliverables are a source-canon card, claim/evidence ledger, "
        "safe-practice lab packet, failure-mode note, instructor rubric, and "
        "debrief memo. The full source-lane and evidence-package ledgers appear "
        "in the orientation and appendices; this unit introduction keeps only "
        f"the learner-facing spine for {source_context}\n\n"
        "This unit's safety gates are scope authorization, rights review, data "
        "provenance, tool allowlisting, human oversight, rollback, and "
        "non-operational output. A missing gate turns the activity into a "
        "tabletop, audit, or written governance exercise until the gate is "
        f"restored against {source_context}\n\n"
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
        rows.append(
            f"| {chapter['title']} | {section_ref} | "
            f"{source_citation_spine(chapter['citations'])} |"
        )
    return "\n".join(rows)

def _source_canon(chapter: dict[str, Any], part: dict[str, Any], source_spine: str) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return "\n".join(
        [
            f"The source canon for this module has three tiers; the local spine begins with {source_context}",
            "",
            "| Tier | What counts | How it is used |",
            "|---|---|---|",
            f"| Source guide | {source_spine} | Preserves the inherited AGEINT outline and `ageintNNN` keys. |",
            (
                "| Verified anchors | Official, standards, public-domain, or scholarly "
                "sources in `references-*.bib` | Supplies governance, quality, "
                "legal, safety, and technical constraints. |"
            ),
            (
                "| Runtime profile | The profile matched to "
                "the current unit and current module | "
                "Selects the practice lens, method stack, failure modes, and "
                "defensive boundary for generated prose. |"
            ),
            "",
            f"Maintenance rule for this module: Perplexity may suggest candidates for {topic_context} and {source_context}, "
            "but only directly verified source URLs are encoded as citations.",
        ]
    )

def _claim_evidence_ledger(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return (
        "The claim and evidence ledger for this module follows the canonical "
        "claim-class ladder in the shared method-and-assurance reference "
        "([@sec:method-assurance-reference]). Apply the source-spine, "
        "research-backed governance, agentic-workflow, safety, and cross-module "
        "claim classes to every assertion in this module, attaching the required "
        "evidence and clearing the matching review gate before reuse. The local "
        f"topic cluster is {topic_context}, and the source spine for these checks "
        f"begins with {source_context}"
    )

def _safe_practice_lab(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            "Build a safe lab packet for this module using public, benign, "
            f"owned-lab, or synthetic material only; source checks begin with {source_context}",
            "",
            "| Lab step | Required artifact | Safety gate |",
            "|---|---|---|",
            (
                "| Scope | One-sentence authorized learning objective plus excluded "
                "actions | Instructor signs off before any tool or dataset is named. |"
            ),
            (
                "| Evidence | Source list with provenance, timestamps, and caveats | "
                "No credentials, private data, live targets, or sensitive records. |"
            ),
            (
                "| Agent support | Prompt, tool allowlist, budget, logging plan, and "
                "stop condition | Agent may summarize, compare, retrieve, or audit; "
                "it may not act externally. |"
            ),
            (
                "| Output | Map, memo, matrix, rubric, or tabletop packet | Output "
                "must preserve uncertainty and separate observation from judgment. |"
            ),
            (
                "| Debrief | What changed, what remains unknown, and what would require "
                "human review | No deployment or operational follow-through. |"
            ),
        ]
    )

def _failure_mode_drill(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            "Use the drill to stress-test this module before treating the module "
            f"artifact as complete; the drill starts from {source_context}",
            "",
            "| Failure mode | Drill question | Recovery move |",
            "|---|---|---|",
            (
                "| Source laundering | Which claim lost its original source, "
                "timestamp, or caveat? | Reattach the source descriptor or remove "
                "the claim. |"
            ),
            (
                "| Automation bias | Which agent output looks authoritative without "
                "independent support? | Add competing explanations and human review. |"
            ),
            (
                "| Boundary drift | Which step could become collection, targeting, "
                "exploitation, influence, or cyber-physical action? | Replace it "
                "with a tabletop, audit, or governance exercise. |"
            ),
            (
                "| Overconfident synthesis | Which uncertainty did the prose smooth "
                "over? | Restore confidence language, alternatives, and unresolved "
                "questions. |"
            ),
            (
                "| Handoff loss | What would the next reviewer be unable to reproduce? | "
                "Add inputs, transformation notes, output schema, and review owner. |"
            ),
        ]
    )

def _instructor_artifact(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Instructors should collect a compact artifact bundle for this module and {source_context}",
            "",
            "| Artifact | Minimum contents |",
            "|---|---|",
            "| Source-canon card | Guide citation spine, verified anchors, and update date. |",
            "| Claim ledger | Claims, evidence, uncertainty, and reviewer initials. |",
            "| Lab packet | Synthetic dataset description, tool allowlist, and stop conditions. |",
            "| Safety note | Prohibited actions, safe substitutions, and escalation triggers. |",
            "| Assessment note | Rubric scores, feedback, and required revision before reuse. |",
        ]
    )

def _review_checklist(chapter: dict[str, Any], part: dict[str, Any] | None = None) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part) if part is not None else "the local topic cluster"
    return "\n".join(
        [
            f"Before marking this module complete, verify the local source spine beginning with {source_context}",
            "",
            f"- The module source spine resolves to Pandoc citation keys and no raw source URLs are pasted into prose; source context: {source_context}; topic focus: {topic_context}",
            "- Every research-backed claim has a directly verified source anchor or is clearly marked as source-guide context.",
            "- Agentic affordances are limited to retrieval, comparison, drafting, simulation, critique, and audit support.",
            "- The lab packet uses public, benign, owned-lab, or synthetic material only.",
            "- The artifact names assumptions, caveats, uncertainty, excluded actions, and human review points.",
            "- No Figure, Section, Equation, chapter, or appendix numbers are hard-coded outside generated labels.",
        ]
    )

def _authority_accountability_model(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return "\n".join(
        [
            f"Use this accountability model before applying this module in any exercise; topic focus: {topic_context}.",
            "",
            "| Accountability layer | Required decision | Evidence retained |",

            "|---|---|---|",
            (
                f"| Sponsor | Why this unit needs the module now | "
                f"authorized learning objective, excluded actions, and source context {source_context} |"
            ),
            "| Instructor | Which data, tools, and roles are allowed | signed scope card and stop condition |",
            (
                "| Human reviewer | Which claims, recommendations, and agent outputs need "
                "approval | review initials, caveats, and revision notes |"
            ),
            (
                "| Learner | Which assumptions and uncertainties remain | claim ledger, "
                "confidence statement, and handoff memo |"
            ),
            (
                "| System steward | Which logs, prompts, sources, and outputs are retained | "
                "retention rule, access boundary, and deletion or refresh date |"
            ),
        ]
    )
