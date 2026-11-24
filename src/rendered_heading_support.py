"""Inventory structural heading navigation, never evidentiary adequacy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Any

from rendered_reference_audit import SUPPORT_DOC_NAMES


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LOCAL_LABEL_RE = re.compile(r"\{#(?:sec|fig|tbl|eq):[^}]+\}")
PANDOC_REF_RE = re.compile(
    r"\[@(?:ageint\d{3}|sec:[^\]\s;]+|fig:[^\]\s;]+|tbl:[^\]\s;]+|eq:[^\]\s;]+|"
    r"[A-Za-z_][A-Za-z0-9_:-]*)(?:[^\]]*)\]"
)
SECTION_LABEL_RE = re.compile(r"\{#(sec:[A-Za-z0-9_-]+)(?:\s+[^}]*)?\}")


@dataclass(frozen=True)
class HeadingSupportRow:
    """Structural reference presence; ``supported`` never means evidence-backed."""

    path: str
    line_number: int
    level: int
    title: str
    supported: bool
    support_refs: tuple[str, ...]


@dataclass(frozen=True)
class HeadingSupportSummary:
    """Aggregate structural navigation coverage, not substantive claim support."""

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
    """Return structural reference-presence rows for generated headings."""

    root = Path(manuscript_dir)
    rows: list[HeadingSupportRow] = []
    for path in sorted(root.rglob("*.md")):
        if path.name in SUPPORT_DOC_NAMES:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        for block in _heading_blocks(text):
            refs = _support_refs(block.text)
            rows.append(HeadingSupportRow(path=relative, line_number=block.line_number, level=block.level, title=_clean_heading_title(block.title), supported=bool(refs), support_refs=tuple(refs)))
    return rows


def heading_support_summary(rows: list[HeadingSupportRow]) -> HeadingSupportSummary:
    """Return navigation coverage without assessing source relevance or validity."""

    files = {row.path for row in rows}
    supported = sum(1 for row in rows if row.supported)
    return HeadingSupportSummary(file_count=len(files), heading_count=len(rows), supported_heading_count=supported, unsupported_heading_count=len(rows) - supported)


def unsupported_heading_rows(manuscript_dir: Path) -> list[HeadingSupportRow]:
    """Return headings lacking a local navigation label or reference."""

    return [row for row in heading_support_inventory(manuscript_dir) if not row.supported]


def render_heading_support_markdown(manuscript_dir: Path) -> str:
    """Report navigation presence explicitly separately from evidentiary support."""

    rows = heading_support_inventory(manuscript_dir)
    summary = heading_support_summary(rows)
    lines = [
        "# AGEINT Heading Navigation",
        "",
        "Labels and references provide structural navigation, not evidence for a heading's claims. Source relevance and link resolution require separate review.",
        "",
        "| Measure | Count |",
        "|---|---:|",
        f"| Markdown files | {summary.file_count} |",
        f"| Headings | {summary.heading_count} |",
        f"| Headings with navigation | {summary.supported_heading_count} |",
        f"| Headings without navigation | {summary.unsupported_heading_count} |",
        f"| OK | {str(summary.ok).lower()} |",
    ]
    unsupported = [row for row in rows if not row.supported]
    if unsupported:
        lines.extend(["", "## Headings Without Navigation", "", "| Path | Line | Heading |", "|---|---:|---|"])
        for row in unsupported:
            lines.append(f"| {_table_cell(row.path)} | {row.line_number} | {_table_cell(row.title)} |")
    return "\n".join(lines)


def heading_support_json(manuscript_dir: Path) -> str:
    """Return stable navigation-presence JSON; legacy support fields are structural."""

    rows = heading_support_inventory(manuscript_dir)
    summary = heading_support_summary(rows)
    unsupported = [row for row in rows if not row.supported]
    return json.dumps(
        {
            **summary.as_dict(),
            "scope": "structural_navigation_not_evidence",
            "unsupported_headings": [{"path": row.path, "line_number": row.line_number, "level": row.level, "title": row.title} for row in unsupported],
        },
        indent=2,
        sort_keys=True,
    )


def add_heading_support(text: str, *, section_text: str | None = None) -> str:
    """Add parent navigation only to a target declared in the actual source section."""

    blocks = _heading_blocks(text)
    navigation = _navigation_sentence(text if section_text is None else section_text)
    if not blocks or not navigation:
        return text
    lines = text.splitlines()
    for block in reversed(blocks):
        if _support_refs(block.text):
            continue
        insert_at = block.line_index + 1
        if insert_at < len(lines) and not lines[insert_at].strip():
            insert_at += 1
        lines[insert_at:insert_at] = [navigation, ""]
    return "\n".join(lines).rstrip() + "\n"


def ensure_heading_support_in_tree(manuscript_dir: Path) -> list[Path]:
    """Add available structural navigation without manufacturing source support."""

    root = Path(manuscript_dir)
    changed: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        if path.name in SUPPORT_DOC_NAMES:
            continue
        original = path.read_text(encoding="utf-8")
        revised = add_heading_support(original)
        if revised != original:
            path.write_text(revised, encoding="utf-8")
            changed.append(path)
    return changed


def _heading_blocks(text: str) -> list[_HeadingBlock]:
    lines = text.splitlines()
    headings: list[tuple[int, int, int, str]] = []
    fence = ""
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not fence:
                fence = marker
            elif fence == marker:
                fence = ""
            continue
        if fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((index, index + 1, len(match.group(1)), match.group(2).strip()))

    blocks: list[_HeadingBlock] = []
    for position, (index, line_number, level, title) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        blocks.append(_HeadingBlock(line_index=index, line_number=line_number, level=level, title=title, text="\n".join(lines[index:end])))
    return blocks


def _support_refs(text: str) -> list[str]:
    prose_text = _reference_text(text)
    refs = [match.group(0) for match in LOCAL_LABEL_RE.finditer(prose_text)]
    refs.extend(match.group(0) for match in PANDOC_REF_RE.finditer(prose_text))
    return list(dict.fromkeys(refs))


def _navigation_sentence(file_text: str) -> str:
    """Return only parent navigation, never a borrowed citation or evidence claim."""
    match = SECTION_LABEL_RE.search(_reference_text(file_text))
    if not match:
        return ""
    return f"**Navigation.** Parent section: [@{match.group(1)}]."


def _reference_text(text: str) -> str:
    """Exclude code examples from structural reference presence."""
    lines: list[str] = []
    fence = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not fence:
                fence = marker
            elif fence == marker:
                fence = ""
            continue
        if not fence:
            lines.append(re.sub(r"`[^`\n]*`", "", line))
    return "\n".join(lines)


def _clean_heading_title(title: str) -> str:
    title = re.sub(r"\s*\{#[^}]+\}", "", title)
    title = re.sub(r"\s*\{\.[^}]+\}", "", title)
    return re.sub(r"\s+", " ", title).strip()


def _table_cell(value: object) -> str:
    from markdown_cell import plain_table_cell

    return plain_table_cell(value)


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
