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

BRACKET_CITATION_RE = re.compile(r"\[@([^\]]+)\]")
_CROSSREF_PREFIXES = ("sec:", "fig:", "tbl:", "eq:", "lst:")
_BIB_ENTRY_RE = re.compile(r"^@\w+\{([^,]+),", re.MULTILINE)
_TEX_HEADING_COMMAND_RE = re.compile(r"\\(?:part|chapter|section|subsection|subsubsection|paragraph)\*?\{")
_SECTION_LABEL_RE = re.compile(r"\{#(sec:[A-Za-z0-9_-]+)\}")
_REFERENCE_GROUP_RE = re.compile(r"\[@([^\]\n]*)(?:\]|$)")


@dataclass(frozen=True)
class TitleRule:
    """A section title and its label-backed navigation replacement."""

    title: str
    replacement: str
    kind: str
    section_label: str = ""


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
    """Return navigation rules using the manifest's actual section labels."""

    rules: list[TitleRule] = []
    for section in sections:
        title = str(getattr(section, "title", "")).strip()
        kind = str(getattr(section, "kind", "")).strip()
        if not _title_is_scannable(title):
            continue
        label = str(getattr(section, "section_label", "")).strip()
        rules.append(TitleRule(title=title, replacement=f"[@{label}]" if label else "", kind=kind, section_label=label))
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
    """Normalize explicit navigation only; preserve domain and source names."""

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
        lines.append(_normalize_navigation(line, sorted_rules))
    if text.endswith("\n"):
        return "\n".join(lines) + "\n"
    return "\n".join(lines)


