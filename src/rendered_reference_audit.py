"""Rendered-reference integrity checks for AGEINT output artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Sequence


SUPPORT_DOC_NAMES = {"AGENTS.md", "README.md"}
REFERENCE_DOC_NAMES = {"references.md"}
TITLE_STOPLIST = {"References"}
HARD_CODED_REFERENCE_RE = re.compile(
    r"\b(?:Figure|Fig\.|Section|Sec\.|Equation|Eq\.|Formalism|Chapter)\s+"
    r"(?:[0-9]+(?:\.[0-9]+)*|[IVXLC]+)\b|\bAppendix\s+[A-Z]\b"
)
RAW_LATEX_REF_RE = re.compile(r"\\(?:ref|autoref|cref|Cref|eqref)\{")
UNRESOLVED_TEMPLATE_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}|\[\[(?:SEC|FIG|REF):")

# Bracketed Pandoc citation tokens: ``[@key]`` (optionally ``[@key1; @key2]``).
# Only the bracket form is matched so a bare ``@user`` inside a Markdown URL
# (e.g. ``medium.com/@anil.jain.baba``) is never treated as a citation.
BRACKET_CITATION_RE = re.compile(r"\[@([^\]]+)\]")
# Cross-reference namespaces (handled by pandoc-crossref, not the bib) to skip.
_CROSSREF_PREFIXES = ("sec:", "fig:", "tbl:", "eq:", "lst:")
# BibTeX entry header: ``@misc{key,`` / ``@article{key,`` etc.
_BIB_ENTRY_RE = re.compile(r"^@\w+\{([^,]+),", re.MULTILINE)
# Strong-emphasis spans used to protect authored phrases from title matching.
_BOLD_SPAN_RE = re.compile(r"\*\*(.+?)\*\*|__(.+?)__")


@dataclass(frozen=True)
class TitleRule:
    """A generated section title and the generic reader-facing replacement."""

    title: str
    replacement: str
    kind: str


@dataclass(frozen=True)
class RenderedReferenceViolation:
    """A rendered text line that contains a forbidden reference form."""

    path: Path
    line_number: int
    reason: str
    title: str
    line: str

    def format(self, root: Path | None = None) -> str:
        display = self.path
        if root is not None:
            try:
                display = self.path.relative_to(root)
            except ValueError:
                display = self.path
        title = f" [{self.title}]" if self.title else ""
        return f"{display.as_posix()}:{self.line_number}: {self.reason}{title}: {self.line.strip()}"


def section_title_rules(sections: Iterable[object]) -> tuple[TitleRule, ...]:
    """Return replacement rules for rendered section titles."""

    rules: list[TitleRule] = []
    for section in sections:
        title = str(getattr(section, "title", "")).strip()
        kind = str(getattr(section, "kind", "")).strip()
        if not _title_is_scannable(title):
            continue
        rules.append(TitleRule(title=title, replacement=_replacement_for_kind(kind, title), kind=kind))
    return _dedupe_rules(rules)


def collect_rendered_section_titles(output_root: Path) -> tuple[str, ...]:
    """Collect generated section titles from rendered manuscript headings."""

    manuscript = output_root / "manuscript"
    titles: list[str] = []
    if not manuscript.is_dir():
        return ()
    for path in sorted(manuscript.rglob("*.md")):
        if _is_support_or_reference_doc(path):
            continue
        in_code = False
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code = not in_code
                continue
            if in_code or not stripped.startswith("# "):
                continue
            title = _strip_markdown_heading(stripped)
            if _title_is_scannable(title):
                titles.append(title)
    return tuple(dict.fromkeys(titles))


def sanitize_rendered_section_title_mentions(text: str, rules: Iterable[TitleRule]) -> str:
    """Remove generated section titles from non-structural Markdown prose."""

    sorted_rules = _sort_rules(rules)
    if not sorted_rules:
        return text
    lines: list[str] = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            lines.append(line)
            continue
        if in_code or _is_markdown_structural_line(stripped):
            lines.append(line)
            continue
        sanitized = _neutralize_title_mentions(line, sorted_rules)
        lines.append(_clean_generic_reference_grammar(sanitized))
    if text.endswith("\n"):
        return "\n".join(lines) + "\n"
    return "\n".join(lines)


def iter_rendered_text_files(output_root: Path) -> list[Path]:
    """Return reader-facing rendered text artifacts to audit."""

    files: list[Path] = []
    manuscript = output_root / "manuscript"
    if manuscript.is_dir():
        files.extend(
            path
            for path in sorted(manuscript.rglob("*.md"))
            if not _is_support_or_reference_doc(path)
        )
    web = output_root / "web"
    if web.is_dir():
        files.extend(sorted(web.glob("*.html")))
        combined_web = web / "_combined_manuscript.md"
        if combined_web.is_file():
            files.append(combined_web)
    pdf = output_root / "pdf"
    if pdf.is_dir():
        for name in ("_combined_manuscript.md", "_combined_manuscript.tex"):
            path = pdf / name
            if path.is_file():
                files.append(path)
    return sorted(dict.fromkeys(files))


def load_bib_keys(output_root: Path) -> frozenset[str]:
    """Return the set of citation keys defined across the manuscript ``.bib`` files.

    Keys are read from every ``manuscript/references-*.bib`` entry header so the
    audit can flag any rendered ``[@key]`` that resolves to no bibliography
    entry (a dangling citation a generator might emit after a key renumber).
    """
    keys: set[str] = set()
    bib_dir = output_root / "manuscript"
    if not bib_dir.is_dir():
        return frozenset()
    for bib in sorted(bib_dir.glob("references-*.bib")):
        text = bib.read_text(encoding="utf-8")
        keys.update(match.group(1).strip() for match in _BIB_ENTRY_RE.finditer(text))
    return frozenset(keys)


def _unresolved_citation_keys(line: str, defined: frozenset[str]) -> list[str]:
    """Return bracketed citation keys on ``line`` that are not defined in the bib.

    Cross-reference namespaces (``@sec:``/``@fig:``/...) are skipped because they
    are resolved by pandoc-crossref rather than the bibliography. A ``[@key]``
    group may carry several semicolon-separated keys, each validated separately.
    """
    if not defined:
        return []
    unresolved: list[str] = []
    for group in BRACKET_CITATION_RE.findall(line):
        for token in re.split(r"[;,]", group):
            key = token.strip().lstrip("@").strip()
            if not key or key.lower().startswith(_CROSSREF_PREFIXES):
                continue
            # Ignore locator suffixes (``[@key, p. 4]`` → key already isolated).
            key = key.split()[0]
            if key and key not in defined:
                unresolved.append(key)
    return unresolved


def audit_rendered_references(output_root: Path) -> list[RenderedReferenceViolation]:
    """Find hard-coded rendered references and disallowed section-title mentions."""

    titles = collect_rendered_section_titles(output_root)
    title_patterns = [(title, _title_pattern(title)) for title in sorted(titles, key=len, reverse=True)]
    known_titles = frozenset(titles)
    bib_keys = load_bib_keys(output_root)
    violations: list[RenderedReferenceViolation] = []
    for path in iter_rendered_text_files(output_root):
        suffix = path.suffix.lower()
        in_code = False
        in_html_figure = False
        in_html_heading = False
        in_html_nav = False
        in_html_table = False
        in_tex_table = False
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if suffix == ".md" and stripped.startswith("```"):
                in_code = not in_code
                continue
            if suffix == ".html":
                if re.search(r"<nav\b", stripped):
                    in_html_nav = True
                if re.search(r"<h[1-6]\b", stripped):
                    in_html_heading = True
                if re.search(r"<(?:figure|figcaption)\b", stripped):
                    in_html_figure = True
                if re.search(r"<(?:table|thead|tbody|tr|td|th|colgroup|col)\b", stripped):
                    in_html_table = True
            if suffix == ".tex":
                if re.match(r"\\begin\{(?:longtable|tabular|tabularx)\}", stripped):
                    in_tex_table = True
                if re.match(r"\\end\{(?:longtable|tabular|tabularx)\}", stripped):
                    in_tex_table = False
                    continue
            if _line_allows_titles(
                path,
                stripped,
                in_code=in_code,
                in_html_figure=in_html_figure,
                in_html_heading=in_html_heading,
                in_html_nav=in_html_nav,
                in_html_table=in_html_table,
                in_tex_table=in_tex_table,
            ):
                if suffix == ".html":
                    if "</nav>" in stripped:
                        in_html_nav = False
                    if re.search(r"</h[1-6]>", stripped):
                        in_html_heading = False
                    if "</figure>" in stripped or "</figcaption>" in stripped:
                        in_html_figure = False
                    if "</table>" in stripped:
                        in_html_table = False
                continue
            if suffix != ".html" and (match := HARD_CODED_REFERENCE_RE.search(line)):
                violations.append(
                    RenderedReferenceViolation(path, line_number, "hard-coded numbered reference", match.group(0), line)
                )
            if suffix != ".tex" and (match := RAW_LATEX_REF_RE.search(line)):
                violations.append(
                    RenderedReferenceViolation(path, line_number, "raw LaTeX reference", match.group(0), line)
                )
            if match := UNRESOLVED_TEMPLATE_RE.search(line):
                violations.append(
                    RenderedReferenceViolation(path, line_number, "unresolved reference token", match.group(0), line)
                )
            if suffix == ".md":
                for key in _unresolved_citation_keys(line, bib_keys):
                    violations.append(
                        RenderedReferenceViolation(
                            path, line_number, "unresolved citation key", f"@{key}", line
                        )
                    )
            protected = _authored_bold_ranges(line, known_titles)
            for title, pattern in title_patterns:
                if any(not _within_ranges(m.start(), protected) for m in pattern.finditer(line)):
                    violations.append(
                        RenderedReferenceViolation(path, line_number, "generated title in prose", title, line)
                    )
                    break
            if suffix == ".html":
                if "</nav>" in stripped:
                    in_html_nav = False
                if re.search(r"</h[1-6]>", stripped):
                    in_html_heading = False
                if "</figure>" in stripped or "</figcaption>" in stripped:
                    in_html_figure = False
                if "</table>" in stripped:
                    in_html_table = False
    return violations


def _dedupe_rules(rules: Iterable[TitleRule]) -> tuple[TitleRule, ...]:
    deduped: dict[str, TitleRule] = {}
    for rule in rules:
        deduped.setdefault(rule.title, rule)
    return tuple(deduped.values())


def _sort_rules(rules: Iterable[TitleRule]) -> list[TitleRule]:
    return sorted(_dedupe_rules(rules), key=lambda rule: len(rule.title), reverse=True)


def _replacement_for_kind(kind: str, title: str) -> str:
    if kind == "chapter":
        return "the module"
    if kind == "part":
        return "the unit"
    if kind == "appendix":
        return "the current appendix"
    if kind == "bibliography":
        return "the bibliography appendix"
    if title == "Abstract":
        return "the abstract"
    if title == "Curriculum Orientation":
        return "the orientation section"
    return "the current section"


def _authored_bold_ranges(line: str, known_titles: frozenset[str]) -> list[tuple[int, int]]:
    """Char ranges of ``**...**`` spans whose inner text is NOT a known section title (authored woven lesson titles), protected from matching."""
    ranges: list[tuple[int, int]] = []
    for match in _BOLD_SPAN_RE.finditer(line):
        inner = (match.group(1) or match.group(2) or "").strip()
        if inner and inner not in known_titles:
            ranges.append((match.start(), match.end()))
    return ranges


def _within_ranges(index: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= index < end for start, end in ranges)


def _neutralize_plain_text(text: str, rules: Sequence[TitleRule]) -> str:
    """Replace bare (non-emphasised) section-title cross-references with generic
    phrases. Titles inside authored ``**bold**`` spans are handled by the caller
    (the topic-cluster generator bolds its lesson-title list so it is preserved);
    bare matches here are genuine cross-references and are always neutralised."""
    for rule in rules:
        text = _title_pattern(rule.title).sub(rule.replacement, text)
    return text


def _neutralize_title_mentions(line: str, rules: Sequence[TitleRule]) -> str:
    """Neutralise section-title cross-references in one line, leaving authored
    bold spans verbatim (neutralised only when the whole span is a known title)."""
    rule_by_title = {rule.title: rule for rule in rules}
    pieces: list[str] = []
    cursor = 0
    for match in _BOLD_SPAN_RE.finditer(line):
        pieces.append(_neutralize_plain_text(line[cursor : match.start()], rules))
        inner = (match.group(1) or match.group(2) or "").strip()
        rule = rule_by_title.get(inner)
        pieces.append(rule.replacement if rule is not None else match.group(0))
        cursor = match.end()
    pieces.append(_neutralize_plain_text(line[cursor:], rules))
    return "".join(pieces)


def _title_pattern(title: str) -> re.Pattern[str]:
    escaped = re.escape(title)
    return re.compile(rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])")


def _title_is_scannable(title: str) -> bool:
    return len(title) >= 4 and title not in TITLE_STOPLIST


def _strip_markdown_heading(line: str) -> str:
    text = re.sub(r"^#+\s+", "", line).strip()
    text = re.sub(r"\s+\{#sec:[^}]+\}\s*$", "", text).strip()
    text = re.sub(r"[*_`]+", "", text).strip()
    return text


def _is_support_or_reference_doc(path: Path) -> bool:
    return path.name in SUPPORT_DOC_NAMES or path.name in REFERENCE_DOC_NAMES


def _is_markdown_structural_line(stripped: str) -> bool:
    return (
        not stripped
        or stripped.startswith("#")
        or stripped.startswith("|")
        or re.fullmatch(r"\[@[^\]]+\](?:,\s*\[@[^\]]+\]|\s*)*", stripped) is not None
    )


def _line_allows_titles(
    path: Path,
    stripped: str,
    *,
    in_code: bool,
    in_html_figure: bool,
    in_html_heading: bool,
    in_html_nav: bool,
    in_html_table: bool,
    in_tex_table: bool,
) -> bool:
    if in_code:
        return True
    suffix = path.suffix.lower()
    if suffix == ".md":
        return _is_markdown_structural_line(stripped)
    if suffix == ".html":
        return (
            in_html_figure
            or in_html_heading
            or in_html_nav
            or in_html_table
            or _is_html_structural_line(stripped)
        )
    if suffix == ".tex":
        return in_tex_table or _is_tex_structural_line(stripped)
    return True


def _is_html_structural_line(stripped: str) -> bool:
    return bool(
        not stripped
        or re.match(r"</?(?:h[1-6]|title|table|thead|tbody|tr|th|td|colgroup|col)\b", stripped)
        or stripped.startswith("<!DOCTYPE")
        or stripped.startswith("<html")
        or stripped.startswith("</html")
        or stripped.startswith("<head")
        or stripped.startswith("</head")
        or stripped.startswith("<body")
        or stripped.startswith("</body")
        or stripped.startswith("<meta")
        or stripped.startswith("<style")
        or stripped.startswith("</style")
    )


def _is_tex_structural_line(stripped: str) -> bool:
    return bool(
        not stripped
        or stripped.startswith("%")
        or re.match(r"\\(?:part|chapter|section|subsection|subsubsection|paragraph)\*?\{", stripped)
        or stripped.startswith(r"\label{")
        or stripped.startswith(r"\hypertarget{")
        or stripped.startswith(r"\addcontentsline")
        or stripped.startswith(r"\begin{document}")
        or stripped.startswith(r"\end{document}")
    )


def _clean_generic_reference_grammar(line: str) -> str:
    replacements = (
        ("The the module", "The module"),
        ("the the module", "the module"),
        ("a the module", "a module"),
        ("an the module", "a module"),
        ("The the unit", "The unit"),
        ("the the unit", "the unit"),
        ("a the unit", "a unit"),
        ("an the unit", "a unit"),
        ("The the current appendix", "The current appendix"),
        ("the the current appendix", "the current appendix"),
        ("the broader the unit thread", "the broader unit thread"),
        ("Minimum the module submission", "Minimum module submission"),
        ("Minimum the unit submission", "Minimum unit submission"),
        ("The module matched profile", "The module profile"),
        ("The unit matched profile", "The unit profile"),
        ("the module matched profile", "the module profile"),
        ("the unit matched profile", "the unit profile"),
        ("Each the module", "Each module"),
        ("Each the unit", "Each unit"),
        ("Use this the module", "Use this module"),
        ("Use this the unit", "Use this unit"),
        ("This unit deliverables", "This unit's deliverables"),
        ("This unit safety gates", "This unit's safety gates"),
        ("one the unit", "one unit"),
        ("the current appendix methods appendix", "current appendix"),
    )
    for old, new in replacements:
        line = line.replace(old, new)
    if line.startswith("the module"):
        line = "This module" + line[len("the module") :]
    if line.startswith("the unit"):
        line = "This unit" + line[len("the unit") :]
    if line.startswith("the current appendix"):
        line = "This appendix" + line[len("the current appendix") :]
    return line
