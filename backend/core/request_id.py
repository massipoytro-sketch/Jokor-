import uuid
from flask import g, request


def request_id_middleware(app):
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex

    @app.after_request
    def attach_request_id(response):
        response.headers["X-Request-ID"] = get_request_id()
        return response


def get_request_id():
    return getattr(g, "request_id", "unknown")
