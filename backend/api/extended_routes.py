from flask import Blueprint, jsonify, request

from core.request_id import get_request_id
from services.catalog_service import categories, modes, ranks, regions, seasons, status
from services.service_registry import all_services, get_service

extended = Blueprint("extended", __name__)


def ok(data, count=None):
    payload = {"success": True, "data": data, "request_id": get_request_id()}
    if count is not None:
        payload["count"] = count
    return jsonify(payload)


@extended.get("/catalog")
def catalog():
    return ok({"regions": regions(), "modes": modes(), "ranks": ranks(), "categories": categories(), "seasons": seasons()})


@extended.get("/catalog/regions")
def catalog_regions():
    data = regions(); return ok(data, len(data))


@extended.get("/catalog/modes")
def catalog_modes():
    data = modes(); return ok(data, len(data))


@extended.get("/catalog/ranks")
def catalog_ranks():
    data = ranks(); return ok(data, len(data))


@extended.get("/catalog/categories")
def catalog_categories():
    data = categories(); return ok(data, len(data))


@extended.get("/catalog/seasons")
def catalog_seasons():
    data = seasons(); return ok(data, len(data))


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
    data = [{"id": x, "name": label} for x, label in [("active_skill", "Active Skills"), ("passive_skill", "Passive Skills"), ("awakening", "Awakened Characters")]]
    return ok(data, len(data))


@extended.get("/pets")
def pets():
    data = [{"id": "pet", "name": "Pets", "status": "catalog-provider-ready"}]
    return ok(data, len(data))


@extended.get("/cosmetics")
def cosmetics():
    data = [{"id": x, "name": label} for x, label in [("bundle", "Bundles"), ("outfit", "Outfits"), ("avatar", "Avatars"), ("banner", "Banners"), ("emote", "Emotes")]]
    return ok(data, len(data))


@extended.get("/vehicles")
def vehicles():
    data = [{"id": x, "name": label} for x, label in [("car", "Cars"), ("motorbike", "Motorbikes"), ("vehicle_skin", "Vehicle Skins")]]
    return ok(data, len(data))


@extended.get("/service-status")
def service_status():
    return ok(status())


@extended.get("/services")
def service_list():
    data = all_services()
    group = request.args.get("group")
    state = request.args.get("status")
    if group:
        data = [x for x in data if x["group"] == group]
    if state:
        data = [x for x in data if x["status"] == state]
    return ok(data, len(data))


@extended.get("/services/<service_id>")
def service_detail(service_id):
    item = get_service(service_id)
    if item is None:
        return jsonify({"success": False, "error": {"code": "SERVICE_NOT_FOUND", "message": "Unknown Jokor service."}, "request_id": get_request_id()}), 404
    return ok(item)


@extended.get("/capabilities")
def capabilities():
    return ok({
        "live": ["player_profile", "player_stats", "search", "guild", "compare"],
        "catalog": ["regions", "modes", "ranks", "seasons", "weapons", "characters", "pets", "cosmetics", "vehicles"],
        "analytics": ["derived_stats", "comparison_metrics", "profile_completeness"],
        "history": ["rank_history", "activity_history"],
        "competitive": ["leaderboards"],
        "social": ["friends", "dynamic_duo"],
        "account_intelligence": ["ban_status", "inventory", "wishlist", "wallet"],
        "infrastructure": ["health", "ready", "metrics", "request_id", "rate_limit", "cache", "service_registry"],
        "provider_dependent": ["ban_status", "friends", "login_history", "wishlist", "wallet", "dynamic_duo", "live_leaderboards", "inventory"],
    })
