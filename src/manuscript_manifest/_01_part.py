from __future__ import annotations

"""Build and render the AGEINT semantic manuscript manifest."""


from dataclasses import dataclass
import json
from pathlib import Path
import re
import shutil
from typing import Any

try:  # Resolve the sibling template checkout for standalone AGEINT imports.
    from .template_resolver import ensure_template_repo_on_path
except ImportError:  # pragma: no cover - exercised by thin CLI wrappers
    from template_resolver import ensure_template_repo_on_path  # type: ignore[no-redef]

ensure_template_repo_on_path(Path(__file__).resolve())

from infrastructure.rendering.manuscript_injection import substitute_manuscript_text  # noqa: E402

try:  # Support package and script-level imports.
    from .curriculum import Curriculum
    from .figures import figure_markdown, figures_for_section
    from .markdown_refs import figure_ref_list, section_ref_list
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
        chapter_textbook_primer,
        chapter_topic_lessons,
        chapter_worked_example,
        _safe_topic_entries,
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
    from .manuscript_variables import appendix_rows, citation_spine
except ImportError:  # pragma: no cover - exercised by thin CLI wrappers
    from curriculum import Curriculum  # type: ignore[no-redef]
    from figures import figure_markdown, figures_for_section  # type: ignore[no-redef]
    from markdown_refs import figure_ref_list, section_ref_list  # type: ignore[no-redef]
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
        chapter_textbook_primer,
        chapter_topic_lessons,
        chapter_worked_example,
        _safe_topic_entries,
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
        citation_spine,
    )


@dataclass(frozen=True)
class ManuscriptSection:
    """A generated manuscript section with semantic output path and context."""

    kind: str
    title: str
    relative_path: str
    template_name: str
    context: dict[str, str]
    order: int
    section_label: str = ""
    parent_label: str = ""
    previous_label: str = ""
    next_label: str = ""
    figure_labels: tuple[str, ...] = ()
    chapter_number: int | None = None
    appendix_letter: str | None = None


@dataclass(frozen=True)
class ManuscriptManifest:
    """Ordered AGEINT manuscript manifest."""

    sections: list[ManuscriptSection]
    units: list[dict[str, Any]]
    appendix_files: list[str]

    @property
    def chapter_sections(self) -> list[ManuscriptSection]:
        return [section for section in self.sections if section.kind == "chapter"]

    @property
    def part_sections(self) -> list[ManuscriptSection]:
        return [section for section in self.sections if section.kind == "part"]

    @property
    def appendix_sections(self) -> list[ManuscriptSection]:
        return [section for section in self.sections if section.kind == "appendix"]

    def section_for_chapter(self, number: int) -> ManuscriptSection:
        for section in self.chapter_sections:
            if section.chapter_number == number:
                return section
        raise KeyError(f"No chapter section {number}")

    def section_for_appendix(self, letter: str) -> ManuscriptSection:
        normalized = letter.upper()
        for section in self.appendix_sections:
            if section.appendix_letter == normalized:
                return section
        raise KeyError(f"No appendix section {letter}")

    def config_yaml(self) -> str:
        """Return YAML ordering understood by infrastructure manuscript discovery."""
        return _ordering_config_yaml(["abstract.md", "orientation.md"], self.units, self.appendix_files)


def _ordering_config_yaml(
    front_matter_files: list[str],
    units: list[dict[str, Any]],
    appendix_files: list[str],
) -> str:
    """Return YAML ordering understood by infrastructure manuscript discovery."""
    lines = [
        "front_matter:",
        "  include_front_matter: true",
        "  files:",
    ]
    lines.extend(f"    - file: {file_name}" for file_name in front_matter_files)
    lines.append("units:")
    for unit in units:
        lines.extend(
            [
                f"  - id: {unit['id']}",
                f"    directory: {unit['directory']}",
                "    chapters:",
            ]
        )
        for chapter_file in unit["chapters"]:
            lines.append(f"      - file: {chapter_file}")

    lines.extend(
        [
            "appendices:",
            "  include_reference: true",
            "  reference:",
        ]
    )
    for file_name in appendix_files:
        lines.append(f"    - file: {file_name}")
    return "\n".join(lines) + "\n"


class _SlugRegistry:
    def __init__(self) -> None:
        self._seen: dict[str, set[str]] = {}

    def unique(self, namespace: str, value: str) -> str:
        base = _slug(value)
        seen = self._seen.setdefault(namespace, set())
        if base not in seen:
            seen.add(base)
            return base
        suffix = 2
        while f"{base}-{suffix}" in seen:
            suffix += 1
        resolved = f"{base}-{suffix}"
        seen.add(resolved)
        return resolved


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def _label(kind: str, slug: str) -> str:
    return f"sec:{kind}-{slug}"


