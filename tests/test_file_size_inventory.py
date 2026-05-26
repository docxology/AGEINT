"""Inventory guard for AGEINT source and generated text file size."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAX_LINES = 500
TEXT_SUFFIXES = {
    ".bib",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".toml",
    ".yaml",
    ".yml",
}
INCLUDED_ROOTS = [
    "AGENTS.md",
    "README.md",
    "docs",
    "data",
    "manuscript",
    "scripts",
    "src",
    "tests",
    "output/data",
    "output/manuscript",
]
EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}
EXCLUDED_NAMES = {"uv.lock"}
EXCLUDED_RELATIVE_PREFIXES = (
    "tests/fixtures/",
)


def _candidate_files() -> list[Path]:
    files: list[Path] = []
    for root_name in INCLUDED_ROOTS:
        root = PROJECT_ROOT / root_name
        if root.is_file():
            files.append(root)
            continue
        if root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(files)


def test_source_and_generated_text_files_stay_under_500_lines() -> None:
    violations: list[str] = []
    for path in _candidate_files():
        relative = path.relative_to(PROJECT_ROOT)
        if path.suffix not in TEXT_SUFFIXES or path.name in EXCLUDED_NAMES:
            continue
        if any(relative.as_posix().startswith(prefix) for prefix in EXCLUDED_RELATIVE_PREFIXES):
            continue
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > MAX_LINES:
            violations.append(f"{relative.as_posix()}: {line_count}")

    assert violations == []
