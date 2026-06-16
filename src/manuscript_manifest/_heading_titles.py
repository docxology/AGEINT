from __future__ import annotations


def chapter_landmark_titles(
    chapter_title: str,
    *,
    profile_title: str = "",
    practice_lens_title: str = "",
) -> dict[str, str]:
    """Return reader-facing H2 landmarks for a generated module chapter."""
    title = chapter_title.strip()
    profile = profile_title.strip() or f"{title} source profile"
    lens = practice_lens_title.strip() or f"{title} practice lens"
    return {
        "frame": f"{profile} frame for {title}: source context, topic focus, and reader task",
        "path": f"{lens} path for {title}: lesson cluster, safe artifact, and review",
        "assurance": f"{title} assurance handoff: evidence, governance, refresh, and capstone",
    }


def chapter_scaffold_titles(chapter_title: str) -> dict[str, str]:
    """Return body-level scaffold landmarks that stay below PDF ToC depth."""
    title = chapter_title.strip()
    return {
        "orientation": (
            f"{title} orientation: reader task, conceptual primer, outcomes, and vocabulary"
        ),
        "practice": (
            f"{title} practice studio: topic lessons, safe worked example, and knowledge check"
        ),
        "evidence": (
            f"{title} evidence contract: source spine, verified anchors, transfer architecture, "
            "and claim limits"
        ),
        "governance": (
            f"{title} governance boundary: synthesis, agent-assistance rules, rights, and "
            "assurance gates"
        ),
        "assessment": (
            f"{title} assessment route: capstone artifacts, refresh duties, reviewer challenges, "
            "and handoff"
        ),
    }


def chapter_teaching_titles(chapter_title: str) -> dict[str, str]:
    """Return chapter-specific H3 teaching landmarks for generated modules."""
    title = chapter_title.strip()
    return {
        "primer": f"{title} conceptual primer: source context, core model, and reader task",
        "outcomes": f"{title} learning outcomes: analytic moves, evidence duties, and transfer",
        "vocabulary": f"{title} core vocabulary: source terms, method roles, and safety limits",
        "lessons": f"{title} topic lessons: source-backed concepts and transfer tasks",
        "example": f"{title} worked safe example: synthetic inputs, evidence, and review",
        "sequence": f"{title} practice sequence: studio moves, artifact steps, and limits",
        "check": f"{title} knowledge check: misconceptions, evidence, and reviewer prompts",
    }


def chapter_detail_titles(chapter_title: str) -> dict[str, str]:
    """Return chapter-specific H3/H4 body landmarks for generated module scaffolds."""
    title = chapter_title.strip()
    return {
        "figures": f"{title} figures and course links: visual evidence, source flow, and navigation",
        "architecture": f"{title} transfer architecture: module inputs, outputs, and review boundary",
        "evidence": f"{title} evidence spine: source roles, citation support, and claim limits",
        "source_spine": f"{title} guide source spine: inherited keys and local citation roles",
        "verified_canon": f"{title} verified source canon: direct anchors and claim boundaries",
        "practice_lens": f"{title} intelligence practice lens: evidence artifact and safety check",
        "runtime_map": f"{title} runtime-to-reader map: generated sections and verifier surfaces",
        "subsection_contract": (
            f"{title} reusable subsection contract: topic rows, artifacts, and safety duties"
        ),
        "source_ledger": f"{title} annotated source ledger: real titles and local contribution",
        "synthesis": f"{title} analytic synthesis: source-backed claims and forbidden leaps",
        "evidence_standard": (
            f"{title} evidence standard and citation floor: source families and discovery limits"
        ),
        "agentic": f"{title} agentic boundary: assist, approve, block, and record",
        "permitted_utility": f"{title} permitted defensive utility: curriculum uses and safe outputs",
        "excluded_boundary": f"{title} excluded operational boundary: blocked actions and stop rules",
        "governance": f"{title} governance assurance: authority, rights, evidence, and human review",
        "governance_card": f"{title} governance card: gates, retained evidence, and review owner",
        "evidence_handoff": f"{title} evidence package handoff: appendices, records, and reuse",
        "current_source": (
            f"{title} current-source assurance: verified anchors and local artifact fit"
        ),
        "assessment": f"{title} assessment pathway: capstone artifacts and mastery evidence",
        "capstone_pathway": f"{title} capstone pathway: reviewable packet and excluded use",
        "facilitation": f"{title} instructor facilitation notes: studio roles and pause points",
        "rubric": f"{title} assessment rubric: topic evidence and mastery criteria",
        "refresh": f"{title} refresh map: source changes, safety triggers, and retest duties",
        "refresh_triggers": f"{title} refresh triggers: source changes and required actions",
        "claim_ledger": f"{title} claim and evidence ledger: claim classes, caveats, and owners",
        "review": f"{title} reviewer challenge route: checklist, failure evidence, and remediation",
        "links": f"{title} learning-path links: module map, overview, and curriculum atlas",
    }


__all__ = [
    "chapter_detail_titles",
    "chapter_landmark_titles",
    "chapter_scaffold_titles",
    "chapter_teaching_titles",
]
