"""Project path bootstrap for AGEINT scripts and tests."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_project_paths(project_root: Path) -> Path:
    """Add ``project_root`` and ``project_root/src`` to ``sys.path`` if missing."""
    root = Path(project_root).resolve()
    src = root / "src"
    for path in (src, root):
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)
    return root
