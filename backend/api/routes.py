from flask import Blueprint, jsonify

from services.player_service import PlayerService

api = Blueprint("api", __name__)
player_service = PlayerService()

SUPPORTED_REGIONS = {
    "BD", "BR", "CIS", "EU", "ID", "IND", "ME", "NA", "PK",
    "RU", "SAC", "SG", "TH", "TW", "US", "VN"
}


def error(message, code, status):
    return jsonify({
        "success": False,
        "error": code,
        "message": message,
    }), status


@api.get("/health")
def health():
    return jsonify({
        "success": True,
        "service": "jokor-api",
        "status": "healthy",
        "version": "0.1.0",
    })


@api.get("/regions")
def regions():
    return jsonify({
        "success": True,
        "regions": sorted(SUPPORTED_REGIONS),
    })


@api.get("/player/<region>/<uid>")
def player(region, uid):
    region = region.upper().strip()
    uid = uid.strip()

    if region not in SUPPORTED_REGIONS:
        return error(f"Unsupported region: {region}", "INVALID_REGION", 400)
    if not uid.isdigit() or int(uid) <= 0:
        return error("UID must be a positive numeric value", "INVALID_UID", 400)

    result = player_service.get_profile(region, uid)
    return jsonify(result), result.get("http_status", 200)