def iter_rendered_text_files(output_root: Path) -> list[Path]:
    """Return reader-facing rendered text artifacts to audit."""

    files: list[Path] = []
    manuscript = output_root / "manuscript"
    if manuscript.is_dir():
        files.extend(path for path in sorted(manuscript.rglob("*.md")) if not _is_support_or_reference_doc(path))
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
    """Find malformed references and unlabelled navigational title mentions."""

    titles = collect_rendered_section_titles(output_root)
    title_patterns = [(title, _navigation_pattern(title)) for title in sorted(titles, key=len, reverse=True)]
    section_labels = _defined_section_labels(output_root / "manuscript")
    bib_keys = load_bib_keys(output_root)
    violations: list[RenderedReferenceViolation] = []
    for path in iter_rendered_text_files(output_root):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        in_code = False
        in_html_figure = False
        in_html_heading = False
        in_html_nav = False
        in_html_table = False
        in_tex_table = False
        tex_heading_depth = 0
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
            in_tex_heading, next_tex_heading_depth = _tex_heading_line_state(stripped, tex_heading_depth)
            if suffix == ".md" and not in_code:
                prose = re.sub(r"`[^`\n]*`", "", line)
                for reason, label in _section_reference_issues(prose, section_labels):
                    violations.append(RenderedReferenceViolation(path, line_number, reason, label, line))
            if _line_allows_titles(
                path,
                stripped,
                in_code=in_code,
                in_html_figure=in_html_figure,
                in_html_heading=in_html_heading,
                in_html_nav=in_html_nav,
                in_html_table=in_html_table,
                in_tex_table=in_tex_table,
                in_tex_heading=in_tex_heading,
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
                if suffix == ".tex":
                    tex_heading_depth = next_tex_heading_depth
                continue
            if suffix != ".html" and (match := HARD_CODED_REFERENCE_RE.search(line)):
                violations.append(RenderedReferenceViolation(path, line_number, "hard-coded numbered reference", match.group(0), line))
            if suffix != ".tex" and (match := RAW_LATEX_REF_RE.search(line)):
                violations.append(RenderedReferenceViolation(path, line_number, "raw LaTeX reference", match.group(0), line))
            if match := UNRESOLVED_TEMPLATE_RE.search(line):
                violations.append(RenderedReferenceViolation(path, line_number, "unresolved reference token", match.group(0), line))
            if suffix == ".md":
                for key in _unresolved_citation_keys(line, bib_keys):
                    violations.append(RenderedReferenceViolation(path, line_number, "unresolved citation key", f"@{key}", line))
            for title, pattern in title_patterns:
                if pattern.search(line):
                    violations.append(RenderedReferenceViolation(path, line_number, "unlabelled section navigation", title, line))
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
            if suffix == ".tex":
                tex_heading_depth = next_tex_heading_depth
    return violations


def _defined_section_labels(manuscript: Path) -> set[str]:
    labels: set[str] = set()
    for path in manuscript.rglob("*.md"):
        fence = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                marker = stripped[:3]
                if not fence:
                    fence = marker
                elif fence == marker:
                    fence = ""
                continue
            if not fence:
                labels.update(_SECTION_LABEL_RE.findall(re.sub(r"`[^`\n]*`", "", line)))
    return labels


def _section_reference_issues(prose: str, labels: set[str]) -> Iterable[tuple[str, str]]:
    for match in _REFERENCE_GROUP_RE.finditer(prose):
        for token in match.group(1).split(";"):
            label = token.strip().lstrip("@")
            if not label.startswith("sec:"):
                continue
            if not match.group(0).endswith("]") or not re.fullmatch(r"sec:[A-Za-z0-9_-]+", label):
                yield "malformed section reference", label
            elif label not in labels:
                yield "unresolved section reference", label


def _dedupe_rules(rules: Iterable[TitleRule]) -> tuple[TitleRule, ...]:
    deduped: dict[str, TitleRule] = {}
    for rule in rules:
        deduped.setdefault(rule.title, rule)
    return tuple(deduped.values())


def _sort_rules(rules: Iterable[TitleRule]) -> list[TitleRule]:
    return sorted(_dedupe_rules(rules), key=lambda rule: len(rule.title), reverse=True)


def _navigation_pattern(title: str) -> re.Pattern[str]:
    """Match explicit reading directions, not bare or quoted source titles."""
    opening = r"(?:\*\*|__|<strong>|<em>|\\textbf\{|\\emph\{)?"
    closing = r"(?:\*\*|__|</strong>|</em>|\})?"
    return re.compile(
        rf"(?P<lead>\b(?:[Ss]ee|[Cc]onsult|[Rr]efer to|[Rr]eturn to|[Cc]ontinue in))\s+"
        rf"{opening}{re.escape(title)}{closing}"
        r"(?=\s+(?:for|before|after|to)\b|[.,;:]|$)"
    )


def _normalize_navigation(line: str, rules: Sequence[TitleRule]) -> str:
    for rule in rules:
        if re.fullmatch(r"sec:[A-Za-z0-9_-]+", rule.section_label):
            line = _navigation_pattern(rule.title).sub(
                lambda match: f"{match.group('lead')} [@{rule.section_label}]", line
            )
    return line


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
    return not stripped or stripped.startswith("#") or stripped.startswith("|") or re.fullmatch(r"\[@[^\]]+\](?:,\s*\[@[^\]]+\]|\s*)*", stripped) is not None


def _line_allows_titles(
    path: Path, stripped: str, *, in_code: bool, in_html_figure: bool, in_html_heading: bool, in_html_nav: bool, in_html_table: bool, in_tex_table: bool, in_tex_heading: bool
) -> bool:
    if in_code:
        return True
    suffix = path.suffix.lower()
    if suffix == ".md":
        return _is_markdown_structural_line(stripped)
    if suffix == ".html":
        return in_html_figure or in_html_heading or in_html_nav or in_html_table or _is_html_structural_line(stripped)
    if suffix == ".tex":
        return in_tex_table or in_tex_heading or _is_tex_structural_line(stripped)
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
        or _TEX_HEADING_COMMAND_RE.match(stripped)
        or stripped.startswith(r"\label{")
        or stripped.startswith(r"\hypertarget{")
        or stripped.startswith(r"\addcontentsline")
        or stripped.startswith(r"\begin{document}")
        or stripped.startswith(r"\end{document}")
    )


def _tex_heading_line_state(stripped: str, current_depth: int) -> tuple[bool, int]:
    """Return whether this TeX line is part of a wrapped heading command."""

    starts_heading = bool(_TEX_HEADING_COMMAND_RE.match(stripped))
    if current_depth <= 0 and not starts_heading:
        return False, 0
    next_depth = current_depth + _unescaped_brace_delta(stripped)
    return True, max(next_depth, 0)


def _unescaped_brace_delta(text: str) -> int:
    text = re.sub(r"\\.", "", text)
    return text.count("{") - text.count("}")


