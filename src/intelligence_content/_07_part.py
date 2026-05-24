"""Safe curriculum treatment and source-lane constants."""

from __future__ import annotations

from typing import Final

from ._07_risk_categories import _topic_risk_category
from ._07_safe_titles import (
    GENERIC_DISPLAY_TITLE_MARKERS,
    _topic_anchor_words,
    is_generic_display_title,
    safe_curriculum_treatment,
)

REQUIRED_SOURCE_LANES: Final[tuple[str, ...]] = (
    "ai_conformity_compliance",
    "education_assessment",
    "public_sector_agentic_ai",
    "cross_border_data_spaces",
    "human_rights_governance",
    "agent_interoperability_standards",
    "workforce_governance",
    "model_data_provenance",
    "accessibility_digital_inclusion",
    "procurement_vendor_governance",
    "agent_incident_response",
    "ai_red_team_assurance",
    "public_sector_transparency",
    "rights_impact_privacy",
)
