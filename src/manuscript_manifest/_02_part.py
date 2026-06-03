from __future__ import annotations

from typing import Any

from curriculum import PATTERN_REGISTRY_CHAPTER_NUMBER
from intelligence_content import (
    accessibility_review_rows,
    adversarial_assurance_rows,
    agent_incident_response_rows,
    assessment_integrity_rows,
    data_lineage_registry_rows,
    hria_dpia_worksheet_rows,
    learner_support_rows,
    model_dataset_card_rows,
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
    transparency_notice_rows,
)

from ._01_part import _chapter_source_context, _chapter_topic_context

def _data_provenance_model(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            "Treat this module as a provenance-first workflow. Data may enter "
            f"only through public, benign, owned-lab, or synthetic channels tied to {source_context}",
            "",
            "| Data object | Provenance field | Quality test |",
            "|---|---|---|",
            "| Source-guide citation | `ageintNNN`, title, URL, and source identity lock status | key and URL match the lock or append-only v2 reference list |",
            "| Verified anchor | lane, tier, checked-as-of date, verification method, and claim scope | official or standards source resolves directly |",
            "| Dataset or example | origin, license, sensitivity class, transformation note, and retention date | instructor can reproduce the artifact without private or live data |",
            "| Agent output | prompt, tool allowlist, model context, budget, and reviewer | output is separated from evidence and cannot act externally |",
            "| Handoff record | relation to the current unit and module | next reviewer can audit assumptions, transformations, and uncertainty |",
        ]
    )

def _evaluation_assurance_protocol(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            "Evaluate this module with a short assurance protocol before any "
            f"student artifact is accepted; source checks begin with {source_context}",
            "",
            "| Assurance step | Passing evidence | Failing condition |",
            "|---|---|---|",
            "| Source verification | every material claim cites a guide reference or verified anchor | unverified source, broken URL, or missing checked date |",
            "| Rights and safety | privacy, IP, labour, education, and human-rights impacts are named where relevant | rights impact is skipped or minimized |",
            "| Agent control | tools are allowlisted, logged, revocable, and limited to benign analysis | agent can collect, contact, modify, or deploy outside the lab |",
            "| Robustness | alternatives, uncertainty, confidence, and failure modes are explicit | single-path reasoning or unsupported confidence |",
            "| Reproducibility | another reviewer can rebuild the map, memo, matrix, or rubric | missing inputs, hidden transformations, or vague prompt history |",
        ]
    )

def _compliance_rights_map(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            "The compliance and rights map for this module converts source lanes "
            f"into review questions anchored by {source_context}",
            "",
            "| Source lane | Review question | Minimum artifact |",
            "|---|---|---|",
            "| AI conformity/compliance | Does the workflow have risk classification, impact assessment, and accountability evidence? | conformity note and impact register |",
            "| Education and assessment | Does the learning design preserve assessment integrity and instructor oversight? | rubric, allowed-use note, and feedback plan |",
            "| Public-sector agentic AI | Would a public institution know the authority, service impact, and audit owner? | authority map and public-value statement |",
            "| Cross-border data/data spaces | Are data access, reuse, metadata, and sharing limits explicit? | data provenance card and access rule |",
            "| Human-rights governance | Are privacy, expression, equality, redress, and harm risks considered? | rights impact note and escalation path |",
            "| Agent interoperability standards | Are APIs, credentials, tool descriptions, and errors contract-bound? | interface contract and revocation rule |",
            "| Workforce governance | Are labour impacts, skill needs, and human role changes visible? | workforce impact note and training plan |",
            "| Model/data provenance | Can sources, transformations, datasets, and outputs be traced? | claim ledger and provenance chain |",
        ]
    )

def _safe_substitution_patterns(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use the v2 safe-substitution table whenever this module inherits "
            "a risky motif from the source guide. The source identity remains "
            f"visible through {source_context}, but the classroom treatment becomes bounded and non-operational.",
            "",
            safe_substitution_rows(),
        ]
    )

