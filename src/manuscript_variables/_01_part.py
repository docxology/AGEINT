"""Runtime manuscript-variable generation for the AGEINT curriculum atlas."""

from __future__ import annotations

import re
from typing import Any, Final
import unicodedata

try:  # Support both ``import src.manuscript_variables`` and script-level imports.
    from .curriculum import Curriculum
    from .citation_workflow import (
        source_citation_cell,
        source_citation_spine,
    )
    from .markdown_refs import (
        citation_ref,
        crossref_slug,
        figure_ref,
        part_module_map_figure_label,
        section_ref,
    )
    from .intelligence_content import (
        INTELLIGENCE_RESEARCH_ANCHORS,
        safe_curriculum_treatment,
        safe_pattern_rows,
        safe_pattern_treatment,
    )
    from .intelligence_content.source_grounding import safe_source_note as _sg_safe_note, safe_source_title as _sg_safe_title  # noqa: E501
except ImportError:  # pragma: no cover - exercised by thin CLI wrappers
    from curriculum import Curriculum  # type: ignore[no-redef]
    from citation_workflow import (  # type: ignore[no-redef]
        source_citation_cell,
        source_citation_spine,
    )
    from markdown_refs import (  # type: ignore[no-redef]
        citation_ref,
        crossref_slug,
        figure_ref,
        part_module_map_figure_label,
        section_ref,
    )
    from intelligence_content import (  # type: ignore[no-redef]
        INTELLIGENCE_RESEARCH_ANCHORS,
        safe_curriculum_treatment,
        safe_pattern_rows,
        safe_pattern_treatment,
    )
    from intelligence_content.source_grounding import safe_source_note as _sg_safe_note, safe_source_title as _sg_safe_title  # type: ignore[no-redef]  # noqa: E501


SOURCE_QUALITY_ANCHORS: Final[list[dict[str, str]]] = [
    {
        "key": "official_oecd_agentic_ai",
        "title": "The Agentic AI Landscape and Its Conceptual Foundations",
        "author": "OECD",
        "year": "2026",
        "url": "https://www.oecd.org/en/publications/the-agentic-ai-landscape-and-its-conceptual-foundations_396cf758-en.html",
        "note": "Official OECD conceptual foundation for agentic AI.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official OECD source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_nist_ai_rmf",
        "title": "Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
        "author": "National Institute of Standards and Technology",
        "year": "2023",
        "url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
        "note": "Official NIST.AI.100-1 risk-management framework.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official NIST source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_nist_ai_600_1",
        "title": "Artificial Intelligence Risk Management Framework: Generative AI Profile",
        "author": "National Institute of Standards and Technology",
        "year": "2024",
        "url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
        "note": "Official NIST AI 600-1 generative AI profile.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official NIST source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_nsa_mcp_security",
        "title": "Security Design Considerations for AI-Driven Automation Leveraging MCP",
        "author": "National Security Agency",
        "year": "2025",
        "url": "https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4496698/nsa-releases-security-design-considerations-for-ai-driven-automation-leveraging/",
        "note": "Official NSA security guidance for Model Context Protocol automation.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official NSA source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_nist_sp_800_82r3",
        "title": "Guide to Operational Technology Security, NIST SP 800-82 Rev. 3",
        "author": "National Institute of Standards and Technology",
        "year": "2024",
        "url": "https://csrc.nist.gov/pubs/sp/800/82/r3/final",
        "note": "Official NIST operational technology security guidance.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official NIST source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_isa_iec_62443",
        "title": "ISA/IEC 62443 Series of Standards",
        "author": "International Society of Automation",
        "year": "2026",
        "url": "https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards",
        "note": "Official ISA overview of industrial automation and control security standards.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official ISA source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_odni_icd_203",
        "title": "Intelligence Community Directive 203: Analytic Standards",
        "author": "Office of the Director of National Intelligence",
        "year": "2015",
        "url": "https://www.intel.gov/assets/documents/Intelligence%20Community%20Directives/ICD_203.pdf",
        "note": "Official ODNI analytic tradecraft standards directive.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official ODNI source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_eu_ai_act",
        "title": "Regulation (EU) 2024/1689: Artificial Intelligence Act",
        "author": "European Union",
        "year": "2024",
        "url": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng",
        "note": "Official EU Artificial Intelligence Act legal text.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official EU source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_cisa_foreign_influence",
        "title": "Preparing for and Mitigating Foreign Influence Operations",
        "author": "Cybersecurity and Infrastructure Security Agency",
        "year": "2024",
        "url": "https://www.cisa.gov/resources-tools/resources/cisa-insights-preparing-and-mitigating-foreign-influence-operations-targeting-critical",
        "note": "Official CISA guidance on foreign influence operations targeting critical infrastructure.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official CISA source URL.",
        "citation_role": "source_quality_anchor",
    },
    {
        "key": "official_nato_counter_information_threats",
        "title": "Countering Information Threats",
        "author": "North Atlantic Treaty Organization",
        "year": "2026",
        "url": "https://www.nato.int/cps/en/natohq/topics_219728.htm",
        "note": "Official NATO counter-information-threat guidance.",
        "checked_as_of": "2026-05-21",
        "verification_note": "Directly verified official NATO source URL.",
        "citation_role": "source_quality_anchor",
    },
]

