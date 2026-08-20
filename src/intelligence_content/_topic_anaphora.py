"""Title keyword retention and grammatical anaphora for topic-lesson fields.

Extracted from _11_part.py so that module stays comfortably below the 500-line cap.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from .topic_lesson_voice import short_title


@dataclass
class AnchorState:
    """Tracks how many title references a lesson body has already emitted."""

    slot: int = 0


# Articles and possessives that may already precede a title token; when present
# we emit a bare noun so we never produce "the this topic".
_LEADING_DETERMINERS = ("the", "a", "an", "this", "that", "its", "their", "each")

# Bare nouns used after a determiner (e.g. "the topic artifact"). These carry no
# title keyword, so they are only used on the SECOND+ occurrence within a single
# field, after that field already anchored the title keywords via short form.
_BARE_NOUNS = ("topic", "lesson topic", "subject")

# Standalone anaphora used after a determiner is absent and the field already
# carries title keywords from an earlier short-form mention.
_STANDALONE = ("this topic", "the same topic", "this subject")

_TITLE_KEYWORD_STOPWORDS = {
    "about", "after", "against", "agent", "agentic", "analysis", "and",
    "from", "into", "module", "source", "that", "the", "their", "through",
    "using", "with",
}


def title_keywords(title: str) -> set[str]:
    """Title keywords used by the reader-quality anchor gate (mirrors the test)."""
    words = {
        word
        for word in re.findall(r"[a-z0-9]+", title.lower())
        if len(word) >= 4 and word not in _TITLE_KEYWORD_STOPWORDS
    }
    return words or set(re.findall(r"[a-z0-9]+", title.lower()))


def keeps_title_keywords(candidate: str, title: str) -> bool:
    """True when ``candidate`` retains enough title keywords to anchor a field."""
    keywords = title_keywords(title)
    haystack = set(re.findall(r"[a-z0-9]+", candidate.lower()))
    return len(haystack & keywords) >= min(2, len(keywords))


def anaphor(before: str, anchor: AnchorState) -> str:
    """Choose a grammatical anaphor for a repeated title within one field."""
    anchor.slot += 1
    trimmed = before.rstrip()
    last_word = trimmed.rsplit(" ", 1)[-1].lower() if trimmed else ""
    if last_word in _LEADING_DETERMINERS:
        return _BARE_NOUNS[anchor.slot % len(_BARE_NOUNS)]
    reference = _STANDALONE[anchor.slot % len(_STANDALONE)]
    at_sentence_start = (not trimmed) or trimmed[-1] in ".!?:*"
    if at_sentence_start:
        return reference[0].upper() + reference[1:]
    return reference


def anaphorize_field(
    display_title: str,
    field: str,
    *,
    anchor: AnchorState,
    forbidden: frozenset[str] | set[str] = frozenset(),
) -> str:
    """Replace repeated bold full titles in one body field with shorter references.

    The first title occurrence WITHIN a field becomes the bolded short form so
    the field keeps the lesson's title keywords (required by the reader-quality
    anchor gate) while shedding the long colon tail. Any further occurrences in
    the same field — the source of the field-to-field "stutter" — collapse to a
    grammar-aware anaphor. This runs after frame resolution so it covers every
    title-injection site uniformly, and it stops the generator restating the
    full bold title ~9 times per lesson.
    """
    token = f"**{display_title}**"
    if token not in field:
        return field
    parts = field.split(token)
    rebuilt = parts[0]
    compact = short_title(display_title)
    # The anchor gate requires each field to keep the lesson's title keywords. If
    # the short form drops them, or collides with a chapter/part title that the
    # section-title sanitiser would collapse to "the module", fall back to the
    # full title for the field's first mention so the field still anchors.
    if not keeps_title_keywords(compact, display_title) or compact.casefold() in forbidden:
        compact = display_title
    field_has_anchor = False
    for tail in parts[1:]:
        if not field_has_anchor:
            # First mention in this field: keep title keywords via short form.
            field_has_anchor = True
            anchor.slot += 1
            rebuilt += f"**{compact}**" + tail
            continue
        rebuilt += anaphor(rebuilt, anchor) + tail
    return rebuilt


def misconception_line(
    display_title: str,
    misconception: str,
    *,
    forbidden: frozenset[str] | set[str] = frozenset(),
) -> str:
    """Render the misconception sentence, anchoring the topic only once.

    Risk-category templates already name the topic; keyword-routed and fallback
    templates do not, so a short-form prefix supplies the title keywords the
    field-anchor gate needs without producing the old double-title stutter.
    """
    text = misconception.strip().rstrip(".")
    inner_anchored = (
        f"**{display_title}**" in text
        or display_title in text
        or keeps_title_keywords(text, display_title)
    )
    if inner_anchored:
        return f"Correct the misconception {text}."
    compact = short_title(display_title)
    if not keeps_title_keywords(compact, display_title) or compact.casefold() in forbidden:
        compact = display_title
    return f"Correct the misconception about **{compact}**: {text}."
