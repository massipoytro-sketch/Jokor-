from flask import Blueprint, jsonify, request

from core.regions import SUPPORTED_REGIONS
from core.request_id import get_request_id
from services.analytics_service import AnalyticsService
from services.asset_service import AssetService
from services.guild_service import GuildService
from services.player_service import PlayerService
from services.search_service import SearchService
from services.stats_service import StatsService
from services.statistics import derive_metrics

api = Blueprint("api", __name__)
player_service = PlayerService()
stats_service = StatsService(player_service)
search_service = SearchService()
guild_service = GuildService()
asset_service = AssetService()
analytics_service = AnalyticsService(stats_service)


def error(message, code, status=400, details=None):
    payload = {"success": False, "error": code, "message": message, "request_id": get_request_id()}
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status


def validate_uid(uid):
    return uid.isdigit() and 0 < int(uid) <= 999999999999999


def validate_region(region):
    return region.upper().strip() in SUPPORTED_REGIONS


@api.get("/meta")
def meta():
    return jsonify({
        "success": True,
        "name": "Jokor API",
        "version": "1.0.0",
        "request_id": get_request_id(),
        "features": ["player", "stats", "search", "guild", "assets", "analytics", "derived_stats", "health"],
    })


@api.get("/health")
def health():
    return jsonify({"success": True, "service": "jokor-api", "status": "healthy", "request_id": get_request_id()})


@api.get("/ready")
def ready():
    return jsonify({"success": True, "ready": True, "request_id": get_request_id()})


@api.get("/regions")
def regions():
    return jsonify({"success": True, "regions": sorted(SUPPORTED_REGIONS), "count": len(SUPPORTED_REGIONS)})


@api.post("/tools/derive-stats")
def derive_stats():
    """Calculate rates from counters supplied by a trusted data source or user."""
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("Request body must be a JSON object", "INVALID_BODY")
    stats = body.get("stats")
    if not isinstance(stats, dict):
        return error("'stats' must be a JSON object", "INVALID_STATS")
    allowed = {"matches", "wins", "kills", "deaths", "headshots"}
    unknown = sorted(set(stats) - allowed)
    if unknown:
        return error("Unsupported statistic fields", "UNKNOWN_STATS", details={"fields": unknown})
    for key, value in stats.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            return error(f"'{key}' must be a non-negative number", "INVALID_STAT_VALUE")
    return jsonify({
        "success": True,
        "metrics": derive_metrics(stats),
        "request_id": get_request_id(),
        "source": "provided_counters",
    })


@api.get("/player/<region>/<uid>")
def player(region, uid):
    region = region.upper().strip()
    uid = uid.strip()
    if not validate_region(region):
        return error(f"Unsupported region: {region}", "INVALID_REGION")
    if not validate_uid(uid):
        return error("UID must be a positive numeric value", "INVALID_UID")
    return jsonify(player_service.get_profile(region, uid))


@api.get("/player/<region>/<uid>/stats")
def player_stats(region, uid):
    region, uid = region.upper().strip(), uid.strip()
    if not validate_region(region) or not validate_uid(uid):
        return error("Invalid region or UID", "INVALID_REQUEST")
    mode = request.args.get("mode", "br").lower()
    if mode not in {"br", "cs"}:
        return error("Mode must be 'br' or 'cs'", "INVALID_MODE")
    return jsonify(stats_service.get_stats(region, uid, mode))


@api.get("/player/<region>/<uid>/compare/<other_uid>")
def compare(region, uid, other_uid):
    region, uid, other_uid = region.upper().strip(), uid.strip(), other_uid.strip()
    if not validate_region(region) or not validate_uid(uid) or not validate_uid(other_uid):
        return error("Invalid region or UID", "INVALID_REQUEST")
    return jsonify(analytics_service.compare(region, uid, other_uid))


@api.get("/search/<region>/<keyword>")
def search(region, keyword):
    region = region.upper().strip()
    if not validate_region(region):
        return error(f"Unsupported region: {region}", "INVALID_REGION")
    if len(keyword.strip()) < 2:
        return error("Search keyword must contain at least 2 characters", "INVALID_KEYWORD")
    return jsonify(search_service.search(region, keyword.strip()))


@api.get("/guild/<region>/<guild_id>")
def guild(region, guild_id):
    region = region.upper().strip()
    if not validate_region(region) or not guild_id.isdigit():
        return error("Invalid region or guild ID", "INVALID_REQUEST")
    return jsonify(guild_service.get_guild(region, guild_id))


@api.get("/assets/<int:item_id>")
def asset(item_id):
    return jsonify(asset_service.get_asset(item_id))