SOURCE_QUALITY_DEFAULTS: Final[dict[str, str]] = {
    "domain": "source_quality_spine",
    "source_type": "source_quality_anchor",
    "source_lane": "source_quality_spine",
    "source_tier": "source_quality_anchor",
    "refresh_cadence": "semiannual",
    "refresh_trigger": "source version, legal status, standard revision, or official guidance changes",
    "verification_method": "direct_source_url_review",
    "claim_scope": "baseline source-quality guardrail for generated AGEINT curriculum claims",
    "stakeholder_role": "curriculum maintainer, instructor, reviewer, and learner",
    "assurance_use": "source-quality triangulation and claim-boundary review",
    "rights_dimension": "source transparency, accountability, and evidence traceability",
}


def _slug(value: str) -> str:
    """Return a Pandoc-safe lowercase label slug."""
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "item"


def section_label(kind: str, title: str, suffix: str = "") -> str:
    """Stable section label without embedding source-guide chapter numbers."""
    suffix_part = f"_{_slug(suffix)}" if suffix else ""
    return f"sec:{_slug(kind)}_{_slug(title)}{suffix_part}"


def citation_spine(citation_numbers: list[int]) -> str:
    """Return a Pandoc citation spine for source-guide reference numbers."""
    return source_citation_spine(citation_numbers)


def _citation_cell(citation_numbers: list[int]) -> str:
    return source_citation_cell(citation_numbers)


def _append_unique(values: list[Any], value: Any) -> None:
    if value not in values:
        values.append(value)


def section_rows(sections: list[dict[str, Any]], *, safe_patterns: bool = False) -> str:
    """Render source-guide subsection rows for a generated chapter."""
    if not sections:
        return (
            "| Curriculum treatment | Source loci | Citation spine |\n"
            "|---|---|---|\n"
            "| Module-level synthesis | Module source spine | - |"
        )
    grouped: dict[str, dict[str, list[Any]]] = {}
    active_pattern_number: int | None = None
    for section in sections:
        citations = section.get("citations", [])
        source_locus = str(section.get("number") or "module section")
        title = str(section["title"])
        if safe_patterns:
            title, active_pattern_number = safe_pattern_treatment(title, active_pattern_number)
        title = safe_curriculum_treatment(title)
        bucket = grouped.setdefault(title, {"source_loci": [], "citations": []})
        _append_unique(bucket["source_loci"], source_locus)
        for citation in citations:
            _append_unique(bucket["citations"], citation)

    rows = ["| Curriculum treatment | Source loci | Citation spine |", "|---|---|---|"]
    for title, bucket in grouped.items():
        loci = "; ".join(str(value) for value in bucket["source_loci"])
        cite_text = _citation_cell([int(value) for value in bucket["citations"]])
        rows.append(f"| {title} | {loci} | {cite_text} |")
    return "\n".join(rows)


def part_rows(curriculum: Curriculum) -> str:
    """Render the top-level curriculum map."""
    rows = [
        "| Curriculum area | Part intro | Modules | Unit map | Runtime source |",
        "|:--------------------------------------|:----------|--------:|:---------|:----------------|",
    ]
    for part in curriculum.parts:
        title = _curriculum_area_title(str(part["title"]))
        part_intro = section_ref(f"sec:part-{crossref_slug(title)}")
        unit_map = figure_ref(part_module_map_figure_label(part))
        rows.append(
            f"| {title} | {part_intro} | {len(part['chapters'])} | {unit_map} | parsed source guide |"
        )
    return "\n".join(rows)


def _curriculum_area_title(title: str) -> str:
    """Render source guide part titles in a PDF-friendly curriculum-map cell."""
    if not title.isupper():
        return title
    words = []
    acronyms = {"AGEINT", "HUMINT", "SIGINT", "OSINT", "FININT", "ICS"}
    lowercase = {"and", "of", "the", "to", "in"}
    for raw in title.split():
        stripped = raw.strip("()")
        if stripped in acronyms:
            word = stripped
        else:
            word = raw.lower().capitalize()
            if word.lower() in lowercase:
                word = word.lower()
        if raw.startswith("(") and raw.endswith(")"):
            word = f"({word})"
        words.append(word)
    return " ".join(words)