def _capstone_deliverable(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return "\n".join(
        [
            "The capstone deliverable for this module is a reviewable packet that "
            "plugs into the broader unit thread. Run it through the canonical "
            "phase, artifact, and review-gate ladder in the Method & Assurance "
            f"Reference ([@sec:method-assurance-reference]); the local topic "
            f"cluster is {topic_context}.",
            "",
            "Minimum module submission: one-page analytic memo, source-lane map, "
            "claim ledger, safe-lab packet, rubric self-assessment, and debrief "
            "note. The packet must name what is excluded, who may approve reuse, "
            f"and what would trigger a source refresh for {topic_context} and {source_context}",
        ]
    )

def _instructor_facilitation_notes(chapter: dict[str, Any], part: dict[str, Any] | None = None) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part) if part is not None else "the local topic cluster"
    return "\n".join(
        [
            f"Facilitate this module as a bounded studio around {topic_context}, not as a lecture-only module.",
            "",
            f"- Start with the authority card and excluded-action list before showing examples from {topic_context} and {source_context}",
            "- Assign one learner to maintain the claim ledger and one learner to challenge source quality.",
            "- Keep agent prompts visible enough for review and separate from final judgment.",
            "- Pause any activity that drifts toward live systems, real people, sensitive data, or external action.",
            "- End with a debrief that separates evidence learned, uncertainty preserved, rights impact, and next refresh owner.",
        ]
    )

def _refresh_triggers(chapter: dict[str, Any], part: dict[str, Any] | None = None) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = (
        _chapter_topic_context(chapter, part) if part is not None else "the local topic cluster"
    )
    return (
        "Refresh this module against the canonical trigger-and-action table in "
        "the Method & Assurance Reference ([@sec:method-assurance-reference]). "
        "When a source-guide reference, official standard, AI or public-sector "
        "policy, interface specification, safety audit, or instructor debrief "
        f"signal appears, take the matching required action before reuse for "
        f"{topic_context}. The local signals for this module begin with {source_context}"
    )

def _accessibility_udl_review(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Review this module for accessibility and Universal Design for Learning before reuse; source context: {source_context}",
            "",
            accessibility_review_rows(),
            "",
            (
                "Minimum gate: no learner-facing artifact should depend on a single modality, "
                "unstated accommodation, inaccessible figure, unlabeled table, or hidden tool assumption."
            ),
        ]
    )

def _procurement_vendor_oversight(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Treat any tool, dataset, platform, or service used in this module as a governed vendor input; source context: {source_context}",
            "",
            procurement_oversight_rows(),
            "",
            (
                "Minimum gate: a classroom tool must be revocable, auditable, accessible, "
                "privacy-reviewed, and replaceable with a synthetic or instructor-provided substitute."
            ),
        ]
    )

def _hria_dpia_worksheet(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use this HRIA/DPIA worksheet when this module touches people, public services, education, or data reuse; source context: {source_context}",
            "",
            hria_dpia_worksheet_rows(),
            "",
            (
                "Minimum gate: if a scenario cannot identify affected groups, safeguards, "
                "review owner, and residual risk, it stays at the discussion stage."
            ),
        ]
    )

def _data_lineage_registry(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The data lineage registry for this module keeps claims, examples, prompts, and outputs traceable; source context: {source_context}",
            "",
            data_lineage_registry_rows(),
            "",
            (
                "Minimum gate: every retained artifact names source identity, transformation, "
                "reviewer, sensitivity status, retention rule, and refresh owner."
            ),
        ]
    )

def _assessment_integrity_protocol(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Assessment integrity for this module depends on visible, bounded, and reviewable AI assistance; source context: {source_context}",
            "",
            assessment_integrity_rows(),
            "",
            (
                "Minimum gate: learners may use agents only when tool use is declared, "
                "evidence is retained, independent reasoning is visible, and grading criteria remain human-reviewed."
            ),
        ]
    )

