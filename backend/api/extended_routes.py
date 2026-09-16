from flask import Blueprint, jsonify

from core.request_id import get_request_id
from services.catalog_service import categories, modes, ranks, regions, seasons, status

extended = Blueprint("extended", __name__)


def ok(data, count=None):
    payload = {"success": True, "data": data, "request_id": get_request_id()}
    if count is not None:
        payload["count"] = count
    return jsonify(payload)


# Discovery / catalog
@extended.get("/catalog")
def catalog():
    return ok({
        "regions": regions(),
        "modes": modes(),
        "ranks": ranks(),
        "categories": categories(),
        "seasons": seasons(),
    })


@extended.get("/catalog/regions")
def catalog_regions():
    data = regions()
    return ok(data, len(data))


@extended.get("/catalog/modes")
def catalog_modes():
    data = modes()
    return ok(data, len(data))


@extended.get("/catalog/ranks")
def catalog_ranks():
    data = ranks()
    return ok(data, len(data))


@extended.get("/catalog/categories")
def catalog_categories():
    return ok(categories(), len(categories()))


@extended.get("/catalog/seasons")
def catalog_seasons():
    data = seasons()
    return ok(data, len(data))


# Product-style discovery endpoints. These expose stable schemas now and can
# later be backed by a live provider without changing the public API.
@extended.get("/weapons")
def weapons():
    data = [
        {"id": "assault_rifle", "name": "Assault Rifles", "category": "weapons"},
        {"id": "smg", "name": "SMG", "category": "weapons"},
        {"id": "shotgun", "name": "Shotguns", "category": "weapons"},
        {"id": "sniper", "name": "Snipers", "category": "weapons"},
        {"id": "pistol", "name": "Pistols", "category": "weapons"},
        {"id": "melee", "name": "Melee", "category": "weapons"},
    ]
    return ok(data, len(data))


@extended.get("/characters")
def characters():
    data = [
        {"id": "active_skill", "name": "Active Skills"},
        {"id": "passive_skill", "name": "Passive Skills"},
        {"id": "awakening", "name": "Awakened Characters"},
    ]
    return ok(data, len(data))


@extended.get("/pets")
def pets():
    data = [{"id": "pet", "name": "Pets", "status": "catalog-provider-ready"}]
    return ok(data, len(data))


@extended.get("/cosmetics")
def cosmetics():
    data = [
        {"id": "bundle", "name": "Bundles"},
        {"id": "outfit", "name": "Outfits"},
        {"id": "avatar", "name": "Avatars"},
        {"id": "banner", "name": "Banners"},
        {"id": "emote", "name": "Emotes"},
    ]
    return ok(data, len(data))


@extended.get("/vehicles")
def vehicles():
    data = [
        {"id": "car", "name": "Cars"},
        {"id": "motorbike", "name": "Motorbikes"},
        {"id": "vehicle_skin", "name": "Vehicle Skins"},
    ]
    return ok(data, len(data))


@extended.get("/service-status")
def service_status():
    return ok(status())


# Public schema for clients: tells them which capability is provider-backed.
@extended.get("/capabilities")
def capabilities():
    data = {
        "live": [
            "player_profile", "player_stats", "search", "guild", "compare",
        ],
        "catalog": [
            "regions", "modes", "ranks", "seasons", "weapons", "characters",
            "pets", "cosmetics", "vehicles",
        ],
        "analytics": [
            "derived_stats", "comparison_metrics", "profile_completeness",
        ],
        "infrastructure": [
            "health", "ready", "metrics", "request_id", "rate_limit", "cache",
        ],
        "provider_dependent": [
            "ban_status", "friends", "login_history", "wishlist", "wallet",
            "dynamic_duo", "live_leaderboards", "inventory",
        ],
    }
    return ok(data)
