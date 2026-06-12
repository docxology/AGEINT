"""Canonical, chapter-independent method and assurance tables.

These emitters hold the single source of truth for the shared method,
governance, and assurance tables that every module previously restamped. The
new ``Method & Assurance Reference`` front section
(``sec:method-assurance-reference``) renders each table exactly once, and the
per-chapter emitters point readers here with a cross-reference paragraph
instead of repeating the table body.
"""

from __future__ import annotations


def canonical_claim_ledger_rows() -> str:
    """Chapter-independent claim/evidence ledger (was _01_part._claim_evidence_ledger)."""
    return "\n".join(
        [
            "| Claim class | Evidence required | Review gate |",
            "|---|---|---|",
            (
                "| Source-spine claim | Parsed module title, module section map, and "
                "curriculum citation spine | Confirm the generated text does not invent "
                "counts, paths, or labels. |"
            ),
            (
                "| Research-backed governance claim | Direct official, standards, "
                "public-domain, or scholarly anchor in `references-*.bib` | "
                "Confirm the anchor has verification metadata and a stable URL. |"
            ),
            (
                "| Agentic workflow claim | Tool boundary, authority contract, human "
                "review point, and rollback condition | Confirm the workflow remains "
                "educational, logged, reversible, and non-operational. |"
            ),
            (
                "| Technical or theoretical claim | Direct domain source for the "
                "formal expression, protocol, architecture, or theory, with analogy limits "
                "spelled out | Confirm the prose does not cite governance guidance "
                "as proof of technical performance or autonomous agency. |"
            ),
            (
                "| Empirical or evaluated capability claim | Direct benchmark, field "
                "evaluation, user study, incident evidence, or scholarly empirical "
                "source with context and subgroup caveats | Confirm the claim is "
                "not merely inferred from the AGEINT curriculum architecture. |"
            ),
            (
                "| Source-construction claim | Search surface, query or prompt, "
                "retrieval date, inclusion and exclusion rule, deduplication note, "
                "source tier, and direct URL | Confirm discovery sources are not "
                "treated as final citations unless directly verified. |"
            ),
            (
                "| Safety claim | Explicit prohibition plus safe alternative | Confirm "
                "the module blocks live targeting, exploitation, covert collection, "
                "manipulation, and unsafe cyber-physical action. |"
            ),
            (
                "| Cross-module claim | Link to the current unit and adjacent curriculum "
                "modules | Confirm the handoff names inputs, outputs, uncertainty, and "
                "next-review owner. |"
            ),
        ]
    )


def canonical_competency_rubric_rows() -> str:
    """Chapter-independent competency rubric (was _03_part._assessment_and_capstone_pathway)."""
    return "\n".join(
        [
            "| Competency | Evidence of mastery |",
            "|---|---|",
            "| Conceptual command | Terms are defined precisely and linked to the source spine. |",
            "| Analytic rigor | Assumptions, uncertainty, alternatives, and confidence are explicit. |",
            "| Agentic design | Human oversight, tool boundaries, logging, and rollback are specified. |",
            "| Governance and rights | Authority, procurement, privacy, accessibility, retention, and redress evidence are visible. |",
            "| Safety posture | Exercises remain authorized, synthetic, defensive, lawful, and non-operational. |",
        ]
    )


def canonical_refresh_trigger_rows() -> str:
    """Chapter-independent refresh triggers (was _02_part._refresh_triggers)."""
    return "\n".join(
        [
            "| Trigger | Required action |",
            "|---|---|",
            "| Source guide reference changes | preserve existing `ageintNNN` identities and append new references only after the locked range |",
            "| Official or standards source updates | update source-lane metadata, checked date, and bibliography note |",
            "| AI law, public-sector policy, education guidance, or rights guidance changes | rerun the compliance and rights map |",
            "| API, protocol, data-space, or provenance specification changes | rerun interface and data-provenance checks |",
            "| Safety audit finds operational wording | replace the treatment with tabletop, audit, governance, or synthetic-data framing |",
            "| Instructor debrief finds unreproducible evidence | rebuild the source canon and claim ledger before reuse |",
        ]
    )


def canonical_mastery_rows() -> str:
    """Chapter-independent answer-quality rubric (was knowledge-check 'Answer quality rubric')."""
    return "\n".join(
        [
            "| Level | Evidence in the answer |",
            "|---|---|",
            "| Strong | Uses source evidence, distinguishes observation from judgment, names uncertainty, and states the safe boundary. |",
            "| Adequate | Defines the concept and names a relevant artifact, but leaves one caveat or review owner vague. |",
            "| Revise | Gives a memorized definition without source evidence, uncertainty, or a safe transfer task. |",
        ]
    )


def canonical_safety_boundary() -> str:
    """The single canonical default safety-boundary paragraph (non-pattern chapters)."""
    return (
        "Keep all practice authorized, synthetic, defensive, logged, reversible, and "
        "non-operational. Do not convert any module into live targeting, evasion, "
        "exploitation, covert collection, manipulation, or unsafe cyber-physical "
        "action. Where a module inherits a risky source motif, treat it as a "
        "tabletop, audit, provenance, or governance exercise."
    )
