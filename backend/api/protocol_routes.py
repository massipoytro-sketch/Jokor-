from flask import Blueprint, jsonify

from core.request_id import get_request_id
from providers.freefire_tcp import FreeFireTCPProvider

protocol = Blueprint("protocol", __name__)
_provider = FreeFireTCPProvider()


@protocol.get("/protocol/tcp/status")
def tcp_status():
    return jsonify({
        "success": True,
        "data": {
            "provider": _provider.name,
            "health": _provider.health(),
            "scope": "protocol-transport-only",
            "credentials": "not accepted or stored",
        },
        "request_id": get_request_id(),
    })
