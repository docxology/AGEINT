#!/usr/bin/env python3
"""One-time migration: stitch pyfrag shards into package modules under 500 lines."""

from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path

MAX_LINES = 480
SRC = Path(__file__).resolve().parents[1] / "src"

PACKAGE_SPECS: dict[str, dict[str, object]] = {
    "figures": {
        "parts_dir": "figures_parts",
        "public_names": [
            "FigureKind",
            "FigureSpec",
            "build_figure_specs",
            "render_figures",
            "load_figure_registry",
            "figures_for_section",
            "figure_markdown",
        ],
    },
    "manuscript_variables": {
        "parts_dir": "manuscript_variables_parts",
        "public_names": [
            "generate_variables",
            "save_variables",
            "reference_bibtex_files",
            "write_bibtex_files",
        ],
    },
    "manuscript_manifest": {
        "parts_dir": "manuscript_manifest_parts",
        "public_names": [
            "ManuscriptManifest",
            "ManuscriptSection",
            "build_manuscript_manifest",
            "render_manuscript",
        ],
    },
    "intelligence_content": {
        "parts_dir": "intelligence_content_parts",
        "public_names": [],
    },
}


def stitch_pyfrags(parts_dir: Path) -> str:
    names = sorted(path.name for path in parts_dir.glob("*.pyfrag"))
    return "\n".join((parts_dir / name).read_text(encoding="utf-8") for name in names)


def _normalize_imports(source: str) -> str:
    patterns = [
        (
            r"try:\s*# Support both package imports[^\n]*\n"
            r"    from \.(\w+) import ([^\n]+)\n"
            r"    from \.(\w+) import ([^\n]+)\n"
            r"except ImportError:[^\n]*\n"
            r"    from \1 import [^\n]+\n"
            r"    from \3 import [^\n]+\n"
        ),
        (
            r"try:\s*\n"
            r"    from \.(\w+) import ([^\n]+)\n"
            r"except ImportError:[^\n]*\n"
            r"    from \1 import [^\n]+\n"
        ),
    ]
    for pattern in patterns:
        def _repl(match: re.Match[str]) -> str:
            groups = match.groups()
            if len(groups) == 4:
                return f"from {groups[0]} import {groups[1]}\nfrom {groups[2]} import {groups[3]}\n"
            return f"from {groups[0]} import {groups[1]}\n"

        source = re.sub(pattern, _repl, source, flags=re.MULTILINE)
    return source


def _top_level_chunks(source: str, max_lines: int = MAX_LINES) -> list[str]:
    """Split source at top-level AST statement boundaries."""
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    spans = [(node.lineno - 1, node.end_lineno or node.lineno) for node in tree.body]
    if not spans:
        return [source]

    chunks: list[str] = []
    chunk_start = 0
    chunk_end = 0
    for start, end in spans:
        if end - chunk_start > max_lines and chunk_end > chunk_start:
            chunks.append("".join(lines[chunk_start:chunk_end]))
            chunk_start = chunk_end
        chunk_end = end
    if chunk_end > chunk_start:
        chunks.append("".join(lines[chunk_start:chunk_end]))
    return chunks or [source]


def _collect_public_names(source: str) -> list[str]:
    tree = ast.parse(source)
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    names.append(target.id)
    return names


def _module_header(index: int, prior_modules: list[str]) -> str:
    lines = ["from __future__ import annotations", ""]
    for mod in prior_modules:
        lines.append(f"from .{mod} import *  # noqa: F403")
    if prior_modules:
        lines.append("")
    return "\n".join(lines) + ("\n" if lines else "")


def migrate_package(name: str, spec: dict[str, object]) -> None:
    parts_dir = SRC / str(spec["parts_dir"])
    stitched = _normalize_imports(stitch_pyfrags(parts_dir))
    chunks = _top_level_chunks(stitched)
    package_dir = SRC / name
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()

    module_names: list[str] = []
    for index, chunk in enumerate(chunks):
        mod_name = f"_{index + 1:02d}_part"
        module_names.append(mod_name)
        header = _module_header(index, module_names[:-1])
        (package_dir / f"{mod_name}.py").write_text(header + chunk, encoding="utf-8")

    public = list(spec.get("public_names") or []) or _collect_public_names(stitched)
    init_lines = [
        f'"""AGEINT {name} package."""',
        "",
        *[f"from .{mod} import *  # noqa: F403" for mod in module_names],
        "",
        "__all__ = [",
        *[f'    "{symbol}",' for symbol in public],
        "]",
        "",
    ]
    (package_dir / "__init__.py").write_text("\n".join(init_lines), encoding="utf-8")

    facade = SRC / f"{name}.py"
    if facade.is_file():
        facade.unlink()
    line_counts = [
        len((package_dir / f"{mod}.py").read_text(encoding="utf-8").splitlines())
        for mod in module_names
    ]
    print(f"migrated {name}: {len(chunks)} modules, lines={line_counts}, exports={len(public)}")


def remove_parts_dirs() -> None:
    for spec in PACKAGE_SPECS.values():
        parts_dir = SRC / str(spec["parts_dir"])
        if parts_dir.is_dir():
            shutil.rmtree(parts_dir)
            print(f"removed {parts_dir.name}")


def main() -> None:
    for name, spec in PACKAGE_SPECS.items():
        migrate_package(name, spec)
    remove_parts_dirs()


if __name__ == "__main__":
    main()
