from flask import Blueprint, jsonify, request

from core.regions import REGION_GROUPS, SUPPORTED_REGIONS, normalize_region, region_group
from core.request_id import get_request_id
from services.analytics_service import AnalyticsService
from services.asset_service import AssetService
from services.game_info import catalog as game_catalog, mode as game_mode
from services.guild_service import GuildService
from services.intelligence_service import IntelligenceService
from services.player_service import PlayerService
from services.search_service import SearchService
from services.stats_service import StatsService
from services.statistics import derive_metrics
from adapters.freefire.client import FreeFireClient
from adapters.freefire.normalizer import normalize_profile

api = Blueprint("api", __name__)
player_service = PlayerService()
stats_service = StatsService(player_service)
search_service = SearchService()
guild_service = GuildService()
asset_service = AssetService()
analytics_service = AnalyticsService(stats_service)
intelligence_service = IntelligenceService(player_service, stats_service)
auto_client = FreeFireClient()


def error(message, code, status=400, details=None):
    payload = {"success": False, "error": code, "message": message, "request_id": get_request_id()}
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status


def validate_uid(uid):
    return uid.isdigit() and 0 < int(uid) <= 999999999999999


def validate_region(region):
    return normalize_region(region) in SUPPORTED_REGIONS


@api.get("/meta")
def meta():
    return jsonify({
        "success": True,
        "name": "Jokor API",
        "version": "2.2.0",
        "request_id": get_request_id(),
        "features": ["player", "player_auto", "player_intelligence", "stats", "search", "guild", "assets", "analytics", "derived_stats", "game_info", "region_directory", "catalog", "weapons", "characters", "pets", "cosmetics", "vehicles", "seasons", "capabilities", "health", "ready", "metrics"],
    })


@api.get("/health")
def health():
    return jsonify({"success": True, "service": "jokor-api", "status": "healthy", "request_id": get_request_id()})


@api.get("/ready")
def ready():
    return jsonify({"success": True, "ready": True, "request_id": get_request_id()})


@api.get("/regions")
def regions():
    entries = [{"code": code, "group": region_group(code)} for code in sorted(SUPPORTED_REGIONS)]
    return jsonify({"success": True, "regions": entries, "count": len(entries)})


@api.get("/regions/<region>")
def region_detail(region):
    code = normalize_region(region)
    if code not in SUPPORTED_REGIONS:
        return error(f"Unsupported region: {code}", "INVALID_REGION")
    return jsonify({"success": True, "region": {"code": code, "group": region_group(code)}, "group_members": sorted(k for k, v in REGION_GROUPS.items() if v == region_group(code)), "request_id": get_request_id()})


@api.get("/game-info")
def game_info():
    return jsonify({"success": True, "data": game_catalog(), "request_id": get_request_id()})


@api.get("/game-info/modes/<mode_id>")
def game_mode_info(mode_id):
    info = game_mode(mode_id)
    if info is None:
        return error("Mode must be 'br' or 'cs'", "INVALID_MODE")
    return jsonify({"success": True, "data": info, "request_id": get_request_id()})


@api.post("/tools/derive-stats")
def derive_stats():
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
    return jsonify({"success": True, "metrics": derive_metrics(stats), "request_id": get_request_id(), "source": "provided_counters"})


@api.get("/player/auto/<uid>")
def player_auto(uid):
    uid = uid.strip()
    if not validate_uid(uid):
        return error("UID must be a positive numeric value", "INVALID_UID")
    try:
        region, payload = auto_client.detect_profile(uid)
        profile = normalize_profile(payload, region, uid)
        return jsonify({"success": True, "data": profile, "metadata": {"uid": uid, "region": region, "provider": "freefire-public", "detection": "automatic"}, "request_id": get_request_id()})
    except LookupError as exc:
        return error(str(exc), "PLAYER_NOT_FOUND", 404)
    except Exception:
        return error("The public player data source is temporarily unavailable.", "DATA_SOURCE_UNAVAILABLE", 503)


@api.get("/player/<region>/<uid>")
def player(region, uid):
    region = normalize_region(region)
    uid = uid.strip()
    if not validate_region(region):
        return error(f"Unsupported region: {region}", "INVALID_REGION")
    if not validate_uid(uid):
        return error("UID must be a positive numeric value", "INVALID_UID")
    return jsonify(player_service.get_profile(region, uid))


@api.get("/player/<region>/<uid>/intelligence")
def player_intelligence(region, uid):
    region, uid = normalize_region(region), uid.strip()
    if not validate_region(region) or not validate_uid(uid):
        return error("Invalid region or UID", "INVALID_REQUEST")
    return jsonify(intelligence_service.scan(region, uid))


@api.get("/player/<region>/<uid>/stats")
def player_stats(region, uid):
    region, uid = normalize_region(region), uid.strip()
    if not validate_region(region) or not validate_uid(uid):
        return error("Invalid region or UID", "INVALID_REQUEST")
    mode = request.args.get("mode", "br").lower()
    if mode not in {"br", "cs"}:
        return error("Mode must be 'br' or 'cs'", "INVALID_MODE")
    return jsonify(stats_service.get_stats(region, uid, mode))


@api.get("/player/<region>/<uid>/compare/<other_uid>")
def compare(region, uid, other_uid):
    region, uid, other_uid = normalize_region(region), uid.strip(), other_uid.strip()
    if not validate_region(region) or not validate_uid(uid) or not validate_uid(other_uid):
        return error("Invalid region or UID", "INVALID_REQUEST")
    return jsonify(analytics_service.compare(region, uid, other_uid))


@api.get("/search/<region>/<keyword>")
def search(region, keyword):
    region = normalize_region(region)
    if not validate_region(region):
        return error(f"Unsupported region: {region}", "INVALID_REGION")
    if len(keyword.strip()) < 2:
        return error("Search keyword must contain at least 2 characters", "INVALID_KEYWORD")
    return jsonify(search_service.search(region, keyword.strip()))


@api.get("/guild/<region>/<guild_id>")
def guild(region, guild_id):
    region = normalize_region(region)
    if not validate_region(region) or not guild_id.isdigit():
        return error("Invalid region or guild ID", "INVALID_REQUEST")
    return jsonify(guild_service.get_guild(region, guild_id))


@api.get("/assets/<int:item_id>")
def asset(item_id):
    return jsonify(asset_service.get_asset(item_id))
