"""Reader-voice helpers for generated topic-lesson prose."""

from __future__ import annotations

from typing import TYPE_CHECKING

from unit_education import UnitEducationProfile, unit_lesson_artifact_line, unit_lesson_evidence_line

if TYPE_CHECKING:
    from ._01_part import TopicEntry


def lower_first_word(text: str) -> str:
    stripped = text.strip()
    return stripped[:1].lower() + stripped[1:] if stripped else stripped


# Prepositions/conjunctions that begin a trailing qualifier in a colon-free
# title ("Micro-Expression Analysis FOR Source Validation"). Cutting before the
# first one yields the natural noun-phrase short form.
_TITLE_TAIL_MARKERS = (
    " for ",
    " of ",
    " in ",
    " with ",
    " and ",
    " using ",
    " through ",
    " across ",
    " under ",
    " from ",
    " to ",
    " as ",
    " via ",
    " between ",
)


def short_title(display_title: str) -> str:
    """Return a compact reference for a topic title.

    Long titles carry a colon-delimited headline ("APT Attribution: Technical
    Indicators...") whose left segment reads as the natural short form. Colon-free
    long titles ("Micro-Expression Analysis for Source Validation") are shortened
    at the first trailing-qualifier preposition. Titles already compact are
    returned unchanged. The result is never bolded — the caller decides emphasis.
    """
    title = display_title.strip()
    head = title.split(":", 1)[0].strip()
    if head and head != title and len(head) <= len(title) - 6:
        return head
    # Colon-free title: cut before the first trailing-qualifier marker if doing so
    # leaves a substantial head (>=2 words, >=12 chars) and a real reduction.
    lowered = f" {title.lower()} "
    cut_positions = [lowered.find(marker) for marker in _TITLE_TAIL_MARKERS]
    cut_positions = [pos for pos in cut_positions if pos > 0]
    if cut_positions:
        cut = min(cut_positions)  # offset includes the leading space we added
        candidate = title[:cut].rstrip(" ,;:-—")
        if (
            candidate
            and candidate != title
            and "," not in candidate  # avoid stranded list fragments
            and candidate.count("(") == candidate.count(")")
            and len(candidate.split()) >= 2
            and len(candidate) >= 12
            and len(candidate) <= len(title) - 6
        ):
            return candidate
    return title


# Anaphoric references that stand in for the bold title after its first mention.
# Indexed by a stable per-lesson hash so the same lesson varies its references
# across fields without ever drifting into a fixed cadence.
_ANAPHORA = (
    "this topic",
    "the same topic",
    "this lesson topic",
    "the topic above",
)


def topic_reference(display_title: str, slot: int) -> str:
    """Return a short or anaphoric reference for the title at body field ``slot``.

    Slot 0 is reserved for the first body mention and resolves to the (bolded)
    short form so the reader still sees the concrete topic name once more after
    the header. Later slots rotate through anaphora so subsequent fields read as
    natural prose rather than a repeated bold restatement.
    """
    if slot <= 0:
        compact = short_title(display_title)
        return f"**{compact}**"
    return _ANAPHORA[(slot - 1) % len(_ANAPHORA)]


def for_topic(entry: TopicEntry, text: str, *, slot: int = 1) -> str:
    if entry.display_title in text or f"**{entry.display_title}**" in text:
        return text
    # No title in the text yet: anchor it once with the bolded short form so the
    # downstream anaphora pass has a token to vary, and the reader still sees a
    # concrete topic name in this field.
    return f"For **{short_title(entry.display_title)}**, {lower_first_word(text)}"


def reader_facing_concept(entry: TopicEntry, frame: str) -> str:
    text = frame.strip()
    if f"**{entry.display_title}**" in text:
        return text
    replacements = {
        "Analyze ": "analyzes ",
        "Apply ": "applies ",
        "Applies ": "applies ",
        "Compare ": "compares ",
        "Connect ": "connects ",
        "Define ": "defines ",
        "Design ": "designs ",
        "Distinguish ": "distinguishes ",
        "Document ": "documents ",
        "Evaluate ": "evaluates ",
        "Explain how ": "shows how ",
        "Focus on ": "focuses on ",
        "Frame ": "frames ",
        "Identify ": "identifies ",
        "Manage ": "manages ",
        "Map ": "maps ",
        "Protect ": "protects ",
        "Read ": "reads ",
        "Shows ": "shows ",
        "Structure ": "structures ",
        "Study ": "studies ",
        "Teach ": "teaches ",
        "Trace ": "traces ",
        "Translate ": "translates ",
        "Treat ": "treats ",
        "Use ": "uses ",
    }
    matched = False
    for prefix, replacement in replacements.items():
        if text.startswith(prefix):
            text = replacement + text[len(prefix) :]
            matched = True
            break
    if matched:
        return f"**{entry.display_title}** {text}"
    # No verb mapping fit: the frame still leads with a capitalized clause, so
    # insert an em-dash connective rather than abutting the bold noun phrase
    # against a capital letter (which reads as machine-generated).
    return f"**{entry.display_title}** — {text}"


def evidence_packet_sentence(
    entry: TopicEntry,
    text: str,
    *,
    unit_profile: UnitEducationProfile | None = None,
    slot: int = 1,
) -> str:
    rendered = for_topic(entry, text, slot=slot)
    rendered = rendered.replace(", evidence packet:", ", the evidence packet contains", 1)
    if unit_profile is not None:
        rendered = f"{rendered} {unit_lesson_evidence_line(unit_profile, entry.display_title)}"
    return rendered


def student_artifact_sentence(
    entry: TopicEntry,
    text: str,
    *,
    unit_profile: UnitEducationProfile | None = None,
    slot: int = 1,
) -> str:
    rendered = for_topic(entry, text, slot=slot)
    for source, replacement in (
        (", submit a completed **", ", build a **"),
        (", submit an ", ", build an "),
        (", submit a ", ", build a "),
    ):
        rendered = rendered.replace(source, replacement, 1)
    if rendered.startswith("Submit a completed **"):
        rendered = "Build a **" + rendered.removeprefix("Submit a completed **")
    elif rendered.startswith("Submit an "):
        rendered = "Build an " + rendered.removeprefix("Submit an ")
    elif rendered.startswith("Submit a "):
        rendered = "Build a " + rendered.removeprefix("Submit a ")
    if unit_profile is not None:
        rendered = f"{rendered} {unit_lesson_artifact_line(unit_profile, entry.display_title)}"
    return rendered


__all__ = [
    "evidence_packet_sentence",
    "for_topic",
    "lower_first_word",
    "reader_facing_concept",
    "short_title",
    "student_artifact_sentence",
    "topic_reference",
]
