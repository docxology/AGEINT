"""Topic risk-category classification for safe curriculum treatment."""

from __future__ import annotations

try:
    from intelligence_content.risk_routes import (
        chapter_context_risk_category as _chapter_context_risk_category,
    )
    from intelligence_content.risk_routes import topic_risk_category as _topic_risk_category
except ImportError:  # pragma: no cover - merged part module import
    from .risk_routes import chapter_context_risk_category as _chapter_context_risk_category  # type: ignore[no-redef]
    from .risk_routes import topic_risk_category as _topic_risk_category  # type: ignore[no-redef]

__all__ = ["_chapter_context_risk_category", "_topic_risk_category"]
