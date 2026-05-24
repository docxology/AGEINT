from __future__ import annotations

def _import_prior_parts(*module_names: str) -> None:
    import importlib

    for module_name in module_names:
        mod = importlib.import_module(f".{module_name}", __package__)
        globals().update({k: v for k, v in vars(mod).items() if not k.startswith("__")})


_import_prior_parts("_01_part")




def _data_provenance_model(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"Treat **{title}** as a provenance-first workflow. Data may enter "
            "only through public, benign, owned-lab, or synthetic channels.",
            "",
            "| Data object | Provenance field | Quality test |",
            "|---|---|---|",
            "| Source-guide citation | `ageintNNN`, title, URL, and source identity lock status | key and URL match the lock or append-only v2 reference list |",
            "| Verified anchor | lane, tier, checked-as-of date, verification method, and claim scope | official or standards source resolves directly |",
            "| Dataset or example | origin, license, sensitivity class, transformation note, and retention date | instructor can reproduce the artifact without private or live data |",
            "| Agent output | prompt, tool allowlist, model context, budget, and reviewer | output is separated from evidence and cannot act externally |",
            f"| Handoff record | relation to **{part['title']}** and **{title}** | next reviewer can audit assumptions, transformations, and uncertainty |",
        ]
    )


def _evaluation_assurance_protocol(chapter: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"Evaluate **{title}** with a short assurance protocol before any "
            "student artifact is accepted.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"The compliance and rights map for **{title}** converts source lanes "
            "into review questions:",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Use the v2 safe-substitution table whenever **{title}** inherits "
            "a risky motif from the source guide. The source identity remains "
            "visible, but the classroom treatment becomes bounded and non-operational.",
            "",
            safe_substitution_rows(),
        ]
    )


def _capstone_deliverable(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"The capstone deliverable for **{title}** is a reviewable packet "
            f"that can plug into the broader **{part['title']}** thread.",
            "",
            capstone_scaffold_rows(),
            "",
            f"Minimum **{title}** submission: one-page analytic memo, source-lane "
            "map, claim ledger, safe-lab packet, rubric self-assessment, and "
            "debrief note. The packet must name what is excluded, who may "
            "approve reuse, and what would trigger a source refresh.",
        ]
    )


def _instructor_facilitation_notes(chapter: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"Facilitate **{title}** as a bounded studio rather than a lecture-only module.",
            "",
            f"- Start **{title}** with the authority card and excluded-action list before showing examples.",
            "- Assign one learner to maintain the claim ledger and one learner to challenge source quality.",
            "- Keep agent prompts visible enough for review and separate from final judgment.",
            "- Pause any activity that drifts toward live systems, real people, sensitive data, or external action.",
            "- End with a debrief that separates evidence learned, uncertainty preserved, rights impact, and next refresh owner.",
        ]
    )


def _refresh_triggers(chapter: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"Refresh **{title}** when one of these signals appears:",
            "",
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


def _accessibility_udl_review(chapter: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"Review **{title}** for accessibility and Universal Design for Learning before reuse.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Treat any tool, dataset, platform, or service used in **{title}** as a governed vendor input.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Use this HRIA/DPIA worksheet when **{title}** touches people, public services, education, or data reuse.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"The data lineage registry for **{title}** keeps claims, examples, prompts, and outputs traceable.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Assessment integrity for **{title}** depends on visible, bounded, and reviewable AI assistance.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Run an agent incident response drill for **{title}** using synthetic tickets and bounded logs.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"The role-based competency map for **{title}** clarifies who must prove which skill.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Use the adversarial assurance cycle to stress-test **{title}** before classroom reuse.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Use a model and dataset documentation card whenever **{title}** relies on a model, dataset, example corpus, or synthetic fixture.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"The transparency notice for **{title}** converts internal evidence into a plain-language accountability record.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"The records-retention and audit trail for **{title}** preserves enough evidence to review without retaining unnecessary sensitive material.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Before a **{title}** artifact is reused, pass it through a release and change-control gate.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"If **{title}** cannot satisfy a gate, use a risk exception memo instead of silently lowering the standard.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"The learner support and accommodation plan for **{title}** keeps access, cognitive load, and assessment fairness explicit.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Use these instructor question prompts to deepen **{title}** during facilitation and review.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"The remediation backlog for **{title}** turns review findings into accountable follow-through.",
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
    return (
        source_title.replace("Scaffolding", "Documentation")
        .replace("scaffolding", "documentation")
        .replace("Scaffolds", "Workflows")
        .replace("scaffolds", "workflows")
        .replace("Scaffold", "Workflow")
        .replace("scaffold", "workflow")
    )


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
    safe_patterns = chapter.get("number") == 32
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
    return "\n".join(
        [
            (
                f"**{title}** sits in the **{profile.title}** research lane and "
                f"uses the **{lens.title}** practice lens."
            ),
            "",
            (
                "The teaching claim is concrete: intelligence work becomes "
                "reviewable when authority, evidence, provenance, accessibility, "
                "rights, assurance, and refresh duties are visible in the artifact."
            ),
            "",
            (
                f"The chapter artifact is a **{lens.evidence_artifact}** plus a "
                "claim ledger, safe-lab packet, and reproducible handoff."
            ),
        ]
    )