def appendix_rows(appendix: dict[str, Any]) -> str:
    """Render appendix item rows."""
    grouped: dict[str, dict[str, list[Any]]] = {}
    for item in appendix["items"]:
        citations = item.get("citations", [])
        raw_title = str(item["title"])
        title = safe_curriculum_treatment(raw_title)
        bucket = grouped.setdefault(title, {"source_items": [], "citations": []})
        _append_unique(bucket["source_items"], _blocked_appendix_source_label(raw_title, title))
        for citation in citations:
            _append_unique(bucket["citations"], citation)

    rows = [
        (
            "| Safe curriculum treatment | Blocked source motif, audit-only | "
            "Allowed fixture | Rejected action | Required artifact | Citation spine |"
        ),
        "|---|---|---|---|---|---|",
    ]
    for title, bucket in grouped.items():
        source_items = "; ".join(str(value) for value in bucket["source_items"])
        cite_text = _citation_cell([int(value) for value in bucket["citations"]])
        rows.append(
            f"| {title} | {source_items} | {_appendix_allowed_fixture(title)} | "
            f"{_appendix_rejected_action(title)} | {_appendix_required_artifact(title)} | "
            f"{cite_text} |"
        )
    return "\n".join(rows)


def _blocked_appendix_source_label(raw_title: str, safe_title: str) -> str:
    """Keep appendix provenance without reprinting unsafe learner-facing wording."""
    if raw_title == safe_title:
        # No risky motif needed transforming, so the "blocked source motif" column
        # carries no signal — say so rather than duplicating the safe-treatment cell.
        return "no blocked motif; source title used verbatim"
    prefix = re.match(r"^\s*([A-Z]\.\d+)", raw_title)
    source_id = prefix.group(1) if prefix else "source item"
    return f"{source_id} retained for audit; operational wording transformed"


def _appendix_allowed_fixture(title: str) -> str:
    lower = title.lower()
    if "sandbox" in lower or "tool-isolation" in lower:
        return "toy OSINT fixtures, sandbox policy cards, and blocked-action logs"
    if "osint" in lower or "source aggregation" in lower or "search-exposure" in lower or "social-source" in lower:
        return "instructor-provided source cards, toy records, and provenance notes"
    if "geoint" in lower or "geolocation" in lower or "imagery" in lower:
        return "provided imagery metadata, synthetic change examples, and uncertainty notes"
    if "humint" in lower or "identity" in lower or "source-protection" in lower:
        return "sample role records, ethics cards, and reviewer notes"
    if "cyber" in lower or "soc" in lower or "control-coverage" in lower:
        return "fabricated alerts, published defensive taxonomy labels, and debrief notes"
    if "ics" in lower:
        return "synthetic process logs, operator-decision cards, and safety stop rules"
    if "cognitive" in lower or "media-literacy" in lower:
        return "sample messages, transparent labels, and opt-in classroom discussion cards"
    return "public sources, synthetic records, owned-lab notes, and instructor handouts"


def _appendix_rejected_action(title: str) -> str:
    lower = title.lower()
    if "sandbox" in lower or "tool-isolation" in lower:
        return "external execution, credentialed access, network calls, or unmanaged tool use"
    if (
        "osint" in lower
        or "geoint" in lower
        or "geolocation" in lower
        or "source aggregation" in lower
        or "search-exposure" in lower
        or "social-source" in lower
    ):
        return "live collection expansion, tracking, private-data discovery, or targeting"
    if "humint" in lower or "identity" in lower or "source-protection" in lower:
        return "impersonation, contact activity, elicitation, handling, or source exposure"
    if "cyber" in lower or "soc" in lower or "control-coverage" in lower:
        return "scanning, exploitation, credential use, blocking, containment, or evasion"
    if "ics" in lower:
        return "live device interaction, process manipulation, unsafe actuation, or plant operation"
    if "cognitive" in lower or "media-literacy" in lower:
        return "covert persuasion, microtargeting, impersonation, or campaign design"
    return "external action, private-data processing, unsafe system interaction, or deployment"


