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
    clan = payload.get("clanBasicInfo") or payload.get("guildInfo") or {}
    return {
        "uid": str(_first(basic, "accountId", "uid", "account_id") or uid),
        "region": str(_first(basic, "region") or region).upper(),
        "nickname": _first(basic, "nickname", "name", "accountName"),
        "level": _first(basic, "level", "accountLevel"),
        "likes": _first(basic, "liked", "likes", "likedCount"),
        "rank": _first(basic, "rank"),
        "rank_points": _first(basic, "rankingPoints", "rankPoints", "ranking_points"),
        "cs_rank": _first(basic, "csRank", "cs_rank"),
        "cs_rank_points": _first(basic, "csRankingPoints", "cs_rank_points"),
        "guild_id": _first(clan, "clanId", "guildId", "guild_id"),
        "guild_name": _first(clan, "clanName", "guildName", "guild_name"),
        "raw": payload,
    }


def normalize_stats(payload: Any) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Stats payload must be an object")
    source = payload.get("stats") or payload.get("data")
    if not isinstance(source, dict):
        source = payload
    # The public provider returns soloStats/duoStats/quadStats rather than a
    # single stats object. Use the richest populated mode as the stable view.
    candidates = [source.get("quadStats"), source.get("soloStats"), source.get("duoStats"), source]
    chosen = next((x for x in candidates if isinstance(x, dict) and x), source)
    detailed = chosen.get("detailedStats") if isinstance(chosen.get("detailedStats"), dict) else {}
    merged = {**chosen, **detailed}
    aliases = {
        "matches": ("matches", "gamesPlayed", "match_count", "games"),
        "wins": ("wins", "win_count"),
        "kills": ("kills", "kill_count"),
        "deaths": ("deaths", "death_count"),
        "headshots": ("headshots", "headshot_kills"),
        "rank": ("rank", "csRank", "cs_rank"),
        "ranking_points": ("rankingPoints", "ranking_points", "rankPoints"),
        "kd": ("kd", "kdr", "kdRatio"),
        "win_rate": ("winRate", "win_rate"),
    }
    normalized = {field: _first(merged, *keys) for field, keys in aliases.items()}
    normalized["raw"] = payload
    return normalized
