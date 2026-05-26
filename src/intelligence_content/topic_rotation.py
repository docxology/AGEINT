"""Stable template-slot rotation for topic lesson fields."""

from __future__ import annotations

import zlib


def template_index(*parts: str, count: int) -> int:
    """Return a stable template slot from joined identity parts."""
    if count <= 0:
        raise ValueError("template count must be positive")
    seed = "|".join(parts).encode("utf-8")
    return zlib.adler32(seed) % count


__all__ = ["template_index"]
