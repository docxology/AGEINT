"""Safety and artifact table rows loaded from declarative YAML.

Module globals are bound in a loop from ``SAFETY_ARTIFACT_TABLE_NAMES``.
"""

from __future__ import annotations

from _data_loaders import SAFETY_ARTIFACT_TABLE_NAMES, safety_artifact_table

for _name in SAFETY_ARTIFACT_TABLE_NAMES:
    globals()[_name] = safety_artifact_table(_name)

__all__ = list(SAFETY_ARTIFACT_TABLE_NAMES)
