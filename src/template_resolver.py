"""Resolve the sibling docxology/template checkout for standalone AGEINT runs."""

from __future__ import annotations

import os
from pathlib import Path
import sys

_TEMPLATE_ENV_VARS = (
    "AGEINT_TEMPLATE_REPO",
    "DOCXOLOGY_TEMPLATE_REPO",
    "DOCXOLOGY_TEMPLATE_ROOT",
    "TEMPLATE_REPO_ROOT",
)


def _looks_like_template_repo(path: Path) -> bool:
    validation_cli = path / "infrastructure" / "validation" / "cli.py"
    validation_cli_package = path / "infrastructure" / "validation" / "cli" / "__init__.py"
    return (
        (path / "infrastructure" / "rendering").is_dir()
        and (validation_cli.is_file() or validation_cli_package.is_file())
    )


def _candidate_paths(start: Path) -> list[Path]:
    candidates: list[Path] = []
    for name in _TEMPLATE_ENV_VARS:
        configured = os.environ.get(name)
        if configured:
            candidates.append(Path(configured).expanduser())

    anchor = start if start.is_dir() else start.parent
    for ancestor in (anchor, *anchor.parents):
        candidates.extend(
            [
                ancestor,
                ancestor / "template",
                ancestor.parent / "template",
            ]
        )
    return candidates


def resolve_template_repo(start: Path | None = None) -> Path | None:
    """Return the public template checkout if it can be found from ``start``."""
    search_start = (start or Path.cwd()).resolve()
    seen: set[Path] = set()
    for candidate in _candidate_paths(search_start):
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if _looks_like_template_repo(resolved):
            return resolved
    return None


def ensure_template_repo_on_path(start: Path | None = None) -> Path | None:
    """Add the resolved template checkout to ``sys.path`` and return it."""
    template_repo = resolve_template_repo(start)
    if template_repo is None:
        return None
    template_path = str(template_repo)
    if template_path not in sys.path:
        sys.path.insert(0, template_path)
    return template_repo
