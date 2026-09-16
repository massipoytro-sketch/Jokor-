"""Static, presentation-ready Free Fire information for the Jokor frontend.

This module contains product metadata only. It does not pretend to be live player data.
Live values must come from a validated provider through the adapter layer.
"""

GAME_MODES = {
    "br": {
        "id": "br",
        "name": "Battle Royale",
        "short_name": "BR",
        "description": "Battle Royale statistics and performance counters.",
        "stats": ["matches", "wins", "kills", "deaths", "headshots"],
    },
    "cs": {
        "id": "cs",
        "name": "Clash Squad",
        "short_name": "CS",
        "description": "Clash Squad statistics when supplied by the data provider.",
        "stats": ["matches", "wins", "kills", "deaths", "headshots"],
    },
}

RANKS = [
    {"id": "bronze", "name": "Bronze", "order": 1},
    {"id": "silver", "name": "Silver", "order": 2},
    {"id": "gold", "name": "Gold", "order": 3},
    {"id": "platinum", "name": "Platinum", "order": 4},
    {"id": "diamond", "name": "Diamond", "order": 5},
    {"id": "heroic", "name": "Heroic", "order": 6},
    {"id": "master", "name": "Master", "order": 7},
    {"id": "grandmaster", "name": "Grandmaster", "order": 8},
]

PLAYER_FIELDS = {
    "identity": ["uid", "region", "nickname", "level"],
    "social": ["likes", "guild_id", "guild_name"],
    "competitive": ["rank", "rank_points", "mode"],
    "performance": ["matches", "wins", "kills", "deaths", "headshots"],
    "derived": ["win_rate_pct", "kd_ratio", "headshot_rate_pct"],
}


def catalog() -> dict:
    return {
        "game": "Free Fire",
        "product": "Jokor",
        "modes": list(GAME_MODES.values()),
        "ranks": RANKS,
        "player_fields": PLAYER_FIELDS,
        "analysis": [
            "win rate",
            "K/D ratio",
            "headshot rate",
            "match volume",
            "profile completeness",
        ],
        "data_policy": "Live values are shown only when supplied by a configured provider.",
    }


def mode(mode_id: str) -> dict | None:
    return GAME_MODES.get(str(mode_id).lower())
