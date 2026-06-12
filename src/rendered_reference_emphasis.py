"""Track authored emphasis spans in rendered reference-audit inputs."""

from __future__ import annotations

import html
import re

_MARKDOWN_EMPHASIS_RE = re.compile(r"\*\*(.+?)\*\*|__(.+?)__")
_HTML_EMPHASIS_OPEN_RE = re.compile(r"<(strong|b)>", re.IGNORECASE)
_TEX_EMPHASIS_OPEN_RE = re.compile(r"\\(?:textbf|emph)\{")


def authored_emphasis_ranges(
    line: str,
    known_titles: frozenset[str],
    suffix: str,
    in_html_span: bool,
    in_tex_span: bool,
) -> tuple[list[tuple[int, int]], bool, bool]:
    ranges = _markdown_emphasis_ranges(line, known_titles)
    if suffix == ".html":
        html_ranges, in_html_span = _html_emphasis_ranges(line, known_titles, in_html_span)
        ranges.extend(html_ranges)
    if suffix == ".tex":
        tex_ranges, in_tex_span = _tex_emphasis_ranges(line, known_titles, in_tex_span)
        ranges.extend(tex_ranges)
    return ranges, in_html_span, in_tex_span


def _markdown_emphasis_ranges(line: str, known_titles: frozenset[str]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for match in _MARKDOWN_EMPHASIS_RE.finditer(line):
        inner = next((group for group in match.groups() if group), "").strip()
        if inner and inner not in known_titles:
            ranges.append((match.start(), match.end()))
    return ranges


def _html_emphasis_ranges(
    line: str,
    known_titles: frozenset[str],
    in_span: bool,
) -> tuple[list[tuple[int, int]], bool]:
    ranges: list[tuple[int, int]] = []
    lower = line.lower()
    pos = _protect_open_html_span(line, lower, ranges, in_span)
    if pos is None:
        return ranges, True
    while match := _HTML_EMPHASIS_OPEN_RE.search(line, pos):
        tag = match.group(1).lower()
        close_tag = f"</{tag}>"
        close = lower.find(close_tag, match.end())
        if close < 0:
            ranges.append((match.start(), len(line)))
            return ranges, True
        inner = _clean_html_inner(line[match.end() : close])
        if inner and inner not in known_titles:
            ranges.append((match.start(), close + len(close_tag)))
        pos = close + len(close_tag)
    return ranges, False


def _protect_open_html_span(
    line: str,
    lower: str,
    ranges: list[tuple[int, int]],
    in_span: bool,
) -> int | None:
    if not in_span:
        return 0
    strong = lower.find("</strong>")
    bold = lower.find("</b>")
    closes = [close for close in (strong, bold) if close >= 0]
    if not closes:
        ranges.append((0, len(line)))
        return None
    close = min(closes)
    end = close + (9 if lower.startswith("</strong>", close) else 4)
    ranges.append((0, end))
    return end


def _clean_html_inner(inner: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()


def _tex_emphasis_ranges(
    line: str,
    known_titles: frozenset[str],
    in_span: bool,
) -> tuple[list[tuple[int, int]], bool]:
    ranges: list[tuple[int, int]] = []
    pos = _protect_open_tex_span(line, ranges, in_span)
    if pos is None:
        return ranges, True
    for match in _TEX_EMPHASIS_OPEN_RE.finditer(line, pos):
        close = line.find("}", match.end())
        if close < 0:
            ranges.append((match.start(), len(line)))
            return ranges, True
        inner = line[match.end() : close].strip()
        if inner and inner not in known_titles:
            ranges.append((match.start(), close + 1))
    return ranges, False


def _protect_open_tex_span(
    line: str,
    ranges: list[tuple[int, int]],
    in_span: bool,
) -> int | None:
    if not in_span:
        return 0
    close = line.find("}")
    if close < 0:
        ranges.append((0, len(line)))
        return None
    ranges.append((0, close + 1))
    return close + 1


__all__ = ["authored_emphasis_ranges"]
