"""Deterministic, topic-varying phrasing for source-grounded lesson prose.

Extracted from :mod:`source_grounding` so that module stays under the 500-line
file cap and the de-boilerplating rotation logic lives in one cohesive place.

Every selection here is deterministic: a fixed ordinal digest (not Python's
salted ``hash``) chooses a phrasing variant from a small bank, so the same
lesson always renders the same prose across build runs while different lessons
get visibly different closing clauses instead of one verbatim stamp.
"""

from __future__ import annotations

from collections.abc import Iterable
import re

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def stable_index(seed: str, modulo: int) -> int:
    """Deterministic 0..modulo-1 index from ``seed``.

    Built-in ``hash`` is salted per process, which would make the otherwise
    deterministic curriculum build non-reproducible. A fixed ordinal digest
    keeps the same seed mapped to the same phrasing across runs.
    """
    if modulo <= 1:
        return 0
    total = 0
    for position, character in enumerate(seed):
        total = (total * 131 + ord(character) + position) % 1_000_003
    return total % modulo


def lead_clause(note: str, seed: str = "") -> str:
    """Return one complete sentence of ``note`` for an inline citation.

    Reproducing a source's full note inline stamps the same 100-plus-character
    block onto every lesson that happens to cite that anchor. Surfacing a single
    sentence keeps the attribution specific while preventing one over-cited
    source from repeating its whole note verbatim across the atlas. When ``seed``
    is supplied, the surfaced sentence is chosen deterministically from the
    note's sentences, so two lessons that share the same lead note foreground
    different sentences instead of an identical verbatim stamp.
    """
    sentences = [part.strip() for part in _SENTENCE_END.split(note.strip()) if part.strip()]
    if not sentences:
        return ""
    clause = sentences[stable_index(seed, len(sentences))] if seed else sentences[0]
    if clause and clause[-1] not in ".!?":
        clause += "."
    return clause


def note_carrier(notes: Iterable[str]) -> str:
    """Pick the most topic-specific note (the longest), not just the first.

    The longest surviving note is the one that actually describes the row rather
    than a generic anchor that merely appears first in the citation list, so the
    inline detail tracks the lesson's real subject and a single anchor stops
    dominating hundreds of lessons.
    """
    candidates = [note for note in notes if note]
    if not candidates:
        return ""
    return max(candidates, key=len)


# Rotated lead-note introductions for the "source support" line. The note text
# that follows varies per lesson, so these labels never read as a verbatim stamp.
NOTE_INTROS: tuple[str, ...] = (
    "The closest source to this row notes:",
    "Its anchor reference records:",
    "The most specific cited work observes:",
    "The lead source's own note reads:",
)

# Rotated closing instructions for the "source support" line. Each names the
# same method (define, bound, refresh) in different words AND weaves the lesson's
# safe display title ({title}), so the rendered closing sentence is topic-specific
# instead of one of four clauses stamped verbatim onto ~70 lessons each. The title
# is bolded here so longer authored lesson-title fragments survive the
# rendered-reference sanitizer instead of collapsing embedded chapter names.
# Selection stays deterministic via stable_index; ``source_support_sentence`` calls
# ``.format(title=display_title)`` exactly as ``EVIDENCE_CLOSERS`` already does.
USE_CLAUSES: tuple[str, ...] = (
    "the working definition that **{title}** can defend, where that scope ends, and the refresh check owed before this evidence transfers.",
    "fixing what **{title}** covers, marking the boundary it must not cross, and timing the next source refresh.",
    "the claim that **{title}** lets you defend here, the limit it has to respect, and the re-check owed before reuse.",
    "pinning down the scope of **{title}**, the edge of that scope, and when these citations need re-verifying before transfer.",
)

# Rotated closers for the "evidence to inspect" prose. ``{title}`` is the
# lesson's safe display title, woven in so each closer is topic-specific.
EVIDENCE_CLOSERS: tuple[str, ...] = (
    "From each source, pull the bounded claim it can carry for **{title}**, its provenance, the stated uncertainty, and the one condition that would overturn that judgment.",
    "Read each cited work for what it can support about **{title}**, where that claim originated, how confident it is, and what evidence would change it.",
    "Work source by source: name the bounded claim, its origin, the residual uncertainty, and the trigger that would change how **{title}** is judged.",
    "Each source above earns its place in **{title}** only when you can state its bounded claim, its provenance, its uncertainty, and the fact that would retire it.",
)

# Rotated lead-ins for the "evidence to inspect" prose. Previously a single
# verbatim opener ("For **{title}**, work from the cited evidence behind this
# row.") was stamped onto every lesson (~564x). Each variant weaves the lesson's
# safe display title so the opener is topic-specific and no single phrasing
# dominates the corpus.
EVIDENCE_LEADS: tuple[str, ...] = (
    "For **{title}**, work from the cited evidence behind this row.",
    "For **{title}**, reason from the sources cited in this row.",
    "Ground **{title}** in the evidence the row cites.",
    "Read **{title}** against the works cited for this row.",
)


__all__ = [
    "EVIDENCE_CLOSERS",
    "EVIDENCE_LEADS",
    "NOTE_INTROS",
    "USE_CLAUSES",
    "lead_clause",
    "note_carrier",
    "stable_index",
]
