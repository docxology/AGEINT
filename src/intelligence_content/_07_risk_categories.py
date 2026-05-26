"""Topic risk-category classification for safe curriculum treatment."""

from __future__ import annotations

from .risk_routes import chapter_context_risk_category as _chapter_context_risk_category
from .risk_routes import topic_risk_category as _topic_risk_category

__all__ = ["_chapter_context_risk_category", "_topic_risk_category"]
