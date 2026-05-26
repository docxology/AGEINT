"""Shared loader for multi-part AGEINT packages."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType
from typing import Any


def merge_part_modules(package_name: str, part_names: list[str]) -> dict[str, Any]:
    """Import part modules in order, seeding each with prior part globals."""
    merged: dict[str, Any] = {}
    loaded: list[ModuleType] = []
    package = importlib.import_module(package_name)
    for name in part_names:
        full_name = f"{package_name}.{name}"
        spec = importlib.util.find_spec(full_name)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load part module {full_name}")
        module = importlib.util.module_from_spec(spec)
        module.__dict__.update(merged)
        sys.modules[full_name] = module
        spec.loader.exec_module(module)
        loaded.append(module)
        merged.update({key: value for key, value in vars(module).items() if not key.startswith("__")})
    for module in loaded:
        module.__dict__.update(merged)
    package.__dict__.update(merged)
    return merged