def _agent_incident_response_drill(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Run an agent incident response drill for this module using synthetic tickets and bounded logs; source context: {source_context}",
            "",
            agent_incident_response_rows(),
            "",
            (
                "Minimum gate: the drill rehearses pause, revoke, preserve, review, "
                "recover, and debrief actions without touching live services or private data."
            ),
        ]
    )

def _role_based_competency_map(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The role-based competency map for this module clarifies who must prove which skill; source context: {source_context}",
            "",
            role_competency_rows(),
            "",
            (
                "Minimum gate: no artifact is accepted unless learner, instructor, source "
                "steward, assurance reviewer, and rights/procurement responsibilities are separable."
            ),
        ]
    )

def _adversarial_assurance_cycle(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use the adversarial assurance cycle to stress-test this module before classroom reuse; source context: {source_context}",
            "",
            adversarial_assurance_rows(),
            "",
            (
                "Minimum gate: every challenge produces an owner, a remediation path, "
                "a retest result, and a source or safety refresh trigger."
            ),
        ]
    )

def _model_dataset_documentation_card(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use a model and dataset documentation card whenever this module relies on a model, dataset, example corpus, or synthetic fixture; source context: {source_context}",
            "",
            model_dataset_card_rows(),
            "",
            (
                "Minimum gate: model and data claims must name intended use, excluded use, "
                "composition limits, evaluation evidence, lifecycle owner, and refresh trigger."
            ),
        ]
    )

def _transparency_communication_notice(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The transparency notice for this module converts internal evidence into a plain-language accountability record; source context: {source_context}",
            "",
            transparency_notice_rows(),
            "",
            (
                "Minimum gate: a learner, reviewer, or affected public audience can see purpose, "
                "authority, data summary, safeguards, human review, contact point, and publication limits."
            ),
        ]
    )

def _records_retention_audit_trail(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The records-retention and audit trail for this module preserves enough evidence to review without retaining unnecessary sensitive material; source context: {source_context}",
            "",
            retention_audit_rows(),
            "",
            (
                "Minimum gate: prompts, sources, decisions, exceptions, incidents, outputs, "
                "and remediation records have owners, retention rules, and deletion or refresh conditions."
            ),
        ]
    )

def _release_change_control_gate(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Before a module artifact is reused, pass it through a release and change-control gate; source context: {source_context}",
            "",
            release_change_control_rows(),
            "",
            (
                "Minimum gate: scope, rights, security, version, rollback, monitoring, "
                "incident threshold, and post-release review are all visible."
            ),
        ]
    )

def _risk_exception_acceptance_memo(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"If this module cannot satisfy a gate, use a risk exception memo instead of silently lowering the standard; source context: {source_context}",
            "",
            risk_exception_rows(),
            "",
            (
                "Minimum gate: exceptions are narrow, time-bound, evidence-backed, "
                "rights-reviewed, and closed by retest rather than left as permanent workarounds."
            ),
        ]
    )

def _learner_support_accommodation_plan(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The learner support and accommodation plan for this module keeps access, cognitive load, and assessment fairness explicit; source context: {source_context}",
            "",
            learner_support_rows(),
            "",
            (
                "Minimum gate: each learner-facing artifact has an access path, alternative means, "
                "allowed-tool statement, feedback path, and remediation owner."
            ),
        ]
    )

def _instructor_question_bank(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use these instructor question prompts to deepen this module during facilitation and review; source context: {source_context}",
            "",
            question_bank_rows(),
            "",
            (
                "Minimum gate: every question must produce a revision, retained evidence, "
                "or an explicit decision that no change is required."
            ),
        ]
    )

def _remediation_backlog(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The remediation backlog for this module turns review findings into accountable follow-through; source context: {source_context}",
            "",
            remediation_backlog_rows(),
            "",
            (
                "Minimum gate: backlog items have a trigger, owner, due date, closure evidence, "
                "and retest result before the artifact is reused."
            ),
        ]
    )

