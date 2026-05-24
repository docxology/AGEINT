"""Shared loader for multi-part AGEINT packages."""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any


def merge_part_modules(package_name: str, part_names: list[str]) -> dict[str, Any]:
    """Import part modules in order and merge their globals for cross-part calls."""
    merged: dict[str, Any] = {}
    loaded: list[ModuleType] = []
    for name in part_names:
        module = importlib.import_module(f".{name}", package_name)
        loaded.append(module)
        merged.update({key: value for key, value in vars(module).items() if not key.startswith("__")})
    for module in loaded:
        module.__dict__.update(merged)
    return merged
