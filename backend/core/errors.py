from flask import jsonify
from werkzeug.exceptions import HTTPException
from core.request_id import get_request_id


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return jsonify({"success": False, "error": exc.name.upper().replace(" ", "_"), "message": exc.description, "request_id": get_request_id()}), exc.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc):
        app.logger.exception("Unhandled Jokor error: %s", exc)
        return jsonify({"success": False, "error": "INTERNAL_ERROR", "message": "An unexpected server error occurred.", "request_id": get_request_id()}), 500
