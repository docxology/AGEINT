"""YAML-driven topic and chapter risk-category evaluation."""

from __future__ import annotations

from typing import Any

from _data_loaders import topic_risk_routes_payload


def _any_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def _all_phrases(text: str, phrases: tuple[str, ...]) -> bool:
    return all(phrase in text for phrase in phrases)


def _tuple_phrases(raw: object) -> tuple[str, ...]:
    if not isinstance(raw, list):
        raise ValueError("Expected phrase list in risk route rule")
    return tuple(str(item).lower() for item in raw)


def _resolve_context_overrides(
    rule: dict[str, Any],
    context: str,
) -> str | None:
    overrides = rule.get("context_overrides")
    if not isinstance(overrides, list):
        return str(rule["category"])
    for override in overrides:
        if not isinstance(override, dict):
            continue
        phrases = _tuple_phrases(override.get("context_any", []))
        if phrases and _any_phrase(context, phrases):
            return str(override["category"])
    return str(rule["category"])


def _topic_rule_matches(
    rule: dict[str, Any],
    *,
    lower: str,
    context: str,
) -> bool:
    title_any = rule.get("title_any")
    if title_any is not None and not _any_phrase(lower, _tuple_phrases(title_any)):
        return False
    context_any = rule.get("context_any")
    if context_any is not None and not _any_phrase(context, _tuple_phrases(context_any)):
        return False
    context_all = rule.get("context_all")
    if context_all is not None and not _all_phrases(context, _tuple_phrases(context_all)):
        return False
    return title_any is not None or context_any is not None or context_all is not None


def _chapter_rule_matches(rule: dict[str, Any], chapter_lower: str) -> bool:
    exact = rule.get("chapter_exact")
    if exact is not None and chapter_lower != str(exact).lower():
        return False
    any_in = rule.get("any_in_chapter")
    if any_in is not None and not _any_phrase(chapter_lower, _tuple_phrases(any_in)):
        return False
    all_in = rule.get("all_in_chapter")
    if all_in is not None and not _all_phrases(chapter_lower, _tuple_phrases(all_in)):
        return False
    return (
        exact is not None
        or any_in is not None
        or all_in is not None
    )


def chapter_context_risk_category(chapter_lower: str) -> str | None:
    """Chapter-wide default applied only when topic-level classification is standard."""
    for rule in topic_risk_routes_payload()["chapter_context_rules"]:
        if _chapter_rule_matches(rule, chapter_lower):
            return str(rule["category"])
    return None


def topic_risk_category(title: str, part_title: str = "", chapter_title: str = "") -> str:
    """Classify high-risk or context-sensitive source-guide topic labels."""
    lower = title.lower()
    context = f"{part_title} {chapter_title}".lower()
    chapter_lower = chapter_title.lower()

    for rule in topic_risk_routes_payload()["topic_rules"]:
        if not _topic_rule_matches(rule, lower=lower, context=context):
            continue
        return _resolve_context_overrides(rule, context) or str(rule["category"])

    chapter_default = chapter_context_risk_category(chapter_lower)
    if chapter_default:
        return chapter_default
    return "standard"


__all__ = ["chapter_context_risk_category", "topic_risk_category"]
