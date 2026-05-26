"""Keyword concept routes for topic lesson frames."""

from __future__ import annotations

import re

from _data_loaders import merged_concept_keyword_routes

CONCEPT_KEYWORD_ROUTES = merged_concept_keyword_routes()


def _title_tokens(raw_lower: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", raw_lower))


def _match_keywords(raw_lower: str, keywords: tuple[str, ...]) -> bool:
    tokens = _title_tokens(raw_lower)
    for keyword in keywords:
        normalized = keyword.strip().lower()
        if not normalized:
            continue
        if " " in normalized or "-" in normalized:
            if normalized in raw_lower:
                return True
        elif normalized in tokens:
            return True
    return False


def _first_matching_frame(raw_lower: str, routes: tuple[tuple[tuple[str, ...], str], ...]) -> str | None:
    for keywords, frame in routes:
        if _match_keywords(raw_lower, keywords):
            return frame
    return None