def _part_summary(part: dict[str, Any]) -> str:
    title = part["title"]
    return (
        f"The **{title}** unit introduction tells instructors what learners should do "
        "before they enter the individual modules. Start with the unit's guiding "
        "question, identify the evidence artifacts students will produce, and "
        "keep the capstone thread visible across this unit.\n\n"
        f"Learners carry one **{title}** capstone thread through the part: define an "
        "authorized intelligence question, bind it to source-quality constraints, "
        "produce a reviewable artifact, test the artifact against failure modes, "
        "and hand it off with enough context for another analyst or instructor "
        "to audit. The capstone remains public, synthetic, or owned-lab "
        "throughout.\n\n"
        f"**{title}** deliverables are a source-canon card, claim/evidence ledger, "
        "safe-practice lab packet, failure-mode note, instructor rubric, and "
        "debrief memo. The full source-lane and evidence-package ledgers appear "
        "in the orientation and appendices; this unit introduction keeps only "
        "the learner-facing spine.\n\n"
        f"**{title}** safety gates are scope authorization, rights review, data "
        "provenance, tool allowlisting, human oversight, rollback, and "
        "non-operational output. A missing gate turns the activity into a "
        "tabletop, audit, or written governance exercise until the gate is "
        "restored.\n\n"
        "Capstone thread:\n\n"
        f"{capstone_scaffold_rows()}\n\n"
        f"{part_research_brief(part)}"
    )


def _part_chapter_rows(part: dict[str, Any], chapter_files: dict[int, str]) -> str:
    rows = ["| Module | Section reference | Source spine |", "|---|---|---|"]
    for chapter in part["chapters"]:
        chapter_slug = Path(chapter_files[chapter["number"]]).stem
        section_ref = f"[@{_label('chapter', chapter_slug)}]"
        rows.append(
            f"| {chapter['title']} | {section_ref} | "
            f"{citation_spine(chapter['citations'])} |"
        )
    return "\n".join(rows)


def _source_canon(chapter: dict[str, Any], part: dict[str, Any], source_spine: str) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"The source canon for **{title}** has three tiers:",
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
                f"**{part['title']}** and **{chapter['title']}** | "
                "Selects the practice lens, method stack, failure modes, and "
                "defensive boundary for generated prose. |"
            ),
            "",
            f"Maintenance rule for **{title}**: Perplexity may suggest candidates, "
            "but only directly verified source URLs are encoded as citations.",
        ]
    )


def _claim_evidence_ledger(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            "| Claim class | Evidence required | Review gate |",
            "|---|---|---|",
            (
                f"| Source-spine claim about **{title}** | Parsed module title, "
                "module section map, and curriculum citation spine | "
                "Confirm the generated text does not invent counts, paths, or labels. |"
            ),
            (
                "| Research-backed governance claim | Direct official, standards, "
                "public-domain, or scholarly anchor in `references-*.bib` | "
                "Confirm the anchor has verification metadata and a stable URL. |"
            ),
            (
                "| Agentic workflow claim | Tool boundary, authority contract, "
                "human review point, and rollback condition | Confirm the workflow "
                "remains educational, logged, reversible, and non-operational. |"
            ),
            (
                "| Safety claim | Explicit prohibition plus safe alternative | Confirm "
                "the module blocks live targeting, exploitation, covert collection, "
                "manipulation, and unsafe cyber-physical action. |"
            ),
            (
                f"| Cross-module claim | Link to **{part['title']}** and adjacent "
                "curriculum modules | Confirm the handoff names inputs, outputs, "
                "uncertainty, and next-review owner. |"
            ),
        ]
    )


def _safe_practice_lab(chapter: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"Build a safe lab packet for **{title}** using public, benign, "
            "owned-lab, or synthetic material only.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Use the drill to stress-test **{title}** before treating the module "
            "artifact as complete.",
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
    title = chapter["title"]
    return "\n".join(
        [
            f"Instructors should collect a compact artifact bundle for **{title}**:",
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


def _review_checklist(chapter: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"Before marking **{title}** complete, verify:",
            "",
            f"- The **{title}** source spine resolves to Pandoc citation keys and no raw source URLs are pasted into prose.",
            "- Every research-backed claim has a directly verified source anchor or is clearly marked as source-guide context.",
            "- Agentic affordances are limited to retrieval, comparison, drafting, simulation, critique, and audit support.",
            "- The lab packet uses public, benign, owned-lab, or synthetic material only.",
            "- The artifact names assumptions, caveats, uncertainty, excluded actions, and human review points.",
            "- No Figure, Section, Equation, chapter, or appendix numbers are hard-coded outside generated labels.",
        ]
    )


def _authority_accountability_model(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    return "\n".join(
        [
            f"Use this accountability model before applying **{title}** in any exercise:",
            "",
            "| Accountability layer | Required decision | Evidence retained |",

            "|---|---|---|",
            (
                f"| Sponsor | Why **{part['title']}** needs this module now | "
                "authorized learning objective and excluded actions |"
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
