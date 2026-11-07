"""Preserve source-guide identity without inventing claim-specific support.

Source-guide notes are curriculum annotations, not source-authored quotations.
An inherited citation or a verified annotation does not establish topical fit,
empirical efficacy, normative authority, or independent verification of a lesson
claim. Claim-specific support requires checking the original passage and scope.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re
from typing import TYPE_CHECKING

from _jsonl import read_jsonl
from prose_policy import source_identifier_text
from safety_contract import text_is_operational

from . import _source_prose as prose
from ._source_cleaners import (
    SITE_SUFFIXES as _SITE_SUFFIXES,
    has_formula_phrase as _has_formula_phrase,
    rewrite_hard_coded_refs as _rewrite_hard_coded_refs,
    strip_unsupported_glyphs as _strip_unsupported_glyphs,
    trim_trailing_stopwords as _trim_trailing_stopwords,
)
from .source_tiers import source_evidence_status

if TYPE_CHECKING:
    from ._01_part import TopicEntry

_REFERENCES_DIR = Path(__file__).resolve().parents[2] / "data" / "curriculum" / "references"

_SENTENCE_END = re.compile(
    r"(?<!\bNo\.)(?<!\bVol\.)(?<!\bDr\.)(?<!\bMr\.)(?<!\bMs\.)(?<!\b[A-Za-z]\.)"
    r"(?<!\bProf\.)(?<!\be\.g\.)(?<!\bi\.e\.)(?<!\bet al\.)(?<=[.!?])\s+"
)


@dataclass(frozen=True)
class SourceRecord:
    """A source-guide identity and editorial note; ``verified`` is note metadata."""

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
    """Keep intact notes or complete leading sentences of a truncated note.

    Never turn a captured fragment into an apparently complete assertion by
    deleting its final word or adding punctuation. Incomplete single-sentence
    notes are omitted; their source identity remains available.
    """
    raw = note.strip()
    if not raw:
        return ""
    was_truncated = bool(re.search(r"(?:\.{2,}|…)$", raw))
    text = re.sub(r"\s*(?:\.{2,}|…)+$", "", raw).strip()
    if not text:
        return ""
    if not was_truncated and text[-1] in ".!?":
        return text
    sentences = _SENTENCE_END.split(text)
    return " ".join(sentences[:-1]).strip()


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
    return result.strip()


def safe_source_note(note: str) -> str:
    """Return a safe editorial annotation without fabricating a sentence.

    Operational notes are omitted. Glyphs and hard-coded references are cleaned;
    display capping retains only complete leading sentences, never a word-cut
    fragment. Neither cleaning nor the source's verification flag validates the
    annotation as a quotation or as support for a generated lesson claim.
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


def sources_for_numbers(numbers: Iterable[int], *, limit: int | None = None) -> tuple[SourceRecord, ...]:
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


def cited_sources(entry: TopicEntry, *, limit: int | None = None) -> tuple[SourceRecord, ...]:
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
    """Preserve inherited source identity while keeping claim-support limits explicit."""
    display_title = source_identifier_text(display_title)
    if not records:
        return f"No source-guide citation is available for **{display_title}**; claim-specific support remains unestablished."
    spine = _join_clause([record.citation for record in records])
    return (
        f"Inherited source-guide context for **{display_title}**: {spine}. "
        "These citations preserve source identity, not automatic topical relevance, "
        "empirical validation or normative authority. No claim-specific primary "
        "support is established by this source-guide association alone."
    )


def evidence_from_sources(display_title: str, records: tuple[SourceRecord, ...]) -> str:
    """Present key-bound curriculum annotations as leads for passage-level review."""
    display_title = source_identifier_text(display_title)
    if not records:
        return f"No source-guide citation is available to inspect for **{display_title}**; record the evidence gap."
    annotations = [prose.curriculum_annotation(record.citation, source_identifier_text(record.note)) for record in records if record.note]
    body = " ".join(annotations) if annotations else (f"No displayable curriculum annotation is available for {_join_clause([record.citation for record in records])}.")
    return (
        f"For **{display_title}**, inspect the original passages. {body} "
        "These editorial descriptions are not source-authored quotations or "
        "independently verified lesson support. Record a passage and locator, "
        "distinguishing primary findings, normative requirements, proposals and "
        "context using [@sec:analytic-workflow]; unsupported claims remain gaps."
    )


def _cell(value: str) -> str:
    """Collapse whitespace and escape pipes for a Markdown table cell."""
    return re.sub(r"\s+", " ", value).replace("|", "/").strip()


def annotated_source_table(records: tuple[SourceRecord, ...]) -> str:
    """Render source identities, key-bound editorial notes, and annotation metadata.

    The status column retains inherited verification/context flags; it does not
    certify claim relevance or independently verify the generated lesson.
    """
    rows = ["| Source | Cited work | Curriculum annotation | Status |", "|---|---|---|---|"]
    for record in records:
        title = source_identifier_text(safe_source_title(record.title))
        if title and record.url:
            # Hyperlinked title — safe inside a table cell; the sanitiser skips table rows
            safe_url = record.url.replace("@", "%40").replace(" ", "%20")
            title_cell = _cell(f"[{title}]({safe_url})")
        elif title:
            title_cell = _cell(title)
        else:
            title_cell = "Cited source (see bibliography)"
        note_cell = _cell(source_identifier_text(record.note)) if record.note else "No displayable curriculum annotation; see original work for scope."
        status = f"{source_evidence_status(record)}; annotation metadata, not claim verification"
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
