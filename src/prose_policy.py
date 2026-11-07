"""Shared reader-facing prose transforms for AGEINT titles and labels."""

from __future__ import annotations

import re


# Protect literal Markdown before marking visible identifier atoms. In particular,
# a linked title is display prose, but its destination is never rewritten.
_SOURCE_LITERAL_RE = re.compile(
    r"(?<!`)(?P<ticks>`+)(?!`)[\s\S]*?(?<!`)(?P=ticks)(?!`)"
    r"|^[ \t]{0,3}(?P<tildes>~{3,})[^\n]*\n[\s\S]*?"
    r"^[ \t]{0,3}(?P=tildes)~*[ \t]*(?=\n|$)"
    r"|\]\("
    r"|https?://[^\s<>`]+"
    r"|^[ \t]{0,3}\[[^\]\n]+\]:[^\n]*",
    re.MULTILINE,
)
_SOURCE_IDENTIFIER_RE = re.compile(
    r"(?<![\w/.-])(?:"
    r"(?:Executive Order|E\.O\.|EO)\s+(?:No\.\s+)?\d{4,6}"
    r"|\d+\s+FR\s+\d+"
    r"|(?:Intelligence Community Directive|Presidential Policy Directive"
    r"|National Security Decision Directive|National Security Presidential Directive"
    r"|Homeland Security Presidential Directive)\s+(?:No\.\s+)?\d+"
    r"|(?:ICD|PPD|NSDD|NSPD|HSPD)[ -]\d+"
    r"|(?:ISO(?:/IEC)?|ISA/IEC|IEC|ISA)\s+(?:(?:TR|TS|PAS)\s+)?"
    r"\d+(?:-\d+)*(?::\d{4})?"
    r"|Regulation\s+\(EU\)\s+(?:No\s+)?\d+/\d+"
    r"|(?:Unit|institutional identifier)\s+\d+"
    r"|section\s+\d+(?:\.\d+)*(?:\([a-z0-9]+\))*"
    r")(?![\w/-]|\.\d|:\d)",
    re.IGNORECASE,
)


def source_identifier_text(text: str) -> str:
    """Mark source identifiers for display, never quantities or source identity.

    Call only at metadata, source-title, topic-context and annotation rendering
    boundaries, not on raw records or assembled manuscript Markdown. Spelling,
    editions and surrounding caveats are retained; existing code, URLs and link
    destinations are opaque. Institutional unit designations do not substantiate
    claims about that institution's capabilities.
    """
    pieces: list[str] = []
    end = 0
    while literal := _SOURCE_LITERAL_RE.search(text, end):
        literal_end = literal.end()
        if literal[0] == "](":
            # Markdown destinations may contain nested or escaped parentheses.
            depth = 1
            while literal_end < len(text) and depth:
                char = text[literal_end]
                literal_end += 1
                if char == "\\":
                    literal_end = min(literal_end + 1, len(text))
                elif char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
        pieces.append(_SOURCE_IDENTIFIER_RE.sub(lambda match: f"`{match[0]}`", text[end : literal.start()]))
        pieces.append(text[literal.start() : literal_end])
        end = literal_end
    pieces.append(_SOURCE_IDENTIFIER_RE.sub(lambda match: f"`{match[0]}`", text[end:]))
    return "".join(pieces)


def reader_source_title(value: str) -> str:
    """Replace scaffold-oriented wording in contributor-facing source titles."""
    return (
        value.replace("Scaffolding", "Documentation")
        .replace("scaffolding", "documentation")
        .replace("Scaffolds", "Workflows")
        .replace("scaffolds", "workflows")
        .replace("Scaffold", "Workflow")
        .replace("scaffold", "workflow")
    )


__all__ = ["reader_source_title", "source_identifier_text"]
