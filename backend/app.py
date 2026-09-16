from flask import Flask, jsonify, request
from flask_cors import CORS

from api.routes import api
from core.config import settings
from core.errors import register_error_handlers
from core.health import health_snapshot
from core.metrics import metrics
from core.rate_limit import RateLimiter
from core.request_id import request_id_middleware


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": settings.cors_origins}})
    app.config["JSON_SORT_KEYS"] = False

    limiter = RateLimiter(settings.rate_limit, 60)
    request_id_middleware(app)

    @app.before_request
    def enforce_rate_limit():
        if not request.path.startswith("/api/"):
            return None
        allowed, retry_after = limiter.allow(request.remote_addr or "unknown")
        if not allowed:
            metrics.record_error("RATE_LIMITED")
            response = jsonify({
                "success": False,
                "error": "RATE_LIMITED",
                "message": "Too many requests. Try again later.",
                "request_id": getattr(request, "request_id", None),
            })
            response.status_code = 429
            response.headers["Retry-After"] = str(retry_after)
            return response
        return None

    @app.after_request
    def record_metrics(response):
        metrics.record_request(request.path, response.status_code)
        return response

    register_error_handlers(app)
    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def root():
        return jsonify({
            "name": "Jokor API",
            "status": "online",
            "version": settings.version,
            "docs": "/api/meta",
            "health": "/api/health",
        })

    @app.get("/api/system/metrics")
    def system_metrics():
        return jsonify({"success": True, "data": metrics.snapshot()})

    @app.get("/api/system/health-detail")
    def health_detail():
        return jsonify({"success": True, "data": health_snapshot()})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.port, debug=settings.debug)
