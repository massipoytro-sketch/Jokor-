"""Normalize heterogeneous provider payloads into stable Jokor shapes."""
from typing import Any


def _first(mapping: dict, *keys: str) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value is not None:
            return value
    return None


def normalize_profile(payload: Any, region: str, uid: str) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Profile payload must be an object")
    basic = payload.get("basicInfo") or payload.get("basic_info") or payload
    if not isinstance(basic, dict):
        raise ValueError("Profile basic info must be an object")
    return {
        "uid": str(_first(basic, "accountId", "uid", "account_id") or uid),
        "region": str(_first(basic, "region") or region).upper(),
        "nickname": _first(basic, "nickname", "name", "accountName"),
        "level": _first(basic, "level", "accountLevel"),
        "likes": _first(basic, "liked", "likes", "likedCount"),
        "guild_id": _first(basic, "guildId", "guild_id"),
        "guild_name": _first(basic, "guildName", "guild_name"),
        "raw": payload,
    }


def normalize_stats(payload: Any) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Stats payload must be an object")
    source = payload.get("stats") or payload.get("data") or payload
    if not isinstance(source, dict):
        raise ValueError("Stats data must be an object")
    aliases = {
        "matches": ("matches", "match_count", "games"),
        "wins": ("wins", "win_count"),
        "kills": ("kills", "kill_count"),
        "deaths": ("deaths", "death_count"),
        "headshots": ("headshots", "headshot_kills"),
    }
    normalized = {}
    for field, keys in aliases.items():
        normalized[field] = _first(source, *keys)
    normalized["raw"] = payload
    return normalized
