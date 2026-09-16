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
    basic = payload.get("basicInfo") or payload.get("basic_info") or payload.get("data") or payload
    if not isinstance(basic, dict):
        raise ValueError("Profile basic info must be an object")
    clan = payload.get("clanBasicInfo") or payload.get("guildInfo") or {}
    if not clan and isinstance(basic.get("guild"), dict):
        clan = basic.get("guild")
    return {
        "uid": str(_first(basic, "accountId", "uid", "account_id") or uid),
        "region": str(_first(basic, "region") or region).upper(),
        "nickname": _first(basic, "nickname", "name", "accountName"),
        "level": _first(basic, "level", "accountLevel"),
        "likes": _first(basic, "liked", "likes", "likedCount"),
        "rank": _first(basic, "rank", "tier"),
        "rank_points": _first(basic, "rankingPoints", "rankPoints", "ranking_points"),
        "cs_rank": _first(basic, "csRank", "cs_rank"),
        "cs_rank_points": _first(basic, "csRankingPoints", "cs_rank_points"),
        "guild_id": _first(clan, "clanId", "guildId", "guild_id") or _first(basic, "guildId", "clanId"),
        "guild_name": _first(clan, "clanName", "guildName", "guild_name") or _first(basic, "guild", "guildName", "clanName"),
        "raw": payload,
    }


def normalize_stats(payload: Any, mode: str = "br") -> dict:
    """Normalize the documented /playerstats aggregate.

    The upstream endpoint returns BR-style solo/duo/quad aggregates and does
    not expose a documented CS statistics query. For CS, callers must rely on
    the profile's CS rank fields rather than duplicating BR data.
    """
    if not isinstance(payload, dict):
        raise ValueError("Stats payload must be an object")
    if mode == "cs":
        return {"available": False, "mode": "cs", "reason": "Provider does not expose CS career statistics." , "raw": payload}

    source = payload.get("stats") or payload.get("data")
    if not isinstance(source, dict):
        source = payload
    # Prefer quadStats because it is the broadest documented aggregate, then
    # fall back to solo/duo if a provider variant omits it.
    candidates = [source.get("quadStats"), source.get("soloStats"), source.get("duoStats"), source.get("squad"), source]
    chosen = next((x for x in candidates if isinstance(x, dict) and x), source)
    detailed = chosen.get("detailedStats") if isinstance(chosen.get("detailedStats"), dict) else {}
    merged = {**chosen, **detailed}
    aliases = {
        "matches": ("matches", "gamesPlayed", "match_count", "games"),
        "wins": ("wins", "win_count"),
        "kills": ("kills", "kill_count"),
        "deaths": ("deaths", "death_count"),
        "headshots": ("headshots", "headshot_kills"),
        "rank": ("rank", "tier"),
        "ranking_points": ("rankingPoints", "ranking_points", "rankPoints"),
        "kd": ("kd", "kdr", "kdRatio"),
        "win_rate": ("winRate", "win_rate", "winRatePercentage"),
    }
    normalized = {field: _first(merged, *keys) for field, keys in aliases.items()}
    normalized["mode"] = "br"
    normalized["available"] = True
    normalized["raw"] = payload
    return normalized
