#!/usr/bin/env python3
"""Post-migration fixes for AGEINT subpackages."""

from __future__ import annotations

import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"


def clean_part_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    cleaned: list[str] = []
    seen_future = False
    for line in lines:
        if line.startswith("from __future__ import annotations"):
            if seen_future:
                continue
            seen_future = True
        if line.startswith('"""') and cleaned and cleaned[-1].strip() == "":
            # Drop module docstring after header imports in continuation parts
            if not path.name.endswith("_01_part.py"):
                if '"""' in line and line.count('"""') == 2:
                    continue
        cleaned.append(line)
    path.write_text("".join(cleaned), encoding="utf-8")


def replace_anchors_module(package_dir: Path) -> None:
    anchors_path = package_dir / "_02_part.py"
    anchors_path.write_text(
        '''from __future__ import annotations

from pathlib import Path
from typing import Final

from _jsonl import read_jsonl

from ._01_part import *  # noqa: F403


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_intelligence_research_anchors() -> tuple[ResearchAnchor, ...]:
    data_dir = _project_root() / "data" / "research_anchors"
    rows: list[dict] = []
    for path in sorted(data_dir.glob("intelligence-anchors-*.jsonl")):
        rows.extend(read_jsonl(path))
    return tuple(ResearchAnchor(**row) for row in rows)


INTELLIGENCE_RESEARCH_ANCHORS: Final[tuple[ResearchAnchor, ...]] = _load_intelligence_research_anchors()
''',
        encoding="utf-8",
    )


def split_large_module(path: Path, max_lines: int = 480) -> None:
    text = path.read_text(encoding="utf-8")
    if len(text.splitlines()) <= max_lines:
        return

    lines = text.splitlines(keepends=True)
    header_end = 0
    for index, line in enumerate(lines):
        if line.strip() and not line.startswith(("from ", "import ", "#")):
            header_end = index
            break

    header = "".join(lines[:header_end])
    body_lines = lines[header_end:]
    chunks: list[list[str]] = []
    current: list[str] = []
    for line in body_lines:
        if (
            current
            and line.startswith(("INTELLIGENCE_", "PRACTICE_", "SAFE_", "COURSEBOOK_", "CHAPTER_"))
            and "=" in line
            and len(current) > 50
        ):
            chunks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        chunks.append(current)

    if len(chunks) <= 1:
        return

    stem = path.stem
    parent = path.parent
    path.unlink()
    for index, chunk in enumerate(chunks, start=1):
        new_name = f"{stem}_{index}.py"
        prior = [f"{stem}_{i}" for i in range(1, index)]
        imports = "".join(f"from .{mod} import *  # noqa: F403\n" for mod in prior)
        (parent / new_name).write_text(header + imports + ("\n" if imports else "") + "".join(chunk), encoding="utf-8")


def renumber_package(package_dir: Path) -> None:
    parts = sorted(package_dir.glob("_*.py"))
    if not parts:
        return
    # Collect all part modules in order
    modules = [p.stem for p in parts if p.name != "__init__.py"]
    public_source = (package_dir / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r"__all__ = \[(.*?)\]", public_source, re.DOTALL)
    public = match.group(1) if match else ""
    init = ['"""AGEINT package."""', ""]
    for mod in sorted(modules):
        init.append(f"from .{mod} import *  # noqa: F403")
    init.extend(["", "__all__ = [", public.strip(), "]", ""])
    (package_dir / "__init__.py").write_text("\n".join(init), encoding="utf-8")


def main() -> None:
    for package_dir in SRC.iterdir():
        if not package_dir.is_dir() or package_dir.name.startswith("_"):
            continue
        for part in package_dir.glob("_*.py"):
            clean_part_file(part)
        if package_dir.name == "intelligence_content":
            replace_anchors_module(package_dir)
            split_large_module(package_dir / "_04_part.py")
        renumber_package(package_dir)


if __name__ == "__main__":
    main()
