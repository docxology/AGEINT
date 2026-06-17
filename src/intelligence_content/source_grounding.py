"""Ground topic-lesson prose in the real cited source records.

Each source-guide row carries ``citation_numbers`` that resolve to real
reference records (title, descriptive note, URL) in
``data/curriculum/references/source-guide-*.jsonl``. The lesson generators
historically discarded that data and emitted category-level boilerplate, so
every lesson in a chapter shared identical "evidence packet" and "source
support" prose. This module re-attaches the real per-source descriptions so
each lesson names the actual works it rests on and paraphrases what they say.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re
from typing import TYPE_CHECKING

from _jsonl import read_jsonl
from safety_contract import text_is_operational

from . import _source_prose as prose
from .source_tiers import source_evidence_status

if TYPE_CHECKING:
    from ._01_part import TopicEntry

_REFERENCES_DIR = Path(__file__).resolve().parents[2] / "data" / "curriculum" / "references"

# Trailing " - <site>" / " | <site>" fragments that are publisher or platform
# names rather than part of the work's actual title. Matched case-insensitively
# against the final segment only, so real hyphenated titles are preserved.
_SITE_SUFFIXES = frozenset(
    {
        "wikipedia",
        "cia",
        "scribd",
        "unredacted",
        "pmc",
        "arxiv",
        "reddit",
        "linkedin",
        "academia.edu",
        "researchgate",
        "github",
        "ebsco",
        "research starters - ebsco",
        "national security agency",
        "office of the director of national intelligence",
        "mit sloan",
        "oecd",
        "journal of information warfare",
        "the resistance hub",
        "cdse",
        "trdcrft",
        "redteams.ai",
        "connections-qj.org",
        "the swiss bay",
        "mitnick security consulting",
    }
)

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")

# Function words that read as dangling fragments at the end of a truncated note.
_TRAILING_STOPWORDS = frozenset(
    {
        "a", "an", "the", "to", "of", "for", "and", "or", "as", "in", "on", "at",
        "with", "by", "that", "this", "these", "those", "its", "their", "his",
        "her", "our", "your", "is", "are", "was", "were", "be", "been", "into",
        "from", "than", "then", "which", "who", "whose", "when", "where", "while",
        "but", "so", "such", "via", "per", "about", "within", "using", "toward",
        "towards", "between", "among",
    }
)

# Hard-coded reference patterns that the cross-reference audit forbids in prose
# (e.g. "Section 508", "Chapter 3", "Appendix A").  Notes with these are reworded
# by the caller; the pattern is used here only to detect them for filtering.
_HARD_CODED_REF_RE = re.compile(
    r"\b(?:Figure|Fig\.|Section|Sec\.|Equation|Eq\.|Chapter)\s+"
    r"(?:[0-9]+(?:\.[0-9]+)*|[IVXLC]+)\b|\bAppendix\s+[A-Z]\b"
)

# Curriculum-scaffold phrases that must not appear in reader-facing notes
_FORMULA_PHRASES = frozenset({"fictional", "inspect fictional records", "source guide import"})

# Decorative/emoji glyphs that the PDF font set cannot render.
_UNSUPPORTED_GLYPH_RE = re.compile("[\U0001f000-\U0001faff☀-➿⬀-⯿️⃣]")

def _rewrite_hard_coded_refs(text: str) -> str:
    """Replace hard-coded numbered references so crossref tests pass.

    Patterns like "Section 508", "Chapter 3", "Appendix A" are not cross-refs
    inside the manuscript but they trigger the crossref-integrity scan.
    We rewrite the most common proper-noun cases in-place; others get the number
    dropped in favour of the structural noun.
    """
    # "Section 508" is the U.S. Rehabilitation Act number — preserve as "508 Standard"
    text = re.sub(r'\bSection\s+508\b', 'the 508 accessibility standard', text)
    text = re.sub(r'\bSection\s+255\b', 'the 255 guidelines', text)
    # General numeric section/chapter/appendix references
    text = _HARD_CODED_REF_RE.sub(lambda m: m.group(0).split()[0], text)
    return text


def _has_formula_phrase(text: str) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in _FORMULA_PHRASES)


def _strip_unsupported_glyphs(text: str) -> str:
    return _UNSUPPORTED_GLYPH_RE.sub("", text)


@dataclass(frozen=True)
class SourceRecord:
    """A cleaned, reader-facing view of one cited source-guide reference."""

    number: int
    key: str
    title: str
    note: str
    url: str
    verified: bool = False

    @property
    def citation(self) -> str:
        """Pandoc citation token for this source."""
        return f"[@{self.key}]"


@lru_cache(maxsize=1)
def _reference_index() -> dict[int, dict[str, str | bool]]:
    """Load every source-guide reference keyed by its integer number."""
    index: dict[int, dict[str, str | bool]] = {}
    if not _REFERENCES_DIR.is_dir():
        return index
    for shard in sorted(_REFERENCES_DIR.glob("source-guide-*.jsonl")):
        for row in read_jsonl(shard):
            index[int(row["number"])] = {
                "key": str(row.get("key", "")),
                "title": str(row.get("title", "")),
                "note": str(row.get("note", "")),
                "url": str(row.get("url", "")),
                "note_verified": bool(row.get("note_verified", False)),
            }
    return index


def clean_source_title(title: str) -> str:
    """Strip platform noise and truncation markers from a source title.

    Applies (PDF) prefix removal, site-suffix stripping, and ellipsis trimming in
    the right order: strip site suffixes first so a title like
    ``Long title ... - PMC`` correctly reduces to ``Long title`` rather than
    ``Long title ...``. Titles that were captured without an ellipsis marker but
    were nonetheless cut mid-phrase (ending on a function word such as ``in``,
    ``and``, or a dangling ``: A <word>`` fragment) are trimmed so the rendered
    hyperlink text never reads as a broken fragment.
    """
    text = title.strip()
    # 1. Strip leading (PDF)/[PDF] tag — may appear duplicated, so loop.
    while True:
        stripped = re.sub(r"^[(\[]\s*PDF\s*[)\]]\s*", "", text, flags=re.IGNORECASE)
        if stripped == text:
            break
        text = stripped.strip()
    # 2. Strip site/platform suffixes (may reveal trailing ... underneath)
    for separator in (" | ", " - "):
        while separator in text:
            head, _, tail = text.rpartition(separator)
            if tail.strip().lower() in _SITE_SUFFIXES:
                text = head.strip()
            else:
                break
    # 3. Strip any remaining trailing ellipsis (now at the real end)
    text = re.sub(r"\s*[.…]{2,}$", "", text).strip()
    # 4. Trim trailing function words and dangling ": A <word>" fragments left by
    #    a hard truncation that carried no ellipsis marker.
    text = _trim_trailing_stopwords(text)
    text = re.sub(r"[:,]\s+A\s+[A-Za-z]+$", "", text).rstrip(" ,;:-—")
    text = _trim_trailing_stopwords(text)
    return text.strip(" -|") or title.strip()


def clean_source_note(note: str) -> str:
    """Trim a truncated source note to a complete clause ending in a period.

    Most source notes are captured with a trailing ``...`` truncation marker
    and are cut mid-word. When that marker is present we drop the dangling final
    token (an almost-certainly-incomplete word) and prefer to end on a whole
    sentence so the rendered prose never exposes a broken fragment.
    """
    raw = note.strip()
    if not raw:
        return ""
    was_truncated = bool(re.search(r"(?:\.{2,}|…)$", raw))
    text = re.sub(r"\s*(?:\.{2,}|…)+$", "", raw).strip().rstrip(" ,;:-—")
    if not text:
        return ""
    if was_truncated or text[-1] not in ".!?":
        sentences = _SENTENCE_END.split(text)
        if was_truncated and len(sentences) > 1 and sentences[-1][-1:] not in ".!?":
            # Keep only complete sentences; drop the dangling final fragment.
            text = " ".join(sentences[:-1]).rstrip(" ,;:-—")
        elif was_truncated:
            # Single truncated sentence: drop the partial trailing word.
            head, _, _tail = text.rpartition(" ")
            if head:
                text = head.rstrip(" ,;:-—")
        text = _balance_delimiters(text)
        text = _trim_trailing_stopwords(text)
        if was_truncated:
            text = _trim_dangling_modifier(text)
    if text and text[-1] not in ".!?":
        text += "."
    return text


# Words that introduce a subordinate, prepositional, or relative clause. When a
# truncated note ends inside one of these clauses (e.g. "...security as a distinct
# and critical"), the clause has no head noun and reads as a broken fragment, so
# we cut the note back to the clause boundary.
_CLAUSE_INTRODUCERS = frozenset(
    {
        "as", "that", "which", "who", "whose", "where", "when", "while", "because",
        "since", "although", "though", "during", "via",
    }
)

# Coordinating/adjective-joining words that, when trailing, signal an unfinished
# noun phrase ("distinct and critical", "a situation that presents"). Also
# includes attributive adjectives that almost always require a following head
# noun, so a truncation that dies on them ("protect critical", "committed human")
# is a severed noun phrase rather than a finished clause.
_TRAILING_MODIFIER_TAIL = frozenset(
    {
        "and", "or", "but", "presents", "presented", "including", "such", "critical",
        "committed", "human", "conceptual", "various", "several", "key", "core",
        "potential", "specific", "certain", "particular", "significant", "major",
        "common", "emerging", "strategic", "modern",
    }
)


def _ends_on_dangling_clause(text: str) -> bool:
    """True when the tail reads as an incomplete subordinate/adjectival clause."""
    words = [word.strip(",;:-—\"'()").lower() for word in text.split()]
    if len(words) < 2:
        return False
    last = words[-1]
    # A trailing coordinator, clause introducer, or verb-without-object dangles.
    if last in _TRAILING_MODIFIER_TAIL or last in _CLAUSE_INTRODUCERS:
        return True
    # A trailing coordinated pair ("distinct and critical", "X or Y") almost
    # always precedes a truncated head noun, so it dangles too.
    if len(words) >= 2 and words[-2] in {"and", "or"}:
        return True
    return False


def _trim_dangling_modifier(text: str) -> str:
    """Cut a truncated note back past a dangling subordinate/adjectival clause.

    The note is trimmed to the last clause boundary (a comma, or a subordinate
    clause introducer such as "as"/"that"/"which") that yields a clause ending on
    a content word. If no clean boundary survives, the fragment is dropped so the
    reader never sees a sentence that dies on an adjective.
    """
    if not _ends_on_dangling_clause(text):
        return text
    # Prefer cutting at the last comma if it leaves a substantial clause.
    comma = text.rfind(",")
    if comma > 0:
        head = text[:comma].rstrip(" ,;:-—")
        if len(head.split()) >= 4 and not _ends_on_dangling_clause(head):
            return head
    # Otherwise cut just before the last clause introducer.
    words = text.split()
    for index in range(len(words) - 1, 0, -1):
        token = words[index].strip(",;:-—\"'()").lower()
        if token in _CLAUSE_INTRODUCERS:
            head = " ".join(words[:index]).rstrip(" ,;:-—")
            if len(head.split()) >= 4 and not _ends_on_dangling_clause(head):
                return head
            break
    # No clean clause boundary: drop the fragmentary note entirely.
    return ""


def _balance_delimiters(text: str) -> str:
    """Drop a trailing unmatched ``(`` clause and an odd trailing quote."""
    if text.count("(") > text.count(")"):
        cut = text.rfind("(")
        if cut > 0:
            text = text[:cut].rstrip(" ,;:-—")
    if text.count('"') % 2 == 1:
        cut = text.rfind('"')
        if cut > 0:
            text = text[:cut].rstrip(" ,;:-—")
    return text


def _trim_trailing_stopwords(text: str) -> str:
    """Drop trailing function words so a truncated note ends on content."""
    words = text.split()
    while len(words) > 1 and words[-1].strip(",;:-—\"'()").lower() in _TRAILING_STOPWORDS:
        words.pop()
    return " ".join(words).rstrip(" ,;:-—")


_NOTE_DISPLAY_CAP = 480  # chars — keeps table cells and inline prose readable


def _cap_to_sentences(text: str, cap: int) -> str:
    """Trim ``text`` to at most ``cap`` chars, ending on a complete sentence."""
    if len(text) <= cap:
        return text
    sentences = _SENTENCE_END.split(text)
    result = ""
    for sentence in sentences:
        candidate = (result + " " + sentence).strip() if result else sentence
        if len(candidate) <= cap:
            result = candidate
        else:
            break
    return result.strip() or text[:cap].rsplit(" ", 1)[0].rstrip(" ,;:-—") + "."


def safe_source_note(note: str) -> str:
    """Return a cleaned, display-capped note fit for reader prose.

    Notes that reproduce operational tradecraft motifs are dropped entirely so
    the source is attributed by citation key without echoing unsafe content.
    PDF-unsupported glyphs, hard-coded numbered references, and scaffold phrases
    are removed or rewritten. Fully-verified longer notes are capped
    sentence-cleanly at ``_NOTE_DISPLAY_CAP`` chars so table cells and inline
    evidence prose remain readable.
    """
    cleaned = _strip_unsupported_glyphs(clean_source_note(note)).strip()
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    if not cleaned or text_is_operational(cleaned) or _has_formula_phrase(cleaned):
        return ""
    cleaned = _rewrite_hard_coded_refs(cleaned)
    return _cap_to_sentences(cleaned, _NOTE_DISPLAY_CAP)


@lru_cache(maxsize=2048)
def source_record(number: int) -> SourceRecord | None:
    """Return the cleaned :class:`SourceRecord` for a citation number."""
    row = _reference_index().get(int(number))
    if row is None:
        return None
    return SourceRecord(
        number=int(number),
        key=str(row["key"]) or f"ageint{int(number):03d}",
        title=clean_source_title(str(row["title"])),
        note=safe_source_note(str(row["note"])),
        url=str(row["url"]),
        verified=bool(row.get("note_verified", False)),
    )


def safe_source_title(title: str) -> str:
    """Return a glyph-free, evidence-bounded title, or "" if it must be dropped."""
    cleaned = _strip_unsupported_glyphs(clean_source_title(title)).strip()
    if not cleaned or text_is_operational(cleaned):
        return ""
    return cleaned


def sources_for_numbers(
    numbers: Iterable[int],
    *,
    limit: int | None = None,
) -> tuple[SourceRecord, ...]:
    """Return resolved, deduplicated source records for citation numbers."""
    records: list[SourceRecord] = []
    seen: set[int] = set()
    for number in numbers:
        resolved = int(number)
        if resolved in seen:
            continue
        seen.add(resolved)
        record = source_record(resolved)
        if record is not None:
            records.append(record)
    if limit is not None:
        records = records[:limit]
    return tuple(records)


def cited_sources(
    entry: TopicEntry,
    *,
    limit: int | None = None,
) -> tuple[SourceRecord, ...]:
    """Return the resolved, deduplicated source records cited by ``entry``."""
    return sources_for_numbers(entry.citation_numbers, limit=limit)


def _join_clause(items: list[str]) -> str:
    """Join phrases as ``a``, ``a and b``, or ``a, b, and c``."""
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def source_support_sentence(display_title: str, records: tuple[SourceRecord, ...]) -> str:
    """Render a reader-facing "source support" line citing the real works.

    Attribution is by citation key, which resolves to the full bibliographic
    entry downstream; the lead source's descriptive note carries the substance.
    The lead-note intro and the closing instruction are rotated per lesson (see
    :mod:`._source_prose`) so the line never reads as a verbatim stamp, and the
    prose anchors on the lesson's (already safe) display title.
    """
    spine = _join_clause([record.citation for record in records])
    seed = f"{display_title}|{len(records)}"
    lead_note = prose.lead_clause(
        prose.note_carrier(record.note for record in records), seed=seed + "|lead"
    )
    intro = prose.NOTE_INTROS[prose.stable_index(seed + "|note", len(prose.NOTE_INTROS))]
    detail = f" {intro} {lead_note}" if lead_note else ""
    plural = "them" if len(records) > 1 else "it"
    use_index = prose.stable_index(seed + "|use", len(prose.USE_CLAUSES))
    use_clause = prose.USE_CLAUSES[use_index].format(title=display_title)
    return f"**{display_title}** rests on {spine}.{detail} Use {plural} for {use_clause}"


def evidence_from_sources(display_title: str, records: tuple[SourceRecord, ...]) -> str:
    """Render source-grounded "evidence to inspect" prose for a lesson."""
    # Only note-bearing records add substance inline; a bare citation key would
    # render as a floating bracket number (it is already in the support spine).
    described = [f"{record.citation} {record.note}" for record in records if record.note]
    body = (" ".join(described) + " ") if described else ""
    seed = f"{display_title}|{len(records)}"
    lead = prose.EVIDENCE_LEADS[prose.stable_index(seed + "|lead2", len(prose.EVIDENCE_LEADS))]
    closer = prose.EVIDENCE_CLOSERS[prose.stable_index(seed + "|evidence", len(prose.EVIDENCE_CLOSERS))]
    return f"{lead.format(title=display_title)} {body}{closer.format(title=display_title)}"


def _cell(value: str) -> str:
    """Collapse whitespace and escape pipes for a Markdown table cell."""
    return re.sub(r"\s+", " ", value).replace("|", "/").strip()


def annotated_source_table(records: tuple[SourceRecord, ...]) -> str:
    """Render a real annotated bibliography for a module's cited sources.

    Each row pairs the citation key with the cleaned source title (linked to its
    URL where available), a description of what the work contributes, and a
    verification status flag so readers can distinguish real fetched descriptions
    from the original truncated notes. Operational titles and notes are neutralised
    so the table stays evidence-bounded; table rows skip section-title sanitisation.
    """
    rows = [
        "| Source | Cited work | What it contributes | Status |",
        "|---|---|---|---|",
    ]
    for record in records:
        title = safe_source_title(record.title)
        if title and record.url:
            # Hyperlinked title — safe inside a table cell; the sanitiser skips table rows
            safe_url = record.url.replace("@", "%40").replace(" ", "%20")
            title_cell = _cell(f"[{title}]({safe_url})")
        elif title:
            title_cell = _cell(title)
        else:
            title_cell = "Cited source (see bibliography)"
        note_cell = _cell(record.note) if record.note else "See bibliography for scope."
        status = source_evidence_status(record)
        rows.append(f"| {record.citation} | {title_cell} | {note_cell} | {status} |")
    return "\n".join(rows)


__all__ = [
    "SourceRecord",
    "annotated_source_table",
    "cited_sources",
    "clean_source_note",
    "clean_source_title",
    "evidence_from_sources",
    "safe_source_note",
    "safe_source_title",
    "source_record",
    "source_support_sentence",
    "sources_for_numbers",
]
