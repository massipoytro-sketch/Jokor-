"""Static Free Fire catalog and utility services for Jokor.

Catalog data is intentionally separated from live player providers. It never
pretends that a static catalog is live account data.
"""

REGIONS = {
    "ME": {"name": "Middle East", "group": "MENA"},
    "IND": {"name": "India", "group": "ASIA"},
    "BR": {"name": "Brazil", "group": "LATAM"},
    "SG": {"name": "Singapore", "group": "SEA"},
    "EU": {"name": "Europe", "group": "EU"},
    "US": {"name": "United States", "group": "NA"},
}

MODES = {
    "br": {"id": "br", "name": "Battle Royale", "team_sizes": [1, 2, 4]},
    "cs": {"id": "cs", "name": "Clash Squad", "team_sizes": [1, 2, 4]},
}

RANKS = [
    {"id": "bronze", "name": "Bronze", "tier": 1},
    {"id": "silver", "name": "Silver", "tier": 2},
    {"id": "gold", "name": "Gold", "tier": 3},
    {"id": "platinum", "name": "Platinum", "tier": 4},
    {"id": "diamond", "name": "Diamond", "tier": 5},
    {"id": "heroic", "name": "Heroic", "tier": 6},
    {"id": "master", "name": "Master", "tier": 7},
    {"id": "grandmaster", "name": "Grandmaster", "tier": 8},
]

CATEGORIES = {
    "weapons": ["assault_rifle", "smg", "shotgun", "sniper", "pistol", "melee"],
    "characters": ["active_skill", "passive_skill", "awakening"],
    "pets": ["skill", "appearance"],
    "cosmetics": ["bundle", "outfit", "avatar", "banner", "emote"],
    "vehicles": ["car", "motorbike", "vehicle_skin"],
}

SEASONS = [
    {"id": "current", "name": "Current Season", "status": "catalog-placeholder"},
    {"id": "previous", "name": "Previous Season", "status": "catalog-placeholder"},
]


def regions():
    return [{"code": k, **v} for k, v in REGIONS.items()]


def modes():
    return list(MODES.values())


def ranks():
    return RANKS


def categories():
    return CATEGORIES


def seasons():
    return SEASONS


def status():
    return {
        "catalog": "available",
        "live_player_data": "provider-dependent",
        "message": "Catalog endpoints are ready; live account fields require a configured provider.",
    }