def _reader_section_title(source_title: str, part_title: str = "", chapter_title: str = "") -> str:
    """Normalize source-guide pseudo-headings into reader-facing titles."""
    title = source_title.strip()
    lower = title.lower()
    if (
        lower.startswith("pattern ")
        or lower.startswith("safe methods:")
        or lower.startswith("safe defensive")
        or lower.startswith("safe architecture")
    ):
        return title
    if lower.startswith("v2 source-lane extension:"):
        return "Source-lane evidence, public registers, and claim-ledger studio"
    if lower.startswith("deep expansion:"):
        return "Bounded autonomy, procurement, incident-response, and assurance studio"
    if lower.startswith("evidence-package expansion:"):
        return "Model-card, recoverability, retention, and learner-support evidence package"
    if lower.startswith("v2 ageint-depth extension:"):
        return "AGEINT pattern registry, agent identity, and interface-contract studio"
    return safe_curriculum_treatment(title, part_title, chapter_title)

def _reader_provenance_title(source_title: str) -> str:
    """Keep provenance useful without leaking scaffold wording into prose."""
    from prose_policy import reader_source_title

    return reader_source_title(source_title)

def _runtime_section_map(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render source-guide sections as polished runtime/provenance rows."""
    sections = chapter.get("sections", [])
    if not sections:
        lens = practice_lens_for_titles(str(part["title"]), str(chapter["title"]), chapter=chapter)
        return "\n".join(
            [
                "| Rendered title | Source loci | Source provenance | Practice lens | Evidence artifact | Safety check |",
                "|---|---|---|---|---|---|",
                (
                    f"| Module source spine | Module source spine | Parsed chapter title and citation spine | "
                    f"{lens.title} | {lens.evidence_artifact} | {lens.safety_check} |"
                ),
            ]
        )

    rows = [
        "| Rendered title | Source loci | Source provenance | Practice lens | Evidence artifact | Safety check |",
        "|---|---|---|---|---|---|",
    ]
    safe_patterns = chapter.get("number") == PATTERN_REGISTRY_CHAPTER_NUMBER
    active_pattern_number: int | None = None
    for section in sections:
        source_title = str(section.get("title", "module section"))
        source_title_for_provenance = _reader_provenance_title(source_title)
        source_number = str(section.get("number", "")).strip()
        working_title = source_title
        provenance = f"{source_number} {source_title_for_provenance}".strip()

        if safe_patterns:
            working_title, active_pattern_number = safe_pattern_treatment(
                working_title,
                active_pattern_number,
            )
            provenance = "Source identity preserved in pattern registry with safe classroom treatment"

        rendered_title = _reader_section_title(working_title, str(part["title"]), str(chapter["title"]))
        source_locus = str(section.get("number") or "module section")
        if not safe_patterns and rendered_title != source_title:
            provenance = (
                f"{source_locus} source title transformed into safe curriculum treatment; "
                f"original: {source_title_for_provenance}"
            )
        lens = practice_lens_for_titles(str(part["title"]), rendered_title)
        rows.append(
            f"| {rendered_title} | {source_locus} | {provenance} | {lens.title} | "
            f"{lens.evidence_artifact} | {lens.safety_check} |"
        )
    return "\n".join(rows)

def _module_thesis(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    profile = profile_for_titles(str(part["title"]), title, chapter=chapter)
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return "\n".join(
        [
            (
                f"This module sits in the **{profile.title}** research lane and "
                f"uses the **{lens.title}** practice lens for {topic_context}."
            ),
            "",
            (
                "The teaching claim is concrete: intelligence work becomes "
                "reviewable when authority, evidence, provenance, accessibility, "
                f"rights, assurance, and refresh duties are visible in the artifact. Source context: {source_context}"
            ),
            "",
            (
                f"The chapter artifact is a **{lens.evidence_artifact}** plus a "
                "claim ledger, safe-lab packet, and reproducible handoff."
            ),
        ]
    )