def _appendix_required_artifact(title: str) -> str:
    lower = title.lower()
    if "sandbox" in lower or "tool-isolation" in lower:
        return "tool-isolation run card and denied-action evidence"
    if (
        "osint" in lower
        or "geoint" in lower
        or "geolocation" in lower
        or "source aggregation" in lower
        or "search-exposure" in lower
        or "social-source" in lower
    ):
        return "source-quality card and minimization note"
    if "humint" in lower or "identity" in lower or "source-protection" in lower:
        return "source-protection ethics memo and escalation path"
    if "cyber" in lower or "soc" in lower or "control-coverage" in lower:
        return "defensive coverage matrix and incident debrief"
    if "ics" in lower:
        return "tabletop packet with asset, consequence, operator decision, and recovery evidence"
    if "cognitive" in lower or "media-literacy" in lower:
        return "narrative-risk map and transparent education note"
    return "claim ledger, safe-lab packet, and reviewer handoff"


def pattern_rows(patterns: list[dict[str, Any]]) -> str:
    """Render AGEINT design-pattern rows."""
    return safe_pattern_rows(patterns)


def _source_quality_references() -> list[dict[str, str]]:
    """Return source-quality anchors with v2 lane and refresh metadata."""
    return [{**SOURCE_QUALITY_DEFAULTS, **anchor} for anchor in SOURCE_QUALITY_ANCHORS]


def _all_references(references: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        *references,
        *_source_quality_references(),
        *(anchor.as_reference() for anchor in INTELLIGENCE_RESEARCH_ANCHORS),
    ]


def bibliography_rows(references: list[dict[str, Any]]) -> str:
    """Render a bibliography atlas table."""
    rows = [
        "| Citation key | Title | Role | Lane | Tier | Checked | Refresh | Stakeholder | Assurance use | Rights dimension | Source note |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for ref in _all_references(references):
        # Route note + title through the same cleaners as the .bib emission so the
        # atlas never shows a truncated fragment, [PDF] tag, or dangling title.
        note = _sg_safe_note(str(ref.get("note") or "")) or "Source-guide bibliography entry."
        note = re.sub(r"https?://\S+", "source URL noted in guide", str(note))
        cleaned_title = _sg_safe_title(str(ref["title"])) or str(ref["title"])
        title = re.sub(r"\bChapter\s+(?:[0-9]+(?:\.[0-9]+)*|[IVXLC]+)\s*:\s*", "Source-guide chapter: ", cleaned_title)
        role = ref.get("citation_role") or "source_guide_reference"
        lane = ref.get("source_lane") or "source_guide_reference"
        tier = ref.get("source_tier") or ref.get("source_type") or "source_guide_reference"
        checked = ref.get("checked_as_of") or "source guide import"
        refresh = ref.get("refresh_cadence") or "source guide lifecycle"
        stakeholder = ref.get("stakeholder_role") or "source guide context"
        assurance = ref.get("assurance_use") or "bibliography traceability"
        rights = ref.get("rights_dimension") or "source guide context"
        rows.append(
            f"| {citation_ref(str(ref['key']))} | {_clean_markdown_table_cell(title)} | {_clean_markdown_table_cell(role)} | "
            f"{_clean_markdown_table_cell(lane)} | {_clean_markdown_table_cell(tier)} | "
            f"{_clean_markdown_table_cell(checked)} | {_clean_markdown_table_cell(refresh)} | "
            f"{_clean_markdown_table_cell(stakeholder)} | {_clean_markdown_table_cell(assurance)} | "
            f"{_clean_markdown_table_cell(rights)} | {_clean_markdown_table_cell(note)} |"
        )
    return "\n".join(rows)


def _clean_markdown_table_cell(value: object) -> str:
    """Keep generated bibliography tables plain-text and PDF-renderable."""
    text = re.sub(r"\s+", " ", str(value)).strip()
    replacements = {
        "🛰": "satellite",
        "3️⃣": "3",
        "\ufe0f": "",
        "\u20e3": "",
        "|": "/",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def _clean_bibtex_value(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).replace("{", "").replace("}", "")).strip()


def _clean_bibtex_text(value: object) -> str:
    text = _clean_bibtex_value(value)
    text = text.replace("\\", "/")
    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',

        "\u00ae": "(R)",
        "\u2122": "(TM)",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
    }
    text = "".join(replacements.get(char, char) for char in text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text


def _reference_author(ref: dict[str, Any]) -> str:
    if ref.get("author"):
        return _clean_bibtex_text(ref["author"])
    number = ref.get("number")
    if isinstance(number, int):
        return f"SIST Guide Reference {number:03d}"
    key_digits = re.sub(r"\D+", "", str(ref.get("key", "")))
    if key_digits:
        return f"SIST Guide Reference {int(key_digits):03d}"
    return "SIST Guide Reference"


def _join_note_parts(parts: list[str]) -> str:
    return ". ".join(part.strip().rstrip(".") for part in parts if part.strip())
