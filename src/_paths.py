"""Project path bootstrap for AGEINT scripts and tests."""

from __future__ import annotations

import os
import shutil
import stat
import sys
from pathlib import Path


def _clear_readonly(func, path: str, exc_info: object) -> None:
    os.chmod(path, stat.S_IWUSR | stat.S_IREAD)
    func(path)


def remove_tree(path: Path) -> None:
    """Remove a directory tree, including read-only files and symlinks."""
    root = Path(path)
    if not root.exists():
        return
    if root.is_symlink() or root.is_file():
        root.unlink(missing_ok=True)
        return
    for child in sorted(root.iterdir(), key=lambda item: item.name, reverse=True):
        if child.is_symlink() or child.is_file():
            child.unlink(missing_ok=True)
        else:
            remove_tree(child)
    try:
        root.rmdir()
    except OSError:
        shutil.rmtree(root, onerror=_clear_readonly)


def ensure_project_paths(project_root: Path) -> Path:
    """Add ``project_root`` and ``project_root/src`` to ``sys.path`` if missing."""
    root = Path(project_root).resolve()
    src = root / "src"
    for path in (src, root):
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)
    return root
