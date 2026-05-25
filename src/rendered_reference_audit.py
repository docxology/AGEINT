"""Rendered-reference integrity checks for AGEINT output artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


SUPPORT_DOC_NAMES = {"AGENTS.md", "README.md"}
REFERENCE_DOC_NAMES = {"references.md"}
TITLE_STOPLIST = {"References"}
HARD_CODED_REFERENCE_RE = re.compile(
    r"\b(?:Figure|Fig\.|Section|Sec\.|Equation|Eq\.|Formalism|Chapter)\s+"
    r"(?:[0-9]+(?:\.[0-9]+)*|[IVXLC]+)\b|\bAppendix\s+[A-Z]\b"
)
RAW_LATEX_REF_RE = re.compile(r"\\(?:ref|autoref|cref|Cref|eqref)\{")
UNRESOLVED_TEMPLATE_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}|\[\[(?:SEC|FIG|REF):")


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
        sanitized = line
        for rule in sorted_rules:
            sanitized = _replace_title(sanitized, rule.title, rule.replacement)
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


def audit_rendered_references(output_root: Path) -> list[RenderedReferenceViolation]:
    """Find hard-coded rendered references and disallowed section-title mentions."""

    titles = collect_rendered_section_titles(output_root)
    title_patterns = [(title, _title_pattern(title)) for title in sorted(titles, key=len, reverse=True)]
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
            if match := HARD_CODED_REFERENCE_RE.search(line):
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
            for title, pattern in title_patterns:
                if pattern.search(line):
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


def _replace_title(line: str, title: str, replacement: str) -> str:
    line = line.replace(f"**{title}**", replacement)
    line = line.replace(f"__{title}__", replacement)
    return _title_pattern(title).sub(replacement, line)


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
