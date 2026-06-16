"""Deterministic expansion for named AGEINT source packs."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from ._01_part import IntelligenceProfile


@dataclass(frozen=True)
class SourcePackContract:
    """One source-pack YAML surface and its validation contract."""

    source_class: str
    path: Path
    purpose: str
    supports_profile_routes: bool = False

    @property
    def label(self) -> str:
        return f"{self.source_class} source packs"

    def as_dict(self, project_root: Path | None = None) -> dict[str, Any]:
        path = self.path
        if project_root is not None:
            try:
                path = path.relative_to(project_root)
            except ValueError:
                pass
        return {
            "source_class": self.source_class,
            "path": path.as_posix(),
            "purpose": self.purpose,
            "supports_profile_routes": self.supports_profile_routes,
        }


@dataclass(frozen=True)
class SourcePackRegistry:
    """Loaded source-pack payload plus profile routes for one source class."""

    contract: SourcePackContract
    packs: dict[str, tuple[str, ...]]
    profile_routes: dict[str, tuple[str, ...]]

    def as_dict(self, project_root: Path | None = None) -> dict[str, Any]:
        return {
            **self.contract.as_dict(project_root),
            "pack_count": len(self.packs),
            "profile_route_count": len(self.profile_routes),
            "packs": {pack_id: list(keys) for pack_id, keys in self.packs.items()},
            "profile_routes": {
                profile_id: list(pack_ids)
                for profile_id, pack_ids in self.profile_routes.items()
            },
        }

    def validate_known_keys(self, known_keys: set[str]) -> list[dict[str, str]]:
        issues: list[dict[str, str]] = []
        for pack_id, keys in self.packs.items():
            missing = [key for key in keys if key not in known_keys]
            for key in missing:
                issues.append(
                    {
                        "source_class": self.contract.source_class,
                        "pack_id": pack_id,
                        "issue": "unknown_source_key",
                        "key": key,
                    }
                )
        return issues


def _contract(project_root: Path | None, source_class: str) -> SourcePackContract:
    root = Path(project_root) if project_root is not None else Path(__file__).resolve().parents[2]
    if source_class == "agency":
        return SourcePackContract(
            source_class="agency",
            path=root / "data" / "agency_source_packs.yaml",
            purpose="Official US IC source packs routed through profile source_pack_ids.",
        )
    if source_class == "research":
        return SourcePackContract(
            source_class="research",
            path=root / "data" / "research_source_packs.yaml",
            purpose="Non-agency scholarly, public, standards, and professional packs routed by profile id.",
            supports_profile_routes=True,
        )
    raise ValueError(f"Unknown AGEINT source-pack class: {source_class}")


def agency_source_pack_payload(project_root: Path | None = None) -> dict[str, tuple[str, ...]]:
    """Return named agency source packs from ``data/agency_source_packs.yaml``."""

    if project_root is None:
        return _cached_source_pack_registry(_contract(None, "agency")).packs
    return source_pack_registry("agency", project_root).packs


def research_source_pack_payload(project_root: Path | None = None) -> dict[str, tuple[str, ...]]:
    """Return named non-agency research packs from ``data/research_source_packs.yaml``."""

    if project_root is None:
        return _cached_source_pack_registry(_contract(None, "research")).packs
    return source_pack_registry("research", project_root).packs


def research_source_profile_routes(project_root: Path | None = None) -> dict[str, tuple[str, ...]]:
    """Return profile-to-research-pack routes from ``data/research_source_packs.yaml``."""

    if project_root is None:
        return _cached_source_pack_registry(_contract(None, "research")).profile_routes
    return source_pack_registry("research", project_root).profile_routes


@lru_cache(maxsize=1)
def _cached_source_pack_registry(contract: SourcePackContract) -> SourcePackRegistry:
    return _load_source_pack_registry(contract)


def source_pack_registry(
    source_class: str,
    project_root: Path | None = None,
) -> SourcePackRegistry:
    """Return a validated registry for one source-pack class."""
    contract = _contract(project_root, source_class)
    if project_root is None:
        return _cached_source_pack_registry(contract)
    return _load_source_pack_registry(contract)


def source_pack_contract_report(
    project_root: Path | None = None,
    *,
    known_source_keys: set[str] | None = None,
) -> dict[str, Any]:
    """Return machine-readable source-pack contract metadata and validation issues."""
    root = Path(project_root) if project_root is not None else None
    registries = [
        source_pack_registry("agency", project_root),
        source_pack_registry("research", project_root),
    ]
    issues: list[dict[str, str]] = []
    if known_source_keys is not None:
        for registry in registries:
            issues.extend(registry.validate_known_keys(known_source_keys))
    return {
        "schema_version": "1.0",
        "registry_count": len(registries),
        "registries": [registry.as_dict(root) for registry in registries],
        "issue_count": len(issues),
        "issues": issues,
    }


def _load_source_pack_registry(contract: SourcePackContract) -> SourcePackRegistry:
    packs = _load_pack_payload(contract)
    routes = _load_profile_routes(contract, packs) if contract.supports_profile_routes else {}
    return SourcePackRegistry(contract=contract, packs=packs, profile_routes=routes)


def _load_pack_payload(contract: SourcePackContract) -> dict[str, tuple[str, ...]]:
    path = contract.path
    if not path.is_file():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("packs"), dict):
        raise ValueError(f"{contract.label} must define a 'packs' mapping: {path}")
    packs: dict[str, tuple[str, ...]] = {}
    for pack_id, raw_keys in payload["packs"].items():
        if not isinstance(pack_id, str) or not pack_id:
            raise ValueError(f"{contract.label} id must be a non-empty string: {pack_id!r}")
        if not isinstance(raw_keys, list) or not raw_keys:
            raise ValueError(f"{contract.label} entry must contain at least one key: {pack_id}")
        duplicates = _duplicates(str(key) for key in raw_keys)
        if duplicates:
            raise ValueError(
                f"{contract.label} entry {pack_id} has duplicate source keys: {', '.join(duplicates)}"
            )
        keys = tuple(_dedupe(str(key) for key in raw_keys))
        packs[pack_id] = keys
    return packs


def _load_profile_routes(
    contract: SourcePackContract,
    packs: dict[str, tuple[str, ...]],
) -> dict[str, tuple[str, ...]]:
    path = contract.path
    if not path.is_file():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{contract.label} must define a mapping payload: {path}")
    raw_routes = payload.get("profile_routes", {})
    if not isinstance(raw_routes, dict):
        raise ValueError(f"{contract.label} profile_routes must be a mapping: {path}")
    routes: dict[str, tuple[str, ...]] = {}
    for profile_id, raw_pack_ids in raw_routes.items():
        if not isinstance(profile_id, str) or not profile_id:
            raise ValueError(f"Profile route id must be a non-empty string: {profile_id!r}")
        if not isinstance(raw_pack_ids, list) or not raw_pack_ids:
            raise ValueError(f"Profile route must contain at least one pack id: {profile_id}")
        duplicates = _duplicates(str(pack_id) for pack_id in raw_pack_ids)
        if duplicates:
            raise ValueError(
                f"{contract.label} profile route {profile_id} has duplicate pack ids: {', '.join(duplicates)}"
            )
        pack_ids = tuple(_dedupe(str(pack_id) for pack_id in raw_pack_ids))
        missing = [pack_id for pack_id in pack_ids if pack_id not in packs]
        if missing:
            raise KeyError(f"Unknown {contract.source_class} source packs for {profile_id}: {', '.join(missing)}")
        routes[profile_id] = pack_ids
    return routes


def agency_source_pack_keys(pack_id: str, project_root: Path | None = None) -> tuple[str, ...]:
    """Return source keys for one named pack."""

    packs = agency_source_pack_payload(project_root)
    try:
        return packs[pack_id]
    except KeyError as exc:
        raise KeyError(f"Unknown AGEINT agency source pack: {pack_id}") from exc


def research_source_pack_keys(pack_id: str, project_root: Path | None = None) -> tuple[str, ...]:
    """Return source keys for one named non-agency research pack."""

    packs = research_source_pack_payload(project_root)
    try:
        return packs[pack_id]
    except KeyError as exc:
        raise KeyError(f"Unknown AGEINT research source pack: {pack_id}") from exc


def expanded_profile_anchor_keys(
    profile: IntelligenceProfile,
    project_root: Path | None = None,
) -> tuple[str, ...]:
    """Return profile anchors plus deterministic source-pack expansion."""

    keys: list[str] = list(profile.anchor_keys)
    for pack_id in research_source_profile_routes(project_root).get(profile.identifier, ()):
        keys.extend(research_source_pack_keys(pack_id, project_root))
    for pack_id in profile.source_pack_ids:
        keys.extend(agency_source_pack_keys(pack_id, project_root))
    return tuple(_dedupe(keys))


def _dedupe(keys: Any) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for key in keys:
        if key in seen:
            continue
        seen.add(key)
        result.append(key)
    return result


def _duplicates(keys: Any) -> list[str]:
    seen: set[str] = set()
    duplicated: list[str] = []
    for key in keys:
        if key in seen and key not in duplicated:
            duplicated.append(key)
        seen.add(key)
    return duplicated


__all__ = [
    "SourcePackContract",
    "SourcePackRegistry",
    "agency_source_pack_keys",
    "agency_source_pack_payload",
    "expanded_profile_anchor_keys",
    "research_source_pack_keys",
    "research_source_pack_payload",
    "research_source_profile_routes",
    "source_pack_contract_report",
    "source_pack_registry",
]
