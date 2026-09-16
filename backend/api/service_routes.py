from flask import Blueprint, jsonify, request

from core.request_id import get_request_id
from services.service_registry import all_services, get_service

services = Blueprint("services", __name__)


def ok(data, count=None):
    payload = {"success": True, "data": data, "request_id": get_request_id()}
    if count is not None:
        payload["count"] = count
    return jsonify(payload)


@services.get("/services")
def service_list():
    items = all_services()
    group = request.args.get("group")
    status = request.args.get("status")
    if group:
        items = [x for x in items if x["group"] == group]
    if status:
        items = [x for x in items if x["status"] == status]
    return ok(items, len(items))


@services.get("/services/<service_id>")
def service_detail(service_id):
    item = get_service(service_id)
    if item is None:
        return jsonify({
            "success": False,
            "error": {"code": "SERVICE_NOT_FOUND", "message": "Unknown Jokor service."},
            "request_id": get_request_id(),
        }), 404
    return ok(item)
