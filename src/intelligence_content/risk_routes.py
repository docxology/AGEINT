"""YAML-driven topic and chapter risk-category evaluation."""

from __future__ import annotations

from functools import lru_cache
from typing import NamedTuple

from _data_loaders import topic_risk_routes_payload


class _ContextOverride(NamedTuple):
    category: str
    context_any: tuple[str, ...]


class _TopicRule(NamedTuple):
    category: str
    title_any: tuple[str, ...] | None
    context_any: tuple[str, ...] | None
    context_all: tuple[str, ...] | None
    overrides: tuple[_ContextOverride, ...]


class _ChapterRule(NamedTuple):
    category: str
    chapter_exact: str | None
    any_in_chapter: tuple[str, ...] | None
    all_in_chapter: tuple[str, ...] | None


def _tuple_phrases(raw: object) -> tuple[str, ...]:
    if not isinstance(raw, list):
        raise ValueError("Expected phrase list in risk route rule")
    return tuple(str(item).lower() for item in raw)


@lru_cache(maxsize=1)
def _compiled_rules() -> tuple[tuple[_TopicRule, ...], tuple[_ChapterRule, ...]]:
    payload = topic_risk_routes_payload()
    topic_rules: list[_TopicRule] = []
    for raw in payload["topic_rules"]:
        category = str(raw["category"])
        title_any = _tuple_phrases(raw["title_any"]) if raw.get("title_any") is not None else None
        context_any = _tuple_phrases(raw["context_any"]) if raw.get("context_any") is not None else None
        context_all = _tuple_phrases(raw["context_all"]) if raw.get("context_all") is not None else None
        raw_overrides = raw.get("context_overrides")
        overrides: list[_ContextOverride] = []
        if isinstance(raw_overrides, list):
            for item in raw_overrides:
                if isinstance(item, dict):
                    overrides.append(_ContextOverride(category=str(item["category"]), context_any=_tuple_phrases(item.get("context_any", []))))
        topic_rules.append(_TopicRule(category=category, title_any=title_any, context_any=context_any, context_all=context_all, overrides=tuple(overrides)))

    chapter_rules: list[_ChapterRule] = []
    for raw in payload["chapter_context_rules"]:
        category = str(raw["category"])
        chapter_exact = str(raw["chapter_exact"]).lower() if raw.get("chapter_exact") is not None else None
        any_in = _tuple_phrases(raw["any_in_chapter"]) if raw.get("any_in_chapter") is not None else None
        all_in = _tuple_phrases(raw["all_in_chapter"]) if raw.get("all_in_chapter") is not None else None
        chapter_rules.append(_ChapterRule(category=category, chapter_exact=chapter_exact, any_in_chapter=any_in, all_in_chapter=all_in))
    return tuple(topic_rules), tuple(chapter_rules)


def _any_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def _all_phrases(text: str, phrases: tuple[str, ...]) -> bool:
    return all(phrase in text for phrase in phrases)


def _resolve_context_overrides(rule: _TopicRule, context: str) -> str:
    for override in rule.overrides:
        if override.context_any and _any_phrase(context, override.context_any):
            return override.category
    return rule.category


def _topic_rule_matches(rule: _TopicRule, *, lower: str, context: str) -> bool:
    if rule.title_any is not None and not _any_phrase(lower, rule.title_any):
        return False
    if rule.context_any is not None and not _any_phrase(context, rule.context_any):
        return False
    if rule.context_all is not None and not _all_phrases(context, rule.context_all):
        return False
    return rule.title_any is not None or rule.context_any is not None or rule.context_all is not None


def _chapter_rule_matches(rule: _ChapterRule, chapter_lower: str) -> bool:
    if rule.chapter_exact is not None and chapter_lower != rule.chapter_exact:
        return False
    if rule.any_in_chapter is not None and not _any_phrase(chapter_lower, rule.any_in_chapter):
        return False
    if rule.all_in_chapter is not None and not _all_phrases(chapter_lower, rule.all_in_chapter):
        return False
    return rule.chapter_exact is not None or rule.any_in_chapter is not None or rule.all_in_chapter is not None


def chapter_context_risk_category(chapter_lower: str) -> str | None:
    """Chapter-wide default applied only when topic-level classification is standard."""
    _, chapter_rules = _compiled_rules()
    for rule in chapter_rules:
        if _chapter_rule_matches(rule, chapter_lower):
            return rule.category
    return None


def topic_risk_category(title: str, part_title: str = "", chapter_title: str = "") -> str:
    """Classify high-risk or context-sensitive source-guide topic labels."""
    lower = title.lower()
    context = f"{part_title} {chapter_title}".lower()
    chapter_lower = chapter_title.lower()

    topic_rules, _ = _compiled_rules()
    for rule in topic_rules:
        if not _topic_rule_matches(rule, lower=lower, context=context):
            continue
        return _resolve_context_overrides(rule, context) or rule.category

    chapter_default = chapter_context_risk_category(chapter_lower)
    if chapter_default:
        return chapter_default
    return "standard"


__all__ = ["chapter_context_risk_category", "topic_risk_category"]
