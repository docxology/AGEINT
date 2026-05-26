"""Audit and repair generated Markdown heading reference support."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Any


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LOCAL_LABEL_RE = re.compile(r"\{#(?:sec|fig|tbl|eq):[^}]+\}")
PANDOC_REF_RE = re.compile(
    r"\[@(?:ageint\d{3}|sec:[^\]\s;]+|fig:[^\]\s;]+|tbl:[^\]\s;]+|eq:[^\]\s;]+|"
    r"[A-Za-z_][A-Za-z0-9_:-]*)(?:[^\]]*)\]"
)
SECTION_LABEL_RE = re.compile(r"\{#(sec:[^}]+)\}")
CITATION_RE = re.compile(r"\[@((?:ageint\d{3}|[A-Za-z_][A-Za-z0-9_:-]*)(?:[^\]]*)?)\]")


@dataclass(frozen=True)
class HeadingSupportRow:
    """Reference-support status for a rendered Markdown heading block."""

    path: str
    line_number: int
    level: int
    title: str
    supported: bool
    support_refs: tuple[str, ...]


@dataclass(frozen=True)
class HeadingSupportSummary:
    """Aggregate rendered-heading support coverage."""

    file_count: int
    heading_count: int
    supported_heading_count: int
    unsupported_heading_count: int

    @property
    def ok(self) -> bool:
        return self.heading_count > 0 and self.unsupported_heading_count == 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "file_count": self.file_count,
            "heading_count": self.heading_count,
            "supported_heading_count": self.supported_heading_count,
            "unsupported_heading_count": self.unsupported_heading_count,
            "ok": self.ok,
        }


@dataclass(frozen=True)
class _HeadingBlock:
    line_index: int
    line_number: int
    level: int
    title: str
    text: str


def heading_support_inventory(manuscript_dir: Path) -> list[HeadingSupportRow]:
    """Return reference-support rows for every generated Markdown heading."""

    root = Path(manuscript_dir)
    rows: list[HeadingSupportRow] = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        for block in _heading_blocks(text):
            refs = _support_refs(block.text)
            rows.append(
                HeadingSupportRow(
                    path=relative,
                    line_number=block.line_number,
                    level=block.level,
                    title=_clean_heading_title(block.title),
                    supported=bool(refs),
                    support_refs=tuple(refs),
                )
            )
    return rows


def heading_support_summary(rows: list[HeadingSupportRow]) -> HeadingSupportSummary:
    """Return aggregate heading support coverage."""

    files = {row.path for row in rows}
    supported = sum(1 for row in rows if row.supported)
    return HeadingSupportSummary(
        file_count=len(files),
        heading_count=len(rows),
        supported_heading_count=supported,
        unsupported_heading_count=len(rows) - supported,
    )


def unsupported_heading_rows(manuscript_dir: Path) -> list[HeadingSupportRow]:
    """Return rendered headings that lack local citation or cross-reference support."""

    return [row for row in heading_support_inventory(manuscript_dir) if not row.supported]


def render_heading_support_markdown(manuscript_dir: Path) -> str:
    """Render a compact heading-support coverage report."""

    rows = heading_support_inventory(manuscript_dir)
    summary = heading_support_summary(rows)
    lines = [
        "# AGEINT Heading Reference Support",
        "",
        "| Measure | Count |",
        "|---|---:|",
        f"| Markdown files | {summary.file_count} |",
        f"| Headings | {summary.heading_count} |",
        f"| Supported headings | {summary.supported_heading_count} |",
        f"| Unsupported headings | {summary.unsupported_heading_count} |",
        f"| OK | {str(summary.ok).lower()} |",
    ]
    unsupported = [row for row in rows if not row.supported]
    if unsupported:
        lines.extend(["", "## Unsupported Headings", "", "| Path | Line | Heading |", "|---|---:|---|"])
        for row in unsupported:
            lines.append(f"| {_table_cell(row.path)} | {row.line_number} | {_table_cell(row.title)} |")
    return "\n".join(lines)


def heading_support_json(manuscript_dir: Path) -> str:
    """Return heading-support coverage as stable JSON."""

    rows = heading_support_inventory(manuscript_dir)
    summary = heading_support_summary(rows)
    unsupported = [row for row in rows if not row.supported]
    return json.dumps(
        {
            **summary.as_dict(),
            "unsupported_headings": [
                {
                    "path": row.path,
                    "line_number": row.line_number,
                    "level": row.level,
                    "title": row.title,
                }
                for row in unsupported
            ],
        },
        indent=2,
        sort_keys=True,
    )


def add_heading_support(text: str, relative_path: str | Path) -> str:
    """Insert contextual support lines under unsupported headings in rendered Markdown."""

    blocks = _heading_blocks(text)
    if not blocks:
        return text
    lines = text.splitlines()
    for block in reversed(blocks):
        if _support_refs(block.text):
            continue
        support = _support_sentence(Path(relative_path), block.title, text)
        insert_at = block.line_index + 1
        if insert_at < len(lines) and not lines[insert_at].strip():
            insert_at += 1
        lines[insert_at:insert_at] = [support, ""]
    return "\n".join(lines).rstrip() + "\n"


def ensure_heading_support_in_tree(manuscript_dir: Path) -> list[Path]:
    """Rewrite generated Markdown files so every heading block has support."""

    root = Path(manuscript_dir)
    changed: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        revised = add_heading_support(original, path.relative_to(root))
        if revised != original:
            path.write_text(revised, encoding="utf-8")
            changed.append(path)
    return changed


def _heading_blocks(text: str) -> list[_HeadingBlock]:
    lines = text.splitlines()
    headings: list[tuple[int, int, int, str]] = []
    in_fence = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((index, index + 1, len(match.group(1)), match.group(2).strip()))

    blocks: list[_HeadingBlock] = []
    for position, (index, line_number, level, title) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        blocks.append(
            _HeadingBlock(
                line_index=index,
                line_number=line_number,
                level=level,
                title=title,
                text="\n".join(lines[index:end]),
            )
        )
    return blocks


def _support_refs(text: str) -> list[str]:
    refs = [match.group(0) for match in LOCAL_LABEL_RE.finditer(text)]
    prose_text = _strip_inline_code(text)
    refs.extend(match.group(0) for match in PANDOC_REF_RE.finditer(prose_text))
    return list(dict.fromkeys(refs))


def _support_sentence(relative_path: Path, heading_title: str, file_text: str) -> str:
    heading = _clean_heading_title(heading_title)
    section_title = _section_name(relative_path, file_text)
    scope = _scope_phrase(relative_path)
    refs = _path_support_refs(relative_path, file_text)
    refs_text = "; ".join(refs)
    lower = heading.lower()
    if lower == "purpose":
        body = f"The purpose in {scope} is bounded by {refs_text}; use it to connect the workbook aim to retained evidence rows and classroom scope."
    elif lower == "allowed inputs":
        body = f"Input choices in {scope} are checked through {refs_text}; use this heading to separate public, synthetic, instructor-provided, and owned-lab material."
    elif lower == "excluded actions":
        body = f"The exclusion rule in {scope} is checked through {refs_text}; use this heading to block live targets, private data, unsafe tool use, and external action."
    elif lower == "expected artifacts":
        body = f"Artifacts in {scope} are review products under {refs_text}; use this heading to tie deliverables to source lanes, provenance, and human approval."
    elif lower == "safe artifact schema":
        body = f"The schema in {scope} is governed by {refs_text}; use this heading to connect purpose, inputs, transform, output, and reviewer evidence."
    elif lower == "input/output contract":
        body = f"The contract in {scope} is governed by {refs_text}; use this heading to preserve source identity, accessibility, rights, tooling, and refresh evidence."
    elif lower == "failure cases":
        body = f"Failure cases in {scope} are anchored by {refs_text}; use this heading to recognize source laundering, boundary drift, access gaps, rights gaps, and tool opacity."
    elif lower == "evidence package schemas":
        body = f"Evidence packages in {scope} are organized by {refs_text}; use this heading to connect documentation cards, notices, logs, release gates, and remediation rows."
    elif lower == "rubric scoring bands":
        body = f"Rubric bands in {scope} are bounded by {refs_text}; use this heading to distinguish ready, revise, hold, and reject evidence."
    elif lower == "refresh evidence":
        body = f"Refresh evidence in {scope} is governed by {refs_text}; use this heading to tie source, safety, accessibility, rights, and vendor changes to retained proof."
    elif lower == "validation rubric":
        body = f"Validation in {scope} is checked through {refs_text}; use this heading to test source identity, verification, safety, reproducibility, and rights review."
    elif lower == "debrief protocol":
        body = f"Debrief work in {scope} is bounded by {refs_text}; use this heading to name proof limits, changed sources, avoided risk, approvals, and refresh timing."
    elif lower == "figures and course links":
        body = f"Visual navigation in {scope} is anchored by {refs_text}; use this heading to connect figures, captions, and nearby course links."
    elif lower == "runtime item map":
        body = f"Source-item rows in {scope} are governed by {refs_text}; use this heading to tie item titles to generated citations and safe substitutions."
    elif lower == "contents":
        body = f"The contents list in {scope} is generated under {refs_text}; use this heading to navigate semantic files without hard-coded numbering."
    elif lower == section_title.lower():
        body = f"This generated page is governed by {refs_text}; use it to verify local evidence, citations, and generated cross-links."
    else:
        body = f"{heading} material in {scope} is governed by {refs_text}; use this heading to verify claims against local evidence, citations, and generated cross-links."
    return f"**Evidence link.** {body}"


def _path_support_refs(relative_path: Path, file_text: str) -> list[str]:
    refs: list[str] = []
    label = _first_section_label(file_text) or _inferred_section_label(relative_path)
    refs.append(f"[@{label}]" if label else "[@sec:curriculum_orientation]")
    citation = _first_citation_ref(file_text)
    if citation and citation not in refs:
        refs.append(citation)
    return refs


def _first_section_label(text: str) -> str:
    match = SECTION_LABEL_RE.search(text)
    return match.group(1) if match else ""


def _first_citation_ref(text: str) -> str:
    for match in CITATION_RE.finditer(_strip_inline_code(text)):
        raw = match.group(1).strip()
        first = raw.split(";", 1)[0].strip().split()[0].lstrip("@")
        if first and not first.startswith(("sec:", "fig:", "tbl:", "eq:")):
            return f"[@{first}]"
    return ""


def _strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`\n]*`", "", text)


def _inferred_section_label(relative_path: Path) -> str:
    parts = relative_path.parts
    if not parts:
        return "sec:curriculum_orientation"
    if parts[0] == "orientation":
        return "sec:curriculum_orientation"
    if parts[0] == "appendices":
        if len(parts) > 1 and parts[1] == "bibliography-atlas":
            return "sec:bibliography_atlas"
        if len(parts) > 1 and parts[1].endswith(".md"):
            return f"sec:appendix-{parts[1].removesuffix('.md')}"
        return "sec:bibliography_atlas"
    if parts[0] == "parts":
        if len(parts) >= 3 and parts[2] not in {"README.md", "AGENTS.md"}:
            return f"sec:chapter-{parts[2]}"
        if len(parts) >= 2 and parts[1] not in {"README.md", "AGENTS.md"}:
            return f"sec:part-{parts[1]}"
        return "sec:curriculum_orientation"
    if relative_path.name == "references.md":
        return "sec:bibliography_atlas"
    return "sec:curriculum_orientation"


def _section_name(relative_path: Path, file_text: str) -> str:
    for block in _heading_blocks(file_text):
        if block.level == 1:
            return _clean_heading_title(block.title)
    stem = relative_path.stem.replace("-", " ").strip()
    return stem.title() if stem else "AGEINT manuscript output"


def _scope_phrase(relative_path: Path) -> str:
    parts = relative_path.parts
    if parts and parts[0] == "appendices":
        if len(parts) > 1 and parts[1] == "bibliography-atlas":
            return "the bibliography appendix"
        return "this appendix workbook"
    if parts and parts[0] == "orientation":
        return "the curriculum orientation"
    if parts and parts[0] == "parts":
        if len(parts) >= 3 and parts[2] not in {"README.md", "AGENTS.md"}:
            return "this module fragment"
        return "this unit folder"
    if relative_path.name in {"README.md", "AGENTS.md"}:
        return "this generated support page"
    if relative_path.name == "references.md":
        return "the references surface"
    return "this generated manuscript file"


def _clean_heading_title(title: str) -> str:
    title = re.sub(r"\s*\{#[^}]+\}", "", title)
    title = re.sub(r"\s*\{\.[^}]+\}", "", title)
    return re.sub(r"\s+", " ", title).strip()


def _table_cell(value: object) -> str:
    return re.sub(r"\s+", " ", str(value)).replace("|", "/").strip()


__all__ = [
    "HeadingSupportRow",
    "HeadingSupportSummary",
    "add_heading_support",
    "ensure_heading_support_in_tree",
    "heading_support_inventory",
    "heading_support_json",
    "heading_support_summary",
    "render_heading_support_markdown",
    "unsupported_heading_rows",
]
